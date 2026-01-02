"""
IVIE Wedding Admin - Modules Package
Chứa các module chức năng được tách riêng để tối ưu hiệu năng
"""

__version__ = "2.0.0"
__all__ = [
    "api_client",
    "dashboard",
    "orders",
    "products",
    "contacts",
    "reviews",
    "banners",
    "customers",
    "calendar_module",
    "gallery",
    "services",
    "blog",
    "combos",
    "homepage",
    "utils",
    "redis_cache",
    "cdn_client",
    "debounce",
]


# Lazy import - chỉ import khi được gọi trực tiếp
def __getattr__(name):
    """Lazy loading cho các module con"""
    if name in __all__:
        import importlib

        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
