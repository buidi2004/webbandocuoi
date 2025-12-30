"""
Module xác thực và phân quyền cho IVIE Wedding Admin
"""
import bcrypt
import streamlit as st

# Dữ liệu người dùng (hardcoded)
# Password hashes được tạo bằng bcrypt
USERS = {
    "ceo": {
        "password_hash": "$2b$12$A/EYGItuXo9FojOoG/Km3.mgArpw87G1DlJPVGJ555LhgO6XLCYAO",  # 123456
        "role": "CEO",
        "full_name": "Giám đốc điều hành",
        "permissions": ["all"]  # Có tất cả quyền
    },
    "nhanvien": {
        "password_hash": "$2b$12$/EccbPLpIX4jhSX5Go7S.OFhZpRp3Nsl2YHIjS4OUDBZYx4k9EgWa",  # 12345
        "role": "Nhân viên",
        "full_name": "Nhân viên",
        "permissions": [
            "dashboard",
            "orders",
            "contacts",
            "consultations",
            "banners",
            "combo",
            "partners",
            "gallery",
            "experts",
            "blog",
            "homepage"
        ]  # Không có "products" và "reviews"
    }
}

# Mapping menu items với permissions
MENU_PERMISSIONS = {
    "📊 Tổng quan": "dashboard",
    "🛒 Quản lý Đơn hàng": "orders",
    "📞 Liên hệ khách hàng": "contacts",
    "💬 Tư vấn khách hàng": "consultations",
    "⏳ Duyệt Đánh Giá": "reviews",  # Nhân viên KHÔNG có
    "🖼️ Quản lý Banner": "banners",
    "👗 Quản lý Sản phẩm": "products",  # Nhân viên KHÔNG có
    "🎁 Quản lý Combo": "combo",
    "🤝 Đối tác & Khiếu nại": "partners",
    "📁 Thư viện ảnh mẫu": "gallery",
    "✨ Dịch vụ Chuyên gia": "experts",
    "📰 Blog & Tin tức": "blog",
    "🏠 Nội dung Trang chủ": "homepage"
}


def hash_password(password: str) -> str:
    """
    Hash password bằng bcrypt (chỉ dùng để tạo hash ban đầu)
    
    Args:
        password: Mật khẩu plain text
        
    Returns:
        Password hash dạng string
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def authenticate(username: str, password: str) -> dict | None:
    """
    Xác thực người dùng
    
    Args:
        username: Tên đăng nhập
        password: Mật khẩu plain text
        
    Returns:
        User dict nếu thành công, None nếu thất bại
    """
    if not username or not password:
        return None
    
    if username not in USERS:
        return None
    
    user = USERS[username]
    
    # Verify password với bcrypt
    try:
        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return {
                "username": username,
                "role": user["role"],
                "full_name": user["full_name"],
                "permissions": user["permissions"]
            }
    except Exception:
        return None
    
    return None


def init_session():
    """Khởi tạo session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None


def login(user_data: dict):
    """
    Đăng nhập và lưu session
    
    Args:
        user_data: Dictionary chứa thông tin user
    """
    st.session_state.authenticated = True
    st.session_state.user = user_data


def logout():
    """Đăng xuất và xóa session"""
    st.session_state.authenticated = False
    st.session_state.user = None


def is_authenticated() -> bool:
    """
    Kiểm tra đã đăng nhập chưa
    
    Returns:
        True nếu đã đăng nhập, False nếu chưa
    """
    return st.session_state.get("authenticated", False)


def get_current_user() -> dict | None:
    """
    Lấy thông tin user hiện tại
    
    Returns:
        User dict hoặc None nếu chưa đăng nhập
    """
    return st.session_state.get("user", None)


def has_permission(permission: str) -> bool:
    """
    Kiểm tra user có quyền không
    
    Args:
        permission: Tên quyền cần kiểm tra
        
    Returns:
        True nếu có quyền, False nếu không
    """
    user = get_current_user()
    if not user:
        return False
    
    # CEO có tất cả quyền
    if "all" in user["permissions"]:
        return True
    
    return permission in user["permissions"]


def get_allowed_menu_items() -> list:
    """
    Lấy danh sách menu items mà user được phép truy cập
    
    Returns:
        List các menu items
    """
    user = get_current_user()
    if not user:
        return []
    
    # CEO thấy tất cả
    if "all" in user["permissions"]:
        return list(MENU_PERMISSIONS.keys())
    
    # Nhân viên chỉ thấy menu có quyền
    allowed = []
    for menu_item, permission in MENU_PERMISSIONS.items():
        if permission in user["permissions"]:
            allowed.append(menu_item)
    
    return allowed


def show_login_page():
    """Hiển thị trang đăng nhập"""
    st.markdown("""
        <div style='text-align: center; padding: 50px 0 30px 0;'>
            <h1 style='font-size: 3em; margin-bottom: 10px;'>🏯 IVIE WEDDING STUDIO</h1>
            <h3 style='font-weight: 300; color: #999;'>Hệ thống quản trị</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Đăng nhập")
            username = st.text_input("Tên đăng nhập", placeholder="Nhập username")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập password")
            submit = st.form_submit_button("ĐĂNG NHẬP", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("⚠️ Vui lòng nhập đầy đủ thông tin")
                else:
                    user_data = authenticate(username, password)
                    if user_data:
                        login(user_data)
                        st.success(f"✅ Đăng nhập thành công! Xin chào {user_data['full_name']}")
                        st.rerun()
                    else:
                        st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng")


def show_user_info_sidebar():
    """Hiển thị thông tin user trong sidebar"""
    user = get_current_user()
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 {user['full_name']}**")
        st.sidebar.markdown(f"*Vai trò: {user['role']}*")
        st.sidebar.markdown(f"*Username: {user['username']}*")
        
        if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
            logout()
            st.rerun()


def require_permission(permission: str, error_message: str = None):
    """
    Decorator/helper để kiểm tra quyền trước khi hiển thị nội dung
    
    Args:
        permission: Quyền cần kiểm tra
        error_message: Thông báo lỗi tùy chỉnh
        
    Returns:
        True nếu có quyền, False và hiển thị error nếu không
    """
    if not has_permission(permission):
        if error_message is None:
            error_message = f"⛔ Bạn không có quyền truy cập chức năng này. Vui lòng liên hệ quản trị viên."
        st.error(error_message)
        return False
    return True
