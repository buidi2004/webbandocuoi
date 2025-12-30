# Implementation Plan: Hệ Thống Xác Thực và Phân Quyền Admin

## Overview

Triển khai hệ thống xác thực và phân quyền cho trang quản trị IVIE Wedding Studio với 2 tài khoản (CEO và Nhân viên), sử dụng Streamlit session state và bcrypt để bảo mật.

## Tasks

- [x] 1. Cài đặt dependencies và tạo module authentication
  - Thêm `bcrypt==4.1.2` vào `admin-python/requirements.txt`
  - Tạo file `admin-python/auth.py` với các hàm authentication cơ bản
  - _Requirements: 1.2, 1.3, 5.1_

- [ ] 2. Implement User Data Store và Password Hashing
  - [ ] 2.1 Tạo USERS dictionary với 2 users (ceo và nhanvien)
    - Hash password "123456" cho ceo
    - Hash password "12345" cho nhanvien
    - Định nghĩa permissions cho từng role
    - _Requirements: 1.5, 5.1_
  
  - [ ] 2.2 Write unit tests cho password hashing
    - Test hash_password function
    - Test bcrypt verification
    - _Requirements: 5.1, 5.2_

- [ ] 3. Implement Authentication Module
  - [ ] 3.1 Viết hàm authenticate(username, password)
    - Kiểm tra username tồn tại
    - Verify password với bcrypt
    - Return user data nếu thành công
    - _Requirements: 1.2, 1.3, 5.2_
  
  - [ ] 3.2 Write property test cho authentication
    - **Property 1: Authentication Success Requires Valid Credentials**
    - **Validates: Requirements 1.2, 1.3**

- [ ] 4. Implement Session Management
  - [ ] 4.1 Viết các hàm quản lý session
    - `init_session()` - Khởi tạo session state
    - `login(user_data)` - Lưu user vào session
    - `logout()` - Xóa session
    - `is_authenticated()` - Kiểm tra đã đăng nhập
    - `get_current_user()` - Lấy thông tin user
    - _Requirements: 4.1, 4.2, 4.4_
  
  - [ ] 4.2 Write unit tests cho session management
    - Test login/logout flow
    - Test session persistence
    - _Requirements: 4.1, 4.4_

- [ ] 5. Implement Authorization Module
  - [ ] 5.1 Tạo MENU_PERMISSIONS mapping
    - Map tất cả menu items với permissions
    - Đánh dấu "products" và "reviews" cho restricted
    - _Requirements: 3.2, 3.3, 3.5_
  
  - [ ] 5.2 Viết hàm has_permission(permission)
    - CEO luôn return True
    - Nhân viên check trong permissions list
    - _Requirements: 2.1, 2.2, 3.2, 3.3_
  
  - [ ] 5.3 Viết hàm get_allowed_menu_items()
    - CEO thấy tất cả menu
    - Nhân viên chỉ thấy menu có quyền
    - _Requirements: 2.3, 3.4, 3.5_
  
  - [ ] 5.4 Write property tests cho authorization
    - **Property 2: CEO Has All Permissions**
    - **Property 3: Nhân viên Cannot Access Restricted Functions**
    - **Property 8: Menu Visibility Based on Permissions**
    - **Validates: Requirements 2.1, 3.2, 3.3, 3.5**

- [ ] 6. Implement Login UI
  - [ ] 6.1 Tạo hàm show_login_page()
    - Form đăng nhập với username/password fields
    - Branding IVIE Wedding Studio
    - Submit button và error handling
    - _Requirements: 1.1, 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ] 6.2 Tích hợp authentication vào login form
    - Call authenticate() khi submit
    - Hiển thị success/error messages
    - Redirect sau khi đăng nhập thành công
    - _Requirements: 1.2, 1.3, 1.4_

- [ ] 7. Implement User Info Display
  - [ ] 7.1 Tạo hàm show_user_info_sidebar()
    - Hiển thị username và role
    - Welcome message
    - Logout button
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 8. Integrate Authentication vào quan_tri.py
  - [ ] 8.1 Import auth module và khởi tạo session
    - Import các hàm từ auth.py
    - Gọi init_session() ở đầu file
    - _Requirements: 4.1_
  
  - [ ] 8.2 Thêm authentication check
    - Kiểm tra is_authenticated()
    - Hiển thị login page nếu chưa đăng nhập
    - Hiển thị admin pages nếu đã đăng nhập
    - _Requirements: 4.5_
  
  - [ ] 8.3 Filter menu items theo permissions
    - Thay thế hardcoded menu list bằng get_allowed_menu_items()
    - Chỉ hiển thị menu items user có quyền
    - _Requirements: 2.3, 3.5_
  
  - [ ] 8.4 Thêm user info vào sidebar
    - Gọi show_user_info_sidebar() trong sidebar
    - Hiển thị username, role, logout button
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 9. Add Authorization Checks cho từng chức năng
  - [ ] 9.1 Wrap mỗi menu choice với permission check
    - Kiểm tra has_permission() trước khi hiển thị nội dung
    - Hiển thị error message nếu không có quyền
    - _Requirements: 3.2, 3.3_
  
  - [ ] 9.2 Write integration tests
    - Test login as CEO → see all menus
    - Test login as Nhân viên → restricted menus hidden
    - Test access restricted page → show error
    - _Requirements: 2.1, 2.2, 3.2, 3.3_

- [ ] 10. Testing và Polish
  - [ ] 10.1 Test toàn bộ flow với cả 2 accounts
    - Login/logout với ceo account
    - Login/logout với nhanvien account
    - Verify menu visibility
    - Verify permission enforcement
    - _Requirements: All_
  
  - [ ] 10.2 Cải thiện UI/UX
    - Đảm bảo styling nhất quán với theme hiện tại
    - Loading states cho login
    - Clear error messages
    - _Requirements: 6.3, 6.4, 6.5_

- [ ] 11. Checkpoint - Đảm bảo tất cả tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Each task references specific requirements for traceability
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Bcrypt hashing chỉ cần chạy 1 lần để tạo password hashes
- Session state tự động persist trong Streamlit, không cần database
