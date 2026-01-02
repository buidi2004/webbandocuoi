"""
Advanced Caching Layer cho IVIE Wedding Studio
- Redis support với fallback về in-memory cache
- Response caching decorator cho FastAPI
- Cache invalidation strategies
- TTL management và auto-cleanup
- Cache statistics và monitoring
"""

import asyncio
import hashlib
import json
import logging
import os
import pickle
import threading
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# CACHE CONFIGURATION
# =============================================================================

# Cache TTL presets (seconds)
CACHE_TTL = {
    "INSTANT": 30,  # 30 giây - real-time data
    "SHORT": 60,  # 1 phút - frequently changing
    "MEDIUM": 300,  # 5 phút - product lists
    "LONG": 900,  # 15 phút - category data
    "EXTENDED": 3600,  # 1 giờ - static content
    "DAY": 86400,  # 1 ngày - rarely changing
}

# Cache keys patterns
CACHE_KEYS = {
    "PRODUCTS": "products",
    "PRODUCT_DETAIL": "product:{id}",
    "CATEGORIES": "categories",
    "BANNERS": "banners",
    "BLOGS": "blogs",
    "BLOG_DETAIL": "blog:{id}",
    "GALLERY": "gallery",
    "EXPERTS": "experts",
    "COMBOS": "combos",
    "STATS": "stats:{type}",
    "USER": "user:{id}",
    "ORDERS": "orders:{user_id}",
}


# =============================================================================
# REDIS CLIENT (với fallback)
# =============================================================================


class RedisClient:
    """
    Redis client wrapper với automatic fallback về in-memory cache.
    """

    def __init__(self):
        self._redis = None
        self._connected = False
        self._fallback_cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._connect()

    def _connect(self):
        """Kết nối Redis nếu có cấu hình"""
        redis_url = os.getenv("REDIS_URL")

        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(
                    redis_url,
                    decode_responses=False,  # Để hỗ trợ pickle
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    retry_on_timeout=True,
                    health_check_interval=30,
                )
                # Test connection
                self._redis.ping()
                self._connected = True
                logger.info("✅ Redis connected successfully")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed, using fallback: {e}")
                self._redis = None
                self._connected = False
        else:
            logger.info("ℹ️ No REDIS_URL configured, using in-memory cache")

    @property
    def is_connected(self) -> bool:
        """Kiểm tra Redis có connected không"""
        return self._connected and self._redis is not None

    def _serialize(self, value: Any) -> bytes:
        """Serialize value để lưu"""
        return pickle.dumps(value)

    def _deserialize(self, data: bytes) -> Any:
        """Deserialize value từ cache"""
        if data is None:
            return None
        return pickle.loads(data)

    def get(self, key: str) -> Optional[Any]:
        """Lấy giá trị từ cache"""
        if self.is_connected:
            try:
                data = self._redis.get(key)
                return self._deserialize(data)
            except Exception as e:
                logger.error(f"Redis GET error: {e}")

        # Fallback
        with self._lock:
            if key in self._fallback_cache:
                item = self._fallback_cache[key]
                if datetime.now() < item["expires"]:
                    return item["value"]
                del self._fallback_cache[key]
        return None

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Lưu giá trị vào cache"""
        if self.is_connected:
            try:
                self._redis.setex(key, ttl, self._serialize(value))
                return True
            except Exception as e:
                logger.error(f"Redis SET error: {e}")

        # Fallback
        with self._lock:
            self._fallback_cache[key] = {
                "value": value,
                "expires": datetime.now() + timedelta(seconds=ttl),
            }
        return True

    def delete(self, key: str) -> bool:
        """Xóa key khỏi cache"""
        if self.is_connected:
            try:
                self._redis.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis DELETE error: {e}")

        # Fallback
        with self._lock:
            if key in self._fallback_cache:
                del self._fallback_cache[key]
                return True
        return False

    def delete_pattern(self, pattern: str) -> int:
        """Xóa tất cả keys match pattern"""
        count = 0

        if self.is_connected:
            try:
                # Redis SCAN để tìm keys
                cursor = 0
                while True:
                    cursor, keys = self._redis.scan(cursor, match=pattern, count=100)
                    if keys:
                        self._redis.delete(*keys)
                        count += len(keys)
                    if cursor == 0:
                        break
                return count
            except Exception as e:
                logger.error(f"Redis DELETE_PATTERN error: {e}")

        # Fallback
        with self._lock:
            # Convert glob pattern to simple matching
            simple_pattern = pattern.replace("*", "")
            keys_to_delete = [k for k in self._fallback_cache if simple_pattern in k]
            for key in keys_to_delete:
                del self._fallback_cache[key]
            count = len(keys_to_delete)

        return count

    def clear(self) -> bool:
        """Xóa toàn bộ cache"""
        if self.is_connected:
            try:
                self._redis.flushdb()
                return True
            except Exception as e:
                logger.error(f"Redis CLEAR error: {e}")

        # Fallback
        with self._lock:
            self._fallback_cache.clear()
        return True

    def exists(self, key: str) -> bool:
        """Kiểm tra key có tồn tại không"""
        if self.is_connected:
            try:
                return self._redis.exists(key) > 0
            except Exception as e:
                logger.error(f"Redis EXISTS error: {e}")

        # Fallback
        with self._lock:
            if key in self._fallback_cache:
                if datetime.now() < self._fallback_cache[key]["expires"]:
                    return True
                del self._fallback_cache[key]
        return False

    def ttl(self, key: str) -> int:
        """Lấy TTL còn lại của key (seconds)"""
        if self.is_connected:
            try:
                return self._redis.ttl(key)
            except Exception as e:
                logger.error(f"Redis TTL error: {e}")

        # Fallback
        with self._lock:
            if key in self._fallback_cache:
                remaining = (
                    self._fallback_cache[key]["expires"] - datetime.now()
                ).total_seconds()
                return max(0, int(remaining))
        return -2  # Key không tồn tại

    def mget(self, keys: List[str]) -> List[Optional[Any]]:
        """Lấy nhiều keys cùng lúc"""
        if self.is_connected:
            try:
                values = self._redis.mget(keys)
                return [self._deserialize(v) for v in values]
            except Exception as e:
                logger.error(f"Redis MGET error: {e}")

        # Fallback
        return [self.get(key) for key in keys]

    def mset(self, mapping: Dict[str, Any], ttl: int = 300) -> bool:
        """Set nhiều keys cùng lúc"""
        if self.is_connected:
            try:
                pipe = self._redis.pipeline()
                for key, value in mapping.items():
                    pipe.setex(key, ttl, self._serialize(value))
                pipe.execute()
                return True
            except Exception as e:
                logger.error(f"Redis MSET error: {e}")

        # Fallback
        for key, value in mapping.items():
            self.set(key, value, ttl)
        return True

    def incr(self, key: str, amount: int = 1) -> int:
        """Tăng giá trị counter"""
        if self.is_connected:
            try:
                return self._redis.incr(key, amount)
            except Exception as e:
                logger.error(f"Redis INCR error: {e}")

        # Fallback
        with self._lock:
            if key not in self._fallback_cache:
                self._fallback_cache[key] = {
                    "value": 0,
                    "expires": datetime.now() + timedelta(days=1),
                }
            self._fallback_cache[key]["value"] += amount
            return self._fallback_cache[key]["value"]

    def stats(self) -> Dict[str, Any]:
        """Thống kê cache"""
        result = {
            "type": "redis" if self.is_connected else "in-memory",
            "connected": self.is_connected,
            "timestamp": datetime.now().isoformat(),
        }

        if self.is_connected:
            try:
                info = self._redis.info()
                result.update(
                    {
                        "used_memory": info.get("used_memory_human", "N/A"),
                        "connected_clients": info.get("connected_clients", 0),
                        "total_keys": self._redis.dbsize(),
                        "hits": info.get("keyspace_hits", 0),
                        "misses": info.get("keyspace_misses", 0),
                    }
                )
            except Exception as e:
                result["error"] = str(e)
        else:
            with self._lock:
                result["total_keys"] = len(self._fallback_cache)

        return result

    def cleanup_expired(self) -> int:
        """Dọn dẹp expired keys (chỉ cho fallback cache)"""
        if self.is_connected:
            return 0  # Redis tự động xử lý

        with self._lock:
            now = datetime.now()
            expired = [
                k for k, v in self._fallback_cache.items() if now >= v["expires"]
            ]
            for key in expired:
                del self._fallback_cache[key]
            return len(expired)


# Global Redis client instance
redis_client = RedisClient()


# =============================================================================
# CACHE DECORATORS
# =============================================================================


def generate_cache_key(*args, **kwargs) -> str:
    """Tạo cache key từ arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = ":".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cached(
    key_prefix: str,
    ttl: int = CACHE_TTL["MEDIUM"],
    key_builder: Optional[Callable] = None,
):
    """
    Decorator để cache kết quả function.

    Args:
        key_prefix: Prefix cho cache key
        ttl: Time-to-live (seconds)
        key_builder: Custom function để build cache key

    Example:
        @cached("products", ttl=300)
        def get_products(category=None):
            ...
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                cache_key = f"{key_prefix}:{generate_cache_key(*args, **kwargs)}"

            # Try get from cache
            cached_value = redis_client.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache HIT: {cache_key}")
                return cached_value

            # Execute function
            logger.debug(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)

            # Store in cache
            redis_client.set(cache_key, result, ttl)

            return result

        # Attach cache utilities
        wrapper.cache_key_prefix = key_prefix
        wrapper.invalidate = lambda: redis_client.delete_pattern(f"{key_prefix}:*")
        wrapper.invalidate_key = lambda k: redis_client.delete(f"{key_prefix}:{k}")

        return wrapper

    return decorator


def cached_async(
    key_prefix: str,
    ttl: int = CACHE_TTL["MEDIUM"],
    key_builder: Optional[Callable] = None,
):
    """
    Async version của cached decorator.
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                cache_key = f"{key_prefix}:{generate_cache_key(*args, **kwargs)}"

            # Try get from cache
            cached_value = redis_client.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute async function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.set(cache_key, result, ttl)

            return result

        wrapper.cache_key_prefix = key_prefix
        wrapper.invalidate = lambda: redis_client.delete_pattern(f"{key_prefix}:*")

        return wrapper

    return decorator


# =============================================================================
# RESPONSE CACHING MIDDLEWARE
# =============================================================================


class ResponseCache:
    """
    Cache cho HTTP responses.
    Lưu response body và headers.
    """

    def __init__(self):
        self.rules: Dict[str, Dict[str, Any]] = {}
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Setup cache rules mặc định"""
        self.rules = {
            # Products
            "/api/san_pham": {"ttl": CACHE_TTL["MEDIUM"], "methods": ["GET"]},
            "/api/san_pham/{id}": {"ttl": CACHE_TTL["LONG"], "methods": ["GET"]},
            # Banners
            "/api/banner": {"ttl": CACHE_TTL["LONG"], "methods": ["GET"]},
            # Gallery
            "/api/thu_vien": {"ttl": CACHE_TTL["EXTENDED"], "methods": ["GET"]},
            # Blog
            "/api/blog": {"ttl": CACHE_TTL["LONG"], "methods": ["GET"]},
            # Experts
            "/api/chuyen_gia": {"ttl": CACHE_TTL["EXTENDED"], "methods": ["GET"]},
            # Combos
            "/api/combo": {"ttl": CACHE_TTL["LONG"], "methods": ["GET"]},
            # Static content
            "/api/noi_dung": {"ttl": CACHE_TTL["EXTENDED"], "methods": ["GET"]},
            # Statistics (shorter TTL)
            "/api/thong_ke": {"ttl": CACHE_TTL["SHORT"], "methods": ["GET"]},
        }

    def add_rule(self, path: str, ttl: int, methods: List[str] = None):
        """Thêm cache rule"""
        self.rules[path] = {
            "ttl": ttl,
            "methods": methods or ["GET"],
        }

    def get_rule(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """Lấy cache rule cho path"""
        # Exact match
        if path in self.rules:
            rule = self.rules[path]
            if method in rule["methods"]:
                return rule

        # Prefix match
        for rule_path, rule in self.rules.items():
            if "{" not in rule_path and path.startswith(rule_path):
                if method in rule["methods"]:
                    return rule

        return None

    def generate_key(self, request: Request) -> str:
        """Generate cache key từ request"""
        # Include path, query params, and relevant headers
        parts = [
            request.method,
            str(request.url.path),
            str(sorted(request.query_params.items())),
        ]

        # Add Accept-Encoding to key (for compressed responses)
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" in accept_encoding:
            parts.append("gzip")

        key_string = ":".join(parts)
        return f"response:{hashlib.md5(key_string.encode()).hexdigest()}"


response_cache = ResponseCache()


class AdvancedCacheMiddleware(BaseHTTPMiddleware):
    """
    Advanced caching middleware với response caching.
    """

    async def dispatch(self, request: Request, call_next):
        # Skip non-cacheable methods
        if request.method not in ["GET", "HEAD"]:
            response = await call_next(request)
            response.headers["Cache-Control"] = "no-store"
            return response

        # Check cache rule
        rule = response_cache.get_rule(request.url.path, request.method)

        if rule is None:
            # No caching rule, just pass through
            return await call_next(request)

        # Generate cache key
        cache_key = response_cache.generate_key(request)

        # Try to get from cache
        cached = redis_client.get(cache_key)
        if cached is not None:
            # Return cached response
            return Response(
                content=cached["body"],
                status_code=cached["status_code"],
                headers={
                    **cached["headers"],
                    "X-Cache": "HIT",
                    "X-Cache-TTL": str(redis_client.ttl(cache_key)),
                },
                media_type=cached.get("media_type"),
            )

        # Execute request
        response = await call_next(request)

        # Only cache successful responses
        if 200 <= response.status_code < 300:
            # Read response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            # Store in cache
            cache_data = {
                "body": body,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "media_type": response.media_type,
            }
            redis_client.set(cache_key, cache_data, rule["ttl"])

            # Return new response with body
            return Response(
                content=body,
                status_code=response.status_code,
                headers={
                    **dict(response.headers),
                    "X-Cache": "MISS",
                    "Cache-Control": f"public, max-age={rule['ttl']}",
                },
                media_type=response.media_type,
            )

        return response


# =============================================================================
# CACHE INVALIDATION UTILITIES
# =============================================================================


class CacheInvalidator:
    """
    Quản lý cache invalidation theo entity.
    """

    @staticmethod
    def invalidate_products():
        """Invalidate tất cả cache liên quan đến products"""
        patterns = ["products:*", "response:*san_pham*", "combos:*"]
        count = 0
        for pattern in patterns:
            count += redis_client.delete_pattern(pattern)
        logger.info(f"Invalidated products cache: {count} keys")
        return count

    @staticmethod
    def invalidate_product(product_id: int):
        """Invalidate cache của một product cụ thể"""
        redis_client.delete(f"product:{product_id}")
        redis_client.delete_pattern(f"*san_pham*{product_id}*")
        CacheInvalidator.invalidate_products()

    @staticmethod
    def invalidate_orders(user_id: Optional[int] = None):
        """Invalidate cache đơn hàng"""
        if user_id:
            redis_client.delete(f"orders:{user_id}")
        else:
            redis_client.delete_pattern("orders:*")
        redis_client.delete_pattern("*don_hang*")

    @staticmethod
    def invalidate_banners():
        """Invalidate cache banners"""
        redis_client.delete_pattern("banners:*")
        redis_client.delete_pattern("*banner*")

    @staticmethod
    def invalidate_blogs():
        """Invalidate cache blogs"""
        redis_client.delete_pattern("blogs:*")
        redis_client.delete_pattern("*blog*")

    @staticmethod
    def invalidate_gallery():
        """Invalidate cache gallery"""
        redis_client.delete_pattern("gallery:*")
        redis_client.delete_pattern("*thu_vien*")

    @staticmethod
    def invalidate_stats():
        """Invalidate cache thống kê"""
        redis_client.delete_pattern("stats:*")
        redis_client.delete_pattern("*thong_ke*")

    @staticmethod
    def invalidate_all():
        """Invalidate toàn bộ cache"""
        redis_client.clear()
        logger.info("Invalidated ALL cache")


invalidator = CacheInvalidator()


# =============================================================================
# CACHE WARMUP
# =============================================================================


class CacheWarmer:
    """
    Pre-warm cache với data thường xuyên truy cập.
    """

    def __init__(self):
        self._warmup_functions: List[Callable] = []

    def register(self, func: Callable):
        """Register function để warmup"""
        self._warmup_functions.append(func)
        return func

    def warmup_all(self):
        """Chạy tất cả warmup functions"""
        logger.info("🔥 Starting cache warmup...")
        start_time = time.time()

        for func in self._warmup_functions:
            try:
                func()
                logger.info(f"  ✓ Warmed up: {func.__name__}")
            except Exception as e:
                logger.error(f"  ✗ Failed to warm up {func.__name__}: {e}")

        elapsed = time.time() - start_time
        logger.info(f"🔥 Cache warmup completed in {elapsed:.2f}s")

    async def warmup_all_async(self):
        """Async version của warmup"""
        logger.info("🔥 Starting async cache warmup...")
        start_time = time.time()

        tasks = []
        for func in self._warmup_functions:
            if asyncio.iscoroutinefunction(func):
                tasks.append(func())
            else:
                # Wrap sync function
                tasks.append(asyncio.to_thread(func))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for func, result in zip(self._warmup_functions, results):
            if isinstance(result, Exception):
                logger.error(f"  ✗ Failed: {func.__name__}: {result}")
            else:
                logger.info(f"  ✓ Warmed: {func.__name__}")

        elapsed = time.time() - start_time
        logger.info(f"🔥 Async cache warmup completed in {elapsed:.2f}s")


cache_warmer = CacheWarmer()


# =============================================================================
# RATE LIMITING (using cache)
# =============================================================================


class RateLimiter:
    """
    Rate limiting sử dụng Redis/cache.
    """

    def __init__(
        self,
        key_prefix: str = "ratelimit",
        limit: int = 100,
        window: int = 60,
    ):
        """
        Args:
            key_prefix: Prefix cho rate limit keys
            limit: Số request tối đa trong window
            window: Thời gian window (seconds)
        """
        self.key_prefix = key_prefix
        self.limit = limit
        self.window = window

    def _get_key(self, identifier: str) -> str:
        """Generate rate limit key"""
        window_id = int(time.time()) // self.window
        return f"{self.key_prefix}:{identifier}:{window_id}"

    def check(self, identifier: str) -> Dict[str, Any]:
        """
        Kiểm tra và increment rate limit.

        Args:
            identifier: IP address hoặc user ID

        Returns:
            Dict với allowed, remaining, reset_at
        """
        key = self._get_key(identifier)

        current = redis_client.incr(key)

        # Set TTL nếu là lần đầu
        if current == 1:
            redis_client.set(key, 1, self.window)

        allowed = current <= self.limit
        remaining = max(0, self.limit - current)
        reset_at = (int(time.time()) // self.window + 1) * self.window

        return {
            "allowed": allowed,
            "remaining": remaining,
            "limit": self.limit,
            "reset_at": reset_at,
            "current": current,
        }

    def is_allowed(self, identifier: str) -> bool:
        """Simple check nếu allowed"""
        return self.check(identifier)["allowed"]


# Default rate limiter instances
api_rate_limiter = RateLimiter(key_prefix="api", limit=100, window=60)
admin_rate_limiter = RateLimiter(key_prefix="admin", limit=200, window=60)


# =============================================================================
# CACHE HEALTH & MONITORING
# =============================================================================


def get_cache_health() -> Dict[str, Any]:
    """
    Kiểm tra sức khỏe hệ thống cache.
    """
    return {
        "status": "healthy" if redis_client.is_connected else "degraded",
        "backend": "redis" if redis_client.is_connected else "in-memory",
        "stats": redis_client.stats(),
        "response_cache_rules": len(response_cache.rules),
        "timestamp": datetime.now().isoformat(),
    }


def cache_cleanup_job():
    """
    Background job để cleanup expired cache.
    Gọi định kỳ (ví dụ: mỗi 5 phút).
    """
    cleaned = redis_client.cleanup_expired()
    if cleaned > 0:
        logger.info(f"🧹 Cleaned up {cleaned} expired cache entries")
    return cleaned


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def get_or_set(
    key: str,
    factory: Callable,
    ttl: int = CACHE_TTL["MEDIUM"],
) -> Any:
    """
    Get from cache or set using factory function.

    Example:
        products = get_or_set(
            "products:all",
            lambda: db.query(Product).all(),
            ttl=300
        )
    """
    value = redis_client.get(key)
    if value is not None:
        return value

    value = factory()
    redis_client.set(key, value, ttl)
    return value


def cache_aside(key: str, ttl: int = CACHE_TTL["MEDIUM"]):
    """
    Decorator cho cache-aside pattern.

    Example:
        @cache_aside("product:{product_id}", ttl=300)
        def get_product(product_id: int):
            return db.query(Product).get(product_id)
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Format key với arguments
            formatted_key = key.format(*args, **kwargs)

            # Try cache
            cached = redis_client.get(formatted_key)
            if cached is not None:
                return cached

            # Get from source
            result = func(*args, **kwargs)

            # Cache result
            if result is not None:
                redis_client.set(formatted_key, result, ttl)

            return result

        return wrapper

    return decorator
