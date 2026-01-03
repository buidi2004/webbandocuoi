"""
Cache utilities cho IVIE Wedding API
Giúp giảm TTFB bằng cách cache response tĩnh
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Cache durations (seconds)
CACHE_TINY = 60        # 1 phút - cho banners
CACHE_SHORT = 300      # 5 phút - cho product list
CACHE_MEDIUM = 600     # 10 phút - cho combos
CACHE_LONG = 3600      # 1 giờ - cho static content (gallery, blog)
CACHE_NONE = 0         # Không cache - cho mutations

# URL patterns và cache duration
CACHE_RULES = {
    # Tất cả các tính năng được đặt về CACHE_NONE (0s) để phản hồi liền lập tức
    "/api/san_pham": CACHE_NONE,
    "/api/banner": CACHE_NONE,
    "/api/thu_vien": CACHE_NONE,
    "/api/blog": CACHE_NONE,
    "/api/noi_dung": CACHE_NONE,
    "/api/chuyen_gia": CACHE_NONE,
    "/api/combo": CACHE_NONE,
    "/api/dich_vu": CACHE_NONE,
    "/pg/": CACHE_NONE,
}


class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware tự động thêm Cache-Control headers cho GET requests
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Chỉ cache GET requests
        if request.method != "GET":
            response.headers["Cache-Control"] = "no-store"
            return response
        
        # Tìm cache rule phù hợp
        path = request.url.path
        cache_duration = CACHE_NONE
        
        for pattern, duration in CACHE_RULES.items():
            if path.startswith(pattern):
                cache_duration = duration
                break
        
        # Set cache headers
        if cache_duration > 0:
            response.headers["Cache-Control"] = f"public, max-age={cache_duration}"
            response.headers["Vary"] = "Accept-Encoding"
        else:
            # Không cache cho các endpoint khác
            if "/api/" in path:
                response.headers["Cache-Control"] = "no-cache"
        
        return response


def set_cache_headers(response: Response, max_age: int = CACHE_SHORT, public: bool = True):
    """
    Set Cache-Control headers cho response (manual use)
    
    Args:
        response: FastAPI Response object
        max_age: Thời gian cache (seconds)
        public: True nếu có thể cache ở CDN/proxy
    """
    if max_age > 0:
        cache_type = "public" if public else "private"
        response.headers["Cache-Control"] = f"{cache_type}, max-age={max_age}"
        response.headers["Vary"] = "Accept-Encoding"
    else:
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
