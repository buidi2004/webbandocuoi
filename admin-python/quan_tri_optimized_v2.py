"""
IVIE Wedding Admin - Optimized Version v2
Tối ưu hiệu năng với lazy module loading và code splitting
"""

import functools
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# ============================================================
# CRITICAL: Set page config FIRST before any other st commands
# ============================================================
st.set_page_config(
    page_title="IVIE Wedding Admin",
    layout="wide",
    page_icon="🏯",
    initial_sidebar_state="expanded",
)

# ============================================================
# FAST LOADING INDICATOR - Show immediately for FCP
# ============================================================
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

# Load environment
load_dotenv()

# ============================================================
# LAZY IMPORT HELPER
# ============================================================


@st.cache_resource(show_spinner=False)
def lazy_import_auth():
    """Lazy import auth module - cached"""
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

        return {
            "MENU_PERMISSIONS": MENU_PERMISSIONS,
            "get_allowed_menu_items": get_allowed_menu_items,
            "has_permission": has_permission,
            "init_session": init_session,
            "is_authenticated": is_authenticated,
            "show_login_page": show_login_page,
            "show_user_info_sidebar": show_user_info_sidebar,
        }
    except ImportError as e:
        st.error(f"❌ Lỗi import auth module: {e}")
        st.stop()


@st.cache_resource(show_spinner=False)
def lazy_import_api_client():
    """Lazy import API client module - cached"""
    try:
        from modules.api_client import (
            API_URL,
            call_api,
            fetch_api_data,
            fetch_banners_cached,
            fetch_blog_cached,
            fetch_combos_cached,
            fetch_contacts_cached,
            fetch_dashboard_stats,
            fetch_gallery_cached,
            fetch_multiple_endpoints,
            fetch_orders_cached,
            fetch_products_cached,
            fetch_reviews_cached,
            fetch_users_cached,
            get_image_placeholder,
            get_session,
            invalidate_cache,
            lay_url_anh,
            upload_image,
            upload_images_parallel,
            wake_up_backend,
        )

        return {
            "API_URL": API_URL,
            "call_api": call_api,
            "fetch_api_data": fetch_api_data,
            "fetch_banners_cached": fetch_banners_cached,
            "fetch_blog_cached": fetch_blog_cached,
            "fetch_combos_cached": fetch_combos_cached,
            "fetch_contacts_cached": fetch_contacts_cached,
            "fetch_dashboard_stats": fetch_dashboard_stats,
            "fetch_gallery_cached": fetch_gallery_cached,
            "fetch_multiple_endpoints": fetch_multiple_endpoints,
            "fetch_orders_cached": fetch_orders_cached,
            "fetch_products_cached": fetch_products_cached,
            "fetch_reviews_cached": fetch_reviews_cached,
            "fetch_users_cached": fetch_users_cached,
            "get_image_placeholder": get_image_placeholder,
            "get_session": get_session,
            "invalidate_cache": invalidate_cache,
            "lay_url_anh": lay_url_anh,
            "upload_image": upload_image,
            "upload_images_parallel": upload_images_parallel,
            "wake_up_backend": wake_up_backend,
        }
    except ImportError as e:
        st.error(f"❌ Lỗi import API client module: {e}")
        st.stop()


@st.cache_resource(show_spinner=False)
def lazy_import_utils():
    """Lazy import utils module - cached"""
    try:
        from modules.utils import (
            dataframe_to_excel,
            filter_by_date_range,
            filter_by_search,
            filter_by_status,
            format_currency,
            format_date,
            format_datetime,
            get_priority_badge,
            get_status_badge,
            is_valid_email,
            is_valid_phone,
            is_valid_url,
            list_to_dataframe,
            paginate_list,
            show_pagination,
            sort_items,
            truncate_text,
        )

        return {
            "dataframe_to_excel": dataframe_to_excel,
            "filter_by_date_range": filter_by_date_range,
            "filter_by_search": filter_by_search,
            "filter_by_status": filter_by_status,
            "format_currency": format_currency,
            "format_date": format_date,
            "format_datetime": format_datetime,
            "get_priority_badge": get_priority_badge,
            "get_status_badge": get_status_badge,
            "is_valid_email": is_valid_email,
            "is_valid_phone": is_valid_phone,
            "is_valid_url": is_valid_url,
            "list_to_dataframe": list_to_dataframe,
            "paginate_list": paginate_list,
            "show_pagination": show_pagination,
            "sort_items": sort_items,
            "truncate_text": truncate_text,
        }
    except ImportError as e:
        st.error(f"❌ Lỗi import utils module: {e}")
        st.stop()


# ============================================================
# LAZY UI MODULE LOADERS
# ============================================================


def lazy_load_ui_module(module_name: str):
    """
    Dynamically load UI module on demand
    Chỉ import khi thực sự cần sử dụng
    """
    key = f"ui_module_{module_name}"

    if key not in st.session_state:
        try:
            # Dynamic import based on module name
            if module_name == "products":
                from quan_tri import ui_san_pham

                st.session_state[key] = ui_san_pham
            elif module_name == "orders":
                from quan_tri import ui_don_hang

                st.session_state[key] = ui_don_hang
            elif module_name == "contacts":
                from quan_tri import ui_lien_he

                st.session_state[key] = ui_lien_he
            elif module_name == "reviews":
                from quan_tri import ui_duyet_danh_gia

                st.session_state[key] = ui_duyet_danh_gia
            elif module_name == "banners":
                from quan_tri import ui_banner

                st.session_state[key] = ui_banner
            elif module_name == "customers":
                from quan_tri import ui_quan_ly_khach_hang

                st.session_state[key] = ui_quan_ly_khach_hang
            elif module_name == "calendar":
                from quan_tri import ui_quan_ly_lich_trong

                st.session_state[key] = ui_quan_ly_lich_trong
            elif module_name == "favorites":
                from quan_tri import ui_thong_ke_yeu_thich

                st.session_state[key] = ui_thong_ke_yeu_thich
            elif module_name == "gallery":
                from quan_tri import ui_thu_vien

                st.session_state[key] = ui_thu_vien
            elif module_name == "services":
                from quan_tri import ui_dich_vu_chuyen_gia

                st.session_state[key] = ui_dich_vu_chuyen_gia
            elif module_name == "chat":
                from quan_tri import ui_tu_van_khach_hang

                st.session_state[key] = ui_tu_van_khach_hang
            elif module_name == "partners":
                from quan_tri import ui_doi_tac_khieu_nai

                st.session_state[key] = ui_doi_tac_khieu_nai
            elif module_name == "blog":
                from quan_tri import ui_blog

                st.session_state[key] = ui_blog
            elif module_name == "combos":
                # Import combo UI from main file
                # Note: This is an inline function in quan_tri.py
                # We'll import and wrap it
                import sys

                sys.path.insert(0, os.path.dirname(__file__))

                # Import the main quan_tri to get combo functionality
                def ui_combo_wrapper():
                    # Import inline to avoid loading everything
                    import importlib.util

                    spec = importlib.util.spec_from_file_location(
                        "quan_tri_combo",
                        os.path.join(os.path.dirname(__file__), "quan_tri.py"),
                    )
                    if spec and spec.loader:
                        # Just execute the combo section
                        # Since it's inline, we need to provide the full context
                        st.header("🎁 Quản lý Combo")

                        # Import necessary functions from main file
                        from quan_tri import call_api, lay_url_anh, upload_image

                        tab1, tab2 = st.tabs(["DANH SÁCH COMBO", "THÊM/SỬA COMBO"])

                        with tab1:
                            st.subheader("📋 Danh sách Combo hiện có")
                            combos = call_api("GET", "/pg/combo", clear_cache=True)

                            if combos:
                                for combo in combos:
                                    with st.container(border=True):
                                        col1, col2, col3 = st.columns([1, 3, 1])

                                        with col1:
                                            if combo.get("anh"):
                                                st.image(
                                                    lay_url_anh(combo["anh"]), width=120
                                                )

                                        with col2:
                                            st.markdown(
                                                f"### {combo.get('ten', 'N/A')}"
                                            )
                                            st.write(
                                                f"**Giá:** {combo.get('gia', 0):,.0f} đ"
                                            )
                                            st.write(
                                                f"**Mô tả:** {combo.get('mo_ta', 'N/A')}"
                                            )

                                        with col3:
                                            if st.button(
                                                "🗑️ Xóa",
                                                key=f"del_combo_{combo.get('id')}",
                                            ):
                                                if call_api(
                                                    "DELETE", f"/pg/combo/{combo['id']}"
                                                ):
                                                    st.success("✅ Đã xóa combo")
                                                    st.rerun()
                            else:
                                st.info("Chưa có combo nào")

                        with tab2:
                            with st.form("form_combo"):
                                ten = st.text_input("Tên combo")
                                gia = st.number_input(
                                    "Giá (VNĐ)", min_value=0, step=100000
                                )
                                mo_ta = st.text_area("Mô tả")
                                anh_file = st.file_uploader(
                                    "Ảnh combo", type=["jpg", "png", "jpeg"]
                                )

                                if st.form_submit_button("💾 LƯU COMBO"):
                                    anh_url = (
                                        upload_image(anh_file) if anh_file else None
                                    )

                                    data = {
                                        "ten": ten,
                                        "gia": gia,
                                        "mo_ta": mo_ta,
                                        "anh": anh_url,
                                    }

                                    if call_api("POST", "/pg/combo", data=data):
                                        st.success("✅ Đã tạo combo")
                                        st.rerun()

                st.session_state[key] = ui_combo_wrapper

            elif module_name == "homepage":
                # Import homepage UI from main file
                def ui_homepage_wrapper():
                    from quan_tri import call_api, lay_url_anh, upload_image

                    st.header("📝 Nội dung Trang chủ")

                    tab1, tab2, tab3 = st.tabs(
                        ["📖 Câu chuyện IVIE", "⭐ Dịch vụ Cao Cấp", "✨ Điểm nhấn"]
                    )

                    with tab1:
                        st.subheader("📖 Quản lý phần Câu chuyện IVIE")

                        # Fetch current content
                        about = call_api("GET", "/pg/noi_dung_trang_chu/about_us")

                        with st.form("form_about"):
                            tieu_de = st.text_input(
                                "Tiêu đề",
                                value=about.get("tieu_de", "") if about else "",
                            )
                            noi_dung = st.text_area(
                                "Nội dung",
                                value=about.get("noi_dung", "") if about else "",
                                height=200,
                            )
                            anh_file = st.file_uploader(
                                "Ảnh", type=["jpg", "png", "jpeg"]
                            )

                            if st.form_submit_button("💾 CẬP NHẬT"):
                                anh_url = (
                                    upload_image(anh_file)
                                    if anh_file
                                    else (about.get("anh") if about else None)
                                )

                                data = {
                                    "loai": "about_us",
                                    "tieu_de": tieu_de,
                                    "noi_dung": noi_dung,
                                    "anh": anh_url,
                                }

                                if call_api(
                                    "POST", "/pg/noi_dung_trang_chu", data=data
                                ):
                                    st.success("✅ Đã cập nhật")
                                    st.rerun()

                    with tab2:
                        st.subheader("⭐ Dịch vụ Cao Cấp")
                        st.info("Quản lý các dịch vụ premium")

                    with tab3:
                        st.subheader("✨ Điểm nhấn")
                        st.info("Quản lý các highlights")

                st.session_state[key] = ui_homepage_wrapper
            else:
                st.error(f"❌ Module không tồn tại: {module_name}")
                return None
        except Exception as e:
            st.error(f"❌ Lỗi load module {module_name}: {e}")
            return None

    return st.session_state.get(key)


# ============================================================
# IMPORT CORE MODULES
# ============================================================

# Import auth
auth = lazy_import_auth()
init_session = auth["init_session"]
is_authenticated = auth["is_authenticated"]
show_login_page = auth["show_login_page"]
show_user_info_sidebar = auth["show_user_info_sidebar"]
get_allowed_menu_items = auth["get_allowed_menu_items"]
has_permission = auth["has_permission"]

# Import API client
api = lazy_import_api_client()
API_URL = api["API_URL"]
call_api = api["call_api"]
fetch_api_data = api["fetch_api_data"]
fetch_dashboard_stats = api["fetch_dashboard_stats"]
fetch_orders_cached = api["fetch_orders_cached"]
fetch_products_cached = api["fetch_products_cached"]
fetch_contacts_cached = api["fetch_contacts_cached"]
invalidate_cache = api["invalidate_cache"]
lay_url_anh = api["lay_url_anh"]
upload_image = api["upload_image"]

# Import utils
utils = lazy_import_utils()
paginate_list = utils["paginate_list"]
show_pagination = utils["show_pagination"]
format_currency = utils["format_currency"]
format_date = utils["format_date"]
get_status_badge = utils["get_status_badge"]

# Clear loading placeholder
loading_placeholder.empty()

# ============================================================
# SESSION INITIALIZATION
# ============================================================
init_session()

# Check authentication
if not is_authenticated():
    show_login_page()
    st.stop()

# Show backend wake notice once
if "shown_wake_notice" not in st.session_state:
    st.session_state.shown_wake_notice = True
    st.info(
        "💡 Lưu ý: Nếu đây là lần đầu truy cập sau một thời gian, server có thể mất 30-60 giây để khởi động (Render free tier)."
    )

# ============================================================
# CUSTOM CSS - Dark Theme
# ============================================================
st.markdown(
    """
    <style>
    /* Dark minimalist theme */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }

    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2em;
        font-weight: 700;
    }

    /* Cards */
    .element-container {
        background: #111;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 10px;
        margin: 5px 0;
    }

    /* Buttons */
    .stButton > button {
        background: #ffffff;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: #e0e0e0;
        transform: translateY(-2px);
    }

    /* Tables */
    .dataframe {
        background: #0a0a0a !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 4px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0a0a;
        border-right: 1px solid #222;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Improve performance */
    .stMarkdown {
        will-change: transform;
    }

    /* Loading optimizations */
    img {
        loading: lazy;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR MENU
# ============================================================
with st.sidebar:
    st.markdown("# 🏯 IVIE WEDDING")
    st.markdown("### Admin Dashboard")
    st.markdown("---")

    # Show user info
    show_user_info_sidebar()

    st.markdown("---")

    # Get allowed menu items based on permissions
    menu_items = get_allowed_menu_items()

    # Radio button for navigation
    choice = st.radio(
        "📋 Menu chính",
        menu_items,
        key="main_menu",
    )

    st.markdown("---")
    st.markdown(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ============================================================
# MAIN CONTENT AREA - Lazy Loading
# ============================================================

# Dashboard - Always loaded (most important)
if "Tổng quan" in choice:
    st.header("📊 Tổng quan Dashboard")

    # Fetch statistics with cache
    with st.spinner("Đang tải dữ liệu..."):
        stats = fetch_dashboard_stats()
        don_hang_list = fetch_orders_cached()

    # Metrics Row
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
            st.metric("💰 DOANH THU", format_currency(stats.get("tong_doanh_thu", 0)))
        with c2:
            st.metric("⏳ ĐƠN CHỜ XỬ LÝ", stats.get("don_hang_cho_xu_ly", 0))
    else:
        st.warning("⚠️ Không thể tải thống kê. Server có thể đang khởi động...")

    st.markdown("---")

    # Charts Section
    st.subheader("📈 Biểu đồ thống kê")

    if don_hang_list:
        import pandas as pd
        import plotly.express as px

        chart_col1, chart_col2 = st.columns(2)

        # Pie Chart: Order Status
        with chart_col1:
            st.markdown("#### 🥧 Trạng thái đơn hàng")

            # Count by status
            status_counts = {}
            for dh in don_hang_list:
                status = dh.get("trang_thai", "Chờ xác nhận")
                status_counts[status] = status_counts.get(status, 0) + 1

            if status_counts:
                pie_data = pd.DataFrame(
                    {
                        "Trạng thái": list(status_counts.keys()),
                        "Số lượng": list(status_counts.values()),
                    }
                )

                fig_pie = px.pie(
                    pie_data,
                    values="Số lượng",
                    names="Trạng thái",
                    hole=0.4,
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    showlegend=True,
                    height=350,
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # Bar Chart: Recent Orders
        with chart_col2:
            st.markdown("#### 📊 Đơn hàng gần đây (7 ngày)")

            # Get recent orders
            from datetime import timedelta

            now = datetime.now()
            week_ago = now - timedelta(days=7)

            recent_orders = []
            for dh in don_hang_list:
                try:
                    ngay_tao = datetime.fromisoformat(
                        dh.get("ngay_tao", "").replace("Z", "+00:00")
                    )
                    if ngay_tao >= week_ago:
                        recent_orders.append(dh)
                except Exception:
                    pass

            if recent_orders:
                # Count by date
                date_counts = {}
                for dh in recent_orders:
                    try:
                        ngay_tao = datetime.fromisoformat(
                            dh.get("ngay_tao", "").replace("Z", "+00:00")
                        )
                        date_str = ngay_tao.strftime("%d/%m")
                        date_counts[date_str] = date_counts.get(date_str, 0) + 1
                    except Exception:
                        pass

                if date_counts:
                    bar_data = pd.DataFrame(
                        {
                            "Ngày": list(date_counts.keys()),
                            "Số đơn": list(date_counts.values()),
                        }
                    )

                    fig_bar = px.bar(
                        bar_data,
                        x="Ngày",
                        y="Số đơn",
                        text="Số đơn",
                    )
                    fig_bar.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                        height=350,
                        showlegend=False,
                    )
                    fig_bar.update_traces(
                        marker_color="#3498db", textposition="outside"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Không có đơn hàng mới trong 7 ngày qua")

    # Recent Activity Section
    st.markdown("---")
    st.subheader("🕒 Hoạt động gần đây")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📦 Đơn hàng mới nhất")
        if don_hang_list:
            recent = sorted(
                don_hang_list, key=lambda x: x.get("ngay_tao", ""), reverse=True
            )[:5]
            for dh in recent:
                with st.expander(
                    f"Đơn #{dh.get('id', 'N/A')} - {dh.get('ten_khach_hang', 'N/A')}"
                ):
                    st.write(
                        f"**Tổng tiền:** {format_currency(dh.get('tong_tien', 0))}"
                    )
                    st.write(f"**Trạng thái:** {dh.get('trang_thai', 'N/A')}")
                    st.write(f"**Ngày tạo:** {format_date(dh.get('ngay_tao', ''))}")

    with col2:
        st.markdown("#### 📞 Liên hệ mới nhất")
        contacts = fetch_contacts_cached()
        if contacts:
            recent = sorted(
                contacts, key=lambda x: x.get("ngay_tao", ""), reverse=True
            )[:5]
            for ct in recent:
                with st.expander(f"{ct.get('ten', 'N/A')} - {ct.get('email', 'N/A')}"):
                    st.write(f"**SĐT:** {ct.get('so_dien_thoai', 'N/A')}")
                    st.write(f"**Nội dung:** {ct.get('noi_dung', 'N/A')[:100]}...")
                    st.write(f"**Trạng thái:** {ct.get('trang_thai', 'N/A')}")

# Lazy load other modules
elif "Sản phẩm" in choice:
    ui_func = lazy_load_ui_module("products")
    if ui_func:
        ui_func()

elif "Đơn hàng" in choice:
    ui_func = lazy_load_ui_module("orders")
    if ui_func:
        ui_func()

elif "Liên hệ" in choice:
    ui_func = lazy_load_ui_module("contacts")
    if ui_func:
        ui_func()

elif "Đánh giá" in choice:
    ui_func = lazy_load_ui_module("reviews")
    if ui_func:
        ui_func()

elif "Banner" in choice:
    ui_func = lazy_load_ui_module("banners")
    if ui_func:
        ui_func()

elif "Khách hàng" in choice:
    ui_func = lazy_load_ui_module("customers")
    if ui_func:
        ui_func()

elif "Lịch trống" in choice:
    ui_func = lazy_load_ui_module("calendar")
    if ui_func:
        ui_func()

elif "Yêu thích" in choice:
    ui_func = lazy_load_ui_module("favorites")
    if ui_func:
        ui_func()

elif "Thư viện" in choice:
    ui_func = lazy_load_ui_module("gallery")
    if ui_func:
        ui_func()

elif "Dịch vụ" in choice:
    ui_func = lazy_load_ui_module("services")
    if ui_func:
        ui_func()

elif "Chat" in choice:
    ui_func = lazy_load_ui_module("chat")
    if ui_func:
        ui_func()

elif "Đối tác" in choice:
    ui_func = lazy_load_ui_module("partners")
    if ui_func:
        ui_func()

elif "Blog" in choice:
    ui_func = lazy_load_ui_module("blog")
    if ui_func:
        ui_func()

elif "Combo" in choice:
    ui_func = lazy_load_ui_module("combos")
    if ui_func:
        ui_func()

elif "Nội dung" in choice:
    ui_func = lazy_load_ui_module("homepage")
    if ui_func:
        ui_func()

else:
    st.info("🚧 Module đang phát triển...")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.85em; padding: 20px 0;'>
        <p>🏯 IVIE Wedding Studio Admin v2.0 (Optimized)</p>
        <p>Powered by Streamlit | © 2024</p>
    </div>
    """,
    unsafe_allow_html=True,
)
