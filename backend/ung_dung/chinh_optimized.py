"""
IVIE Wedding Studio API - Phiên bản tối ưu hóa
==============================================
- Advanced caching với Redis/fallback
- Database connection pooling
- GZip compression
- Rate limiting
- Performance monitoring
- Health checks với cache stats
"""

import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# LIFESPAN MANAGEMENT
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý lifecycle của application.
    - Startup: Khởi tạo database, cache, indexes
    - Shutdown: Cleanup resources
    """
    # STARTUP
    logger.info("🚀 Starting IVIE Wedding API...")

    # Initialize database
    try:
        from .co_so_du_lieu import khoi_tao_csdl

        khoi_tao_csdl()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

    # Initialize optimized database with indexes
    try:
        from .co_so_du_lieu_optimized import (
            create_indexes,
            get_engine,
            init_database_optimized,
        )

        init_database_optimized()
        logger.info("✅ Database indexes created")
    except ImportError:
        logger.info("ℹ️ Optimized database module not available, using standard")
    except Exception as e:
        logger.warning(f"⚠️ Could not create indexes: {e}")

    # Initialize cache
    try:
        from .cache_advanced import cache_warmer, redis_client

        if redis_client.is_connected:
            logger.info("✅ Redis cache connected")
        else:
            logger.info("ℹ️ Using in-memory cache (Redis not available)")
    except ImportError:
        logger.info("ℹ️ Advanced cache not available")

    logger.info("🎉 IVIE Wedding API started successfully!")

    yield  # Application runs here

    # SHUTDOWN
    logger.info("🛑 Shutting down IVIE Wedding API...")

    # Cleanup database connections
    try:
        from .co_so_du_lieu_optimized import cleanup

        cleanup()
        logger.info("✅ Database connections cleaned up")
    except ImportError:
        pass
    except Exception as e:
        logger.warning(f"⚠️ Cleanup warning: {e}")

    logger.info("👋 IVIE Wedding API shutdown complete")


# =============================================================================
# APPLICATION INITIALIZATION
# =============================================================================

ung_dung = FastAPI(
    title="IVIE Wedding Studio API (Optimized)",
    description="API tối ưu hóa cho website IVIE Wedding Studio",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# =============================================================================
# MIDDLEWARE CONFIGURATION
# =============================================================================

# 1. GZip Middleware - Nén response > 500 bytes
ung_dung.add_middleware(GZipMiddleware, minimum_size=500)

# 2. CORS Middleware
nguon_goc = os.getenv("CORS_ORIGINS", "*").split(",")
ung_dung.add_middleware(
    CORSMiddleware,
    allow_origins=nguon_goc,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Cache", "X-Cache-TTL", "X-Response-Time"],
)

# 3. Cache Control Middleware
try:
    from .cache_utils import CacheControlMiddleware

    ung_dung.add_middleware(CacheControlMiddleware)
except ImportError:
    logger.info("ℹ️ Basic cache middleware not available")

# 4. Advanced Cache Middleware (nếu có)
try:
    from .cache_advanced import AdvancedCacheMiddleware

    ung_dung.add_middleware(AdvancedCacheMiddleware)
    logger.info("✅ Advanced cache middleware enabled")
except ImportError:
    pass


# =============================================================================
# REQUEST TIMING MIDDLEWARE
# =============================================================================


@ung_dung.middleware("http")
async def add_response_timing(request: Request, call_next):
    """Middleware để track response time"""
    start_time = time.time()

    response = await call_next(request)

    # Calculate response time
    process_time = time.time() - start_time
    response.headers["X-Response-Time"] = f"{process_time:.4f}s"

    # Log slow requests (> 2 seconds)
    if process_time > 2.0:
        logger.warning(
            f"Slow request: {request.method} {request.url.path} - {process_time:.2f}s"
        )

    return response


# =============================================================================
# STATIC FILES
# =============================================================================

# Mount images directory
thu_muc_anh = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../frontend/public/images")
)
if os.path.exists(thu_muc_anh):
    ung_dung.mount("/images", StaticFiles(directory=thu_muc_anh), name="images")
else:
    logger.warning(f"⚠️ Images directory not found: {thu_muc_anh}")

# Mount uploaded files directory
thu_muc_tep_tin = "tep_tin"
os.makedirs(thu_muc_tep_tin, exist_ok=True)
ung_dung.mount("/tep_tin", StaticFiles(directory=thu_muc_tep_tin), name="tep_tin")


# =============================================================================
# ROUTERS
# =============================================================================

from .dinh_tuyen import (
    api_pg,
    banner,
    blog,
    chat,
    dich_vu,
    doi_tac,
    don_hang,
    lien_he,
    nguoi_dung,
    noi_dung,
    san_pham,
    tap_tin,
    thong_ke,
    thu_vien,
    yeu_thich,
)

# Standard routers
ung_dung.include_router(san_pham.bo_dinh_tuyen)
ung_dung.include_router(dich_vu.bo_dinh_tuyen)
ung_dung.include_router(lien_he.bo_dinh_tuyen)
ung_dung.include_router(tap_tin.bo_dinh_tuyen)
ung_dung.include_router(banner.bo_dinh_tuyen)
ung_dung.include_router(noi_dung.bo_dinh_tuyen)
ung_dung.include_router(thu_vien.bo_dinh_tuyen)
ung_dung.include_router(nguoi_dung.bo_dinh_tuyen)
ung_dung.include_router(chat.bo_dinh_tuyen)
ung_dung.include_router(doi_tac.bo_dinh_tuyen)
ung_dung.include_router(blog.bo_dinh_tuyen)
ung_dung.include_router(yeu_thich.bo_dinh_tuyen)
ung_dung.include_router(thong_ke.bo_dinh_tuyen)
ung_dung.include_router(api_pg.bo_dinh_tuyen)
ung_dung.include_router(don_hang.bo_dinh_tuyen)

# Include optimized routers if available
try:
    from .dinh_tuyen import san_pham_optimized

    ung_dung.include_router(
        san_pham_optimized.bo_dinh_tuyen, prefix="/v2", tags=["san_pham_v2"]
    )
    logger.info("✅ Optimized product router enabled at /v2")
except ImportError:
    pass


# =============================================================================
# ROOT ENDPOINTS
# =============================================================================


@ung_dung.get("/")
def doc_goc():
    """Root endpoint với thông tin API"""
    return {
        "thong_bao": "Chào mừng đến với API IVIE Wedding Studio",
        "phien_ban": "2.0.0 (Optimized)",
        "tai_lieu": "/docs",
        "redoc": "/redoc",
        "suc_khoe": "/api/health",
        "thoi_gian": datetime.now().isoformat(),
    }


@ung_dung.get("/suckhoe")
def kiem_tra_suc_khoe():
    """Legacy health check endpoint"""
    return {"trang_thai": "khoe_manh"}


# =============================================================================
# HEALTH CHECK ENDPOINTS
# =============================================================================


@ung_dung.get("/api/health")
def health_check():
    """
    Comprehensive health check endpoint.
    Kiểm tra trạng thái database, cache, và các services.
    """
    health = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "components": {},
    }

    # Check database
    try:
        from sqlalchemy import text

        from .co_so_du_lieu import dong_co

        with dong_co.connect() as conn:
            conn.execute(text("SELECT 1"))
        health["components"]["database"] = {"status": "healthy"}
    except Exception as e:
        health["components"]["database"] = {"status": "unhealthy", "error": str(e)}
        health["status"] = "degraded"

    # Check cache
    try:
        from .cache_advanced import get_cache_health

        cache_health = get_cache_health()
        health["components"]["cache"] = cache_health
    except ImportError:
        health["components"]["cache"] = {"status": "not_configured"}
    except Exception as e:
        health["components"]["cache"] = {"status": "error", "error": str(e)}

    return health


@ung_dung.get("/api/health/detailed")
def detailed_health_check():
    """
    Detailed health check với performance metrics.
    Dành cho monitoring và debugging.
    """
    import psutil

    health = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "system": {},
        "database": {},
        "cache": {},
    }

    # System metrics
    try:
        health["system"] = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent
            if os.name != "nt"
            else psutil.disk_usage("C:").percent,
        }
    except:
        health["system"] = {"status": "metrics_unavailable"}

    # Database health
    try:
        from .co_so_du_lieu_optimized import check_database_health

        health["database"] = check_database_health()
    except ImportError:
        try:
            from sqlalchemy import text

            from .co_so_du_lieu import dong_co

            with dong_co.connect() as conn:
                conn.execute(text("SELECT 1"))
            health["database"] = {"status": "healthy", "type": "standard"}
        except Exception as e:
            health["database"] = {"status": "unhealthy", "error": str(e)}
            health["status"] = "degraded"

    # Cache health
    try:
        from .cache_advanced import redis_client

        health["cache"] = redis_client.stats()
    except ImportError:
        health["cache"] = {"status": "not_configured"}

    return health


@ung_dung.get("/api/db-test")
def test_database():
    """Test database connection and table creation"""
    from sqlalchemy import text

    from .co_so_du_lieu import NguoiDung, PhienLamViec, dong_co

    try:
        # Test connection
        with dong_co.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            conn_status = "OK"

        # Test table exists
        db = PhienLamViec()
        try:
            user_count = db.query(NguoiDung).count()
            table_status = f"OK - {user_count} users"
        except Exception as e:
            table_status = f"ERROR - {str(e)}"
        finally:
            db.close()

        return {
            "database_url": os.getenv("DATABASE_URL", "Not set")[:50] + "...",
            "connection": conn_status,
            "users_table": table_status,
        }
    except Exception as e:
        return {
            "error": str(e),
            "database_url": os.getenv("DATABASE_URL", "Not set")[:50] + "...",
        }


# =============================================================================
# CACHE MANAGEMENT ENDPOINTS
# =============================================================================


@ung_dung.get("/api/cache/stats")
def cache_stats():
    """Get cache statistics"""
    try:
        from .cache_advanced import redis_client, response_cache

        return {
            "cache": redis_client.stats(),
            "response_cache_rules": len(response_cache.rules),
        }
    except ImportError:
        return {"message": "Advanced cache not configured"}


@ung_dung.post("/api/cache/clear")
def clear_cache(pattern: str = None):
    """
    Clear cache entries.
    Admin only - should be protected in production.
    """
    try:
        from .cache_advanced import invalidator, redis_client

        if pattern:
            count = redis_client.delete_pattern(f"*{pattern}*")
            return {"cleared": count, "pattern": pattern}
        else:
            invalidator.invalidate_all()
            return {"message": "All cache cleared"}
    except ImportError:
        return {"message": "Advanced cache not configured"}


@ung_dung.post("/api/cache/warmup")
def warmup_cache():
    """
    Warm up cache with frequently accessed data.
    Admin only - should be protected in production.
    """
    try:
        from .cache_advanced import cache_warmer

        cache_warmer.warmup_all()
        return {"message": "Cache warmup completed"}
    except ImportError:
        return {"message": "Cache warmer not configured"}


# =============================================================================
# ERROR HANDLERS
# =============================================================================


@ung_dung.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler với logging"""
    logger.error(
        f"Unhandled exception: {exc}\n"
        f"Path: {request.url.path}\n"
        f"Method: {request.method}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
            if os.getenv("DEBUG", "false").lower() == "true"
            else "An error occurred",
            "path": request.url.path,
        },
    )


# =============================================================================
# STARTUP MESSAGE
# =============================================================================

logger.info("""
╔═══════════════════════════════════════════════════════════╗
║          IVIE Wedding Studio API v2.0.0                   ║
║                  Optimized Edition                        ║
╠═══════════════════════════════════════════════════════════╣
║  Features:                                                ║
║  ✓ Database connection pooling                            ║
║  ✓ Query caching with Redis/fallback                      ║
║  ✓ Response compression (GZip)                            ║
║  ✓ Performance monitoring                                 ║
║  ✓ Database indexing                                      ║
╚═══════════════════════════════════════════════════════════╝
""")
