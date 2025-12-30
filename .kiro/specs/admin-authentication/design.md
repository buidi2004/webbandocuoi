# Design Document - Hệ Thống Xác Thực và Phân Quyền Admin

## Overview

Hệ thống xác thực và phân quyền cho trang quản trị IVIE Wedding Studio sử dụng Streamlit session state để quản lý phiên đăng nhập và bcrypt để mã hóa mật khẩu. Hệ thống hỗ trợ 2 vai trò: CEO (full quyền) và Nhân viên (quyền hạn chế).

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Login Page     │
│  (Streamlit)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Authentication │
│  Module         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Session        │◄─────┤  User Data   │
│  Management     │      │  (In-memory) │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐
│  Authorization  │
│  Check          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Admin Pages    │
│  (Conditional)  │
└─────────────────┘
```

### Component Flow

1. **Login Page**: Form đăng nhập với username/password
2. **Authentication Module**: Xác thực credentials với bcrypt
3. **Session Management**: Lưu trữ user info trong `st.session_state`
4. **Authorization Check**: Kiểm tra quyền truy cập trước khi hiển thị chức năng
5. **Admin Pages**: Hiển thị các trang quản trị dựa trên quyền

## Components and Interfaces

### 1. User Data Store

```python
# Cấu trúc dữ liệu người dùng (hardcoded)
USERS = {
    "ceo": {
        "password_hash": "<bcrypt_hash_of_123456>",
        "role": "CEO",
        "full_name": "Giám đốc điều hành",
        "permissions": ["all"]  # Có tất cả quyền
    },
    "nhanvien": {
        "password_hash": "<bcrypt_hash_of_12345>",
        "role": "Nhân viên",
        "full_name": "Nhân viên",
        "permissions": [
            "dashboard",
            "orders",
            "combo",
            "experts",
            "stats"
        ]  # Không có "products" và "reviews"
    }
}
```

### 2. Authentication Module

```python
def authenticate(username: str, password: str) -> dict | None:
    """
    Xác thực người dùng
    
    Args:
        username: Tên đăng nhập
        password: Mật khẩu plain text
        
    Returns:
        User dict nếu thành công, None nếu thất bại
    """
    if username not in USERS:
        return None
    
    user = USERS[username]
    if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return {
            "username": username,
            "role": user["role"],
            "full_name": user["full_name"],
            "permissions": user["permissions"]
        }
    return None
```

### 3. Session Management

```python
# Sử dụng Streamlit session state
def init_session():
    """Khởi tạo session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None

def login(user_data: dict):
    """Đăng nhập và lưu session"""
    st.session_state.authenticated = True
    st.session_state.user = user_data

def logout():
    """Đăng xuất và xóa session"""
    st.session_state.authenticated = False
    st.session_state.user = None

def is_authenticated() -> bool:
    """Kiểm tra đã đăng nhập chưa"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> dict | None:
    """Lấy thông tin user hiện tại"""
    return st.session_state.get("user", None)
```

### 4. Authorization Module

```python
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
```

### 5. Login UI Component

```python
def show_login_page():
    """Hiển thị trang đăng nhập"""
    st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1>🏯 IVIE WEDDING STUDIO</h1>
            <h3>Hệ thống quản trị</h3>
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
```

### 6. User Info Display

```python
def show_user_info_sidebar():
    """Hiển thị thông tin user trong sidebar"""
    user = get_current_user()
    if user:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 {user['full_name']}**")
        st.sidebar.markdown(f"*Vai trò: {user['role']}*")
        
        if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
            logout()
            st.rerun()
```

## Data Models

### User Model

```python
class User:
    username: str          # Tên đăng nhập (unique)
    password_hash: str     # Mật khẩu đã hash bằng bcrypt
    role: str             # "CEO" hoặc "Nhân viên"
    full_name: str        # Tên đầy đủ hiển thị
    permissions: list[str] # Danh sách quyền ["all"] hoặc ["dashboard", "orders", ...]
```

### Session State Model

```python
st.session_state = {
    "authenticated": bool,  # True nếu đã đăng nhập
    "user": {              # None nếu chưa đăng nhập
        "username": str,
        "role": str,
        "full_name": str,
        "permissions": list[str]
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Authentication Success Requires Valid Credentials

*For any* username and password combination, authentication should succeed if and only if the username exists in USERS and the password matches the stored hash.

**Validates: Requirements 1.2, 1.3**

### Property 2: CEO Has All Permissions

*For any* permission check, if the current user has role "CEO", the permission check should always return True.

**Validates: Requirements 2.1, 2.2**

### Property 3: Nhân viên Cannot Access Restricted Functions

*For any* user with role "Nhân viên", permission checks for "products" and "reviews" should always return False.

**Validates: Requirements 3.2, 3.3**

### Property 4: Session Persistence Across Page Navigation

*For any* authenticated user, navigating between pages should maintain the session state with the same user information.

**Validates: Requirements 4.2**

### Property 5: Logout Clears Session

*For any* authenticated user, calling logout should set authenticated to False and user to None.

**Validates: Requirements 4.4**

### Property 6: Unauthenticated Access Redirects to Login

*For any* unauthenticated user attempting to access admin functions, the system should display the login page instead.

**Validates: Requirements 4.5**

### Property 7: Password Hash Verification

*For any* stored password hash, it should be verifiable using bcrypt.checkpw with the correct plain-text password.

**Validates: Requirements 5.1, 5.2**

### Property 8: Menu Visibility Based on Permissions

*For any* user, the menu items displayed should exactly match the set of items for which the user has permissions.

**Validates: Requirements 3.5**

## Error Handling

### Authentication Errors

- **Invalid credentials**: Hiển thị thông báo lỗi "Tên đăng nhập hoặc mật khẩu không đúng" (không tiết lộ username hay password sai)
- **Empty fields**: Hiển thị "Vui lòng nhập đầy đủ thông tin"
- **Network errors**: Không áp dụng (authentication local)

### Authorization Errors

- **Unauthorized access**: Ẩn menu items không có quyền
- **Direct URL access**: Hiển thị thông báo "Bạn không có quyền truy cập chức năng này"

### Session Errors

- **Session expired**: Tự động redirect về login page
- **Invalid session data**: Clear session và redirect về login

## Testing Strategy

### Unit Tests

1. **Test authenticate function**:
   - Valid credentials → return user data
   - Invalid username → return None
   - Invalid password → return None
   - Empty credentials → return None

2. **Test has_permission function**:
   - CEO with any permission → True
   - Nhân viên with allowed permission → True
   - Nhân viên with "products" → False
   - Nhân viên with "reviews" → False
   - Unauthenticated user → False

3. **Test get_allowed_menu_items**:
   - CEO → all menu items
   - Nhân viên → menu items without "Quản lý Sản phẩm" and "Duyệt Đánh Giá"
   - Unauthenticated → empty list

### Integration Tests

1. **Login flow**:
   - Enter valid credentials → see admin dashboard
   - Enter invalid credentials → see error message
   - Logout → return to login page

2. **Permission enforcement**:
   - Login as CEO → see all menu items
   - Login as Nhân viên → restricted menu items hidden
   - Try to access restricted page as Nhân viên → show error

3. **Session persistence**:
   - Login → navigate between pages → session maintained
   - Logout → session cleared

### Property-Based Tests

Sử dụng `hypothesis` library cho Python:

1. **Property 1**: Generate random username/password pairs, verify authentication logic
2. **Property 2**: Generate random permission names, verify CEO always has access
3. **Property 3**: Verify Nhân viên never has "products" or "reviews" permissions
4. **Property 7**: Generate random passwords, hash them, verify bcrypt round-trip

**Test Configuration**: Minimum 100 iterations per property test

## Implementation Notes

### Password Hashing

```python
import bcrypt

# Tạo hash cho password (chỉ chạy 1 lần để tạo USERS dict)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

# Hash cho 2 passwords:
# "123456" → $2b$12$...
# "12345" → $2b$12$...
```

### Streamlit Session State

- Session state tự động persist trong suốt phiên làm việc
- Khi refresh page, session state vẫn giữ nguyên
- Chỉ mất khi đóng tab hoặc clear browser cache

### Security Considerations

1. **Password Storage**: Sử dụng bcrypt với cost factor 12
2. **Session Security**: Streamlit session state chỉ tồn tại client-side
3. **No Database**: User data hardcoded (đủ cho 2 users)
4. **HTTPS**: Nên deploy với HTTPS để bảo vệ credentials khi truyền

### UI/UX Considerations

1. **Minimalist Design**: Giữ nguyên theme đen trắng hiện tại
2. **Clear Feedback**: Hiển thị loading state khi đăng nhập
3. **Error Messages**: Rõ ràng, bằng tiếng Việt
4. **User Info**: Luôn hiển thị username và role trong sidebar
5. **Logout Button**: Dễ tìm, luôn có sẵn

## File Structure

```
admin-python/
├── quan_tri.py          # Main file (cập nhật)
├── auth.py              # Authentication module (mới)
└── requirements.txt     # Thêm bcrypt
```

## Dependencies

```
bcrypt==4.1.2  # Thêm vào requirements.txt
```
