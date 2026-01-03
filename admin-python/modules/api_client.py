"""
API Client Module - Optimized for IVIE Wedding Admin
Handles all API calls with caching, retry logic, and connection pooling
"""

import io
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional

import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Priority: API_BASE_URL (Render env var) > VITE_API_BASE_URL > localhost
API_URL = (
    os.getenv("API_BASE_URL")
    or os.getenv("VITE_API_BASE_URL")
    or "http://localhost:8000"
)

# Thread pool for parallel requests (max 4 concurrent)
executor = ThreadPoolExecutor(max_workers=4)

# Session state initialization
if "backend_awake" not in st.session_state:
    st.session_state.backend_awake = False
if "last_action" not in st.session_state:
    st.session_state.last_action = None


def get_session() -> requests.Session:
    """
    Tạo session requests với connection pooling để tối ưu hiệu suất
    Sử dụng adapter với retry logic và keep-alive
    """
    session = requests.Session()

    # Connection pooling - giữ nhiều connection sẵn sàng
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10,
        pool_maxsize=20,
        max_retries=requests.adapters.Retry(
            total=2, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504]
        ),
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Headers tối ưu
    session.headers.update(
        {
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    return session


def wake_up_backend() -> bool:
    """
    Đánh thức backend nếu đang sleep (Render free tier)
    Trả về True nếu backend đã sẵn sàng
    """
    try:
        session = get_session()
        res = session.get(f"{API_URL}/api/health", timeout=60)
        if res.status_code == 200:
            st.session_state.backend_awake = True
            return True
        return False
    except Exception:
        return False


@st.cache_data(show_spinner=False, ttl=120)  # Cache 2 phút
def fetch_api_data(endpoint: str) -> Optional[Dict]:
    """
    Cached version for GET requests with 2 min TTL
    Tự động cache để giảm số lần gọi API
    """
    url = f"{API_URL}{endpoint}"
    try:
        session = get_session()
        res = session.get(url, timeout=20)
        if res.status_code == 200:
            st.session_state.backend_awake = True
            return res.json()
        return None
    except Exception:
        return None


# ============================================================
# CACHED FETCHERS - TTL khác nhau tùy theo tính chất dữ liệu
# ============================================================


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút - ít thay đổi
def fetch_products_cached() -> Optional[List]:
    """Cached products list - sản phẩm ít thay đổi"""
    return fetch_api_data("/api/san_pham/")


@st.cache_data(show_spinner=False, ttl=60)  # Cache 1 phút - thay đổi thường xuyên
def fetch_orders_cached() -> Optional[List]:
    """Cached orders list - đơn hàng thay đổi thường xuyên"""
    return fetch_api_data("/api/don_hang/")


@st.cache_data(show_spinner=False, ttl=60)  # Cache 1 phút
def fetch_contacts_cached() -> Optional[List]:
    """Cached contacts list"""
    return fetch_api_data("/api/lien_he/")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_banners_cached() -> Optional[List]:
    """Cached banners list"""
    data = fetch_api_data("/api/banner/tat_ca")
    if data is None:
        data = fetch_api_data("/api/banner/")
    return data


@st.cache_data(show_spinner=False, ttl=180)  # Cache 3 phút
def fetch_dashboard_stats() -> Optional[Dict]:
    """Cached dashboard statistics"""
    return fetch_api_data("/api/thong_ke/tong_quan")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_reviews_cached() -> Optional[List]:
    """Cached reviews list - Lấy đánh giá chờ duyệt"""
    return fetch_api_data("/api/san_pham/admin/danh_gia_cho_duyet")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_users_cached() -> Optional[List]:
    """Cached users list"""
    return fetch_api_data("/pg/nguoi-dung")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_combos_cached() -> Optional[List]:
    """Cached combos list"""
    return fetch_api_data("/pg/combo")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_gallery_cached() -> Optional[List]:
    """Cached gallery images"""
    return fetch_api_data("/api/thu_vien/")


@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút
def fetch_blog_cached() -> Optional[List]:
    """Cached blog posts"""
    return fetch_api_data("/api/blog")


# ============================================================
# CACHE INVALIDATION
# ============================================================


def invalidate_cache(scope: Optional[str] = None) -> None:
    """
    Xóa cache theo phạm vi hoặc toàn bộ

    Args:
        scope: "products", "orders", "contacts", "banners", "dashboard",
               "reviews", "users", "combos", "gallery", "blog", hoặc None (xóa tất cả)
    """
    if scope is None:
        st.cache_data.clear()
    elif scope == "products":
        fetch_products_cached.clear()
    elif scope == "orders":
        fetch_orders_cached.clear()
    elif scope == "contacts":
        fetch_contacts_cached.clear()
    elif scope == "banners":
        fetch_banners_cached.clear()
    elif scope == "dashboard":
        fetch_dashboard_stats.clear()
    elif scope == "reviews":
        fetch_reviews_cached.clear()
    elif scope == "users":
        fetch_users_cached.clear()
    elif scope == "combos":
        fetch_combos_cached.clear()
    elif scope == "gallery":
        fetch_gallery_cached.clear()
    elif scope == "blog":
        fetch_blog_cached.clear()


# ============================================================
# PARALLEL REQUESTS
# ============================================================


def fetch_multiple_endpoints(endpoints: List[str]) -> Dict[str, Any]:
    """
    Fetch nhiều endpoints song song với timeout tối ưu
    Sử dụng ThreadPoolExecutor để tăng tốc độ load

    Args:
        endpoints: List of API endpoints to fetch

    Returns:
        Dictionary with endpoint as key and data as value
    """

    def fetch_one(endpoint: str):
        return endpoint, fetch_api_data(endpoint)

    results = {}
    futures = [executor.submit(fetch_one, ep) for ep in endpoints]
    for future in futures:
        try:
            ep, data = future.result(timeout=25)
            results[ep] = data
        except Exception:
            pass
    return results


# ============================================================
# API CALL WITH RETRY LOGIC
# ============================================================


def call_api(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    files: Optional[Dict] = None,
    clear_cache: bool = True,
    retries: int = 2,
) -> Optional[Dict]:
    """
    Gọi API với retry logic cho Render free tier

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        endpoint: API endpoint path
        data: JSON data for request body
        files: Files for upload
        clear_cache: Whether to clear relevant caches after mutation
        retries: Number of retry attempts

    Returns:
        Response JSON or None if failed
    """
    url = f"{API_URL}{endpoint}"
    session = get_session()

    for attempt in range(retries + 1):
        try:
            # Timeout dài hơn cho lần đầu (backend có thể đang sleep)
            timeout = 60 if attempt == 0 and not st.session_state.backend_awake else 15

            if method == "GET":
                if not clear_cache:
                    return fetch_api_data(endpoint)
                res = session.get(url, timeout=timeout)
            elif method == "POST":
                res = session.post(url, json=data, files=files, timeout=timeout)
            elif method == "PUT":
                res = session.put(url, json=data, timeout=timeout)
            elif method == "PATCH":
                res = session.patch(url, json=data, timeout=timeout)
            elif method == "DELETE":
                res = session.delete(url, timeout=timeout)
            else:
                st.error(f"Invalid HTTP method: {method}")
                return None

            if res.status_code in [200, 201]:
                st.session_state.backend_awake = True

                # Smart cache invalidation based on endpoint
                if method != "GET" and clear_cache:
                    if "/san_pham" in endpoint:
                        invalidate_cache("products")
                        invalidate_cache("dashboard")
                    elif "/don_hang" in endpoint:
                        invalidate_cache("orders")
                        invalidate_cache("dashboard")
                    elif "/lien_he" in endpoint:
                        invalidate_cache("contacts")
                        invalidate_cache("dashboard")
                    elif "/banner" in endpoint:
                        invalidate_cache("banners")
                    elif "/danh_gia" in endpoint:
                        invalidate_cache("reviews")
                    elif "/nguoi_dung" in endpoint:
                        invalidate_cache("users")
                    elif "/combo" in endpoint:
                        invalidate_cache("combos")
                    elif "/thu_vien" in endpoint:
                        invalidate_cache("gallery")
                    elif "/blog" in endpoint:
                        invalidate_cache("blog")
                    else:
                        st.cache_data.clear()

                return res.json()
            else:
                st.error(f"❌ Lỗi API ({res.status_code}): {res.text[:200]}")
                return None

        except requests.Timeout:
            if attempt < retries:
                st.warning(
                    f"⏳ Server đang khởi động... (thử lại {attempt + 1}/{retries})"
                )
                continue
            st.error("⏱️ Server phản hồi chậm. Vui lòng thử lại sau.")
            return None

        except requests.ConnectionError:
            if attempt < retries:
                st.warning(f"🔄 Đang kết nối lại... (thử lại {attempt + 1}/{retries})")
                continue
            st.error("❌ Không thể kết nối đến server. Vui lòng kiểm tra kết nối mạng.")
            return None

        except Exception as e:
            st.error(f"❌ Lỗi kết nối: {str(e)}")
            return None

    return None


# ============================================================
# IMAGE UPLOAD WITH COMPRESSION
# ============================================================


def upload_image(uploaded_file) -> Optional[str]:
    """
    Upload ảnh với compression để tối ưu tốc độ

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Image URL if successful, None otherwise
    """
    if uploaded_file is None:
        return None

    try:
        # Compress image trước khi upload - tối ưu hơn
        img = Image.open(uploaded_file)

        # Resize nhỏ hơn để upload nhanh
        max_size = (1000, 1000)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Convert to RGB if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Save to buffer với quality 80%
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80, optimize=True)
        buffer.seek(0)

        files = {
            "file": (
                uploaded_file.name.rsplit(".", 1)[0] + ".jpg",
                buffer,
                "image/jpeg",
            )
        }
    except Exception:
        # Fallback nếu không compress được
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

    url = f"{API_URL}/api/tap_tin/upload"
    try:
        session = get_session()
        # Timeout dài hơn cho upload (60s cho lần đầu khi backend sleep)
        timeout = 60 if not st.session_state.get("backend_awake", False) else 30
        res = session.post(url, files=files, timeout=timeout)

        if res.status_code == 200:
            st.session_state.backend_awake = True
            return res.json().get("url")

        st.error(f"❌ Lỗi tải ảnh ({res.status_code})")
        return None

    except requests.Timeout:
        st.error(
            "⏱️ Upload ảnh quá lâu. Server có thể đang khởi động, vui lòng thử lại."
        )
        return None

    except Exception as e:
        st.error(f"❌ Lỗi upload: {str(e)}")
        return None


def upload_images_parallel(files_list: List) -> List[str]:
    """
    Upload nhiều ảnh song song để tiết kiệm thời gian

    Args:
        files_list: List of uploaded files

    Returns:
        List of image URLs
    """
    if not files_list:
        return []

    def upload_one(f):
        return upload_image(f)

    results = []
    futures = [executor.submit(upload_one, f) for f in files_list]

    for future in futures:
        try:
            url = future.result(timeout=40)
            if url:
                results.append(url)
        except Exception:
            pass

    return results


# ============================================================
# IMAGE URL HELPERS
# ============================================================


@st.cache_data(show_spinner=False, ttl=900)  # Cache URL ảnh 15 phút
def lay_url_anh(path: str) -> str:
    """
    Cached image URL generation

    Args:
        path: Image path (relative or absolute URL)

    Returns:
        Full image URL
    """
    if not path:
        return "https://placehold.co/400x300/000000/ffffff?text=No+Image"
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{API_URL}{path}"


@st.cache_data(show_spinner=False, ttl=300)
def get_image_placeholder() -> str:
    """Placeholder image for lazy loading"""
    return "https://placehold.co/200x200/111/333?text=Loading..."


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "API_URL",
    "get_session",
    "wake_up_backend",
    "fetch_api_data",
    "fetch_products_cached",
    "fetch_orders_cached",
    "fetch_contacts_cached",
    "fetch_banners_cached",
    "fetch_dashboard_stats",
    "fetch_reviews_cached",
    "fetch_users_cached",
    "fetch_combos_cached",
    "fetch_gallery_cached",
    "fetch_blog_cached",
    "invalidate_cache",
    "fetch_multiple_endpoints",
    "call_api",
    "upload_image",
    "upload_images_parallel",
    "lay_url_anh",
    "get_image_placeholder",
]
