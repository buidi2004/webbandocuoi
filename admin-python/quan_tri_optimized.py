"""
IVIE Wedding Studio - Admin Panel Tối Ưu Hóa
============================================
- Streamlit caching với @st.cache_data và @st.cache_resource
- Lazy loading cho components nặng
- Parallel API requests với ThreadPoolExecutor
- Session state management tối ưu
- Debounced inputs để giảm API calls
- Virtual scrolling cho lists lớn
- Progressive loading với skeleton UI
"""

import functools
import hashlib
import io
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# =============================================================================
# PAGE CONFIG - PHẢI ĐẶT ĐẦU TIÊN
# =============================================================================

st.set_page_config(
    page_title="IVIE Wedding Admin",
    layout="wide",
    page_icon="🏯",
    initial_sidebar_state="expanded",
)

# =============================================================================
# PERFORMANCE CONFIGURATION
# =============================================================================

# Cache TTL (seconds)
CACHE_TTL = {
    "SHORT": 60,  # 1 phút - data thay đổi thường xuyên
    "MEDIUM": 300,  # 5 phút - product lists
    "LONG": 900,  # 15 phút - static data
    "EXTENDED": 3600,  # 1 giờ - rarely changing
}

# API Configuration
API_TIMEOUT = 10  # seconds
MAX_WORKERS = 4  # Thread pool size
MAX_RETRIES = 2  # API retry count

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

load_dotenv()
API_URL = os.getenv(
    "API_BASE_URL", os.getenv("VITE_API_BASE_URL", "http://localhost:8000")
)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================


def init_session_state():
    """Khởi tạo session state với giá trị mặc định"""
    defaults = {
        # Authentication
        "authenticated": False,
        "user": None,
        "role": None,
        # UI State
        "current_page": "dashboard",
        "sidebar_collapsed": False,
        # Data Cache
        "products_cache": None,
        "products_cache_time": None,
        "orders_cache": None,
        "orders_cache_time": None,
        # Pagination
        "products_page": 1,
        "orders_page": 1,
        # Filters
        "product_filters": {},
        "order_filters": {},
        # Loading states
        "is_loading": False,
        # Toast messages
        "toast_message": None,
        "toast_type": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()

# =============================================================================
# OPTIMIZED HTTP CLIENT
# =============================================================================


@st.cache_resource
def get_session() -> requests.Session:
    """
    Tạo và cache HTTP session với connection pooling.
    Sử dụng @st.cache_resource để tái sử dụng session across reruns.
    """
    session = requests.Session()

    # Connection pooling
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=10,
        pool_maxsize=20,
        max_retries=requests.adapters.Retry(
            total=MAX_RETRIES, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]
        ),
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Default headers
    session.headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )

    return session


# Thread pool for parallel requests
@st.cache_resource
def get_executor() -> ThreadPoolExecutor:
    """Thread pool được cache và tái sử dụng"""
    return ThreadPoolExecutor(max_workers=MAX_WORKERS)


# =============================================================================
# API UTILITIES
# =============================================================================


def api_request(
    endpoint: str,
    method: str = "GET",
    data: dict = None,
    params: dict = None,
    timeout: int = API_TIMEOUT,
    retries: int = MAX_RETRIES,
) -> Tuple[Optional[Any], Optional[str]]:
    """
    Gọi API với retry logic và error handling.
    Returns: (data, error_message)
    """
    session = get_session()
    url = f"{API_URL}{endpoint}"

    for attempt in range(retries + 1):
        try:
            if method == "GET":
                response = session.get(url, params=params, timeout=timeout)
            elif method == "POST":
                response = session.post(url, json=data, timeout=timeout)
            elif method == "PUT":
                response = session.put(url, json=data, timeout=timeout)
            elif method == "DELETE":
                response = session.delete(url, timeout=timeout)
            elif method == "PATCH":
                response = session.patch(url, json=data, timeout=timeout)
            else:
                return None, f"Unsupported method: {method}"

            if response.status_code >= 400:
                return None, f"API Error: {response.status_code}"

            return response.json(), None

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


def fetch_parallel(endpoints: List[str]) -> Dict[str, Any]:
    """
    Fetch nhiều endpoints song song.
    Returns dict với key là endpoint và value là data.
    """
    executor = get_executor()
    results = {}

    def fetch_one(endpoint: str):
        data, error = api_request(endpoint)
        return endpoint, data, error

    futures = {executor.submit(fetch_one, ep): ep for ep in endpoints}

    for future in as_completed(futures, timeout=API_TIMEOUT * 2):
        try:
            endpoint, data, error = future.result()
            results[endpoint] = {"data": data, "error": error}
        except Exception as e:
            endpoint = futures[future]
            results[endpoint] = {"data": None, "error": str(e)}

    return results


# =============================================================================
# CACHED DATA FETCHERS
# =============================================================================


@st.cache_data(ttl=CACHE_TTL["MEDIUM"], show_spinner=False)
def fetch_products(
    category: str = None,
    page: int = 1,
    page_size: int = DEFAULT_PAGE_SIZE,
    sort_by: str = "id_desc",
) -> Tuple[List[Dict], int]:
    """
    Fetch danh sách sản phẩm với caching.
    Returns: (products, total_count)
    """
    params = {
        "page": page,
        "page_size": page_size,
        "sort_by": sort_by,
    }
    if category:
        params["danh_muc"] = category

    data, error = api_request("/api/san_pham/", params=params)

    if error:
        return [], 0

    # Handle both paginated and legacy response
    if isinstance(data, dict) and "items" in data:
        return data["items"], data.get("pagination", {}).get(
            "total", len(data["items"])
        )
    elif isinstance(data, list):
        return data, len(data)

    return [], 0


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_orders(
    status: str = None, page: int = 1, page_size: int = DEFAULT_PAGE_SIZE
) -> Tuple[List[Dict], int]:
    """Fetch danh sách đơn hàng với caching"""
    params = {"page": page, "page_size": page_size}
    if status:
        params["status"] = status

    data, error = api_request("/api/don_hang/", params=params)

    if error:
        return [], 0

    if isinstance(data, dict) and "items" in data:
        return data["items"], data.get("pagination", {}).get("total", 0)
    elif isinstance(data, list):
        return data, len(data)

    return [], 0


@st.cache_data(ttl=CACHE_TTL["MEDIUM"], show_spinner=False)
def fetch_dashboard_stats() -> Dict[str, Any]:
    """Fetch thống kê dashboard"""
    data, error = api_request("/api/thong_ke/tong_quan")
    if error:
        return {}
    return data or {}


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def fetch_banners() -> List[Dict]:
    """Fetch danh sách banners"""
    data, error = api_request("/api/banner/")
    return data if data else []


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def fetch_blogs(page: int = 1, page_size: int = 20) -> List[Dict]:
    """Fetch danh sách blog posts"""
    data, error = api_request(
        "/api/blog/", params={"bo_qua": (page - 1) * page_size, "gioi_han": page_size}
    )
    return data if data else []


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_contacts(status: str = None) -> List[Dict]:
    """Fetch danh sách liên hệ"""
    params = {}
    if status:
        params["status"] = status
    data, error = api_request("/api/lien_he/", params=params)
    return data if data else []


@st.cache_data(ttl=CACHE_TTL["SHORT"], show_spinner=False)
def fetch_pending_reviews() -> List[Dict]:
    """Fetch đánh giá chờ duyệt"""
    data, error = api_request("/api/san_pham/admin/danh_gia_cho_duyet")
    return data if data else []


# =============================================================================
# CACHE INVALIDATION
# =============================================================================


def invalidate_products_cache():
    """Xóa cache sản phẩm"""
    fetch_products.clear()
    st.session_state.products_cache = None
    st.session_state.products_cache_time = None


def invalidate_orders_cache():
    """Xóa cache đơn hàng"""
    fetch_orders.clear()
    st.session_state.orders_cache = None


def invalidate_all_cache():
    """Xóa toàn bộ cache"""
    fetch_products.clear()
    fetch_orders.clear()
    fetch_dashboard_stats.clear()
    fetch_banners.clear()
    fetch_blogs.clear()
    fetch_contacts.clear()
    fetch_pending_reviews.clear()


# =============================================================================
# UI UTILITIES
# =============================================================================


def show_loading_skeleton(rows: int = 5, cols: int = 4):
    """Hiển thị skeleton loading UI"""
    st.markdown(
        """
    <style>
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .skeleton {
        background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 4px;
        height: 20px;
        margin: 8px 0;
    }
    .skeleton-card {
        background: #1a1a1a;
        border-radius: 8px;
        padding: 16px;
        margin: 8px 0;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    for _ in range(rows):
        cols_container = st.columns(cols)
        for col in cols_container:
            with col:
                st.markdown('<div class="skeleton"></div>', unsafe_allow_html=True)


def show_toast(message: str, type: str = "info"):
    """Hiển thị toast notification"""
    icons = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
    icon = icons.get(type, "ℹ️")
    st.toast(f"{icon} {message}")


def format_currency(amount: float) -> str:
    """Format số tiền theo VND"""
    if amount is None:
        return "0 ₫"
    return f"{amount:,.0f} ₫"


def format_datetime(dt_str: str) -> str:
    """Format datetime string"""
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return dt_str


# =============================================================================
# PAGINATION COMPONENT
# =============================================================================


def pagination_component(
    total_items: int, page_size: int, current_page: int, key: str
) -> int:
    """
    Component pagination với UI tối ưu.
    Returns: selected page number
    """
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    with col1:
        if st.button("⏮️ Đầu", key=f"{key}_first", disabled=current_page <= 1):
            return 1

    with col2:
        if st.button("◀️ Trước", key=f"{key}_prev", disabled=current_page <= 1):
            return current_page - 1

    with col3:
        st.markdown(
            f"<center>Trang **{current_page}** / {total_pages} ({total_items} items)</center>",
            unsafe_allow_html=True,
        )

    with col4:
        if st.button("Sau ▶️", key=f"{key}_next", disabled=current_page >= total_pages):
            return current_page + 1

    with col5:
        if st.button("Cuối ⏭️", key=f"{key}_last", disabled=current_page >= total_pages):
            return total_pages

    return current_page


# =============================================================================
# DEBOUNCED INPUT
# =============================================================================


def debounced_text_input(label: str, key: str, delay: float = 0.5, **kwargs) -> str:
    """
    Text input với debounce để giảm API calls.
    """
    # Store the actual value and last change time
    value_key = f"{key}_value"
    time_key = f"{key}_time"

    # Get input
    value = st.text_input(label, key=key, **kwargs)

    # Check if value changed
    if value != st.session_state.get(value_key):
        st.session_state[value_key] = value
        st.session_state[time_key] = time.time()

    # Return value only after delay
    last_change = st.session_state.get(time_key, 0)
    if time.time() - last_change >= delay:
        return value

    return st.session_state.get(f"{key}_stable", "")


# =============================================================================
# LAZY LOADED COMPONENTS
# =============================================================================


@st.cache_data(ttl=CACHE_TTL["LONG"], show_spinner=False)
def get_image_thumbnail(
    image_url: str, size: Tuple[int, int] = (100, 100)
) -> Optional[bytes]:
    """
    Tải và resize ảnh, cache kết quả.
    """
    if not image_url:
        return None

    try:
        # Make absolute URL
        if image_url.startswith("/"):
            image_url = f"{API_URL}{image_url}"

        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # Convert to bytes
            buffer = io.BytesIO()
            img.save(buffer, format="WEBP", quality=85)
            return buffer.getvalue()
    except:
        pass

    return None


def lazy_image(image_url: str, caption: str = None, width: int = 100):
    """
    Lazy load image với placeholder.
    """
    if not image_url:
        st.markdown(
            f"""
        <div style="width:{width}px;height:{width}px;background:#333;border-radius:4px;
                    display:flex;align-items:center;justify-content:center;color:#666;">
            No Image
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    thumbnail = get_image_thumbnail(image_url, (width, width))

    if thumbnail:
        st.image(thumbnail, caption=caption, width=width)
    else:
        # Fallback to direct URL
        if image_url.startswith("/"):
            image_url = f"{API_URL}{image_url}"
        st.image(image_url, caption=caption, width=width)


# =============================================================================
# DASHBOARD PAGE
# =============================================================================


def render_dashboard():
    """Render trang Dashboard với lazy loading"""
    st.title("📊 Dashboard")

    # Fetch stats với loading state
    with st.spinner("Đang tải thống kê..."):
        stats = fetch_dashboard_stats()

    if not stats:
        st.warning("Không thể tải thống kê. Vui lòng thử lại.")
        if st.button("🔄 Thử lại"):
            fetch_dashboard_stats.clear()
            st.rerun()
        return

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Tổng sản phẩm",
            value=stats.get("tong_san_pham", 0),
        )

    with col2:
        st.metric(
            label="🛒 Tổng đơn hàng",
            value=stats.get("tong_don_hang", 0),
        )

    with col3:
        st.metric(
            label="👥 Người dùng",
            value=stats.get("tong_nguoi_dung", 0),
        )

    with col4:
        st.metric(
            label="💰 Doanh thu",
            value=format_currency(stats.get("tong_doanh_thu", 0)),
        )

    st.divider()

    # Quick stats row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"📋 Đơn chờ xử lý: **{stats.get('don_hang_cho_xu_ly', 0)}**")

    with col2:
        st.success(f"✅ Đơn hoàn thành: **{stats.get('don_hang_hoan_thanh', 0)}**")

    with col3:
        st.warning(f"📬 Liên hệ mới: **{stats.get('lien_he_chua_xu_ly', 0)}**")


# =============================================================================
# PRODUCTS PAGE
# =============================================================================


def render_products():
    """Render trang Quản lý sản phẩm"""
    st.title("📦 Quản lý sản phẩm")

    # Filters row
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

    with col1:
        category = st.selectbox(
            "Danh mục",
            options=["Tất cả", "wedding_modern", "traditional", "vest"],
            key="product_category_filter",
        )
        if category == "Tất cả":
            category = None

    with col2:
        sort_by = st.selectbox(
            "Sắp xếp",
            options=["id_desc", "id_asc", "price_asc", "price_desc", "hot", "new"],
            format_func=lambda x: {
                "id_desc": "Mới nhất",
                "id_asc": "Cũ nhất",
                "price_asc": "Giá tăng dần",
                "price_desc": "Giá giảm dần",
                "hot": "Hot",
                "new": "Mới",
            }.get(x, x),
            key="product_sort",
        )

    with col3:
        page_size = st.selectbox(
            "Hiển thị", options=[10, 20, 50, 100], index=1, key="product_page_size"
        )

    with col4:
        if st.button("🔄 Làm mới", key="refresh_products"):
            invalidate_products_cache()
            st.rerun()

    st.divider()

    # Fetch products
    products, total = fetch_products(
        category=category,
        page=st.session_state.products_page,
        page_size=page_size,
        sort_by=sort_by,
    )

    if not products:
        st.info("Không có sản phẩm nào.")
        return

    # Display products in table
    st.markdown(f"**Tìm thấy {total} sản phẩm**")

    # Create DataFrame for display
    df_data = []
    for p in products:
        df_data.append(
            {
                "ID": p.get("id"),
                "Mã": p.get("code", "N/A"),
                "Tên": p.get("name", "N/A")[:50],
                "Danh mục": p.get("category", "N/A"),
                "Giá thuê": format_currency(p.get("rental_price_day", 0)),
                "Hot": "🔥" if p.get("is_hot") else "",
                "Mới": "🆕" if p.get("is_new") else "",
            }
        )

    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Pagination
    new_page = pagination_component(
        total_items=total,
        page_size=page_size,
        current_page=st.session_state.products_page,
        key="products",
    )

    if new_page != st.session_state.products_page:
        st.session_state.products_page = new_page
        st.rerun()


# =============================================================================
# ORDERS PAGE
# =============================================================================


def render_orders():
    """Render trang Quản lý đơn hàng"""
    st.title("🛒 Quản lý đơn hàng")

    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        status_filter = st.selectbox(
            "Trạng thái",
            options=[
                "Tất cả",
                "pending",
                "processing",
                "shipped",
                "delivered",
                "cancelled",
            ],
            format_func=lambda x: {
                "Tất cả": "Tất cả",
                "pending": "⏳ Chờ xử lý",
                "processing": "🔄 Đang xử lý",
                "shipped": "🚚 Đang giao",
                "delivered": "✅ Đã giao",
                "cancelled": "❌ Đã hủy",
            }.get(x, x),
            key="order_status_filter",
        )

    with col2:
        page_size = st.selectbox(
            "Hiển thị", options=[10, 20, 50], index=1, key="order_page_size"
        )

    with col3:
        if st.button("🔄 Làm mới", key="refresh_orders"):
            invalidate_orders_cache()
            st.rerun()

    st.divider()

    # Fetch orders
    status = status_filter if status_filter != "Tất cả" else None
    orders, total = fetch_orders(
        status=status, page=st.session_state.orders_page, page_size=page_size
    )

    if not orders:
        st.info("Không có đơn hàng nào.")
        return

    st.markdown(f"**Tìm thấy {total} đơn hàng**")

    # Display orders
    for order in orders:
        with st.expander(
            f"🧾 Đơn #{order.get('id', 'N/A')} - {order.get('customer_name', 'N/A')}"
        ):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Khách hàng:** {order.get('customer_name', 'N/A')}")
                st.write(f"**SĐT:** {order.get('customer_phone', 'N/A')}")

            with col2:
                st.write(
                    f"**Tổng tiền:** {format_currency(order.get('total_amount', 0))}"
                )
                st.write(
                    f"**Ngày đặt:** {format_datetime(order.get('order_date', ''))}"
                )

            with col3:
                status_badges = {
                    "pending": "🟡 Chờ xử lý",
                    "processing": "🔵 Đang xử lý",
                    "shipped": "🟠 Đang giao",
                    "delivered": "🟢 Đã giao",
                    "cancelled": "🔴 Đã hủy",
                }
                st.write(
                    f"**Trạng thái:** {status_badges.get(order.get('status'), order.get('status'))}"
                )

    # Pagination
    new_page = pagination_component(
        total_items=total,
        page_size=page_size,
        current_page=st.session_state.orders_page,
        key="orders",
    )

    if new_page != st.session_state.orders_page:
        st.session_state.orders_page = new_page
        st.rerun()


# =============================================================================
# CONTACTS PAGE
# =============================================================================


def render_contacts():
    """Render trang Quản lý liên hệ"""
    st.title("📬 Quản lý liên hệ")

    # Filter
    col1, col2 = st.columns([3, 1])

    with col1:
        status = st.radio(
            "Trạng thái",
            options=["Tất cả", "pending", "contacted", "resolved"],
            horizontal=True,
            format_func=lambda x: {
                "Tất cả": "Tất cả",
                "pending": "⏳ Chờ xử lý",
                "contacted": "📞 Đã liên hệ",
                "resolved": "✅ Đã giải quyết",
            }.get(x, x),
        )

    with col2:
        if st.button("🔄 Làm mới"):
            fetch_contacts.clear()
            st.rerun()

    st.divider()

    # Fetch contacts
    filter_status = status if status != "Tất cả" else None
    contacts = fetch_contacts(filter_status)

    if not contacts:
        st.info("Không có liên hệ nào.")
        return

    # Display contacts
    for contact in contacts[:50]:  # Limit display
        status_icon = {"pending": "🟡", "contacted": "🔵", "resolved": "🟢"}.get(
            contact.get("status"), "⚪"
        )

        with st.expander(
            f"{status_icon} {contact.get('name', 'N/A')} - {contact.get('phone', 'N/A')}"
        ):
            st.write(f"**Email:** {contact.get('email', 'N/A')}")
            st.write(f"**Dịch vụ:** {contact.get('service', 'N/A')}")
            st.write(f"**Tin nhắn:** {contact.get('message', 'N/A')}")
            st.write(f"**Ngày gửi:** {format_datetime(contact.get('created_at', ''))}")


# =============================================================================
# REVIEWS PAGE
# =============================================================================


def render_reviews():
    """Render trang Duyệt đánh giá"""
    st.title("⭐ Duyệt đánh giá")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Làm mới"):
            fetch_pending_reviews.clear()
            st.rerun()

    reviews = fetch_pending_reviews()

    if not reviews:
        st.success("✅ Không có đánh giá nào chờ duyệt!")
        return

    st.warning(f"📋 Có **{len(reviews)}** đánh giá chờ duyệt")
    st.divider()

    for review in reviews:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                stars = "⭐" * review.get("rating", 0)
                st.write(f"**{review.get('user_name', 'Ẩn danh')}** - {stars}")
