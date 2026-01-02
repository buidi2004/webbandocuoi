"""
IVIE Wedding Studio - Admin Panel (Optimized)
===========================================
Mục tiêu:
- Khôi phục đầy đủ luồng admin (login/auth + menu theo quyền) tương đương `quan_tri.py`
- Giữ/đẩy mạnh tối ưu hiệu năng (cache, session pooling, debounce, pagination, lazy rendering)
- Routing/menu rõ ràng, dễ mở rộng

Đã port:
- Banner management (list + create + delete + image upload) với caching & cache invalidation chuẩn

Ghi chú:
- File này dựa trên cấu trúc project hiện có: `auth.py`, `analytics.py`, backend API endpoints.
- Không hardcode secrets. Dùng env `API_BASE_URL` hoặc `VITE_API_BASE_URL`.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# =============================================================================
# PAGE CONFIG (PHẢI Ở ĐẦU)
# =============================================================================

st.set_page_config(
    page_title="IVIE Wedding Admin",
    layout="wide",
    page_icon="🏯",
    initial_sidebar_state="expanded",
)

# =============================================================================
# ENV / CONFIG
# =============================================================================

load_dotenv()
API_URL = os.getenv(
    "API_BASE_URL", os.getenv("VITE_API_BASE_URL", "http://localhost:8000")
)

API_TIMEOUT = int(os.getenv("ADMIN_API_TIMEOUT", "10"))
MAX_WORKERS = int(os.getenv("ADMIN_MAX_WORKERS", "4"))
MAX_RETRIES = int(os.getenv("ADMIN_MAX_RETRIES", "2"))

# Uploads can be slower (especially after Render sleep)
UPLOAD_TIMEOUT = int(os.getenv("ADMIN_UPLOAD_TIMEOUT", "60"))

CACHE_TTL = {
    "SHORT": 60,
    "MEDIUM": 300,
    "LONG": 900,
    "EXTENDED": 3600,
}

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# =============================================================================
# OPTIONAL IMPORTS (AUTH / ANALYTICS)
# =============================================================================

# Auth module (bắt buộc)
try:
    from auth import (  # type: ignore
        MENU_PERMISSIONS,
        get_allowed_menu_items,
        has_permission,
        init_session,
        is_authenticated,
        show_login_page,
        show_user_info_sidebar,
    )
except Exception as e:
    st.error(f"❌ Không import được `auth.py`: {e}")
    st.stop()

# Analytics module (tuỳ chọn)
try:
    from analytics import (  # type: ignore
        du_bao_moving_average,
        goi_y_san_pham,
        phan_tich_cam_xuc,
        phan_tich_danh_gia_list,
        phan_tich_ket_hop,
        phan_tich_rfm,
        thong_ke_cam_xuc,
        thong_ke_rfm,
        tinh_doanh_thu_theo_thang,
        tinh_tang_truong,
    )

    HAS_ANALYTICS = True
except Exception:
    HAS_ANALYTICS = False


# =============================================================================
# CSS (nhẹ, dark)
# =============================================================================

st.markdown(
    """
<style>
.stApp { background-color: #000; color: #fff; }
.main { background-color: #000; }

.stButton>button {
    width: 100%;
    background-color: #000;
    color: #fff;
    border: 1px solid #333;
    border-radius: 6px;
    transition: all .15s ease-in-out;
}
.stButton>button:hover { border-color: #fff; }
.stButton>button:disabled { opacity: .5; }

.stTextInput>div>div>input,
.stSelectbox>div>div>div,
.stNumberInput>div>div>input,
.stTextArea>div>div>textarea {
    background-color: #111 !important;
    color: #fff !important;
    border: 1px solid #333 !important;
}

h1,h2,h3,h4 { color: #fff !important; font-weight: 300; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# SESSION STATE INIT
# =============================================================================


def init_session_state():
    defaults = {
        "current_page": "dashboard",
        "products_page": 1,
        "orders_page": 1,
        "contacts_page": 1,
        "toast_message": None,
        "toast_type": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session_state()


# =============================================================================
# HTTP CLIENT (pooled)
# =============================================================================


@st.cache_resource
def get_session_http() -> requests.Session:
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10,
        pool_maxsize=20,
        max_retries=requests.adapters.Retry(
            total=MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        ),
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(
        {"Accept": "application/json", "Content-Type": "application/json"}
    )
    return session


@st.cache_resource
def get_executor() -> ThreadPoolExecutor:
    return ThreadPoolExecutor(max_workers=MAX_WORKERS)


def api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    timeout: int = API_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Low-level API call.
    - Prefer `get_json()` for GET (cached).
    - Use `invalidate_after_mutation()` after write operations.
    """
    session = get_session_http()
    url = f"{API_URL}{endpoint}"

    for attempt in range(retries + 1):
        try:
            if method == "GET":
                res = session.get(url, params=params, timeout=timeout)
            elif method == "POST":
                res = session.post(url, json=data, timeout=timeout)
            elif method == "PUT":
                res = session.put(url, json=data, timeout=timeout)
            elif method == "PATCH":
                res = session.patch(url, json=data, timeout=timeout)
            elif method == "DELETE":
                res = session.delete(url, timeout=timeout)
            else:
                return None, f"Unsupported method: {method}"

            if res.status_code >= 400:
                try:
                    detail = res.json()
                except Exception:
                    detail = res.text
                return None, f"API Error: {res.status_code} - {detail}"

            # Some endpoints may return empty body
            if not res.text:
                return None, None
            return res.json(), None

        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            return None, "Request timeout"
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            return None, str(e)

    return None, "Max retries exceeded"


def _stable_json_dumps(obj: Any) -> str:
    try:
        return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    except Exception:
        return str(obj)


def _cache_key(endpoint: str, params: Optional[dict]) -> str:
    raw = f"{endpoint}|{_stable_json_dumps(params or {})}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def _cached_get_json(
    endpoint: str, params: Optional[dict], key: str
) -> Tuple[Optional[Any], Optional[str]]:
    data, err = api_request(endpoint, method="GET", params=params)
    return data, err


def get_json(
    endpoint: str, params: Optional[dict] = None
) -> Tuple[Optional[Any], Optional[str]]:
    key = _cache_key(endpoint, params)
    return _cached_get_json(endpoint, params, key)


def invalidate_after_mutation(scopes: Optional[List[str]] = None):
    """
    Clear caches after write operations.
    scopes: "products", "orders", "dashboard", "banners", "blogs", "contacts", "reviews", "all"
    """
    if not scopes or "all" in scopes:
        _cached_get_json.clear()
        fetch_products.clear()
        fetch_orders.clear()
        fetch_dashboard_stats.clear()
        fetch_banners.clear()
        fetch_blogs.clear()
        fetch_contacts.clear()
        fetch_pending_reviews.clear()
        return

    _cached_get_json.clear()
    for s in scopes:
        if s == "products":
            fetch_products.clear()
        elif s == "orders":
            fetch_orders.clear()
        elif s == "dashboard":
            fetch_dashboard_stats.clear()
        elif s == "banners":
            fetch_banners.clear()
        elif s == "blogs":
            fetch_blogs.clear()
        elif s == "contacts":
            fetch_contacts.clear()
        elif s == "reviews":
            fetch_pending_reviews.clear()


def fetch_parallel(endpoints: List[str]) -> Dict[str, Dict[str, Any]]:
    executor = get_executor()
    futures = {}

    def one(ep: str):
        d, e = get_json(ep)
        return ep, d, e

    for ep in endpoints:
        futures[executor.submit(one, ep)] = ep

    out: Dict[str, Dict[str, Any]] = {}
    for fut in as_completed(futures):
        ep = futures[fut]
        try:
            _ep, d, e = fut.result()
            out[ep] = {"data": d, "error": e}
        except Exception as ex:
            out[ep] = {"data": None, "error": str(ex)}
    return out


# =============================================================================
# CACHED FETCHERS (đọc)
# =============================================================================


@st.cache_data(ttl=CACHE_TTL["MEDIUM"], show_spinner=False)
def fetch_products(
    category: Optional[str] = None,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    sort_by: str = "id_desc",
) -> Tuple[List[Dict], int]:
    params: Dict[str, Any] = {"page": page, "page_size": page_size, "sort_by": sort_by}
    if category:
        params["danh_muc"] = category

    data, err = get_json("/api/san_pham/", params=params)
    if err or data is None:
        return [], 0

    if isinstance(data, dict) and "items" in data:
        return data.get("items", []), int(data.get("pagination", {}).get("total", 0))
    if isinstance(data, list):
        return data, len(data)
    return [], 0


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_orders(
    status: Optional[str] = None, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE
) -> Tuple[List[Dict], int]:
    params: Dict[str, Any] = {"page": page, "page_size": page_size}
    if status:
        params["status"] = status

    data, err = get_json("/api/don_hang/", params=params)
    if err or data is None:
        return [], 0

    if isinstance(data, dict) and "items" in data:
        return data.get("items", []), int(data.get("pagination", {}).get("total", 0))
    if isinstance(data, list):
        return data, len(data)
    return [], 0


@st.cache_data(ttl=CACHE_TTL["MEDIUM"], show_spinner=False)
def fetch_dashboard_stats() -> Dict[str, Any]:
    data, err = get_json("/api/thong_ke/tong_quan")
    if err or data is None:
        return {}
    return data if isinstance(data, dict) else {}


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def fetch_banners() -> List[Dict]:
    """
    Banner list endpoint differs between implementations.
    - Prefer /api/banner/tat_ca (admin full list)
    - Fallback /api/banner/ (public/active list)
    """
    data, err = get_json("/api/banner/tat_ca")
    if not err and isinstance(data, list):
        return data

    data2, _ = get_json("/api/banner/")
    return data2 if isinstance(data2, list) else []


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def fetch_blogs(page: int = 1, page_size: int = 20) -> List[Dict]:
    params = {"bo_qua": (page - 1) * page_size, "gioi_han": page_size}
    data, _ = get_json("/api/blog/", params=params)
    return data if isinstance(data, list) else []


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_contacts(status: Optional[str] = None) -> List[Dict]:
    params = {}
    if status:
        params["status"] = status
    data, _ = get_json("/api/lien_he/", params=params)
    return data if isinstance(data, list) else []


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_pending_reviews() -> List[Dict]:
    data, _ = get_json("/api/san_pham/admin/danh_gia_cho_duyet")
    return data if isinstance(data, list) else []


# =============================================================================
# UI HELPERS
# =============================================================================


def show_toast(message: str, type_: str = "info"):
    icons = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
    st.toast(f"{icons.get(type_, 'ℹ️')} {message}")


@st.cache_data(show_spinner=False, ttl=CACHE_TTL["LONG"])
def build_asset_url(path: str) -> str:
    """
    Normalize image/file URL:
    - absolute http(s) -> keep
    - relative -> prefix API_URL
    """
    if not path:
        return "https://placehold.co/400x300/000000/ffffff?text=No+Image"
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{API_URL}{path}"


def upload_image(uploaded_file) -> Optional[str]:
    """
    Upload an image via backend upload endpoint.
    Mirrors behavior in `quan_tri.py` but uses pooled session + longer timeout.
    """
    if uploaded_file is None:
        return None

    files = None

    # Compress/resize before upload (faster, smaller)
    try:
        img = Image.open(uploaded_file)
        max_size = (1000, 1000)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=80, optimize=True)
        buffer.seek(0)

        safe_name = uploaded_file.name.rsplit(".", 1)[0] + ".jpg"
        files = {"file": (safe_name, buffer, "image/jpeg")}
    except Exception:
        # Fallback: upload raw
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }
        except Exception:
            return None

    url = f"{API_URL}/api/tap_tin/upload"
    session = get_session_http()
    try:
        res = session.post(url, files=files, timeout=UPLOAD_TIMEOUT)
        if res.status_code == 200:
            try:
                payload = res.json()
            except Exception:
                payload = {}
            return payload.get("url")
        return None
    except Exception:
        return None


def format_currency(amount: Any) -> str:
    try:
        x = float(amount or 0)
    except Exception:
        x = 0.0
    return f"{x:,.0f} ₫"


def format_datetime(dt_str: str) -> str:
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return dt_str


def pagination_component(
    total_items: int, page_size: int, current_page: int, key: str
) -> int:
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    c1, c2, c3, c4, c5 = st.columns([1, 1, 2, 1, 1])

    with c1:
        if st.button("⏮️", key=f"{key}_first", disabled=current_page <= 1):
            return 1
    with c2:
        if st.button("◀️", key=f"{key}_prev", disabled=current_page <= 1):
            return max(1, current_page - 1)
    with c3:
        st.markdown(
            f"<center>Trang **{current_page}** / {total_pages} ({total_items} items)</center>",
            unsafe_allow_html=True,
        )
    with c4:
        if st.button("▶️", key=f"{key}_next", disabled=current_page >= total_pages):
            return min(total_pages, current_page + 1)
    with c5:
        if st.button("⏭️", key=f"{key}_last", disabled=current_page >= total_pages):
            return total_pages

    return current_page


def debounced_text_input(label: str, key: str, delay: float = 0.5, **kwargs) -> str:
    value_key = f"{key}_value"
    time_key = f"{key}_time"
    stable_key = f"{key}_stable"

    value = st.text_input(label, key=key, **kwargs)

    if stable_key not in st.session_state:
        st.session_state[stable_key] = value

    if value != st.session_state.get(value_key):
        st.session_state[value_key] = value
        st.session_state[time_key] = time.time()

    last_change = st.session_state.get(time_key, 0)
    if time.time() - last_change >= delay:
        st.session_state[stable_key] = value

    return st.session_state.get(stable_key, "")


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def get_image_thumbnail(
    image_url: str, size: Tuple[int, int] = (100, 100)
) -> Optional[bytes]:
    if not image_url:
        return None

    try:
        if image_url.startswith("/"):
            image_url = f"{API_URL}{image_url}"

        session = get_session_http()
        res = session.get(image_url, timeout=5)
        if res.status_code != 200 or not res.content:
            return None

        img = Image.open(io.BytesIO(res.content))
        img.thumbnail(size, Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=85, optimize=True)
        return buf.getvalue()
    except Exception:
        return None


def lazy_image(image_url: str, width: int = 90, caption: Optional[str] = None):
    thumb = get_image_thumbnail(image_url, (width, width))
    if thumb:
        st.image(thumb, width=width, caption=caption)
        return
    if image_url and image_url.startswith("/"):
        image_url = f"{API_URL}{image_url}"
    if image_url:
        st.image(image_url, width=width, caption=caption)
    else:
        st.caption("No Image")


# =============================================================================
# PAGES (optimized, restore routing)
# =============================================================================


def page_dashboard():
    st.title("📊 Tổng quan Dashboard")

    with st.spinner("Đang tải thống kê..."):
        stats = fetch_dashboard_stats()

    if not stats:
        st.warning("Không thể tải thống kê.")
        if st.button("🔄 Thử lại"):
            fetch_dashboard_stats.clear()
            st.rerun()
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🛍️ Sản phẩm", stats.get("tong_san_pham", 0))
    with c2:
        st.metric("📦 Đơn hàng", stats.get("tong_don_hang", 0))
    with c3:
        st.metric("👤 Người dùng", stats.get("tong_nguoi_dung", 0))
    with c4:
        st.metric("💰 Doanh thu", format_currency(stats.get("tong_doanh_thu", 0)))

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"⏳ Đơn chờ xử lý: **{stats.get('don_hang_cho_xu_ly', 0)}**")
    with c2:
        st.success(f"✅ Đơn hoàn thành: **{stats.get('don_hang_hoan_thanh', 0)}**")
    with c3:
        st.warning(f"📬 Liên hệ mới: **{stats.get('lien_he_chua_xu_ly', 0)}**")

    if HAS_ANALYTICS:
        with st.expander("📈 Phân tích nâng cao (Analytics)", expanded=False):
            st.caption(
                "Analytics đã được bật. Các phần chi tiết giữ ở `quan_tri.py` (có thể port dần)."
            )
    else:
        st.caption("ℹ️ Analytics module chưa sẵn sàng trong môi trường hiện tại.")


def page_products():
    st.title("📦 Quản lý sản phẩm")

    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        category = st.selectbox(
            "Danh mục", ["Tất cả", "wedding_modern", "traditional", "vest"], key="p_cat"
        )
        if category == "Tất cả":
            category = None
    with col2:
        sort_by = st.selectbox(
            "Sắp xếp",
            ["id_desc", "id_asc", "price_asc", "price_desc", "hot", "new"],
            format_func=lambda x: {
                "id_desc": "Mới nhất",
                "id_asc": "Cũ nhất",
                "price_asc": "Giá tăng dần",
                "price_desc": "Giá giảm dần",
                "hot": "Hot",
                "new": "Mới",
            }.get(x, x),
            key="p_sort",
        )
    with col3:
        page_size = st.selectbox("Hiển thị", [10, 20, 50, 100], index=1, key="p_ps")
    with col4:
        if st.button("🔄", key="p_refresh"):
            fetch_products.clear()
            st.session_state.products_page = 1
            st.rerun()

    st.divider()
    products, total = fetch_products(
        category=category,
        page=st.session_state.products_page,
        page_size=page_size,
        sort_by=sort_by,
    )
    if not products:
        st.info("Không có sản phẩm.")
        return

    st.markdown(f"**Tìm thấy {total} sản phẩm**")

    df = pd.DataFrame(
        [
            {
                "ID": p.get("id"),
                "Mã": p.get("code", "N/A"),
                "Tên": (p.get("name") or "N/A")[:60],
                "Danh mục": p.get("category", "N/A"),
                "Giá thuê": format_currency(p.get("rental_price_day", 0)),
                "Hot": "🔥" if p.get("is_hot") else "",
                "Mới": "🆕" if p.get("is_new") else "",
            }
            for p in products
        ]
    )
    st.dataframe(df, use_container_width=True, hide_index=True)

    new_page = pagination_component(
        total_items=total,
        page_size=page_size,
        current_page=st.session_state.products_page,
        key="products",
    )
    if new_page != st.session_state.products_page:
        st.session_state.products_page = new_page
        st.rerun()

    st.caption(
        "ℹ️ Các thao tác thêm/sửa/xóa chi tiết hiện vẫn nằm ở `quan_tri.py` (có thể port tiếp)."
    )


def page_orders():
    st.title("🛒 Quản lý đơn hàng")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả", "pending", "processing", "shipped", "delivered", "cancelled"],
            format_func=lambda x: {
                "Tất cả": "Tất cả",
                "pending": "⏳ Chờ xử lý",
                "processing": "🔄 Đang xử lý",
                "shipped": "🚚 Đang giao",
                "delivered": "✅ Đã giao",
                "cancelled": "❌ Đã hủy",
            }.get(x, x),
            key="o_status",
        )
    with col2:
        page_size = st.selectbox("Hiển thị", [10, 20, 50], index=1, key="o_ps")
    with col3:
        if st.button("🔄", key="o_refresh"):
            fetch_orders.clear()
            st.session_state.orders_page = 1
            st.rerun()

    st.divider()
    status = None if status_filter == "Tất cả" else status_filter
    orders, total = fetch_orders(
        status=status, page=st.session_state.orders_page, page_size=page_size
    )
    if not orders:
        st.info("Không có đơn hàng.")
        return

    st.markdown(f"**Tìm thấy {total} đơn hàng**")

    for order in orders:
        with st.expander(
            f"🧾 Đơn #{order.get('id', 'N/A')} - {order.get('customer_name', 'N/A')}"
        ):
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"**Khách hàng:** {order.get('customer_name', 'N/A')}")
                st.write(f"**SĐT:** {order.get('customer_phone', 'N/A')}")
            with c2:
                st.write(
                    f"**Tổng tiền:** {format_currency(order.get('total_amount', 0))}"
                )
                st.write(
                    f"**Ngày đặt:** {format_datetime(order.get('order_date', ''))}"
                )
            with c3:
                badges = {
                    "pending": "🟡 Chờ xử lý",
                    "processing": "🔵 Đang xử lý",
                    "shipped": "🟠 Đang giao",
                    "delivered": "🟢 Đã giao",
                    "cancelled": "🔴 Đã hủy",
                }
                st.write(
                    f"**Trạng thái:** {badges.get(order.get('status'), order.get('status'))}"
                )

    new_page = pagination_component(
        total_items=total,
        page_size=page_size,
        current_page=st.session_state.orders_page,
        key="orders",
    )
    if new_page != st.session_state.orders_page:
        st.session_state.orders_page = new_page
        st.rerun()

    st.caption(
        "ℹ️ Update trạng thái/chi tiết đơn hàng hiện vẫn nằm ở `quan_tri.py` (có thể port tiếp)."
    )


def page_contacts():
    st.title("📬 Quản lý liên hệ")

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        status = st.radio(
            "Trạng thái",
            options=["Tất cả", "pending", "contacted", "completed"],
            horizontal=True,
            format_func=lambda x: {
                "Tất cả": "Tất cả",
                "pending": "⏳ Chờ xử lý",
                "contacted": "📞 Đã liên hệ",
                "completed": "✅ Hoàn tất",
            }.get(x, x),
        )
    with col2:
        page_size = st.selectbox("Hiển thị", [10, 20, 50, 100], index=1, key="c_ps")
    with col3:
        if st.button("🔄", key="c_refresh"):
            fetch_contacts.clear()
            st.session_state.contacts_page = 1
            st.rerun()

    st.divider()
    filter_status = None if status == "Tất cả" else status
    contacts = fetch_contacts(filter_status)
    if not contacts:
        st.info("Không có liên hệ.")
        return

    total_items = len(contacts)
    new_page = pagination_component(
        total_items=total_items,
        page_size=page_size,
        current_page=st.session_state.contacts_page,
        key="contacts",
    )
    if new_page != st.session_state.contacts_page:
        st.session_state.contacts_page = new_page
        st.rerun()

    start = (st.session_state.contacts_page - 1) * page_size
    end = start + page_size
    page_contacts = contacts[start:end]

    for c in page_contacts:
        icon = {"pending": "🟡", "contacted": "🔵", "completed": "🟢"}.get(
            c.get("status"), "⚪"
        )
        with st.expander(f"{icon} {c.get('name', 'N/A')} - {c.get('phone', 'N/A')}"):
            st.write(f"**Email:** {c.get('email', 'N/A')}")
            st.write(f"**Địa chỉ:** {c.get('address', 'N/A')}")
            st.write(f"**Tin nhắn:** {c.get('message', '')}")
            st.write(f"**Ngày gửi:** {format_datetime(c.get('created_at', ''))}")

    st.caption(
        "ℹ️ Cập nhật trạng thái/xóa liên hệ chi tiết hiện vẫn nằm ở `quan_tri.py` (có thể port tiếp)."
    )


def page_reviews():
    st.title("⭐ Duyệt đánh giá")

    reviews = fetch_pending_reviews()

    if not reviews:
        st.success("✅ Không có đánh giá nào chờ duyệt!")
        return

    st.warning(f"📋 Có **{len(reviews)}** đánh giá chờ duyệt")
    st.divider()

    page_size = st.selectbox("Hiển thị", [10, 20, 50], index=1, key="r_ps")
    if "reviews_page" not in st.session_state:
        st.session_state.reviews_page = 1

    total = len(reviews)
    new_page = pagination_component(
        total_items=total,
        page_size=page_size,
        current_page=st.session_state.reviews_page,
        key="reviews",
    )
    if new_page != st.session_state.reviews_page:
        st.session_state.reviews_page = new_page
        st.rerun()

    start = (st.session_state.reviews_page - 1) * page_size
    end = start + page_size
    for review in reviews[start:end]:
        with st.container(border=True):
            stars = "⭐" * int(review.get("rating", 0) or 0)
            st.write(f"**{review.get('user_name', 'Ẩn danh')}** - {stars}")
            st.caption(review.get("comment", "") or "Không có nhận xét")
            if review.get("image_url"):
                lazy_image(review["image_url"], width=120)

    st.caption(
        "ℹ️ Duyệt/Xóa đánh giá (mutation) hiện nằm ở `quan_tri.py` (có thể port tiếp)."
    )


def page_banners():
    """
    Ported from `quan_tri.py`:
    - List banners (admin endpoint)
    - Create banner with image upload
    - Delete banner
    Performance:
    - Uses cached fetch_banners()
    - Uses upload_image() with compression
    - Uses invalidate_after_mutation(['banners', 'dashboard']) after mutations
    """
    st.title("🖼️ Quản lý Banner")

    tab_list, tab_create = st.tabs(["📋 DANH SÁCH", "➕ THÊM MỚI"])

    with tab_create:
        with st.form("banner_create_form", clear_on_submit=True):
            title = st.text_input("Tiêu đề", key="bn_title")
            subtitle = st.text_input("Mô tả phụ", key="bn_subtitle")
            img = st.file_uploader(
                "Ảnh Banner", type=["jpg", "png", "jpeg", "webp"], key="bn_file"
            )
            is_active = st.checkbox("Kích hoạt", value=True, key="bn_active")
            order = st.number_input(
                "Thứ tự (order)",
                min_value=0,
                max_value=9999,
                value=0,
                step=1,
                key="bn_order",
            )

            submitted = st.form_submit_button("THÊM BANNER")
            if submitted:
                if img is None:
                    st.error("Vui lòng chọn ảnh banner.")
                else:
                    with st.spinner("Đang upload ảnh..."):
                        image_url = upload_image(img)

                    if not image_url:
                        st.error("Upload ảnh thất bại. Vui lòng thử lại.")
                    else:
                        payload = {
                            "title": title,
                            "subtitle": subtitle,
                            "image_url": image_url,
                            "is_active": bool(is_active),
                            "order": int(order),
                        }
                        with st.spinner("Đang tạo banner..."):
                            _, err = api_request(
                                "/api/banner/", method="POST", data=payload
                            )
                        if err:
                            st.error(f"Tạo banner thất bại: {err}")
                        else:
                            show_toast("Đã thêm banner", "success")
                            invalidate_after_mutation(["banners", "dashboard"])
                            st.rerun()

    with tab_list:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🔄 Làm mới", key="bn_refresh"):
                fetch_banners.clear()
                st.rerun()

        banners = fetch_banners()

        if not banners:
            st.info("📭 Chưa có banner nào.")
            return

        # Keep UI light: paginate
        page_size = st.selectbox("Hiển thị", [5, 10, 20, 50], index=1, key="bn_ps")
        if "banners_page" not in st.session_state:
            st.session_state.banners_page = 1

        total = len(banners)
        new_page = pagination_component(
            total_items=total,
            page_size=page_size,
            current_page=st.session_state.banners_page,
            key="banners",
        )
        if new_page != st.session_state.banners_page:
            st.session_state.banners_page = new_page
            st.rerun()

        start = (st.session_state.banners_page - 1) * page_size
        end = start + page_size

        for b in banners[start:end]:
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 3, 1])

                with c1:
                    img_url = b.get("image_url") or ""
                    st.image(build_asset_url(img_url), use_container_width=True)

                with c2:
                    st.write(f"**{b.get('title', '') or '—'}**")
                    st.caption(b.get("subtitle", "") or "")
                    st.caption(
                        f"order={b.get('order', 0)} | active={b.get('is_active', True)}"
                    )

                with c3:
                    if st.button("🗑️ XÓA", key=f"bn_del_{b.get('id')}"):
                        banner_id = b.get("id")
                        if not banner_id:
                            st.error("Không tìm thấy ID banner.")
                        else:
                            _, err = api_request(
                                f"/api/banner/{banner_id}", method="DELETE"
                            )
                            if err:
                                st.error(f"Xóa thất bại: {err}")
                            else:
                                show_toast("Đã xóa banner", "success")
                                invalidate_after_mutation(["banners", "dashboard"])
                                st.rerun()


# =============================================================================
# MENU ROUTING (RESTORE FULL)
# =============================================================================


def normalize_choice_to_page(choice: str) -> str:
    """
    Map label (menu) -> internal page key.
    MENU labels come from `auth.get_allowed_menu_items()`; in existing code they contain emojis & Vietnamese.
    """
    c = (choice or "").lower()
    if "tổng quan" in c or "dashboard" in c:
        return "dashboard"
    if "đơn hàng" in c:
        return "orders"
    if "liên hệ" in c:
        return "contacts"
    if "tư vấn" in c or "chat" in c:
        return "consultations"
    if "duyệt" in c and "đánh giá" in c:
        return "reviews"
    if "banner" in c:
        return "banners"
    if "sản phẩm" in c:
        return "products"
    if "combo" in c:
        return "combo"
    if "khách hàng" in c:
        return "customers"
    if "lịch trống" in c or "calendar" in c:
        return "calendar"
    if "yêu thích" in c:
        return "favorites"
    if "đối tác" in c:
        return "partners"
    if "thư viện" in c:
        return "gallery"
    if "dịch vụ" in c:
        return "services"
    if "blog" in c:
        return "blog"
    if "nội dung" in c:
        return "homepage_content"
    return "dashboard"


def render_placeholder_feature(title: str, note: str):
    st.title(title)
    st.info(
        "Mục này đã có đầy đủ trong `quan_tri.py`. "
        "Phiên bản optimized đang được khôi phục dần với caching/pagination/invalidate chuẩn."
    )
    st.caption(note)
    st.caption(
        "✅ Nếu bạn cần mình port ngay mục này, mình sẽ port tiếp theo thứ tự bạn ưu tiên."
    )


# =============================================================================
# ENTRYPOINT
# =============================================================================


def main():
    # Init auth session (same as quan_tri.py)
    init_session()

    if not is_authenticated():
        show_login_page()
        st.stop()

    # Notice about Render sleep (once)
    if "shown_wake_notice" not in st.session_state:
        st.session_state.shown_wake_notice = True
        st.info(
            "💡 Lưu ý: Render free tier có thể sleep, lần đầu vào lại có thể mất 30-60s."
        )

    # Sidebar user info + menu
    show_user_info_sidebar()
    allowed_menu_items = get_allowed_menu_items()

    choice = st.selectbox("MENU QUẢN TRỊ", allowed_menu_items)
    page_key = normalize_choice_to_page(choice)

    # Route
    if page_key == "dashboard":
        page_dashboard()

    elif page_key == "products":
        # Respect permission like quan_tri.py
        if not has_permission("products"):
            st.error(
                "⛔ Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."
            )
            return
        page_products()

    elif page_key == "orders":
        page_orders()

    elif page_key == "contacts":
        page_contacts()

    elif page_key == "reviews":
        if not has_permission("reviews"):
            st.error(
                "⛔ Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."
            )
            return
        page_reviews()

    # The following pages are restored in routing, but still use placeholder until fully ported.
    elif page_key == "consultations":
        render_placeholder_feature(
            "💬 Tư vấn khách hàng", "Cần port chat endpoints + UI from `quan_tri.py`."
        )

    elif page_key == "banners":
        page_banners()

    elif page_key == "combo":
        render_placeholder_feature(
            "🎁 Quản lý Combo", "Cần port combo CRUD from `quan_tri.py`."
        )

    elif page_key == "customers":
        render_placeholder_feature(
            "👥 Quản lý Khách hàng",
            "Cần port customers list/filters from `quan_tri.py`.",
        )

    elif page_key == "calendar":
        render_placeholder_feature(
            "📅 Quản lý Lịch trống", "Cần port calendar CRUD from `quan_tri.py`."
        )

    elif page_key == "favorites":
        render_placeholder_feature(
            "❤️ Thống kê Yêu thích", "Cần port favorites stats from `quan_tri.py`."
        )

    elif page_key == "partners":
        render_placeholder_feature(
            "🤝 Đối tác & Khiếu nại",
            "Cần port partner/complaint admin from `quan_tri.py`.",
        )

    elif page_key == "gallery":
        render_placeholder_feature(
            "🖼️ Thư viện", "Cần port gallery upload/list from `quan_tri.py`."
        )

    elif page_key == "services":
        render_placeholder_feature(
            "🧑‍💼 Dịch vụ & Chuyên gia",
            "Cần port experts/services CRUD from `quan_tri.py`.",
        )

    elif page_key == "blog":
        render_placeholder_feature(
            "📰 Blog & Tin tức",
            "Cần port blog CRUD (quill optional) from `quan_tri.py`.",
        )

    elif page_key == "homepage_content":
        render_placeholder_feature(
            "🏠 Nội dung Trang chủ",
            "Cần port content management tabs from `quan_tri.py`.",
        )

    else:
        page_dashboard()


if __name__ == "__main__":
    main()
