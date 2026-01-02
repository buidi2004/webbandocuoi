"""
Redis Cache Module - IVIE Wedding Admin
Ultra-fast caching layer to reduce API calls by 90%

Usage:
    from modules.redis_cache import cache_get, cache_set, cache_invalidate

    # Get from cache
    data = cache_get("products:all")

    # Set to cache (5 min TTL)
    cache_set("products:all", data, ttl=300)

    # Invalidate pattern
    cache_invalidate("products:*")
"""

import json
import os
from typing import Any, Dict, List, Optional

import streamlit as st

# Redis import with fallback
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not installed. Run: pip install redis")

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "true").lower() == "true"

# Global Redis client
_redis_client = None


def get_redis_client():
    """
    Get Redis client singleton with connection pooling

    Returns:
        Redis client or None if not available
    """
    global _redis_client

    if not REDIS_AVAILABLE or not REDIS_ENABLED:
        return None

    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
                max_connections=10,
            )
            # Test connection
            _redis_client.ping()
            print("✅ Redis connected successfully")
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            _redis_client = None

    return _redis_client


def cache_get(key: str) -> Optional[Any]:
    """
    Get value from Redis cache

    Args:
        key: Cache key

    Returns:
        Cached value (deserialized) or None if not found

    Example:
        products = cache_get("api:products:all")
    """
    client = get_redis_client()
    if not client:
        return None

    try:
        data = client.get(key)
        if data:
            # Deserialize JSON
            return json.loads(data)
        return None
    except redis.RedisError as e:
        print(f"Redis get error for key '{key}': {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for key '{key}': {e}")
        # Delete corrupted cache
        try:
            client.delete(key)
        except:
            pass
        return None
    except Exception as e:
        print(f"Unexpected error in cache_get: {e}")
        return None


def cache_set(key: str, value: Any, ttl: int = 300) -> bool:
    """
    Set value to Redis cache with TTL

    Args:
        key: Cache key
        value: Value to cache (will be JSON serialized)
        ttl: Time to live in seconds (default: 5 minutes)

    Returns:
        True if successful, False otherwise

    Example:
        cache_set("api:products:all", products, ttl=300)
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        # Serialize to JSON
        serialized = json.dumps(value, ensure_ascii=False)

        # Set with expiration
        client.setex(key, ttl, serialized)
        return True
    except redis.RedisError as e:
        print(f"Redis set error for key '{key}': {e}")
        return False
    except (TypeError, ValueError) as e:
        print(f"Serialization error for key '{key}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in cache_set: {e}")
        return False


def cache_delete(key: str) -> bool:
    """
    Delete specific key from cache

    Args:
        key: Cache key to delete

    Returns:
        True if deleted, False otherwise

    Example:
        cache_delete("api:products:123")
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        client.delete(key)
        return True
    except redis.RedisError as e:
        print(f"Redis delete error for key '{key}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in cache_delete: {e}")
        return False


def cache_invalidate(pattern: str) -> int:
    """
    Invalidate cache by pattern (wildcard support)

    Args:
        pattern: Key pattern (supports * wildcard)

    Returns:
        Number of keys deleted

    Example:
        # Delete all product caches
        cache_invalidate("api:products:*")

        # Delete all order caches
        cache_invalidate("api:orders:*")

        # Delete everything
        cache_invalidate("*")
    """
    client = get_redis_client()
    if not client:
        return 0

    try:
        # Find matching keys
        keys = client.keys(pattern)

        if keys:
            # Delete all matching keys
            deleted = client.delete(*keys)
            print(f"🗑️  Invalidated {deleted} cache keys matching '{pattern}'")
            return deleted

        return 0
    except redis.RedisError as e:
        print(f"Redis invalidate error for pattern '{pattern}': {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error in cache_invalidate: {e}")
        return 0


def cache_clear_all() -> bool:
    """
    Clear all cache (use with caution!)

    Returns:
        True if successful, False otherwise

    Example:
        cache_clear_all()
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        client.flushdb()
        print("🗑️  All cache cleared")
        return True
    except redis.RedisError as e:
        print(f"Redis clear all error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in cache_clear_all: {e}")
        return False


def cache_exists(key: str) -> bool:
    """
    Check if key exists in cache

    Args:
        key: Cache key

    Returns:
        True if exists, False otherwise

    Example:
        if cache_exists("api:products:all"):
            print("Cache hit!")
    """
    client = get_redis_client()
    if not client:
        return False

    try:
        return client.exists(key) > 0
    except redis.RedisError as e:
        print(f"Redis exists error for key '{key}': {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in cache_exists: {e}")
        return False


def cache_ttl(key: str) -> int:
    """
    Get remaining TTL for key

    Args:
        key: Cache key

    Returns:
        Remaining TTL in seconds, -1 if no TTL, -2 if key doesn't exist

    Example:
        ttl = cache_ttl("api:products:all")
        print(f"Cache expires in {ttl} seconds")
    """
    client = get_redis_client()
    if not client:
        return -2

    try:
        return client.ttl(key)
    except redis.RedisError as e:
        print(f"Redis TTL error for key '{key}': {e}")
        return -2
    except Exception as e:
        print(f"Unexpected error in cache_ttl: {e}")
        return -2


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics

    Returns:
        Dictionary with cache stats

    Example:
        stats = get_cache_stats()
        print(f"Total keys: {stats['total_keys']}")
    """
    client = get_redis_client()
    if not client:
        return {"available": False, "error": "Redis not available"}

    try:
        info = client.info("stats")
        db_info = client.info("keyspace")

        total_keys = 0
        if "db0" in db_info:
            total_keys = db_info["db0"]["keys"]

        return {
            "available": True,
            "total_keys": total_keys,
            "total_commands": info.get("total_commands_processed", 0),
            "hits": info.get("keyspace_hits", 0),
            "misses": info.get("keyspace_misses", 0),
            "hit_rate": round(
                info.get("keyspace_hits", 0)
                / max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1)
                * 100,
                2,
            ),
        }
    except redis.RedisError as e:
        return {"available": False, "error": str(e)}
    except Exception as e:
        return {"available": False, "error": str(e)}


# ============================================================
# SMART CACHE HELPERS for specific data types
# ============================================================


def cache_api_response(endpoint: str, data: Any, ttl: int = 300) -> bool:
    """
    Cache API response with standard key format

    Args:
        endpoint: API endpoint path
        data: Response data
        ttl: Time to live in seconds

    Returns:
        True if cached successfully

    Example:
        cache_api_response("/api/products", products, ttl=300)
    """
    key = f"api:{endpoint}"
    return cache_set(key, data, ttl)


def get_cached_api_response(endpoint: str) -> Optional[Any]:
    """
    Get cached API response

    Args:
        endpoint: API endpoint path

    Returns:
        Cached response or None

    Example:
        products = get_cached_api_response("/api/products")
    """
    key = f"api:{endpoint}"
    return cache_get(key)


def invalidate_api_cache(endpoint_pattern: str = "*") -> int:
    """
    Invalidate API caches

    Args:
        endpoint_pattern: Pattern to match (default: all)

    Returns:
        Number of keys deleted

    Example:
        # Invalidate all product caches
        invalidate_api_cache("products*")

        # Invalidate all API caches
        invalidate_api_cache()
    """
    pattern = f"api:*{endpoint_pattern}*"
    return cache_invalidate(pattern)


# ============================================================
# STREAMLIT INTEGRATION
# ============================================================


def show_cache_status():
    """
    Display cache status in Streamlit sidebar (for debugging)

    Usage:
        In your Streamlit app:
        with st.sidebar:
            show_cache_status()
    """
    if not REDIS_AVAILABLE:
        st.sidebar.warning("⚠️ Redis not installed")
        return

    if not REDIS_ENABLED:
        st.sidebar.info("ℹ️ Redis disabled")
        return

    stats = get_cache_stats()

    if not stats.get("available"):
        st.sidebar.error(f"❌ Redis error: {stats.get('error', 'Unknown')}")
        return

    with st.sidebar.expander("📊 Cache Stats", expanded=False):
        st.metric("Keys", stats["total_keys"])
        st.metric("Hit Rate", f"{stats['hit_rate']}%")
        st.metric("Hits", stats["hits"])
        st.metric("Misses", stats["misses"])

        if st.button("🗑️ Clear All Cache"):
            if cache_clear_all():
                st.success("Cache cleared!")
                st.rerun()


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    # Core functions
    "cache_get",
    "cache_set",
    "cache_delete",
    "cache_invalidate",
    "cache_clear_all",
    "cache_exists",
    "cache_ttl",
    "get_cache_stats",
    # API helpers
    "cache_api_response",
    "get_cached_api_response",
    "invalidate_api_cache",
    # Streamlit integration
    "show_cache_status",
    # Status
    "REDIS_AVAILABLE",
    "REDIS_ENABLED",
]
