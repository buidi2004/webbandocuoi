"""
Cơ sở dữ liệu tối ưu hóa cho IVIE Wedding Studio
- Connection pooling để quản lý kết nối hiệu quả
- Query caching với TTL
- Database indexing cho truy vấn nhanh
- Async support cho concurrent requests
"""

import logging
import os
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Dict, List, Optional

from sqlalchemy import Index, create_engine, event, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import QueuePool, StaticPool

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base cho models
Base = declarative_base()

# =============================================================================
# QUERY CACHE - In-memory cache với TTL
# =============================================================================


class QueryCache:
    """
    Simple in-memory cache với TTL cho database queries.
    Thread-safe implementation.
    """

    def __init__(self, default_ttl: int = 300):
        """
        Khởi tạo cache.

        Args:
            default_ttl: Thời gian cache mặc định (giây), default 5 phút
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def _generate_key(self, query: str, params: Optional[tuple] = None) -> str:
        """Tạo cache key từ query và params"""
        if params:
            return f"{query}:{hash(params)}"
        return query

    def get(self, key: str) -> Optional[Any]:
        """Lấy giá trị từ cache nếu còn hợp lệ"""
        with self._lock:
            if key in self._cache:
                item = self._cache[key]
                if datetime.now() < item["expires"]:
                    self.hits += 1
                    return item["value"]
                else:
                    # Xóa item hết hạn
                    del self._cache[key]
            self.misses += 1
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Lưu giá trị vào cache"""
        with self._lock:
            expires = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
            self._cache[key] = {
                "value": value,
                "expires": expires,
                "created": datetime.now(),
            }

    def delete(self, key: str) -> bool:
        """Xóa một key khỏi cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def invalidate_pattern(self, pattern: str) -> int:
        """Xóa tất cả keys match với pattern"""
        with self._lock:
            keys_to_delete = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]
            return len(keys_to_delete)

    def clear(self) -> None:
        """Xóa toàn bộ cache"""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

    def cleanup_expired(self) -> int:
        """Dọn dẹp các items hết hạn"""
        with self._lock:
            now = datetime.now()
            expired_keys = [k for k, v in self._cache.items() if now >= v["expires"]]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)

    def stats(self) -> Dict[str, Any]:
        """Thống kê cache"""
        with self._lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0
            return {
                "size": len(self._cache),
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": f"{hit_rate:.2f}%",
            }


# Global cache instance
query_cache = QueryCache(default_ttl=300)


# =============================================================================
# DATABASE ENGINE CONFIGURATION
# =============================================================================


def get_database_url() -> str:
    """Lấy database URL từ environment variables"""
    # Ưu tiên PostgreSQL nếu có
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Render.com sử dụng postgres:// nhưng SQLAlchemy cần postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    # Fallback về SQLite
    return "sqlite:///./ivie.db"


def create_optimized_engine(database_url: Optional[str] = None):
    """
    Tạo database engine với connection pooling tối ưu.

    Args:
        database_url: URL kết nối database (optional)

    Returns:
        SQLAlchemy Engine với connection pool
    """
    url = database_url or get_database_url()
    is_sqlite = url.startswith("sqlite")

    # Cấu hình cho SQLite
    if is_sqlite:
        engine = create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,  # SQLite không hỗ trợ multiple connections tốt
            echo=False,
        )

        # Tối ưu SQLite với PRAGMA
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            # WAL mode cho concurrent reads
            cursor.execute("PRAGMA journal_mode=WAL")
            # Cache size lớn hơn (negative = KB)
            cursor.execute("PRAGMA cache_size=-64000")  # 64MB
            # Synchronous normal cho tốc độ
            cursor.execute("PRAGMA synchronous=NORMAL")
            # Temp store in memory
            cursor.execute("PRAGMA temp_store=MEMORY")
            # Memory mapped I/O
            cursor.execute("PRAGMA mmap_size=268435456")  # 256MB
            cursor.close()

        return engine

    # Cấu hình cho PostgreSQL với connection pooling
    engine = create_engine(
        url,
        poolclass=QueuePool,
        pool_size=5,  # Số connection cơ bản
        max_overflow=10,  # Số connection thêm khi cần
        pool_timeout=30,  # Timeout khi đợi connection
        pool_recycle=1800,  # Recycle connection sau 30 phút
        pool_pre_ping=True,  # Kiểm tra connection trước khi sử dụng
        echo=False,  # Không log SQL (production)
        connect_args={"connect_timeout": 10, "application_name": "ivie_wedding_admin"},
    )

    # Event listeners cho monitoring
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(time.time())

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop()
        # Log slow queries (> 1 giây)
        if total > 1.0:
            logger.warning(f"Slow query ({total:.2f}s): {statement[:100]}...")

    return engine


# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

# Global engine và session factory
_engine = None
_SessionFactory = None


def get_engine():
    """Lazy initialization cho engine"""
    global _engine
    if _engine is None:
        _engine = create_optimized_engine()
    return _engine


def get_session_factory():
    """Lazy initialization cho session factory"""
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(
            bind=get_engine(),
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,  # Tránh query lại sau commit
        )
    return _SessionFactory


def lay_csdl_optimized():
    """
    Generator function để inject database session vào FastAPI endpoints.
    Sử dụng với Depends().
    """
    SessionFactory = get_session_factory()
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Context manager cho database session.
    Sử dụng trong code không phải endpoint.

    Example:
        with get_db_session() as db:
            products = db.query(Product).all()
    """
    SessionFactory = get_session_factory()
    session = SessionFactory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


# =============================================================================
# DATABASE INDEXES
# =============================================================================


def create_indexes(engine):
    """
    Tạo các indexes cần thiết để tăng tốc queries.
    Gọi hàm này sau khi tạo tables.
    """
    indexes = [
        # Sản phẩm indexes
        "CREATE INDEX IF NOT EXISTS idx_san_pham_category ON san_pham(category)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_sub_category ON san_pham(sub_category)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_gender ON san_pham(gender)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_is_hot ON san_pham(is_hot)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_is_new ON san_pham(is_new)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_code ON san_pham(code)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_category_gender ON san_pham(category, gender)",
        "CREATE INDEX IF NOT EXISTS idx_san_pham_price ON san_pham(rental_price_day)",
        # Đơn hàng indexes
        "CREATE INDEX IF NOT EXISTS idx_don_hang_status ON don_hang(status)",
        "CREATE INDEX IF NOT EXISTS idx_don_hang_user_id ON don_hang(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_don_hang_order_date ON don_hang(order_date)",
        "CREATE INDEX IF NOT EXISTS idx_don_hang_status_date ON don_hang(status, order_date)",
        # Chi tiết đơn hàng indexes
        "CREATE INDEX IF NOT EXISTS idx_chi_tiet_don_hang_product ON chi_tiet_don_hang(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_chi_tiet_don_hang_order ON chi_tiet_don_hang(order_id)",
        # Liên hệ indexes
        "CREATE INDEX IF NOT EXISTS idx_lien_he_status ON lien_he_gui(status)",
        "CREATE INDEX IF NOT EXISTS idx_lien_he_date ON lien_he_gui(created_at)",
        # Đánh giá indexes
        "CREATE INDEX IF NOT EXISTS idx_danh_gia_product ON danh_gia(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_danh_gia_approved ON danh_gia(is_approved)",
        "CREATE INDEX IF NOT EXISTS idx_danh_gia_product_approved ON danh_gia(product_id, is_approved)",
        # Người dùng indexes
        "CREATE INDEX IF NOT EXISTS idx_nguoi_dung_email ON nguoi_dung(email)",
        "CREATE INDEX IF NOT EXISTS idx_nguoi_dung_phone ON nguoi_dung(phone)",
        # Blog indexes
        "CREATE INDEX IF NOT EXISTS idx_blog_slug ON bai_viet(slug)",
        "CREATE INDEX IF NOT EXISTS idx_blog_published ON bai_viet(is_published)",
        "CREATE INDEX IF NOT EXISTS idx_blog_category ON bai_viet(category)",
        # Yêu thích indexes
        "CREATE INDEX IF NOT EXISTS idx_yeu_thich_user ON yeu_thich(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_yeu_thich_product ON yeu_thich(product_id)",
        # Combo indexes
        "CREATE INDEX IF NOT EXISTS idx_combo_active ON combo(is_active)",
    ]

    with engine.connect() as conn:
        for idx_sql in indexes:
            try:
                conn.execute(text(idx_sql))
                conn.commit()
            except Exception as e:
                # Index có thể đã tồn tại hoặc table chưa có
                logger.debug(f"Index creation note: {e}")

    logger.info("✅ Database indexes created/verified successfully")


def analyze_tables(engine):
    """
    Chạy ANALYZE để cập nhật statistics cho query optimizer.
    Chỉ dùng cho PostgreSQL.
    """
    database_url = get_database_url()
    if "postgresql" not in database_url:
        return

    tables = [
        "san_pham",
        "don_hang",
        "chi_tiet_don_hang",
        "lien_he_gui",
        "danh_gia",
        "nguoi_dung",
        "bai_viet",
    ]

    with engine.connect() as conn:
        for table in tables:
            try:
                conn.execute(text(f"ANALYZE {table}"))
                conn.commit()
            except Exception as e:
                logger.debug(f"ANALYZE {table}: {e}")

    logger.info("✅ Table statistics updated")


# =============================================================================
# CACHED QUERIES
# =============================================================================


def cached_query(cache_key: str, ttl: int = 300):
    """
    Decorator để cache kết quả query.

    Args:
        cache_key: Key prefix cho cache
        ttl: Time-to-live (giây)

    Example:
        @cached_query("products_list", ttl=300)
        def get_products(category=None):
            ...
    """

    def decorator(func):
        @lru_cache(maxsize=128)
        def wrapper(*args, **kwargs):
            # Tạo full cache key từ arguments
            key_parts = [cache_key]
            if args:
                key_parts.extend(str(a) for a in args)
            if kwargs:
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            full_key = ":".join(key_parts)

            # Check cache
            cached = query_cache.get(full_key)
            if cached is not None:
                return cached

            # Execute query
            result = func(*args, **kwargs)

            # Store in cache
            query_cache.set(full_key, result, ttl)
            return result

        # Copy function metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.cache_clear = lambda: query_cache.invalidate_pattern(cache_key)

        return wrapper

    return decorator


def invalidate_cache(pattern: str):
    """
    Invalidate cache entries matching pattern.
    Gọi sau khi có thay đổi dữ liệu.

    Example:
        invalidate_cache("products")  # Xóa cache sản phẩm
    """
    count = query_cache.invalidate_pattern(pattern)
    logger.info(f"Cache invalidated: {pattern} ({count} entries)")
    return count


# =============================================================================
# BULK OPERATIONS
# =============================================================================


def bulk_insert(session, model_class, data_list: List[Dict], batch_size: int = 100):
    """
    Insert nhiều records cùng lúc để tối ưu performance.

    Args:
        session: Database session
        model_class: SQLAlchemy model class
        data_list: List các dict chứa data
        batch_size: Số records mỗi batch
    """
    total = len(data_list)
    for i in range(0, total, batch_size):
        batch = data_list[i : i + batch_size]
        objects = [model_class(**data) for data in batch]
        session.bulk_save_objects(objects)
        session.commit()
        logger.info(
            f"Inserted batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size}"
        )


def bulk_update(session, model_class, updates: List[Dict], id_field: str = "id"):
    """
    Update nhiều records cùng lúc.

    Args:
        session: Database session
        model_class: SQLAlchemy model class
        updates: List dict với id và fields cần update
        id_field: Tên field ID
    """
    for update in updates:
        record_id = update.pop(id_field)
        session.query(model_class).filter(
            getattr(model_class, id_field) == record_id
        ).update(update, synchronize_session=False)
    session.commit()


# =============================================================================
# DATABASE HEALTH CHECK
# =============================================================================


def check_database_health() -> Dict[str, Any]:
    """
    Kiểm tra sức khỏe database và connection pool.
    """
    engine = get_engine()

    result = {
        "status": "healthy",
        "database_type": "postgresql"
        if "postgresql" in get_database_url()
        else "sqlite",
        "pool_size": engine.pool.size() if hasattr(engine.pool, "size") else "N/A",
        "pool_checkedout": engine.pool.checkedout()
        if hasattr(engine.pool, "checkedout")
        else "N/A",
        "cache_stats": query_cache.stats(),
        "timestamp": datetime.now().isoformat(),
    }

    # Test connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        result["connection"] = "OK"
    except Exception as e:
        result["status"] = "unhealthy"
        result["connection"] = str(e)

    return result


# =============================================================================
# INITIALIZATION
# =============================================================================


def init_database_optimized():
    """
    Khởi tạo database với tối ưu hóa.
    Gọi khi startup application.
    """
    engine = get_engine()

    # Import models để đảm bảo tables được tạo
    from .co_so_du_lieu import Base as OriginalBase

    # Tạo tables nếu chưa có
    OriginalBase.metadata.create_all(bind=engine)

    # Tạo indexes
    create_indexes(engine)

    # Update statistics (PostgreSQL)
    analyze_tables(engine)

    logger.info("✅ Optimized database initialized successfully")
    return engine


# Cleanup function cho shutdown
def cleanup():
    """Dọn dẹp resources khi shutdown"""
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None
    query_cache.clear()
    logger.info("✅ Database connections cleaned up")
