import functools
import io
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# CRITICAL: Set page config FIRST before any other st commands
st.set_page_config(page_title="IVIE Wedding Admin", layout="wide", page_icon="🏯")

# Show loading indicator immediately for FCP
loading_placeholder = st.empty()
loading_placeholder.markdown(
    """
<div style='text-align: center; padding: 100px 0;'>
    <h1 style='font-size: 3em; margin-bottom: 20px;'>🏯 IVIE WEDDING STUDIO</h1>
    <p style='color: #999; font-size: 1.2em;'>Đang tải hệ thống quản trị...</p>
    <div style='margin-top: 30px;'>
        <div style='display: inline-block; width: 40px; height: 40px; border: 3px solid #333; border-top-color: #fff; border-radius: 50%; animation: spin 1s linear infinite;'></div>
    </div>
    <style>
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</div>
""",
    unsafe_allow_html=True,
)

# Import authentication module
try:
    from auth import (
        MENU_PERMISSIONS,
        get_allowed_menu_items,
        has_permission,
        init_session,
        is_authenticated,
        show_login_page,
        show_user_info_sidebar,
    )
except ImportError as e:
    loading_placeholder.empty()
    st.error(f"❌ Lỗi import auth module: {e}")
    st.stop()

# Import analytics module
try:
    from analytics import (
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
except ImportError:
    HAS_ANALYTICS = False

load_dotenv()

API_URL = os.getenv(
    "API_BASE_URL", os.getenv("VITE_API_BASE_URL", "http://localhost:8000")
)

# Thread pool cho parallel requests
executor = ThreadPoolExecutor(max_workers=4)

# Clear loading placeholder
loading_placeholder.empty()

# Khởi tạo session
init_session()

# Kiểm tra authentication
if not is_authenticated():
    show_login_page()
    st.stop()  # Dừng execution nếu chưa đăng nhập

# Thông báo nếu backend có thể đang sleep
if "shown_wake_notice" not in st.session_state:
    st.session_state.shown_wake_notice = True
    st.info(
        "💡 Lưu ý: Nếu đây là lần đầu truy cập sau một thời gian, server có thể mất 30-60 giây để khởi động (Render free tier)."
    )

# CSS custom for minimalist B&W Dark Theme
st.markdown(
    """
    <style>
    /* Dark Theme Logic is handled by top-level config usually, but we enforce some styles */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .main {
        background-color: #000000;
    }

    /* Buttons: White border, black bg, white text for minimalist look */
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: #ffffff;
        border: 1px solid #333;
        border-radius: 4px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        border-color: #ffffff;
        color: #ffffff;
    }

    /* Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #111;
        color: white;
        border: 1px solid #333;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 300;
    }

    /* Remove default streamlit branding if possible (limited via CSS) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Status indicators - Monochrome */
    .status-badge {
        font-size: 0.8em;
        padding: 2px 6px;
        border: 1px solid #333;
        border-radius: 4px;
        background: #111;
    }

    /* Product row */
    .product-row {
        border-bottom: 1px solid #222;
        padding: 10px 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("IVIE STUDIO ADMIN")

with st.sidebar:
    # Hiển thị thông tin user
    show_user_info_sidebar()

    # Lấy menu items theo quyền của user
    allowed_menu_items = get_allowed_menu_items()

    choice = st.selectbox("MENU QUẢN TRỊ", allowed_menu_items)


# --- Helpers ---
# Session cho requests - tái sử dụng connection với connection pooling
@st.cache_resource
def get_session():
    """Tạo session requests với connection pooling để tối ưu hiệu suất"""
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

    session.headers.update(
        {
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    return session


def wake_up_backend():
    """Đánh thức backend nếu đang sleep (Render free tier)"""
    try:
        session = get_session()
        res = session.get(f"{API_URL}/api/health", timeout=60)
        return res.status_code == 200
    except:
        return False


@st.cache_data(show_spinner=False, ttl=120)  # Cache 2 phút
def fetch_api_data(endpoint):
    """Cached version for GET requests with 2 min TTL"""
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


# Cached fetchers cho từng loại dữ liệu - TTL khác nhau
@st.cache_data(show_spinner=False, ttl=300)  # Cache 5 phút - ít thay đổi
def fetch_products_cached():
    """Cached products list"""
    return fetch_api_data("/api/san_pham/")


@st.cache_data(show_spinner=False, ttl=60)  # Cache 1 phút - thay đổi thường xuyên
def fetch_orders_cached():
    """Cached orders list"""
    return fetch_api_data("/api/don_hang/")


@st.cache_data(show_spinner=False, ttl=60)  # Cache 1 phút
def fetch_contacts_cached():
    """Cached contacts list"""
    return fetch_api_data("/api/lien_he/")


@st.cache_data(show_spinner=False, ttl=60)  # Giảm xuống 1 phút cho admin
def fetch_banners_cached():
    """Cached banners list"""
    data = fetch_api_data("/api/banner/tat_ca")
    if data is None:
        data = fetch_api_data("/api/banner/")
    return data


@st.cache_data(show_spinner=False, ttl=180)  # Cache 3 phút
def fetch_dashboard_stats():
    """Cached dashboard statistics"""
    return fetch_api_data("/api/thong_ke/tong_quan")


def invalidate_cache(scope=None):
    """Xóa cache theo phạm vi hoặc toàn bộ"""
    # CRITICAL: Luôn clear fetch_api_data vì nó là base của các function khác
    fetch_api_data.clear()
    
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


# Batch fetch - lấy nhiều endpoint cùng lúc
def fetch_multiple_endpoints(endpoints):
    """Fetch nhiều endpoints song song với timeout tối ưu"""

    def fetch_one(endpoint):
        return endpoint, fetch_api_data(endpoint)

    results = {}
    futures = [executor.submit(fetch_one, ep) for ep in endpoints]
    for future in futures:
        try:
            ep, data = future.result(timeout=25)
            results[ep] = data
        except:
            pass
    return results


# Parallel image upload
def upload_images_parallel(files_list):
    """Upload nhiều ảnh song song để tiết kiệm thời gian"""
    if not files_list:
        return []

    results = []
    futures = [executor.submit(upload_image, f) for f in files_list]
    for future in futures:
        try:
            url = future.result(timeout=40)
            if url:
                results.append(url)
        except:
            pass
    return results


# Session state để tránh rerun không cần thiết
if "last_action" not in st.session_state:
    st.session_state.last_action = None
if "backend_awake" not in st.session_state:
    st.session_state.backend_awake = False


def call_api(method, endpoint, data=None, files=None, clear_cache=True, retries=2):
    """Gọi API với retry logic cho Render free tier"""
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

            if res.status_code in [200, 201]:
                st.session_state.backend_awake = True
                if method != "GET" and clear_cache:
                    # Invalidate relevant caches based on endpoint
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
                    else:
                        st.cache_data.clear()
                return res.json()
            else:
                st.error(f"Lỗi API ({res.status_code})")
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
            st.error(f"Lỗi kết nối: {str(e)}")
            return None

    return None


def upload_image(uploaded_file):
    """Upload ảnh lên ImgBB với compression và error handling"""
    if uploaded_file is None:
        return None
        
    url = f"{API_URL}/api/tap_tin/upload"
    
    try:
        # Đọc file content
        file_bytes = uploaded_file.getvalue()
        
        # Chỉ compress nếu file > 1MB để tránh làm chậm xử lý trên CPU yếu
        file_size_mb = len(file_bytes) / (1024 * 1024)
        if file_size_mb > 1.0:
            try:
                img = Image.open(io.BytesIO(file_bytes))
                
                # Resize nếu rộng > 1600px (tối ưu cho banner)
                if img.width > 1600:
                    new_height = int(img.height * (1600 / img.width))
                    img = img.resize((1600, new_height), Image.Resampling.LANCZOS)
                
                # Convert to RGB if needed
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Save to buffer
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=80, optimize=True)
                file_bytes = buffer.getvalue()
                
                # Tạo filename mới .jpg
                filename = f"{uploaded_file.name.rsplit('.', 1)[0][:30]}.jpg"
                content_type = "image/jpeg"
                st.info(f"⚡ Đã nén ảnh: {file_size_mb:.1f}MB → {len(file_bytes)/(1024*1024):.1f}MB")
                
            except Exception as e:
                st.warning(f"Không thể nén ảnh, sử dụng ảnh gốc: {e}")
                filename = uploaded_file.name
                content_type = uploaded_file.type
        else:
            filename = uploaded_file.name
            content_type = uploaded_file.type
        
        # Tạo files dict đúng format cho requests
        files = {
            "file": (filename, file_bytes, content_type)
        }
        
        # Upload - KHÔNG dùng session vì nó có Content-Type: application/json
        # Dùng requests.post trực tiếp để tự động set multipart/form-data
        timeout = 60 if not st.session_state.get("backend_awake", False) else 30
        
        res = requests.post(url, files=files, timeout=timeout)
        
        if res.status_code == 200:
            st.session_state.backend_awake = True
            result = res.json()
            return result.get("url")
        else:
            # Hiển thị lỗi chi tiết
            try:
                error_detail = res.json().get("detail", res.text)
            except:
                error_detail = res.text
            st.error(f"❌ Lỗi tải ảnh ({res.status_code}): {error_detail}")
            return None
            
    except requests.Timeout:
        st.error("⏱️ Upload ảnh quá lâu. Server có thể đang khởi động, vui lòng thử lại.")
        return None
    except Exception as e:
        st.error(f"❌ Lỗi upload: {str(e)}")
        return None


# Upload nhiều ảnh song song
def upload_images_parallel(files_list):
    """Upload nhiều ảnh cùng lúc"""
    if not files_list:
        return []

    def upload_one(f):
        return upload_image(f)

    results = []
    futures = [executor.submit(upload_one, f) for f in files_list]
    for future in futures:
        try:
            url = future.result(timeout=35)
            if url:
                results.append(url)
        except:
            pass
    return results


@st.cache_data(show_spinner=False, ttl=900)  # Cache URL ảnh 15 phút
def lay_url_anh(path):
    """Cached image URL generation"""
    if not path:
        return "https://placehold.co/400x300/000000/ffffff?text=No+Image"
    if path.startswith("http"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{API_URL}{path}"


# Lazy load image - chỉ load khi cần
@st.cache_data(show_spinner=False, ttl=300)
def get_image_placeholder():
    return "https://placehold.co/200x200/111/333?text=Loading..."


def paginate_list(items, page_size=20):
    """Helper function for pagination - optimized"""
    if not items:
        return [], 1, 1

    # Sử dụng hash đơn giản hơn
    page_key = f"page_{id(items)}"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    total_pages = max(1, -(-len(items) // page_size))  # Ceiling division

    # Ensure current page is valid
    current = st.session_state[page_key]
    if current > total_pages:
        st.session_state[page_key] = total_pages
        current = total_pages

    start_idx = (current - 1) * page_size

    return items[start_idx : start_idx + page_size], current, total_pages


def show_pagination(current_page, total_pages, key_prefix=""):
    """Display pagination controls - compact version"""
    if total_pages <= 1:
        return

    # Sử dụng columns nhỏ gọn hơn
    c1, c2, c3, c4, c5 = st.columns([1, 1, 3, 1, 1])

    with c1:
        if st.button("⏮", disabled=current_page == 1, key=f"{key_prefix}first"):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = 1
            st.rerun()

    with c2:
        if st.button("◀", disabled=current_page == 1, key=f"{key_prefix}prev"):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = max(1, st.session_state[k] - 1)
            st.rerun()

    with c3:
        st.markdown(
            f"<p style='text-align:center;margin:8px 0;'>{current_page}/{total_pages}</p>",
            unsafe_allow_html=True,
        )

    with c4:
        if st.button(
            "▶", disabled=current_page == total_pages, key=f"{key_prefix}next"
        ):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = min(total_pages, st.session_state[k] + 1)
            st.rerun()

    with c5:
        if st.button(
            "⏭", disabled=current_page == total_pages, key=f"{key_prefix}last"
        ):
            for k in list(st.session_state.keys()):
                if k.startswith("page_"):
                    st.session_state[k] = total_pages
            st.rerun()


def cap_nhat_trang_thai_lien_he(id_lien_he, status):
    url = f"{API_URL}/api/lien_he/{id_lien_he}/status"
    try:
        session = get_session()
        res = session.patch(url, json={"status": status}, timeout=8)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Lỗi: {res.text}")
            return None
    except Exception as e:
        st.error(f"Lỗi kết nối")
        return None


# --- UI Sections ---
def ui_lien_he():
    st.header("Quản lý Liên hệ")
    contacts = call_api("GET", "/api/lien_he/", clear_cache=False)
    if not contacts:
        st.info("Chưa có liên hệ nào.")
        return

    search = st.text_input("Tìm kiếm", placeholder="Nhập tên, email...")
    status_filter = st.selectbox("Lọc trạng thái", ["Tất cả", "Chưa xử lý", "Đã xử lý"])

    filtered = contacts
    if search:
        filtered = [c for c in filtered if search.lower() in str(c).lower()]
    if status_filter == "Chưa xử lý":
        filtered = [c for c in filtered if c.get("status") == "pending"]
    elif status_filter == "Đã xử lý":
        filtered = [c for c in filtered if c.get("status") != "pending"]

    st.write(f"Hiển thị: {len(filtered)}")

    for c in filtered:
        with st.container(border=True):
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.write(f"**{c.get('name')}** | {c.get('phone')} | {c.get('email')}")
                st.write(f"📍 **Địa chỉ:** {c.get('address', 'Chưa cung cấp')}")
                st.caption(c.get("message"))
            with c2:
                curr_status = c.get("status", "pending")
                new_status = st.selectbox(
                    "",
                    ["pending", "contacted", "completed"],
                    index=["pending", "contacted", "completed"].index(curr_status)
                    if curr_status in ["pending", "contacted", "completed"]
                    else 0,
                    key=f"st_{c['id']}",
                    label_visibility="collapsed",
                )
                if new_status != curr_status:
                    if st.button("LƯU", key=f"save_{c['id']}"):
                        if cap_nhat_trang_thai_lien_he(c["id"], new_status):
                            st.toast("Đã cập nhật trạng thái!")
                            st.rerun()
            with c3:
                if st.button("XÓA", key=f"del_{c['id']}"):
                    if call_api("DELETE", f"/api/lien_he/{c['id']}"):
                        st.toast("Đã xóa liên hệ")
                        st.rerun()


def ui_banner():
    st.header("Quản lý Banner")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])

    with t2:
        with st.form("new_bn"):
            title = st.text_input("Tiêu đề")
            sub = st.text_input("Mô tả phụ")
            img = st.file_uploader("Ảnh Banner", type=["jpg", "png"])
            if st.form_submit_button("THÊM BANNER"):
                url = upload_image(img)
                if url:
                    if call_api(
                        "POST",
                        "/api/banner/",
                        data={
                            "title": title,
                            "subtitle": sub,
                            "image_url": url,
                            "is_active": True,
                            "order": 0,
                        },
                    ):
                        st.toast("Đã thêm banner")
                        st.rerun()

    with t1:
        banners = call_api("GET", "/api/banner/tat_ca", clear_cache=False)
        if banners is None:
            st.error("❌ Không thể kết nối đến server. Vui lòng thử lại sau.")
        elif len(banners) == 0:
            st.info("📭 Chưa có banner nào. Hãy thêm banner mới ở tab 'THÊM MỚI'.")
        else:
            for b in banners:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        st.image(lay_url_anh(b["image_url"]))
                    with c2:
                        st.write(f"**{b.get('title')}**")
                        st.caption(b.get("subtitle"))
                    with c3:
                        if st.button("XÓA", key=f"del_bn_{b['id']}"):
                            if call_api("DELETE", f"/api/banner/{b['id']}"):
                                st.toast("Đã xóa banner")
                                st.rerun()


# ============ QUẢN LÝ KHÁCH HÀNG ============
def ui_quan_ly_khach_hang():
    st.header("👥 Quản lý Khách hàng")

    # Lấy danh sách người dùng
    users = call_api("GET", "/pg/nguoi-dung", clear_cache=False)

    if users is None:
        st.error("❌ Không thể kết nối đến server")
        return

    if len(users) == 0:
        st.info("📭 Chưa có khách hàng nào đăng ký")
        return

    # Thống kê tổng quan
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Tổng khách hàng", len(users))
    with col2:
        verified = len([u for u in users if u.get("is_verified", False)])
        st.metric("✅ Đã xác thực", verified)
    with col3:
        has_orders = len([u for u in users if u.get("total_orders", 0) > 0])
        st.metric("🛒 Có đơn hàng", has_orders)
    with col4:
        recent = len(
            [
                u
                for u in users
                if u.get("created_at", "")[:7] == datetime.now().strftime("%Y-%m")
            ]
        )
        st.metric("🆕 Tháng này", recent)

    st.markdown("---")

    # Tìm kiếm và lọc
    col_search, col_filter = st.columns([3, 1])
    with col_search:
        search = st.text_input(
            "🔍 Tìm kiếm", placeholder="Tên, email, số điện thoại..."
        )
    with col_filter:
        filter_type = st.selectbox(
            "Lọc", ["Tất cả", "Đã xác thực", "Chưa xác thực", "Có đơn hàng"]
        )

    # Lọc dữ liệu
    filtered = users
    if search:
        search_lower = search.lower()
        filtered = [
            u
            for u in filtered
            if search_lower in str(u.get("full_name", "")).lower()
            or search_lower in str(u.get("email", "")).lower()
            or search_lower in str(u.get("phone", "")).lower()
        ]

    if filter_type == "Đã xác thực":
        filtered = [u for u in filtered if u.get("is_verified", False)]
    elif filter_type == "Chưa xác thực":
        filtered = [u for u in filtered if not u.get("is_verified", False)]
    elif filter_type == "Có đơn hàng":
        filtered = [u for u in filtered if u.get("total_orders", 0) > 0]

    st.write(f"Hiển thị: **{len(filtered)}** khách hàng")

    # Danh sách khách hàng
    for user in filtered:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                verified_icon = "✅" if user.get("is_verified", False) else "⏳"
                st.write(
                    f"**{user.get('full_name', 'Chưa cập nhật')}** {verified_icon}"
                )
                st.caption(f"📧 {user.get('email', 'N/A')}")
                st.caption(f"📱 {user.get('phone', 'Chưa cập nhật')}")

            with col2:
                st.write(f"📍 {user.get('address', 'Chưa cập nhật')[:30]}...")
                if user.get("wedding_date"):
                    st.write(f"💒 Ngày cưới: {user.get('wedding_date')}")

            with col3:
                st.write(f"🛒 Đơn hàng: **{user.get('total_orders', 0)}**")
                st.write(f"💰 Tổng chi: **{user.get('total_spent', 0):,.0f}đ**")
                st.caption(f"📅 Đăng ký: {user.get('created_at', '')[:10]}")

            with col4:
                if st.button("📋 Chi tiết", key=f"detail_user_{user.get('id')}"):
                    st.session_state["viewing_user"] = user
                    st.rerun()

    # Modal xem chi tiết
    if "viewing_user" in st.session_state:
        user = st.session_state["viewing_user"]
        with st.expander(
            f"📋 Chi tiết khách hàng: {user.get('full_name', 'N/A')}", expanded=True
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Thông tin cá nhân:**")
                st.write(f"- Họ tên: {user.get('full_name', 'N/A')}")
                st.write(f"- Email: {user.get('email', 'N/A')}")
                st.write(f"- SĐT: {user.get('phone', 'N/A')}")
                st.write(f"- Địa chỉ: {user.get('address', 'N/A')}")
            with col2:
                st.write("**Thông tin đơn hàng:**")
                st.write(f"- Tổng đơn: {user.get('total_orders', 0)}")
                st.write(f"- Tổng chi tiêu: {user.get('total_spent', 0):,.0f}đ")
                st.write(f"- Ngày cưới: {user.get('wedding_date', 'Chưa cập nhật')}")

            if st.button("❌ Đóng"):
                st.session_state.pop("viewing_user", None)
                st.rerun()


# ============ QUẢN LÝ LỊCH TRỐNG ============
def ui_quan_ly_lich_trong():
    st.header("📅 Quản lý Lịch trống")

    st.info("💡 Quản lý ngày có sẵn/không có sẵn cho dịch vụ cưới")

    # Lấy dữ liệu lịch
    calendar_data = call_api("GET", "/pg/lich_trong", clear_cache=False)

    tab1, tab2 = st.tabs(["📅 Xem lịch", "➕ Thêm ngày"])

    with tab2:
        st.subheader("➕ Thêm/Cập nhật ngày")

        with st.form("form_add_date"):
            col1, col2 = st.columns(2)

            with col1:
                selected_date = st.date_input(
                    "📅 Chọn ngày", min_value=datetime.now().date()
                )
                status = st.selectbox(
                    "Trạng thái",
                    ["available", "booked", "blocked"],
                    format_func=lambda x: {
                        "available": "✅ Có sẵn",
                        "booked": "📌 Đã đặt",
                        "blocked": "🚫 Khóa",
                    }[x],
                )

            with col2:
                slots = st.number_input(
                    "Số slot còn trống", min_value=0, max_value=10, value=3
                )
                note = st.text_input("Ghi chú", placeholder="VD: Đã có 2 đám cưới")

            if st.form_submit_button(
                "💾 Lưu", use_container_width=True, type="primary"
            ):
                data = {
                    "date": selected_date.strftime("%Y-%m-%d"),
                    "status": status,
                    "slots_available": slots,
                    "note": note,
                }
                result = call_api("POST", "/pg/lich_trong", data=data)
                if result:
                    st.success("✅ Đã cập nhật lịch!")
                    st.rerun()

    with tab1:
        st.subheader("📅 Lịch tháng này")

        # Hiển thị tháng hiện tại
        today = datetime.now()
        month_start = today.replace(day=1)

        col_prev, col_month, col_next = st.columns([1, 3, 1])
        with col_month:
            st.markdown(f"### 📆 Tháng {today.month}/{today.year}")

        if calendar_data is None:
            calendar_data = []

        # Tạo dict để tra cứu nhanh
        date_status = {d.get("date"): d for d in calendar_data}

        # Hiển thị lịch dạng grid
        st.markdown("**Chú thích:** ✅ Có sẵn | 📌 Đã đặt | 🚫 Khóa | ⬜ Chưa cập nhật")

        # Tạo calendar grid
        import calendar

        cal = calendar.monthcalendar(today.year, today.month)

        # Header
        cols = st.columns(7)
        days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        for i, day in enumerate(days):
            cols[i].markdown(f"**{day}**")

        # Days
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].write("")
                else:
                    date_str = f"{today.year}-{today.month:02d}-{day:02d}"
                    info = date_status.get(date_str, {})
                    status = info.get("status", "unknown")

                    icon = {"available": "✅", "booked": "📌", "blocked": "🚫"}.get(
                        status, "⬜"
                    )

                    is_today = day == today.day
                    style = (
                        "background: #c9a86c; color: white; padding: 5px; border-radius: 5px;"
                        if is_today
                        else ""
                    )

                    cols[i].markdown(
                        f"<div style='{style}'>{icon} {day}</div>",
                        unsafe_allow_html=True,
                    )

        st.markdown("---")

        # Danh sách chi tiết
        st.subheader("📋 Chi tiết các ngày đã cập nhật")

        if calendar_data:
            for item in sorted(calendar_data, key=lambda x: x.get("date", "")):
                status_icon = {"available": "✅", "booked": "📌", "blocked": "🚫"}.get(
                    item.get("status"), "⬜"
                )
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"**{item.get('date')}** {status_icon}")
                    with col2:
                        st.write(
                            f"Slots: {item.get('slots_available', 0)} | {item.get('note', '')}"
                        )
                    with col3:
                        if st.button("🗑️", key=f"del_cal_{item.get('id')}"):
                            if call_api("DELETE", f"/pg/lich_trong/{item.get('id')}"):
                                st.toast("Đã xóa!")
                                st.rerun()
        else:
            st.info("Chưa có dữ liệu lịch. Hãy thêm ngày ở tab 'Thêm ngày'.")


# ============ THỐNG KÊ YÊU THÍCH ============
def ui_thong_ke_yeu_thich():
    st.header("❤️ Thống kê Yêu thích")

    # Lấy thống kê yêu thích
    favorites_stats = call_api("GET", "/pg/yeu_thich/thong_ke", clear_cache=False)

    if favorites_stats is None:
        st.error("❌ Không thể kết nối đến server")
        return

    # Tổng quan
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❤️ Tổng lượt yêu thích", favorites_stats.get("total_favorites", 0))
    with col2:
        st.metric(
            "👗 Sản phẩm được yêu thích",
            favorites_stats.get("products_with_favorites", 0),
        )
    with col3:
        st.metric(
            "👥 Khách hàng yêu thích", favorites_stats.get("users_with_favorites", 0)
        )

    st.markdown("---")

    # Top sản phẩm được yêu thích
    st.subheader("🏆 Top sản phẩm được yêu thích nhất")

    top_products = favorites_stats.get("top_products", [])

    if top_products:
        for idx, product in enumerate(top_products[:10], 1):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([0.5, 1, 3, 1])

                with col1:
                    medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(idx, f"#{idx}")
                    st.markdown(f"### {medal}")

                with col2:
                    img_url = lay_url_anh(product.get("image_url"))
                    st.image(img_url, width=80)

                with col3:
                    st.write(f"**{product.get('name', 'N/A')}**")
                    st.caption(
                        f"Mã: {product.get('code', 'N/A')} | Danh mục: {product.get('category', 'N/A')}"
                    )
                    st.caption(f"Giá: {product.get('rental_price_day', 0):,.0f}đ/ngày")

                with col4:
                    st.metric("❤️", product.get("favorite_count", 0))
    else:
        st.info("📭 Chưa có dữ liệu yêu thích")

    st.markdown("---")

    # Biểu đồ xu hướng (nếu có dữ liệu)
    st.subheader("📈 Xu hướng yêu thích theo thời gian")

    trend_data = favorites_stats.get("trend", [])
    if trend_data:
        import pandas as pd

        df = pd.DataFrame(trend_data)
        st.line_chart(df.set_index("date")["count"])
    else:
        st.info("Chưa có đủ dữ liệu để hiển thị xu hướng")


def ui_san_pham():
    # Kiểm tra quyền truy cập
    if not has_permission("products"):
        st.error(
            "⛔ Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."
        )
        return

    st.header("Quản lý Sản phẩm")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])

    # Định nghĩa tiểu mục theo danh mục
    tieu_muc_theo_danh_muc = {
        "wedding_modern": [
            ("all", "Tất cả váy cưới"),
            ("xoe", "Váy Xòe"),
            ("duoi_ca", "Váy Đuôi Cá"),
            ("ngan", "Váy Ngắn"),
        ],
        "vest": [
            ("all", "Tất cả Vest"),
            ("hien_dai", "Vest Hiện Đại"),
            ("han_quoc", "Vest Hàn Quốc"),
        ],
        "aodai": [
            ("all", "Tất cả Áo Dài"),
            ("nam", "Áo Dài Nam"),
            ("nu", "Áo Dài Nữ"),
        ],
    }

    with t2:
        st.subheader("📝 Thêm mẫu váy mới")
        with st.form("add_prod"):
            # THÔNG TIN CƠ BẢN
            st.markdown("### 📋 Thông tin cơ bản")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input(
                    "Tên sản phẩm *", placeholder="VD: Váy Cưới Thanh Lịch"
                )
                code = st.text_input("Mã sản phẩm (SKU) *", placeholder="VD: VD-M001")
                cat = st.selectbox(
                    "Danh mục *",
                    ["wedding_modern", "vest", "aodai"],
                    format_func=lambda x: {
                        "wedding_modern": "👰 Váy cưới hiện đại",
                        "vest": "🤵 Vest",
                        "aodai": "👘 Áo dài",
                    }[x],
                )
            with c2:
                # Tiểu mục động theo danh mục
                sub_cat_options = tieu_muc_theo_danh_muc.get(cat, [("all", "Tất cả")])
                sub_cat = st.selectbox(
                    "Tiểu mục *",
                    options=[x[0] for x in sub_cat_options],
                    format_func=lambda x: dict(sub_cat_options).get(x, x),
                )
                gender = st.selectbox(
                    "Giới tính",
                    ["female", "male", "unisex"],
                    format_func=lambda x: {
                        "female": "👰 Nữ",
                        "male": "🤵 Nam",
                        "unisex": "👫 Unisex",
                    }[x],
                )
                is_hot = st.checkbox("🔥 Đánh dấu sản phẩm HOT")

            # SỐ LƯỢNG VÀ TRẠNG THÁI
            st.markdown("### 📦 Số lượng & Trạng thái")
            c1, c2 = st.columns(2)
            with c1:
                so_luong = st.number_input(
                    "Số lượng tồn kho *", min_value=0, value=10, step=1
                )
            with c2:
                het_hang = st.checkbox("❌ Đánh dấu HẾT HÀNG")

            # GIÁ CẢ
            st.markdown("### 💰 Giá cả")
            c1, c2, c3 = st.columns(3)
            with c1:
                price_day = st.number_input(
                    "Giá thuê/ngày (VNĐ) *", min_value=0, value=1000000, step=100000
                )
            with c2:
                price_week = st.number_input(
                    "Giá thuê/tuần (VNĐ)",
                    min_value=0,
                    value=int(price_day * 5),
                    step=100000,
                )
            with c3:
                price_buy = st.number_input(
                    "Giá mua (VNĐ)", min_value=0, value=int(price_day * 20), step=500000
                )

            # CHI TIẾT SẢN PHẨM
            st.markdown("### 🎨 Chi tiết sản phẩm")
            c1, c2 = st.columns(2)
            with c1:
                fabric = st.text_input(
                    "Loại vải", placeholder="VD: Ren cao cấp, Lụa Satin"
                )
                color = st.text_input(
                    "Màu sắc", placeholder="VD: Trắng, Kem, Hồng pastel"
                )
            with c2:
                sizes = st.multiselect(
                    "Size có sẵn *",
                    options=["XS", "S", "M", "L", "XL", "XXL", "Free Size"],
                    default=["S", "M", "L"],
                )
                makeup_tone = st.text_area(
                    "Gợi ý tông makeup",
                    placeholder="VD: Tông nude tự nhiên, môi hồng nhẹ",
                    height=80,
                )

            description = st.text_area(
                "Mô tả chi tiết sản phẩm",
                placeholder="Mô tả về thiết kế, phong cách, đặc điểm nổi bật...",
                height=120,
            )

            # HÌNH ẢNH
            st.markdown("### 📸 Hình ảnh sản phẩm")
            st.info(
                "💡 Mẹo: Ảnh đại diện sẽ là Váy Mẫu 1. Chỉ cần thêm 3 ảnh mẫu còn lại (Mẫu 2, 3, 4)"
            )

            img_file = st.file_uploader(
                "🖼️ Ảnh đại diện - Váy Mẫu 1 (bắt buộc) *",
                type=["jpg", "png", "jpeg", "webp"],
                help="Ảnh này sẽ là Váy Mẫu 1 và hiển thị trên danh sách sản phẩm",
            )

            if img_file:
                st.image(
                    img_file, caption="Xem trước Váy Mẫu 1 (Ảnh đại diện)", width=300
                )

            st.markdown("#### 🎨 3 Ảnh mẫu còn lại (Váy Mẫu 2, 3, 4)")
            st.caption("Upload 3 ảnh để có đủ 4 thumbnail cho khách hàng xem")

            col_img2, col_img3, col_img4 = st.columns(3)

            with col_img2:
                img_mau_2 = st.file_uploader(
                    "📷 Váy Mẫu 2", type=["jpg", "png", "jpeg", "webp"], key="mau2"
                )
                if img_mau_2:
                    st.image(img_mau_2, use_container_width=True)

            with col_img3:
                img_mau_3 = st.file_uploader(
                    "📷 Váy Mẫu 3", type=["jpg", "png", "jpeg", "webp"], key="mau3"
                )
                if img_mau_3:
                    st.image(img_mau_3, use_container_width=True)

            with col_img4:
                img_mau_4 = st.file_uploader(
                    "📷 Váy Mẫu 4", type=["jpg", "png", "jpeg", "webp"], key="mau4"
                )
                if img_mau_4:
                    st.image(img_mau_4, use_container_width=True)

            st.markdown("---")
            st.markdown("#### 🖼️ Bộ sưu tập ảnh bổ sung (tùy chọn)")
            st.caption("Nếu muốn thêm nhiều ảnh khác ngoài 4 ảnh mẫu ở trên")

            gallery_files = st.file_uploader(
                "Chọn thêm ảnh cho bộ sưu tập",
                accept_multiple_files=True,
                type=["jpg", "png", "jpeg", "webp"],
                help="Các ảnh bổ sung sẽ được thêm vào gallery",
            )

            if gallery_files:
                st.write(f"✅ Đã chọn {len(gallery_files)} ảnh bổ sung")
                cols = st.columns(min(len(gallery_files), 4))
                for idx, f in enumerate(gallery_files[:4]):
                    with cols[idx]:
                        st.image(f, caption=f"Ảnh {idx + 1}", use_container_width=True)
                if len(gallery_files) > 4:
                    st.caption(f"... và {len(gallery_files) - 4} ảnh khác")

            # PHỤ KIỆN KÈM THEO (Optional)
            st.markdown("### 🎀 Phụ kiện kèm theo (tùy chọn)")
            with st.expander("Thêm phụ kiện"):
                acc1_name = st.text_input("Tên phụ kiện 1", placeholder="VD: Vai nơ")
                acc1_price = st.number_input(
                    "Giá phụ kiện 1", min_value=0, value=0, step=10000
                )

                acc2_name = st.text_input("Tên phụ kiện 2", placeholder="VD: Lúp voan")
                acc2_price = st.number_input(
                    "Giá phụ kiện 2", min_value=0, value=0, step=10000
                )

                acc3_name = st.text_input(
                    "Tên phụ kiện 3", placeholder="VD: Găng tay ren"
                )
                acc3_price = st.number_input(
                    "Giá phụ kiện 3", min_value=0, value=0, step=10000
                )

            st.markdown("---")
            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col2:
                submitted = st.form_submit_button(
                    "✨ THÊM SẢN PHẨM", use_container_width=True, type="primary"
                )

            if submitted:
                # Validation
                if not name or not code or not img_file:
                    st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
                else:
                    with st.spinner("Đang tải ảnh lên..."):
                        # Upload ảnh đại diện (Váy Mẫu 1)
                        url = upload_image(img_file)

                        # Upload 3 ảnh mẫu còn lại SONG SONG
                        gallery_urls = [url] if url else []
                        mau_images = [m for m in [img_mau_2, img_mau_3, img_mau_4] if m]

                        if mau_images:
                            mau_urls = upload_images_parallel(mau_images)
                            gallery_urls.extend(mau_urls)
                            st.success(f"✅ Đã tải {len(mau_urls)} ảnh mẫu")

                        # Upload các ảnh bổ sung SONG SONG
                        if gallery_files:
                            extra_urls = upload_images_parallel(gallery_files)
                            gallery_urls.extend(extra_urls)
                            st.success(f"✅ Đã tải {len(extra_urls)} ảnh bổ sung")

                    if url:
                        # Prepare accessories data
                        accessories = []
                        if acc1_name and acc1_price > 0:
                            accessories.append({"name": acc1_name, "price": acc1_price})
                        if acc2_name and acc2_price > 0:
                            accessories.append({"name": acc2_name, "price": acc2_price})
                        if acc3_name and acc3_price > 0:
                            accessories.append({"name": acc3_name, "price": acc3_price})

                        data = {
                            "name": name,
                            "code": code,
                            "category": cat,
                            "sub_category": sub_cat,
                            "rental_price_day": price_day,
                            "rental_price_week": price_week,
                            "purchase_price": price_buy,
                            "image_url": url,
                            "gallery_images": gallery_urls,
                            "gender": gender,
                            "fabric_type": fabric or "Cao cấp",
                            "color": color or "Đa dạng",
                            "recommended_size": ", ".join(sizes)
                            if sizes
                            else "Đủ size",
                            "makeup_tone": makeup_tone or "Tự nhiên",
                            "description": description or "",
                            "is_hot": is_hot,
                            "so_luong": so_luong,
                            "het_hang": het_hang,
                            "accessories": accessories,
                        }
                        if call_api("POST", "/api/san_pham/", data=data):
                            st.success(
                                f"✅ Đã thêm sản phẩm mới thành công! ({len(gallery_urls)} ảnh mẫu)"
                            )
                            st.balloons()
                            st.rerun()
                    else:
                        st.error("❌ Lỗi khi tải ảnh lên. Vui lòng thử lại.")

    with t1:
        prods = call_api("GET", "/api/san_pham/", clear_cache=False)
        if prods:
            # THANH TÌM KIẾM VÀ LỌC
            st.markdown("### 🔍 Tìm kiếm & Lọc")
            col_search, col_cat, col_hot, col_sort = st.columns([3, 2, 1, 2])

            with col_search:
                search_term = st.text_input(
                    "🔎 Tìm kiếm",
                    placeholder="Tên, mã sản phẩm...",
                    label_visibility="collapsed",
                )

            with col_cat:
                filter_cat = st.selectbox(
                    "Danh mục",
                    ["Tất cả", "wedding_modern", "vest", "aodai"],
                    format_func=lambda x: {
                        "Tất cả": "📦 Tất cả",
                        "wedding_modern": "👰 Váy cưới",
                        "vest": "🤵 Vest",
                        "aodai": "👘 Áo dài",
                    }.get(x, x),
                )

            with col_hot:
                filter_hot = st.checkbox("🔥 Chỉ HOT")

            with col_sort:
                sort_by = st.selectbox(
                    "Sắp xếp",
                    ["Mới nhất", "Tên A-Z", "Tên Z-A", "Giá tăng", "Giá giảm"],
                )

            # Lọc tiểu mục theo danh mục đã chọn
            if filter_cat != "Tất cả":
                sub_cat_filter_options = {
                    "wedding_modern": ["Tất cả", "xoe", "duoi_ca", "ngan"],
                    "vest": ["Tất cả", "hien_dai", "han_quoc"],
                    "aodai": ["Tất cả", "nam", "nu"],
                }
                sub_cat_labels = {
                    "Tất cả": "Tất cả tiểu mục",
                    "xoe": "Váy Xòe",
                    "duoi_ca": "Váy Đuôi Cá",
                    "ngan": "Váy Ngắn",
                    "hien_dai": "Vest Hiện Đại",
                    "han_quoc": "Vest Hàn Quốc",
                    "nam": "Áo Dài Nam",
                    "nu": "Áo Dài Nữ",
                }
                filter_sub = st.selectbox(
                    "Tiểu mục",
                    sub_cat_filter_options.get(filter_cat, ["Tất cả"]),
                    format_func=lambda x: sub_cat_labels.get(x, x),
                )
            else:
                filter_sub = "Tất cả"

            # LỌC DỮ LIỆU
            filtered_prods = prods.copy()

            # Lọc theo tìm kiếm
            if search_term:
                search_lower = search_term.lower()
                filtered_prods = [
                    p
                    for p in filtered_prods
                    if search_lower in p.get("name", "").lower()
                    or search_lower in p.get("code", "").lower()
                ]

            # Lọc theo danh mục
            if filter_cat != "Tất cả":
                filtered_prods = [
                    p for p in filtered_prods if p.get("category") == filter_cat
                ]

            # Lọc theo tiểu mục
            if filter_sub != "Tất cả":
                filtered_prods = [
                    p for p in filtered_prods if p.get("sub_category") == filter_sub
                ]

            # Lọc theo HOT
            if filter_hot:
                filtered_prods = [p for p in filtered_prods if p.get("is_hot", False)]

            # Sắp xếp
            if sort_by == "Tên A-Z":
                filtered_prods.sort(key=lambda x: x.get("name", "").lower())
            elif sort_by == "Tên Z-A":
                filtered_prods.sort(
                    key=lambda x: x.get("name", "").lower(), reverse=True
                )
            elif sort_by == "Giá tăng":
                filtered_prods.sort(key=lambda x: x.get("rental_price_day", 0))
            elif sort_by == "Giá giảm":
                filtered_prods.sort(
                    key=lambda x: x.get("rental_price_day", 0), reverse=True
                )
            elif sort_by == "Mới nhất":
                filtered_prods.reverse()  # Giả sử API trả về theo thứ tự cũ nhất trước

            # XUẤT EXCEL
            col_info, col_export = st.columns([3, 1])
            with col_info:
                st.text(f"📊 Hiển thị: {len(filtered_prods)}/{len(prods)} sản phẩm")
            with col_export:
                if st.button("📥 XUẤT EXCEL", use_container_width=True):
                    # Tạo DataFrame
                    export_data = []
                    for p in filtered_prods:
                        export_data.append(
                            {
                                "Mã SP": p.get("code", ""),
                                "Tên sản phẩm": p.get("name", ""),
                                "Danh mục": p.get("category", ""),
                                "Tiểu mục": p.get("sub_category", ""),
                                "Giá thuê/ngày": p.get("rental_price_day", 0),
                                "Giá thuê/tuần": p.get("rental_price_week", 0),
                                "Giá mua": p.get("purchase_price", 0),
                                "Loại vải": p.get("fabric_type", ""),
                                "Màu sắc": p.get("color", ""),
                                "Size": p.get("recommended_size", ""),
                                "HOT": "Có" if p.get("is_hot", False) else "Không",
                                "Giới tính": p.get("gender", ""),
                            }
                        )

                    df = pd.DataFrame(export_data)

                    # Tạo file Excel trong memory
                    from io import BytesIO

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, index=False, sheet_name="Sản phẩm")
                    output.seek(0)

                    # Download button
                    st.download_button(
                        label="💾 Tải xuống",
                        data=output,
                        file_name=f"danh_sach_san_pham_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

            st.markdown("---")

            # PAGINATION
            page_size = st.selectbox(
                "Số sản phẩm/trang",
                [10, 20, 50, 100],
                index=1,
                key="page_size_products",
            )
            paginated_prods, current_page, total_pages = paginate_list(
                filtered_prods, page_size
            )

            st.text(
                f"📊 Hiển thị {len(paginated_prods)} / {len(filtered_prods)} sản phẩm (Trang {current_page}/{total_pages})"
            )

            # Pagination controls
            show_pagination(current_page, total_pages)

            st.markdown("---")
            h1, h2, h3, h4 = st.columns([1, 2, 1, 1])
            h1.write("**ẢNH**")
            h2.write("**THÔNG TIN**")
            h3.write("**GIÁ THUÊ**")
            h4.write("**HÀNH ĐỘNG**")
            st.markdown("---")

            for p in paginated_prods:  # Chỉ hiển thị sản phẩm trong trang hiện tại
                edit_key = f"edit_{p['id']}"
                is_editing = st.session_state.get(edit_key, False)

                with st.container():
                    if is_editing:
                        with st.form(f"form_edit_{p['id']}"):
                            c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                            with c1:
                                st.image(
                                    lay_url_anh(p["image_url"]),
                                    use_container_width=True,
                                )
                                new_img = st.file_uploader(
                                    "Đổi ảnh đại diện (Váy Mẫu 1)",
                                    type=["jpg", "png", "jpeg", "webp"],
                                    key=f"u_{p['id']}",
                                )

                                st.markdown("**📸 4 Ảnh mẫu hiện tại:**")
                                st.caption("Mẫu 1 = Ảnh đại diện")
                                current_gallery = p.get("gallery_images", [])
                                if current_gallery:
                                    # Hiển thị ảnh đại diện + 3 ảnh mẫu
                                    st.image(
                                        lay_url_anh(p["image_url"]),
                                        caption="Mẫu 1 (Đại diện)",
                                        use_container_width=True,
                                    )
                                    for idx, g in enumerate(
                                        current_gallery[1:4]
                                    ):  # Bỏ qua ảnh đầu (trùng với đại diện)
                                        st.image(
                                            lay_url_anh(g),
                                            caption=f"Mẫu {idx + 2}",
                                            use_container_width=True,
                                        )
                                else:
                                    st.caption("Chưa có ảnh mẫu")

                                st.markdown("**🔄 Cập nhật 3 ảnh mẫu còn lại:**")
                                st.caption("Mẫu 1 = Ảnh đại diện ở trên")
                                edit_mau_2 = st.file_uploader(
                                    "Váy Mẫu 2",
                                    type=["jpg", "png", "jpeg", "webp"],
                                    key=f"em2_{p['id']}",
                                )
                                edit_mau_3 = st.file_uploader(
                                    "Váy Mẫu 3",
                                    type=["jpg", "png", "jpeg", "webp"],
                                    key=f"em3_{p['id']}",
                                )
                                edit_mau_4 = st.file_uploader(
                                    "Váy Mẫu 4",
                                    type=["jpg", "png", "jpeg", "webp"],
                                    key=f"em4_{p['id']}",
                                )

                                st.caption(
                                    "💡 Chỉ upload ảnh nào muốn thay đổi. Để trống = giữ nguyên ảnh cũ"
                                )
                            with c2:
                                new_name = st.text_input("Tên", value=p["name"])
                                new_code = st.text_input("Mã", value=p["code"])
                                new_cat = st.selectbox(
                                    "Danh mục",
                                    ["wedding_modern", "vest", "aodai"],
                                    index=["wedding_modern", "vest", "aodai"].index(
                                        p["category"]
                                    )
                                    if p["category"]
                                    in ["wedding_modern", "vest", "aodai"]
                                    else 0,
                                    key=f"cat_{p['id']}",
                                )

                                # Tiểu mục động theo danh mục
                                sub_options_edit = {
                                    "wedding_modern": ["", "xoe", "duoi_ca", "ngan"],
                                    "vest": ["", "hien_dai", "han_quoc"],
                                    "aodai": ["", "nam", "nu"],
                                }
                                sub_labels_edit = {
                                    "": "-- Chọn tiểu mục --",
                                    "xoe": "👗 Váy Xòe",
                                    "duoi_ca": "👗 Váy Đuôi Cá",
                                    "ngan": "👗 Váy Ngắn",
                                    "hien_dai": "🤵 Vest Hiện Đại",
                                    "han_quoc": "🤵 Vest Hàn Quốc",
                                    "nam": "👔 Áo Dài Nam",
                                    "nu": "👘 Áo Dài Nữ",
                                }
                                current_sub = p.get("sub_category", "")
                                sub_opts = sub_options_edit.get(new_cat, [""])
                                sub_idx = (
                                    sub_opts.index(current_sub)
                                    if current_sub in sub_opts
                                    else 0
                                )
                                new_sub = st.selectbox(
                                    "Tiểu mục",
                                    sub_opts,
                                    index=sub_idx,
                                    format_func=lambda x: sub_labels_edit.get(x, x),
                                    key=f"sub_{p['id']}",
                                )

                            with c3:
                                new_price = st.number_input(
                                    "Giá thuê ngày", value=float(p["rental_price_day"])
                                )
                                new_price_buy = st.number_input(
                                    "Giá mua", value=float(p.get("purchase_price", 0))
                                )
                                new_hot = st.checkbox(
                                    "Hot",
                                    value=p.get("is_hot", False),
                                    key=f"hot_{p['id']}",
                                )
                                new_so_luong = st.number_input(
                                    "Số lượng",
                                    min_value=0,
                                    value=int(p.get("so_luong", 10)),
                                    key=f"sl_{p['id']}",
                                )
                                new_het_hang = st.checkbox(
                                    "Hết hàng",
                                    value=p.get("het_hang", False),
                                    key=f"hh_{p['id']}",
                                )
                                st.markdown("---")
                                new_fabric = st.text_input(
                                    "Loại vải", value=p.get("fabric_type", "")
                                )
                                new_color = st.text_input(
                                    "Màu sắc", value=p.get("color", "")
                                )
                                # Chuyển size từ string thành list
                                current_sizes = [
                                    s.strip()
                                    for s in (
                                        p.get("recommended_size", "") or ""
                                    ).split(",")
                                    if s.strip()
                                ]
                                all_sizes = [
                                    "XS",
                                    "S",
                                    "M",
                                    "L",
                                    "XL",
                                    "XXL",
                                    "Free Size",
                                ]
                                new_size_list = st.multiselect(
                                    "Size có sẵn",
                                    options=all_sizes,
                                    default=[
                                        s for s in current_sizes if s in all_sizes
                                    ],
                                    key=f"size_{p['id']}",
                                )
                                new_size = (
                                    ", ".join(new_size_list)
                                    if new_size_list
                                    else "Đủ size"
                                )
                                new_makeup = st.text_area(
                                    "Tông makeup", value=p.get("makeup_tone", "")
                                )
                            with c4:
                                if st.form_submit_button("LƯU"):
                                    img_url = p["image_url"]
                                    if new_img:
                                        uploaded = upload_image(new_img)
                                        if uploaded:
                                            img_url = uploaded

                                    # Xử lý 3 ảnh mẫu (Mẫu 2, 3, 4)
                                    # Gallery = [ảnh đại diện, mẫu 2, mẫu 3, mẫu 4, ...]
                                    gallery_urls = [img_url]  # Mẫu 1 = ảnh đại diện
                                    new_mau_images = [
                                        edit_mau_2,
                                        edit_mau_3,
                                        edit_mau_4,
                                    ]
                                    old_gallery = p.get("gallery_images", [])

                                    # Xử lý 3 ảnh mẫu còn lại
                                    for idx, mau_img in enumerate(new_mau_images):
                                        if mau_img:
                                            u = upload_image(mau_img)
                                            if u:
                                                gallery_urls.append(u)
                                                st.success(
                                                    f"✅ Đã cập nhật Váy Mẫu {idx + 2}"
                                                )
                                        else:
                                            # Giữ ảnh cũ nếu không upload mới (bỏ qua ảnh đầu vì đó là ảnh đại diện)
                                            if idx + 1 < len(old_gallery):
                                                gallery_urls.append(
                                                    old_gallery[idx + 1]
                                                )

                                    # Thêm các ảnh bổ sung còn lại (nếu có)
                                    if len(old_gallery) > 4:
                                        gallery_urls.extend(old_gallery[4:])

                                    up_data = {
                                        "name": new_name,
                                        "code": new_code,
                                        "category": new_cat,
                                        "sub_category": new_sub,
                                        "rental_price_day": new_price,
                                        "image_url": img_url,
                                        "gallery_images": gallery_urls,
                                        "is_hot": new_hot,
                                        "gender": p["gender"],
                                        "purchase_price": new_price_buy,
                                        "rental_price_week": p.get(
                                            "rental_price_week", new_price * 5
                                        ),
                                        "fabric_type": new_fabric,
                                        "color": new_color,
                                        "recommended_size": new_size,
                                        "makeup_tone": new_makeup,
                                        "so_luong": new_so_luong,
                                        "het_hang": new_het_hang,
                                    }
                                    if call_api(
                                        "PUT", f"/api/san_pham/{p['id']}", data=up_data
                                    ):
                                        st.session_state[edit_key] = False
                                        st.toast(f"Đã cập nhật sản phẩm (4 ảnh mẫu)")
                                        st.rerun()
                                if st.form_submit_button("HỦY"):
                                    st.session_state[edit_key] = False
                                    st.rerun()
                    else:
                        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                        with c1:
                            st.image(
                                lay_url_anh(p["image_url"]), use_container_width=True
                            )
                        with c2:
                            st.write(f"**{p['code']}**")
                            st.write(p["name"])
                            if p.get("is_hot"):
                                st.caption("🔥 Sản phẩm Hot")
                        with c3:
                            st.write(f"**{p['rental_price_day']:,.0f}đ**")
                        with c4:
                            b_edit, b_del = st.columns(2)
                            if b_edit.button("SỬA", key=f"btn_edit_{p['id']}"):
                                st.session_state[edit_key] = True
                                st.rerun()
                            if b_del.button("XÓA", key=f"dp_{p['id']}"):
                                if call_api("DELETE", f"/api/san_pham/{p['id']}"):
                                    st.toast("Đã xóa sản phẩm")
                                    st.rerun()
                    st.markdown(
                        "<div style='border-bottom: 1px solid #222; margin: 10px 0;'></div>",
                        unsafe_allow_html=True,
                    )

            # Pagination controls ở cuối
            st.markdown("---")
            show_pagination(current_page, total_pages)


def ui_thu_vien():
    st.header("Quản lý Thư viện")
    t1, t2 = st.tabs(["DANH SÁCH", "THÊM MỚI"])
    with t2:
        img_file = st.file_uploader("Chọn ảnh")
        if st.button("TẢI LÊN"):
            url = upload_image(img_file)
            if url:
                if call_api(
                    "POST",
                    "/api/thu_vien/",
                    data={"image_url": url, "title": "", "order": 0},
                ):
                    st.toast("Đã tải ảnh lên thư viện")
                    st.rerun()
    with t1:
        gal = call_api("GET", "/api/thu_vien/", clear_cache=False)
        if gal:
            cols = st.columns(4)
            for idx, item in enumerate(gal):
                with cols[idx % 4]:
                    st.image(lay_url_anh(item["image_url"]), use_container_width=True)
                    if st.button("XÓA", key=f"dg_{item['id']}"):
                        if call_api("DELETE", f"/api/thu_vien/{item['id']}"):
                            st.toast("Đã xóa ảnh")
                            st.rerun()


def ui_dich_vu_chuyen_gia():
    st.header("Chuyên gia & Dịch vụ")
    t_ex, t_sv, t_video = st.tabs(["CHUYÊN GIA", "GÓI DỊCH VỤ", "🎬 VIDEO GIỚI THIỆU"])
    with t_ex:
        with st.expander("THÊM CHUYÊN GIA"):
            with st.form("add_ex"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Tên chuyên gia")
                    title = st.text_input("Danh hiệu (VD: Chuyên viên Makeup)")
                    category = st.selectbox(
                        "Loại chuyên gia",
                        ["makeup", "photo"],
                        format_func=lambda x: "💄 Trang điểm"
                        if x == "makeup"
                        else "📸 Quay chụp",
                    )
                with col2:
                    years_exp = st.number_input(
                        "Số năm kinh nghiệm", min_value=1, value=3
                    )
                    price = st.number_input(
                        "Giá booking (VNĐ)",
                        min_value=100000,
                        value=1000000,
                        step=100000,
                    )
                    location = st.text_input("Khu vực làm việc", value="Hà Nội")
                level = st.selectbox(
                    "Cấp bậc",
                    ["senior", "master", "top_artist"],
                    format_func=lambda x: {
                        "senior": "Senior",
                        "master": "Master",
                        "top_artist": "Top Artist",
                    }[x],
                )
                is_top = st.checkbox("Đánh dấu là TOP Artist (nổi bật)")
                bio = st.text_area(
                    "Giới thiệu ngắn", placeholder="Mô tả về chuyên gia..."
                )
                video_url = st.text_input(
                    "🎬 Link Video YouTube",
                    placeholder="https://www.youtube.com/watch?v=...",
                )
                img_f = st.file_uploader("Ảnh đại diện")
                if st.form_submit_button("THÊM CHUYÊN GIA"):
                    url = upload_image(img_f)
                    if url:
                        data = {
                            "name": name,
                            "title": title,
                            "image_url": url,
                            "years_experience": years_exp,
                            "brides_count": years_exp * 50,
                            "category": category,
                            "level": level,
                            "location": location,
                            "price": price,
                            "is_top": is_top,
                            "bio": bio,
                            "video_url": video_url,
                            "specialties": ["Cưới", "Sự kiện"],
                        }
                        if call_api("POST", "/api/dich_vu/chuyen_gia", data=data):
                            st.toast("Đã thêm chuyên gia mới!")
                            st.rerun()
        exps = call_api("GET", "/api/dich_vu/chuyen_gia", clear_cache=False)
        if exps:
            for e in exps:
                edit_key_ex = f"edit_ex_{e['id']}"
                is_editing_ex = st.session_state.get(edit_key_ex, False)
                with st.container(border=True):
                    if is_editing_ex:
                        with st.form(f"edit_ex_form_{e['id']}"):
                            c1, c2 = st.columns([1, 2])
                            with c1:
                                st.image(lay_url_anh(e["image_url"]))
                                new_img_ex = st.file_uploader(
                                    "Đổi ảnh", type=["jpg", "png"], key=f"ue_{e['id']}"
                                )
                            with c2:
                                en_name = st.text_input("Tên", value=e["name"])
                                en_title = st.text_input("Danh hiệu", value=e["title"])
                                en_cat = st.selectbox(
                                    "Loại",
                                    ["makeup", "photo"],
                                    index=0 if e.get("category") == "makeup" else 1,
                                )
                                en_level = st.selectbox(
                                    "Level", ["senior", "master", "top_artist"], index=0
                                )
                                en_loc = st.text_input(
                                    "Khu vực", value=e.get("location", "Hà Nội")
                                )
                                en_price = st.number_input(
                                    "Giá (Booking)",
                                    value=float(e.get("price", 1000000)),
                                )
                                en_top = st.checkbox(
                                    "Top Artist", value=e.get("is_top", False)
                                )
                                en_bio = st.text_area(
                                    "Giới thiệu", value=e.get("bio", "")
                                )
                                en_video = st.text_input(
                                    "🎬 Link Video YouTube",
                                    value=e.get("video_url", ""),
                                )
                            if st.form_submit_button("LƯU"):
                                img_url = e["image_url"]
                                if new_img_ex:
                                    u = upload_image(new_img_ex)
                                    if u:
                                        img_url = u
                                up_data = {
                                    "name": en_name,
                                    "title": en_title,
                                    "image_url": img_url,
                                    "category": en_cat,
                                    "level": en_level,
                                    "location": en_loc,
                                    "price": en_price,
                                    "is_top": en_top,
                                    "bio": en_bio,
                                    "video_url": en_video,
                                    "years_experience": e["years_experience"],
                                    "brides_count": e["brides_count"],
                                }
                                if call_api(
                                    "PUT",
                                    f"/api/dich_vu/chuyen_gia/{e['id']}",
                                    data=up_data,
                                ):
                                    st.session_state[edit_key_ex] = False
                                    st.toast("Đã cập nhật")
                                    st.rerun()
                    else:
                        c1, c2, c3, c4 = st.columns([1, 2, 1, 1])
                        with c1:
                            st.image(lay_url_anh(e["image_url"]))
                        with c2:
                            st.write(f"**{e['name']}**")
                            st.caption(e["title"])
                            if e.get("video_url"):
                                st.caption(f"🎬 Có video")
                        with c3:
                            st.write(f"{float(e.get('price', 1000000)):,.0f}đ")
                        with c4:
                            if st.button("SỬA", key=f"e_ex_{e['id']}"):
                                st.session_state[edit_key_ex] = True
                                st.rerun()
                            if st.button("XOÁ", key=f"dex_{e['id']}"):
                                if call_api(
                                    "DELETE", f"/api/dich_vu/chuyen_gia/{e['id']}"
                                ):
                                    st.toast("Đã xóa")
                                    st.rerun()

    # Tab Video giới thiệu
    with t_video:
        st.subheader("🎬 Quản lý Video Giới Thiệu Chuyên Gia")
        st.info("💡 Video sẽ hiển thị ở trang Dịch vụ Chuyên gia trên website")

        # Lấy danh sách chuyên gia có video
        exps_with_video = [e for e in (exps or []) if e.get("video_url")]
        exps_without_video = [e for e in (exps or []) if not e.get("video_url")]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎬 Có video", len(exps_with_video))
        with col2:
            st.metric("📷 Chưa có video", len(exps_without_video))

        st.markdown("---")

        # Chuyên gia có video
        st.markdown("### ✅ Chuyên gia đã có video")
        if exps_with_video:
            for e in exps_with_video:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        st.image(lay_url_anh(e["image_url"]), width=100)
                    with c2:
                        st.write(f"**{e['name']}** - {e['title']}")
                        # Hiển thị video preview
                        video_id = ""
                        if "youtube.com/watch?v=" in e["video_url"]:
                            video_id = e["video_url"].split("v=")[1].split("&")[0]
                        elif "youtu.be/" in e["video_url"]:
                            video_id = (
                                e["video_url"].split("youtu.be/")[1].split("?")[0]
                            )

                        if video_id:
                            st.markdown(
                                f"[🎬 Xem video](https://www.youtube.com/watch?v={video_id})"
                            )
                    with c3:
                        new_video = st.text_input(
                            "Đổi link video",
                            value=e["video_url"],
                            key=f"video_{e['id']}",
                        )
                        if st.button("💾 Lưu", key=f"save_video_{e['id']}"):
                            if call_api(
                                "PUT",
                                f"/api/dich_vu/chuyen_gia/{e['id']}",
                                data={**e, "video_url": new_video},
                            ):
                                st.toast("Đã cập nhật video!")
                                st.rerun()
        else:
            st.info("Chưa có chuyên gia nào có video")

        st.markdown("---")

        # Chuyên gia chưa có video
        st.markdown("### ⏳ Chuyên gia chưa có video")
        if exps_without_video:
            for e in exps_without_video:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        st.image(lay_url_anh(e["image_url"]), width=80)
                    with c2:
                        st.write(f"**{e['name']}** - {e['title']}")
                    with c3:
                        add_video = st.text_input(
                            "Thêm link video",
                            placeholder="https://youtube.com/...",
                            key=f"add_video_{e['id']}",
                        )
                        if st.button("➕ Thêm", key=f"add_btn_{e['id']}"):
                            if add_video:
                                if call_api(
                                    "PUT",
                                    f"/api/dich_vu/chuyen_gia/{e['id']}",
                                    data={**e, "video_url": add_video},
                                ):
                                    st.toast("Đã thêm video!")
                                    st.rerun()
        else:
            st.success("Tất cả chuyên gia đều đã có video!")

    with t_sv:
        svs = call_api("GET", "/api/dich_vu/", clear_cache=False)
        if svs:
            for s in svs:
                with st.container(border=True):
                    st.write(f"**{s['name']}**")
                    if st.button("XÓA", key=f"d_sv_{s['id']}"):
                        if call_api("DELETE", f"/api/dich_vu/{s['id']}"):
                            st.toast("Đã xóa")
                            st.rerun()


def ui_tu_van_khach_hang():
    st.header("Trò chuyện hỗ trợ khách hàng")
    st.markdown(
        """
        <style>
        .chat-container { display: flex; flex-direction: column; gap: 10px; padding: 20px; background: #111; border-radius: 8px; height: 500px; overflow-y: auto; border: 1px solid #333; }
        .msg { max-width: 80%; padding: 8px 12px; border-radius: 12px; font-size: 0.9em; line-height: 1.4; }
        .msg-user { align-self: flex-start; background: #222; color: #eee; border: 1px solid #444; }
        .msg-admin { align-self: flex-end; background: #ffffff; color: #000; }
        .chat-time { font-size: 0.7em; opacity: 0.6; margin-top: 4px; }
        </style>
    """,
        unsafe_allow_html=True,
    )
    col_users, col_chat = st.columns([1, 2])
    with col_users:
        sessions = call_api("GET", "/api/chat/admin/cac_phien_chat", clear_cache=False)
        selected_user_id = st.session_state.get("selected_chat_user", None)
        if sessions:
            for s in sessions:
                if st.button(
                    f"{s['full_name'] or s['username']}",
                    key=f"user_chat_{s['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_chat_user = s["id"]
                    st.rerun()
    with col_chat:
        if selected_user_id:
            history = call_api(
                "GET", f"/api/chat/admin/lich_su/{selected_user_id}", clear_cache=False
            )
            if history:
                chat_html = '<div class="chat-container">'
                for m in history:
                    cls = "msg-admin" if m["is_from_admin"] else "msg-user"
                    chat_html += f'<div class="msg {cls}">{m["tin_nhan"]}</div>'
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            with st.form("reply_form", clear_on_submit=True):
                reply_text = st.text_area("Nhập tin nhắn...")
                if st.form_submit_button("GỬI"):
                    if call_api(
                        "POST",
                        f"/api/chat/admin/tra_loi/{selected_user_id}",
                        data={"tin_nhan": reply_text},
                    ):
                        st.toast("Đã gửi")
                        st.rerun()


def ui_duyet_danh_gia():
    # Kiểm tra quyền truy cập
    if not has_permission("reviews"):
        st.error(
            "⛔ Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."
        )
        return

    st.header("⏳ Quản lý Đánh giá chờ duyệt")

    # Nút refresh
    if st.button("🔄 Tải lại"):
        st.cache_data.clear()
        st.rerun()

    pending = call_api(
        "GET", "/api/san_pham/admin/danh_gia_cho_duyet", clear_cache=False
    )

    if pending is None:
        st.error("Không thể kết nối API. Kiểm tra backend đang chạy.")
    elif len(pending) == 0:
        st.info("🎉 Không có đánh giá nào đang chờ duyệt!")
    else:
        st.success(f"Có {len(pending)} đánh giá đang chờ duyệt")
        for dg in pending:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(
                        f"**{dg.get('user_name', 'Ẩn danh')}** - ⭐ {dg.get('rating', 0)}/5"
                    )
                    st.write(f"📦 Sản phẩm ID: {dg.get('product_id')}")
                    st.caption(dg.get("comment", "Không có nhận xét"))
                    if dg.get("image_url"):
                        st.image(lay_url_anh(dg["image_url"]), width=100)
                with col2:
                    if st.button(f"✅ Duyệt", key=f"duyet_{dg['id']}"):
                        if call_api(
                            "POST", f"/api/san_pham/admin/duyet_danh_gia/{dg['id']}"
                        ):
                            st.toast("Đã duyệt đánh giá!")
                            st.rerun()
                    if st.button(f"❌ Xóa", key=f"xoa_{dg['id']}"):
                        if call_api(
                            "DELETE", f"/api/san_pham/admin/xoa_danh_gia/{dg['id']}"
                        ):
                            st.toast("Đã xóa đánh giá!")
                            st.rerun()


def ui_doi_tac_khieu_nai():
    st.header("🤝 Quản lý Đối tác & Khiếu nại")
    tab1, tab2 = st.tabs(["HỒ SƠ ĐỐI TÁC", "KHIẾU NẠI KHÁCH HÀNG"])

    with tab1:
        apps = call_api("GET", "/api/doi_tac/admin/danh_sach")

        if not apps:
            st.info("Chưa có hồ sơ đối tác nào.")
        else:
            for app in apps:
                with st.container(border=True):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.write(f"**{app['full_name']}** ({app['partner_type']})")
                        st.write(f"📞 {app['phone']} | ✉️ {app['email']}")
                        st.write(f"💼 Kinh nghiệm: {app['experience']}")
                        if app["portfolio_url"]:
                            st.write(f"🔗 [Portfolio]({app['portfolio_url']})")
                        if app["cv_url"]:
                            cv_url = (
                                app["cv_url"]
                                if app["cv_url"].startswith("http")
                                else f"{API_URL}{app['cv_url']}"
                            )
                            st.image(cv_url, caption="Ảnh CV / Portfolio", width=300)
                    with c2:
                        curr_status = app["status"]
                        st.write(f"Trạng thái hiện tại: **{curr_status}**")
                        new_status = st.selectbox(
                            "Cập nhật trạng thái",
                            ["pending", "interviewing", "accepted", "rejected"],
                            index=[
                                "pending",
                                "interviewing",
                                "accepted",
                                "rejected",
                            ].index(curr_status),
                            key=f"status_{app['id']}",
                        )
                        reply = st.text_area(
                            "Phản hồi cho đối tác", key=f"reply_{app['id']}"
                        )
                        contract = ""
                        if new_status == "accepted":
                            contract = st.text_area(
                                "Nội dung hợp đồng & Điều khoản",
                                value="CHƯƠNG TRÌNH HỢP TÁC IVIE...\n1. Trách nhiệm...\n2. Quyền lợi...",
                                key=f"contract_{app['id']}",
                            )

                        if st.button(
                            "CẬP NHẬT HỒ SƠ", key=f"btn_{app['id']}", type="primary"
                        ):
                            params = {
                                "status": new_status,
                                "reply": reply,
                                "contract": contract,
                            }
                            try:
                                res = requests.post(
                                    f"{API_URL}/api/doi_tac/admin/{app['id']}/phe_duyet",
                                    params=params,
                                )
                                if res.status_code == 200:
                                    st.toast("Đã cập nhật!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Lỗi API ({res.status_code}): {res.text}")
                            except Exception as e:
                                st.error(f"Lỗi kết nối: {e}")

    with tab2:
        complaints = call_api("GET", "/api/doi_tac/admin/khieu_nai")

        if not complaints:
            st.info("Không có khiếu nại nào.")
        else:
            for kn in complaints:
                with st.container(border=True):
                    st.write(f"**{kn['title']}** - Status: {kn['status']}")
                    st.write(
                        f"Người gửi: {kn['customer_name']} ({kn['customer_phone']})"
                    )
                    st.write(f"Nội dung: {kn['content']}")
                    if kn["admin_reply"]:
                        st.info(f"Đã phản hồi: {kn['admin_reply']}")
                    else:
                        rep = st.text_input(
                            "Câu trả lời của Admin", key=f"rep_kn_{kn['id']}"
                        )
                        if st.button("GỬI PHẢN HỒI", key=f"btn_kn_{kn['id']}"):
                            res = requests.post(
                                f"{API_URL}/api/doi_tac/admin/khieu_nai/{kn['id']}/tra_loi",
                                params={"reply": rep},
                            )
                            if res.status_code == 200:
                                st.toast("Đã phản hồi")
                                st.rerun()


def ui_blog():
    st.header("📰 Quản lý Blog & Tin tức")

    # Kiểm tra và import streamlit-quill
    try:
        from streamlit_quill import st_quill

        has_quill = True
    except ImportError:
        has_quill = False
        st.warning(
            "⚠️ Để sử dụng Rich Text Editor, hãy cài đặt: `pip install streamlit-quill`"
        )

    t1, t2, t3 = st.tabs(
        ["📋 DANH SÁCH BÀI VIẾT", "✏️ THÊM BÀI VIẾT MỚI", "📝 SỬA BÀI VIẾT"]
    )

    # === TAB 2: THÊM BÀI VIẾT MỚI ===
    with t2:
        st.subheader("✏️ Tạo bài viết mới")

        # Không dùng form để có thể sử dụng Rich Text Editor
        title = st.text_input("📌 Tiêu đề bài viết", key="new_blog_title")

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "📁 Danh mục",
                ["tips", "news", "wedding-story"],
                format_func=lambda x: {
                    "tips": "💡 Mẹo cưới",
                    "news": "📰 Tin tức",
                    "wedding-story": "💕 Câu chuyện cưới",
                }[x],
                key="new_blog_category",
            )
        with col2:
            is_published = st.checkbox(
                "🚀 Xuất bản ngay", value=False, key="new_blog_published"
            )

        excerpt = st.text_area(
            "📝 Tóm tắt ngắn (hiển thị ở danh sách)", height=80, key="new_blog_excerpt"
        )

        # SEO Fields
        with st.expander("🔍 SEO Settings (Tùy chọn)"):
            seo_title = st.text_input(
                "Meta Title",
                placeholder="Tiêu đề hiển thị trên Google",
                key="new_seo_title",
            )
            seo_desc = st.text_area(
                "Meta Description",
                placeholder="Mô tả ngắn cho SEO (150-160 ký tự)",
                height=80,
                key="new_seo_desc",
            )
            seo_keywords = st.text_input(
                "Keywords",
                placeholder="từ khóa 1, từ khóa 2, ...",
                key="new_seo_keywords",
            )

        st.markdown("### 📄 Nội dung bài viết")

        # Rich Text Editor
        if has_quill:
            content = st_quill(
                placeholder="Viết nội dung bài viết tại đây...",
                html=True,
                key="new_blog_content",
            )
        else:
            content = st.text_area(
                "Nội dung bài viết (hỗ trợ HTML)",
                height=400,
                key="new_blog_content_fallback",
                help="Cài đặt streamlit-quill để có Rich Text Editor",
            )

        # Ảnh bìa
        st.markdown("### 🖼️ Ảnh bìa")
        img = st.file_uploader(
            "Chọn ảnh bìa", type=["jpg", "png", "webp"], key="new_blog_img"
        )
        if img:
            st.image(img, caption="Xem trước ảnh bìa", width=400)

        # Nút tạo bài viết
        if st.button("💾 TẠO BÀI VIẾT", type="primary", use_container_width=True):
            if not title:
                st.error("⚠️ Vui lòng nhập tiêu đề bài viết!")
            elif not content:
                st.error("⚠️ Vui lòng nhập nội dung bài viết!")
            else:
                with st.spinner("Đang tạo bài viết..."):
                    img_url = upload_image(img) if img else None
                    data = {
                        "title": title,
                        "excerpt": excerpt,
                        "content": content,
                        "image_url": img_url,
                        "category": category,
                        "is_published": is_published,
                        "seo_title": seo_title if seo_title else title,
                        "seo_description": seo_desc if seo_desc else excerpt[:160],
                        "seo_keywords": seo_keywords,
                    }
                    if call_api("POST", "/api/blog/", data=data):
                        st.success("✅ Đã tạo bài viết mới!")
                        st.balloons()
                        st.rerun()

    # === TAB 1: DANH SÁCH BÀI VIẾT ===
    with t1:
        st.subheader("📋 Danh sách bài viết")

        # Bộ lọc
        col1, col2 = st.columns(2)
        with col1:
            filter_status = st.selectbox(
                "Trạng thái",
                ["Tất cả", "Đã xuất bản", "Bản nháp"],
                key="blog_filter_status",
            )
        with col2:
            filter_cat = st.selectbox(
                "Danh mục",
                ["Tất cả", "tips", "news", "wedding-story"],
                key="blog_filter_cat",
            )

        posts = call_api("GET", "/api/blog/?published_only=false", clear_cache=False)

        if posts:
            # Lọc
            filtered_posts = posts
            if filter_status == "Đã xuất bản":
                filtered_posts = [p for p in filtered_posts if p.get("is_published")]
            elif filter_status == "Bản nháp":
                filtered_posts = [
                    p for p in filtered_posts if not p.get("is_published")
                ]

            if filter_cat != "Tất cả":
                filtered_posts = [
                    p for p in filtered_posts if p.get("category") == filter_cat
                ]

            st.write(f"📊 Hiển thị **{len(filtered_posts)}** bài viết")

            for p in filtered_posts:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        if p.get("image_url"):
                            st.image(
                                lay_url_anh(p["image_url"]), use_container_width=True
                            )
                        else:
                            st.info("📷")
                    with c2:
                        # Status badge với màu
                        if p.get("is_published"):
                            st.markdown(
                                f"""
                                **{p["title"]}**
                                <span style="background:#2ecc7120; color:#2ecc71; padding:2px 8px; border-radius:8px; font-size:0.8em;">✅ Đã xuất bản</span>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f"""
                                **{p["title"]}**
                                <span style="background:#FFA50020; color:#FFA500; padding:2px 8px; border-radius:8px; font-size:0.8em;">📝 Bản nháp</span>
                            """,
                                unsafe_allow_html=True,
                            )

                        cat_labels = {
                            "tips": "💡 Mẹo cưới",
                            "news": "📰 Tin tức",
                            "wedding-story": "💕 Câu chuyện cưới",
                        }
                        st.caption(
                            f"📁 {cat_labels.get(p['category'], p['category'])} | 👁️ {p.get('views', 0)} lượt xem"
                        )
                        st.text(
                            p.get("excerpt", "")[:100] + "..."
                            if p.get("excerpt")
                            else ""
                        )
                    with c3:
                        # Nút sửa
                        if st.button("✏️ SỬA", key=f"edit_blog_{p['id']}"):
                            st.session_state["editing_blog"] = p
                            st.rerun()

                        # Nút xóa
                        if st.button("🗑️ XÓA", key=f"del_blog_{p['id']}"):
                            if call_api("DELETE", f"/api/blog/{p['id']}"):
                                st.toast("Đã xóa bài viết")
                                st.rerun()

                        # Nút xuất bản (nếu là bản nháp)
                        if not p.get("is_published"):
                            if st.button("🚀 XUẤT BẢN", key=f"pub_{p['id']}"):
                                data = {
                                    "title": p["title"],
                                    "excerpt": p.get("excerpt", ""),
                                    "content": p["content"],
                                    "image_url": p.get("image_url"),
                                    "category": p["category"],
                                    "is_published": True,
                                }
                                if call_api("PUT", f"/api/blog/{p['id']}", data=data):
                                    st.toast("Đã xuất bản!")
                                    st.rerun()
        else:
            st.info("Chưa có bài viết nào.")

    # === TAB 3: SỬA BÀI VIẾT ===
    with t3:
        editing_blog = st.session_state.get("editing_blog", None)

        if editing_blog:
            st.subheader(f"✏️ Sửa bài viết: {editing_blog.get('title', '')}")

            edit_title = st.text_input(
                "📌 Tiêu đề", value=editing_blog.get("title", ""), key="edit_blog_title"
            )

            col1, col2 = st.columns(2)
            with col1:
                cat_options = ["tips", "news", "wedding-story"]
                current_cat = editing_blog.get("category", "tips")
                edit_category = st.selectbox(
                    "📁 Danh mục",
                    cat_options,
                    index=cat_options.index(current_cat)
                    if current_cat in cat_options
                    else 0,
                    format_func=lambda x: {
                        "tips": "💡 Mẹo cưới",
                        "news": "📰 Tin tức",
                        "wedding-story": "💕 Câu chuyện cưới",
                    }[x],
                    key="edit_blog_category",
                )
            with col2:
                edit_published = st.checkbox(
                    "🚀 Xuất bản",
                    value=editing_blog.get("is_published", False),
                    key="edit_blog_published",
                )

            edit_excerpt = st.text_area(
                "📝 Tóm tắt",
                value=editing_blog.get("excerpt", ""),
                height=80,
                key="edit_blog_excerpt",
            )

            # SEO Fields
            with st.expander("🔍 SEO Settings"):
                edit_seo_title = st.text_input(
                    "Meta Title",
                    value=editing_blog.get("seo_title", ""),
                    key="edit_seo_title",
                )
                edit_seo_desc = st.text_area(
                    "Meta Description",
                    value=editing_blog.get("seo_description", ""),
                    height=80,
                    key="edit_seo_desc",
                )
                edit_seo_keywords = st.text_input(
                    "Keywords",
                    value=editing_blog.get("seo_keywords", ""),
                    key="edit_seo_keywords",
                )

            st.markdown("### 📄 Nội dung bài viết")

            # Rich Text Editor cho sửa
            if has_quill:
                edit_content = st_quill(
                    value=editing_blog.get("content", ""),
                    html=True,
                    key="edit_blog_content",
                )
            else:
                edit_content = st.text_area(
                    "Nội dung (HTML)",
                    value=editing_blog.get("content", ""),
                    height=400,
                    key="edit_blog_content_fallback",
                )

            # Ảnh bìa
            st.markdown("### 🖼️ Ảnh bìa")
            if editing_blog.get("image_url"):
                st.image(
                    lay_url_anh(editing_blog["image_url"]),
                    caption="Ảnh hiện tại",
                    width=300,
                )

            edit_img = st.file_uploader(
                "Thay đổi ảnh bìa", type=["jpg", "png", "webp"], key="edit_blog_img"
            )
            if edit_img:
                st.image(edit_img, caption="Ảnh mới", width=300)

            # Buttons
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("❌ HỦY", use_container_width=True):
                    st.session_state.pop("editing_blog", None)
                    st.rerun()
            with col_btn2:
                if st.button(
                    "💾 LƯU THAY ĐỔI", type="primary", use_container_width=True
                ):
                    with st.spinner("Đang lưu..."):
                        img_url = editing_blog.get("image_url", "")
                        if edit_img:
                            uploaded = upload_image(edit_img)
                            if uploaded:
                                img_url = uploaded

                        data = {
                            "title": edit_title,
                            "excerpt": edit_excerpt,
                            "content": edit_content,
                            "image_url": img_url,
                            "category": edit_category,
                            "is_published": edit_published,
                            "seo_title": edit_seo_title,
                            "seo_description": edit_seo_desc,
                            "seo_keywords": edit_seo_keywords,
                        }

                        if call_api(
                            "PUT", f"/api/blog/{editing_blog['id']}", data=data
                        ):
                            st.success("✅ Đã cập nhật bài viết!")
                            st.session_state.pop("editing_blog", None)
                            st.rerun()
        else:
            st.info("👈 Chọn bài viết từ tab 'Danh sách bài viết' để sửa")


def ui_don_hang():
    st.header("🛒 Quản lý Đơn hàng")

    # CSS cho status badges
    st.markdown(
        """
        <style>
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 500;
            display: inline-block;
        }
        .status-pending { background: #FFA50020; color: #FFA500; border: 1px solid #FFA500; }
        .status-processing { background: #3498db20; color: #3498db; border: 1px solid #3498db; }
        .status-shipped { background: #9b59b620; color: #9b59b6; border: 1px solid #9b59b6; }
        .status-delivered { background: #2ecc7120; color: #2ecc71; border: 1px solid #2ecc71; }
        .status-cancelled { background: #e74c3c20; color: #e74c3c; border: 1px solid #e74c3c; }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Nút refresh
    if st.button("🔄 Làm mới danh sách"):
        st.cache_data.clear()
        st.rerun()

    # Lấy danh sách đơn hàng - không cache để luôn lấy dữ liệu mới nhất
    don_hang_list = call_api("GET", "/api/don_hang/", clear_cache=True)

    if not don_hang_list:
        st.info("Chưa có đơn hàng nào.")
        return

    # Thống kê nhanh theo trạng thái
    status_counts = {
        "pending": 0,
        "processing": 0,
        "shipped": 0,
        "delivered": 0,
        "cancelled": 0,
    }
    total_revenue = 0
    for dh in don_hang_list:
        s = dh.get("status", "pending")
        if s in status_counts:
            status_counts[s] += 1
        if s in ["delivered", "shipped"]:
            total_revenue += dh.get("total_amount", 0)

    # Hiển thị thống kê nhanh
    st.markdown("### 📊 Thống kê nhanh")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; background:#FFA50015; border-radius:8px; border:1px solid #FFA50050;">
                <div style="font-size:1.5em; font-weight:bold; color:#FFA500;">{status_counts["pending"]}</div>
                <div style="font-size:0.8em; color:#888;">Chờ xử lý</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; background:#3498db15; border-radius:8px; border:1px solid #3498db50;">
                <div style="font-size:1.5em; font-weight:bold; color:#3498db;">{status_counts["processing"]}</div>
                <div style="font-size:0.8em; color:#888;">Đang xử lý</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; background:#9b59b615; border-radius:8px; border:1px solid #9b59b650;">
                <div style="font-size:1.5em; font-weight:bold; color:#9b59b6;">{status_counts["shipped"]}</div>
                <div style="font-size:0.8em; color:#888;">Đang giao</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; background:#2ecc7115; border-radius:8px; border:1px solid #2ecc7150;">
                <div style="font-size:1.5em; font-weight:bold; color:#2ecc71;">{status_counts["delivered"]}</div>
                <div style="font-size:0.8em; color:#888;">Đã giao</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m5:
        st.markdown(
            f"""
            <div style="text-align:center; padding:10px; background:#e74c3c15; border-radius:8px; border:1px solid #e74c3c50;">
                <div style="font-size:1.5em; font-weight:bold; color:#e74c3c;">{status_counts["cancelled"]}</div>
                <div style="font-size:0.8em; color:#888;">Đã hủy</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Bộ lọc
    col1, col2 = st.columns(2)
    with col1:
        search = st.text_input("🔍 Tìm kiếm", placeholder="Tên, SĐT, email...")
    with col2:
        status_filter = st.selectbox(
            "Trạng thái", ["Tất cả", "Chờ xử lý", "Đang xử lý", "Đã giao", "Đã hủy"]
        )

    # Lọc dữ liệu
    filtered = don_hang_list
    if search:
        filtered = [d for d in filtered if search.lower() in str(d).lower()]
    if status_filter == "Chờ xử lý":
        filtered = [d for d in filtered if d.get("status") == "pending"]
    elif status_filter == "Đang xử lý":
        filtered = [d for d in filtered if d.get("status") == "processing"]
    elif status_filter == "Đã giao":
        filtered = [d for d in filtered if d.get("status") == "delivered"]
    elif status_filter == "Đã hủy":
        filtered = [d for d in filtered if d.get("status") == "cancelled"]

    st.write(f"📦 Tổng: **{len(filtered)}** đơn hàng")

    # PAGINATION
    page_size_orders = st.selectbox(
        "Số đơn hàng/trang", [10, 20, 50], index=1, key="page_size_orders"
    )
    paginated_orders, current_page, total_pages = paginate_list(
        filtered, page_size_orders
    )

    st.text(
        f"Hiển thị {len(paginated_orders)} / {len(filtered)} đơn (Trang {current_page}/{total_pages})"
    )
    show_pagination(current_page, total_pages)
    st.markdown("---")

    # Hiển thị đơn hàng
    for dh in paginated_orders:
        status = dh.get("status", "pending")

        # Status styling
        status_config = {
            "pending": ("🟡", "status-pending", "Chờ xử lý", "#FFA500"),
            "processing": ("🔵", "status-processing", "Đang xử lý", "#3498db"),
            "shipped": ("🟣", "status-shipped", "Đang giao", "#9b59b6"),
            "delivered": ("🟢", "status-delivered", "Đã giao", "#2ecc71"),
            "cancelled": ("🔴", "status-cancelled", "Đã hủy", "#e74c3c"),
        }

        icon, css_class, status_text, color = status_config.get(
            status, ("⚪", "", status, "#888")
        )

        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.write(f"**#{dh.get('id')}** - {dh.get('customer_name')}")
                st.write(
                    f"📞 {dh.get('customer_phone')} | ✉️ {dh.get('customer_email')}"
                )
                st.write(f"📍 {dh.get('shipping_address')}")
            with c2:
                st.write(f"💰 **{dh.get('total_amount', 0):,.0f}đ**")
                # Color-coded status badge
                st.markdown(
                    f"""
                    <span class="status-badge {css_class}">
                        {icon} {status_text}
                    </span>
                """,
                    unsafe_allow_html=True,
                )
                # Ngày đặt
                order_date = dh.get("order_date", "")
                if order_date:
                    st.caption(
                        f"🕐 {order_date[:16] if len(order_date) > 16 else order_date}"
                    )
            with c3:
                new_status = st.selectbox(
                    "Cập nhật",
                    ["pending", "processing", "shipped", "delivered", "cancelled"],
                    index=[
                        "pending",
                        "processing",
                        "shipped",
                        "delivered",
                        "cancelled",
                    ].index(status)
                    if status
                    in ["pending", "processing", "shipped", "delivered", "cancelled"]
                    else 0,
                    key=f"status_{dh['id']}",
                    format_func=lambda x: {
                        "pending": "Chờ xử lý",
                        "processing": "Đang xử lý",
                        "shipped": "Đang giao",
                        "delivered": "Đã giao",
                        "cancelled": "Đã hủy",
                    }.get(x, x),
                    label_visibility="collapsed",
                )
                if new_status != status:
                    if st.button("💾 Lưu", key=f"save_{dh['id']}"):
                        if call_api(
                            "PUT",
                            f"/api/don_hang/{dh['id']}",
                            data={"status": new_status},
                        ):
                            st.toast("Đã cập nhật trạng thái!")
                            st.rerun()

    # Pagination controls ở cuối
    st.markdown("---")
    show_pagination(current_page, total_pages)


# --- Main Layout ---
if "Tổng quan" in choice:
    st.header("📊 Tổng quan Dashboard")

    # Fetch statistics from new API - với cache
    stats = fetch_api_data("/api/thong_ke/tong_quan")
    don_hang_list = fetch_api_data("/api/don_hang/")

    # === METRICS ROW ===
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🛍️ SẢN PHẨM", stats.get("tong_san_pham", 0))
        with c2:
            st.metric("📦 ĐƠN HÀNG", stats.get("tong_don_hang", 0))
        with c3:
            st.metric("👤 NGƯỜI DÙNG", stats.get("tong_nguoi_dung", 0))
        with c4:
            st.metric("📞 LIÊN HỆ MỚI", stats.get("lien_he_chua_xu_ly", 0))

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("💰 DOANH THU", f"{stats.get('tong_doanh_thu', 0):,.0f}đ")
        with c2:
            st.metric("⏳ ĐƠN CHỜ XỬ LÝ", stats.get("don_hang_cho_xu_ly", 0))
    else:
        # Fallback - fetch song song
        data = fetch_multiple_endpoints(["/api/san_pham/", "/api/lien_he/"])
        products = data.get("/api/san_pham/", [])
        contacts = data.get("/api/lien_he/", [])
        c1, c2 = st.columns(2)
        with c1:
            st.metric("TỔNG SẢN PHẨM", len(products) if products else 0)
        with c2:
            st.metric(
                "LIÊN HỆ MỚI",
                len([c for c in (contacts or []) if c.get("status") == "pending"]),
            )

    st.markdown("---")

    # === CHARTS SECTION ===
    st.subheader("📈 Biểu đồ thống kê")

    chart_col1, chart_col2 = st.columns(2)

    # === PIE CHART: TRẠNG THÁI ĐƠN HÀNG ===
    with chart_col1:
        st.markdown("#### 🥧 Trạng thái đơn hàng")

        if don_hang_list:
            # Đếm số lượng theo trạng thái
            status_counts = {
                "pending": 0,
                "processing": 0,
                "shipped": 0,
                "delivered": 0,
                "cancelled": 0,
            }
            for dh in don_hang_list:
                status = dh.get("status", "pending")
                if status in status_counts:
                    status_counts[status] += 1

            # Tạo DataFrame cho pie chart
            status_labels = {
                "pending": "Chờ xử lý",
                "processing": "Đang xử lý",
                "shipped": "Đang giao",
                "delivered": "Đã giao",
                "cancelled": "Đã hủy",
            }

            pie_data = pd.DataFrame(
                {
                    "Trạng thái": [
                        status_labels.get(k, k)
                        for k, v in status_counts.items()
                        if v > 0
                    ],
                    "Số lượng": [v for v in status_counts.values() if v > 0],
                }
            )

            if not pie_data.empty:
                import plotly.express as px

                fig_pie = px.pie(
                    pie_data,
                    values="Số lượng",
                    names="Trạng thái",
                    color="Trạng thái",
                    color_discrete_map={
                        "Chờ xử lý": "#FFA500",
                        "Đang xử lý": "#3498db",
                        "Đang giao": "#9b59b6",
                        "Đã giao": "#2ecc71",
                        "Đã hủy": "#e74c3c",
                    },
                    hole=0.4,
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu đơn hàng")
        else:
            st.info("Chưa có dữ liệu đơn hàng")

    # === BAR CHART: DOANH THU THEO TUẦN ===
    with chart_col2:
        st.markdown("#### 📊 Doanh thu 7 ngày gần nhất")

        if don_hang_list:
            from datetime import datetime, timedelta

            # Tính doanh thu theo ngày (7 ngày gần nhất)
            today = datetime.now()
            revenue_by_day = {}

            for i in range(7):
                day = today - timedelta(days=i)
                day_str = day.strftime("%d/%m")
                revenue_by_day[day_str] = 0

            for dh in don_hang_list:
                if dh.get("status") in ["delivered", "shipped", "processing"]:
                    order_date_str = dh.get("order_date", "")
                    if order_date_str:
                        try:
                            order_date = datetime.fromisoformat(
                                order_date_str.replace("Z", "+00:00")
                            )
                            day_str = order_date.strftime("%d/%m")
                            if day_str in revenue_by_day:
                                revenue_by_day[day_str] += dh.get("total_amount", 0)
                        except:
                            pass

            # Đảo ngược để hiển thị từ cũ đến mới
            bar_data = pd.DataFrame(
                {
                    "Ngày": list(reversed(list(revenue_by_day.keys()))),
                    "Doanh thu": list(reversed(list(revenue_by_day.values()))),
                }
            )

            import plotly.express as px

            fig_bar = px.bar(
                bar_data, x="Ngày", y="Doanh thu", color_discrete_sequence=["#3498db"]
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu doanh thu")

    st.markdown("---")

    # === ĐƠN HÀNG GẦN ĐÂY ===
    st.subheader("🕐 Đơn hàng gần đây")

    if don_hang_list:
        # Lấy 5 đơn hàng mới nhất
        recent_orders = sorted(
            don_hang_list, key=lambda x: x.get("order_date", ""), reverse=True
        )[:5]

        for dh in recent_orders:
            status = dh.get("status", "pending")

            # Color-coded status badges với HTML
            status_styles = {
                "pending": ("🟡", "#FFA500", "Chờ xử lý"),
                "processing": ("🔵", "#3498db", "Đang xử lý"),
                "shipped": ("🟣", "#9b59b6", "Đang giao"),
                "delivered": ("🟢", "#2ecc71", "Đã giao"),
                "cancelled": ("🔴", "#e74c3c", "Đã hủy"),
            }

            icon, color, text = status_styles.get(status, ("⚪", "#888", status))

            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([1, 3, 2, 2])
                with c1:
                    st.write(f"**#{dh.get('id')}**")
                with c2:
                    st.write(f"{dh.get('customer_name', 'N/A')}")
                    st.caption(f"📞 {dh.get('customer_phone', '')}")
                with c3:
                    st.write(f"💰 **{dh.get('total_amount', 0):,.0f}đ**")
                with c4:
                    st.markdown(
                        f"""
                        <span style="
                            background-color: {color}20;
                            color: {color};
                            padding: 4px 12px;
                            border-radius: 12px;
                            font-size: 0.85em;
                            font-weight: 500;
                            border: 1px solid {color};
                        ">{icon} {text}</span>
                    """,
                        unsafe_allow_html=True,
                    )
    else:
        st.info("Chưa có đơn hàng nào")

elif "Liên hệ" in choice:
    ui_lien_he()
elif "Đơn hàng" in choice:
    ui_don_hang()
elif "Tư vấn" in choice:
    ui_tu_van_khach_hang()
elif "Duyệt Đánh Giá" in choice:
    ui_duyet_danh_gia()
elif "Banner" in choice:
    ui_banner()
elif "Sản phẩm" in choice:
    ui_san_pham()
elif "Khách hàng" in choice:
    ui_quan_ly_khach_hang()
elif "Lịch trống" in choice:
    ui_quan_ly_lich_trong()
elif "Yêu thích" in choice:
    ui_thong_ke_yeu_thich()
elif "Đối tác" in choice:
    ui_doi_tac_khieu_nai()
elif "Thư viện" in choice:
    ui_thu_vien()
elif "Dịch vụ" in choice:
    ui_dich_vu_chuyen_gia()
elif "Blog" in choice:
    ui_blog()
elif "Nội dung Trang chủ" in choice:
    st.header("Nội dung Trang chủ")

    tab1, tab2, tab3 = st.tabs(
        ["📖 Câu chuyện IVIE", "⭐ Dịch vụ Cao Cấp", "✨ Điểm nhấn"]
    )

    # === TAB 1: CÂU CHUYỆN IVIE (about_us) ===
    with tab1:
        st.subheader("📖 Quản lý phần Câu chuyện IVIE")

        # Lấy dữ liệu hiện tại
        about_data = call_api("GET", "/api/noi_dung/gioi_thieu", clear_cache=False)

        with st.form("form_about"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("**Ảnh hiện tại:**")
                if about_data and about_data.get("image_url"):
                    st.image(
                        lay_url_anh(about_data["image_url"]), use_container_width=True
                    )
                else:
                    st.info("Chưa có ảnh")

                new_about_img = st.file_uploader(
                    "📷 Tải ảnh mới",
                    type=["jpg", "png", "jpeg", "webp"],
                    key="about_img",
                )
                if new_about_img:
                    st.image(
                        new_about_img, caption="Xem trước", use_container_width=True
                    )

            with col2:
                about_title = st.text_input(
                    "Tiêu đề",
                    value=about_data.get("title", "Câu Chuyện Của IVIE")
                    if about_data
                    else "Câu Chuyện Của IVIE",
                )
                about_subtitle = st.text_input(
                    "Phụ đề",
                    value=about_data.get("subtitle", "Hơn 10 năm kinh nghiệm")
                    if about_data
                    else "Hơn 10 năm kinh nghiệm",
                )
                about_desc = st.text_area(
                    "Mô tả",
                    value=about_data.get("description", "") if about_data else "",
                    height=150,
                )

                st.markdown("**Thống kê:**")
                c1, c2, c3 = st.columns(3)
                with c1:
                    stat1_num = st.text_input(
                        "Số 1",
                        value=about_data.get("stat1_number", "500+")
                        if about_data
                        else "500+",
                    )
                    stat1_label = st.text_input(
                        "Nhãn 1",
                        value=about_data.get("stat1_label", "Cặp Đôi")
                        if about_data
                        else "Cặp Đôi",
                    )
                with c2:
                    stat2_num = st.text_input(
                        "Số 2",
                        value=about_data.get("stat2_number", "10+")
                        if about_data
                        else "10+",
                    )
                    stat2_label = st.text_input(
                        "Nhãn 2",
                        value=about_data.get("stat2_label", "Năm Kinh Nghiệm")
                        if about_data
                        else "Năm Kinh Nghiệm",
                    )
                with c3:
                    stat3_num = st.text_input(
                        "Số 3",
                        value=about_data.get("stat3_number", "100%")
                        if about_data
                        else "100%",
                    )
                    stat3_label = st.text_input(
                        "Nhãn 3",
                        value=about_data.get("stat3_label", "Hài Lòng")
                        if about_data
                        else "Hài Lòng",
                    )

            if st.form_submit_button("💾 LƯU CÂU CHUYỆN", use_container_width=True):
                img_url = about_data.get("image_url", "") if about_data else ""
                if new_about_img:
                    uploaded = upload_image(new_about_img)
                    if uploaded:
                        img_url = uploaded

                update_data = {
                    "title": about_title,
                    "subtitle": about_subtitle,
                    "description": about_desc,
                    "image_url": img_url,
                    "stat1_number": stat1_num,
                    "stat1_label": stat1_label,
                    "stat2_number": stat2_num,
                    "stat2_label": stat2_label,
                    "stat3_number": stat3_num,
                    "stat3_label": stat3_label,
                }

                if call_api("PUT", "/api/noi_dung/gioi_thieu", data=update_data):
                    st.success("✅ Đã cập nhật Câu chuyện IVIE!")
                    st.rerun()

    # === TAB 2: DỊCH VỤ CAO CẤP (home_highlights) ===
    with tab2:
        st.subheader("⭐ Quản lý 3 Dịch vụ Cao Cấp")
        st.caption("3 card dịch vụ hiển thị trên trang chủ")

        # Lấy dữ liệu điểm nhấn
        highlights = call_api("GET", "/api/noi_dung/diem_nhan", clear_cache=False)
        if not highlights:
            highlights = []

        # Đảm bảo có đủ 3 item
        while len(highlights) < 3:
            highlights.append(
                {"id": None, "title": "", "description": "", "image_url": ""}
            )

        service_names = [
            "📷 Nhiếp Ảnh Nghệ Thuật",
            "💄 Trang Điểm Cô Dâu",
            "👗 Váy Cưới Thiết Kế",
        ]

        for idx, (hl, svc_name) in enumerate(zip(highlights[:3], service_names)):
            st.markdown(f"### {svc_name}")
            with st.form(f"form_highlight_{idx}"):
                col1, col2 = st.columns([1, 2])

                with col1:
                    if hl.get("image_url"):
                        st.image(lay_url_anh(hl["image_url"]), use_container_width=True)
                    else:
                        st.info("Chưa có ảnh")

                    new_hl_img = st.file_uploader(
                        f"📷 Tải ảnh mới",
                        type=["jpg", "png", "jpeg", "webp"],
                        key=f"hl_img_{idx}",
                    )
                    if new_hl_img:
                        st.image(
                            new_hl_img, caption="Xem trước", use_container_width=True
                        )

                with col2:
                    hl_title = st.text_input(
                        "Tiêu đề", value=hl.get("title", ""), key=f"hl_title_{idx}"
                    )
                    hl_desc = st.text_area(
                        "Mô tả",
                        value=hl.get("description", ""),
                        key=f"hl_desc_{idx}",
                        height=100,
                    )
                    hl_order = st.number_input(
                        "Thứ tự", value=hl.get("order", idx), key=f"hl_order_{idx}"
                    )

                if st.form_submit_button(
                    f"💾 LƯU DỊCH VỤ {idx + 1}", use_container_width=True
                ):
                    img_url = hl.get("image_url", "")
                    if new_hl_img:
                        uploaded = upload_image(new_hl_img)
                        if uploaded:
                            img_url = uploaded

                    update_data = {
                        "title": hl_title,
                        "description": hl_desc,
                        "image_url": img_url,
                        "order": hl_order,
                    }

                    if hl.get("id"):
                        # Cập nhật
                        if call_api(
                            "PUT",
                            f"/api/noi_dung/diem_nhan/{hl['id']}",
                            data=update_data,
                        ):
                            st.success(f"✅ Đã cập nhật {svc_name}!")
                            st.rerun()
                    else:
                        # Thêm mới
                        if call_api(
                            "POST", "/api/noi_dung/diem_nhan", data=update_data
                        ):
                            st.success(f"✅ Đã thêm {svc_name}!")
                            st.rerun()

            st.markdown("---")

    # === TAB 3: ĐIỂM NHẤN KHÁC ===
    with tab3:
        st.subheader("✨ Quản lý các điểm nhấn khác")
        st.info("Thêm các điểm nhấn bổ sung cho trang chủ")

        with st.form("form_new_highlight"):
            st.markdown("**Thêm điểm nhấn mới:**")
            new_title = st.text_input("Tiêu đề")
            new_desc = st.text_area("Mô tả")
            new_img = st.file_uploader("Ảnh", type=["jpg", "png", "jpeg", "webp"])
            new_order = st.number_input("Thứ tự", value=10)

            if st.form_submit_button("➕ THÊM ĐIỂM NHẤN"):
                img_url = ""
                if new_img:
                    img_url = upload_image(new_img) or ""

                if call_api(
                    "POST",
                    "/api/noi_dung/diem_nhan",
                    data={
                        "title": new_title,
                        "description": new_desc,
                        "image_url": img_url,
                        "order": new_order,
                    },
                ):
                    st.success("✅ Đã thêm điểm nhấn mới!")
                    st.rerun()

        # Danh sách điểm nhấn hiện có
        st.markdown("### Danh sách điểm nhấn")
        all_highlights = call_api("GET", "/api/noi_dung/diem_nhan", clear_cache=False)
        if all_highlights:
            for hl in all_highlights:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([1, 3, 1])
                    with c1:
                        if hl.get("image_url"):
                            st.image(
                                lay_url_anh(hl["image_url"]), use_container_width=True
                            )
                    with c2:
                        st.write(f"**{hl.get('title', 'Không có tiêu đề')}**")
                        st.caption(hl.get("description", ""))
                    with c3:
                        if st.button("🗑️ XÓA", key=f"del_hl_{hl['id']}"):
                            if call_api(
                                "DELETE", f"/api/noi_dung/diem_nhan/{hl['id']}"
                            ):
                                st.success("Đã xóa!")
                                st.rerun()
        else:
            st.info("Chưa có điểm nhấn nào")


# ============ QUẢN LÝ COMBO ============
if choice == "🎁 Quản lý Combo":
    st.header("🎁 Quản lý Combo")

    tab1, tab2 = st.tabs(["DANH SÁCH COMBO", "THÊM/SỬA COMBO"])

    with tab1:
        st.subheader("📋 Danh sách Combo hiện có")
        combos = call_api("GET", "/pg/combo", clear_cache=True)

        if combos:
            for combo in combos:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([1, 3, 1])

                    with col1:
                        if combo.get("hinh_anh"):
                            st.image(
                                lay_url_anh(combo["hinh_anh"]), use_container_width=True
                            )
                        else:
                            st.info("Chưa có ảnh")

                    with col2:
                        st.markdown(f"### {combo.get('ten', 'Không có tên')}")
                        st.write(f"**Giá:** {combo.get('gia', 0):,.0f}đ")
                        st.write(
                            f"**Giới hạn:** {combo.get('gioi_han', 0)} sản phẩm/loại"
                        )
                        st.write(f"**Mô tả:** {combo.get('mo_ta', '')}")

                        # Hiển thị quyền lợi
                        quyen_loi = combo.get("quyen_loi", [])
                        if isinstance(quyen_loi, str):
                            import json

                            try:
                                quyen_loi = json.loads(quyen_loi)
                            except:
                                quyen_loi = []

                        if quyen_loi:
                            st.write("**Quyền lợi:**")
                            for ql in quyen_loi:
                                st.write(f"✓ {ql}")

                        # Badges
                        badges = []
                        if combo.get("noi_bat"):
                            badges.append("🌟 NỔI BẬT")
                        if combo.get("hoat_dong"):
                            badges.append("✅ HOẠT ĐỘNG")
                        else:
                            badges.append("❌ TẠM DỪNG")

                        st.write(" | ".join(badges))

                    with col3:
                        if st.button("✏️ SỬA", key=f"edit_combo_{combo['id']}"):
                            st.session_state["editing_combo"] = combo
                            st.rerun()

                        if st.button("🗑️ XÓA", key=f"del_combo_{combo['id']}"):
                            if call_api("DELETE", f"/pg/combo/{combo['id']}"):
                                st.success("✅ Đã xóa combo!")
                                st.rerun()
        else:
            st.info("Chưa có combo nào. Hãy thêm combo mới!")

    with tab2:
        # Kiểm tra xem có đang sửa combo không
        editing_combo = st.session_state.get("editing_combo", None)

        if editing_combo:
            st.subheader(f"✏️ Sửa Combo: {editing_combo.get('ten', '')}")
        else:
            st.subheader("➕ Thêm Combo Mới")

        with st.form("combo_form"):
            col1, col2 = st.columns(2)

            with col1:
                ten = st.text_input(
                    "Tên Combo *",
                    value=editing_combo.get("ten", "") if editing_combo else "",
                    placeholder="VD: COMBO TIẾT KIỆM",
                )

                gia = st.number_input(
                    "Giá Combo (VNĐ) *",
                    min_value=0,
                    value=int(editing_combo.get("gia", 5000000))
                    if editing_combo
                    else 5000000,
                    step=100000,
                )

                gioi_han = st.number_input(
                    "Giới hạn sản phẩm/loại *",
                    min_value=1,
                    value=editing_combo.get("gioi_han", 5) if editing_combo else 5,
                    step=1,
                    help="Số lượng váy và vest tối đa khách có thể chọn",
                )

            with col2:
                noi_bat = st.checkbox(
                    "🌟 Đánh dấu NỔI BẬT",
                    value=editing_combo.get("noi_bat", False)
                    if editing_combo
                    else False,
                )

                hoat_dong = st.checkbox(
                    "✅ HOẠT ĐỘNG",
                    value=editing_combo.get("hoat_dong", True)
                    if editing_combo
                    else True,
                )

            mo_ta = st.text_area(
                "Mô tả Combo",
                value=editing_combo.get("mo_ta", "") if editing_combo else "",
                placeholder="VD: Sự lựa chọn phổ biến nhất",
                height=80,
            )

            # Quyền lợi
            st.markdown("### 🎁 Quyền lợi của Combo")

            # Lấy quyền lợi hiện tại nếu đang sửa
            current_quyen_loi = []
            if editing_combo:
                quyen_loi_data = editing_combo.get("quyen_loi", [])
                if isinstance(quyen_loi_data, str):
                    import json

                    try:
                        current_quyen_loi = json.loads(quyen_loi_data)
                    except:
                        current_quyen_loi = []
                else:
                    current_quyen_loi = quyen_loi_data

            # Đảm bảo có ít nhất 5 ô input
            while len(current_quyen_loi) < 5:
                current_quyen_loi.append("")

            quyen_loi_list = []
            for i in range(5):
                ql = st.text_input(
                    f"Quyền lợi {i + 1}",
                    value=current_quyen_loi[i] if i < len(current_quyen_loi) else "",
                    placeholder=f"VD: {i + 1} Váy Cưới tùy chọn",
                    key=f"quyen_loi_{i}",
                )
                if ql.strip():
                    quyen_loi_list.append(ql.strip())

            # Hình ảnh
            st.markdown("### 📸 Hình ảnh đại diện Combo")

            if editing_combo and editing_combo.get("hinh_anh"):
                st.image(
                    lay_url_anh(editing_combo["hinh_anh"]),
                    caption="Ảnh hiện tại",
                    width=300,
                )

            img_file = st.file_uploader(
                "Tải ảnh mới", type=["jpg", "png", "jpeg", "webp"]
            )

            if img_file:
                st.image(img_file, caption="Xem trước", width=300)

            # Buttons
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])

            with col_btn2:
                if editing_combo:
                    cancel = st.form_submit_button("❌ HỦY", use_container_width=True)
                    if cancel:
                        st.session_state.pop("editing_combo", None)
                        st.rerun()

            with col_btn3:
                submitted = st.form_submit_button(
                    "💾 LƯU COMBO", use_container_width=True, type="primary"
                )

            if submitted:
                if not ten or not gia or not gioi_han:
                    st.error("⚠️ Vui lòng điền đầy đủ các trường bắt buộc (*)")
                else:
                    with st.spinner("Đang xử lý..."):
                        # Upload ảnh nếu có
                        hinh_anh_url = (
                            editing_combo.get("hinh_anh", "") if editing_combo else ""
                        )
                        if img_file:
                            uploaded = upload_image(img_file)
                            if uploaded:
                                hinh_anh_url = uploaded

                        # Chuẩn bị dữ liệu
                        import json

                        combo_data = {
                            "ten": ten,
                            "gia": gia,
                            "gioi_han": gioi_han,
                            "mo_ta": mo_ta,
                            "quyen_loi": quyen_loi_list,
                            "hinh_anh": hinh_anh_url,
                            "noi_bat": noi_bat,
                            "hoat_dong": hoat_dong,
                        }

                        if editing_combo:
                            # Cập nhật
                            if call_api(
                                "PUT",
                                f"/pg/combo/{editing_combo['id']}",
                                data=combo_data,
                            ):
                                st.success("✅ Đã cập nhật combo!")
                                st.session_state.pop("editing_combo", None)
                                st.rerun()
                        else:
                            # Thêm mới
                            if call_api("POST", "/pg/combo", data=combo_data):
                                st.success("✅ Đã thêm combo mới!")
                                st.rerun()
