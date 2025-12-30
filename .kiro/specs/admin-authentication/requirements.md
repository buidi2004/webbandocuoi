# Requirements Document - Hệ Thống Xác Thực và Phân Quyền Admin

## Introduction

Hệ thống xác thực và phân quyền cho trang quản trị (admin panel) của IVIE Wedding Studio, cho phép kiểm soát truy cập dựa trên vai trò người dùng.

## Glossary

- **Admin_System**: Hệ thống quản trị Streamlit
- **User**: Người dùng đăng nhập vào hệ thống admin
- **Role**: Vai trò của người dùng (CEO hoặc Nhân viên)
- **Permission**: Quyền truy cập vào các chức năng cụ thể
- **Session**: Phiên làm việc của người dùng sau khi đăng nhập thành công
- **Authentication**: Quá trình xác thực danh tính người dùng
- **Authorization**: Quá trình kiểm tra quyền truy cập chức năng

## Requirements

### Requirement 1: Xác thực người dùng

**User Story:** Là một quản trị viên, tôi muốn đăng nhập vào hệ thống bằng tên đăng nhập và mật khẩu, để có thể truy cập các chức năng quản trị.

#### Acceptance Criteria

1. WHEN a user accesses the admin panel, THE Admin_System SHALL display a login form
2. WHEN a user enters valid credentials (username and password), THE Admin_System SHALL authenticate the user and create a session
3. WHEN a user enters invalid credentials, THE Admin_System SHALL display an error message and prevent access
4. WHEN a user is authenticated, THE Admin_System SHALL store the session state including username and role
5. THE Admin_System SHALL support two predefined users: "ceo" with password "123456" and "nhanvien" with password "12345"

### Requirement 2: Phân quyền theo vai trò

**User Story:** Là một CEO, tôi muốn có quyền truy cập tất cả các chức năng quản trị, để có thể quản lý toàn bộ hệ thống.

#### Acceptance Criteria

1. WHEN a user with role "CEO" is authenticated, THE Admin_System SHALL grant access to all administrative functions
2. THE Admin_System SHALL allow CEO role to access: Dashboard, Quản lý sản phẩm, Quản lý đơn hàng, Quản lý combo, Duyệt đánh giá, Quản lý chuyên gia, and Thống kê
3. WHEN displaying the sidebar menu, THE Admin_System SHALL show all menu items for CEO role

### Requirement 3: Hạn chế quyền truy cập nhân viên

**User Story:** Là một nhân viên, tôi muốn truy cập các chức năng được phép, nhưng không thể truy cập các chức năng nhạy cảm như quản lý sản phẩm và duyệt đánh giá.

#### Acceptance Criteria

1. WHEN a user with role "Nhân viên" is authenticated, THE Admin_System SHALL restrict access to specific functions
2. THE Admin_System SHALL prevent "Nhân viên" role from accessing "Quản lý sản phẩm" function
3. THE Admin_System SHALL prevent "Nhân viên" role from accessing "Duyệt đánh giá" function
4. THE Admin_System SHALL allow "Nhân viên" role to access: Dashboard, Quản lý đơn hàng, Quản lý combo, Quản lý chuyên gia, and Thống kê
5. WHEN displaying the sidebar menu, THE Admin_System SHALL hide restricted menu items for "Nhân viên" role

### Requirement 4: Quản lý phiên làm việc

**User Story:** Là một người dùng đã đăng nhập, tôi muốn duy trì phiên làm việc của mình, để không phải đăng nhập lại liên tục.

#### Acceptance Criteria

1. WHEN a user successfully authenticates, THE Admin_System SHALL create a session with user information
2. WHEN a user navigates between pages, THE Admin_System SHALL maintain the session state
3. THE Admin_System SHALL provide a logout button to terminate the session
4. WHEN a user clicks logout, THE Admin_System SHALL clear the session and redirect to login page
5. WHEN an unauthenticated user attempts to access admin functions, THE Admin_System SHALL redirect to login page

### Requirement 5: Bảo mật mật khẩu

**User Story:** Là một quản trị viên hệ thống, tôi muốn mật khẩu được lưu trữ an toàn, để bảo vệ tài khoản khỏi truy cập trái phép.

#### Acceptance Criteria

1. THE Admin_System SHALL store passwords using bcrypt hashing algorithm
2. WHEN validating credentials, THE Admin_System SHALL compare hashed passwords
3. THE Admin_System SHALL NOT display or log plain-text passwords
4. WHEN authentication fails, THE Admin_System SHALL NOT reveal whether username or password was incorrect

### Requirement 6: Giao diện đăng nhập

**User Story:** Là một người dùng, tôi muốn có giao diện đăng nhập đẹp và dễ sử dụng, để có trải nghiệm tốt khi truy cập hệ thống.

#### Acceptance Criteria

1. THE Admin_System SHALL display a centered login form with username and password fields
2. THE Admin_System SHALL show the IVIE Wedding Studio branding on the login page
3. WHEN a user enters credentials, THE Admin_System SHALL provide visual feedback (loading state)
4. WHEN authentication fails, THE Admin_System SHALL display a clear error message in Vietnamese
5. THE Admin_System SHALL use consistent styling with the rest of the admin panel

### Requirement 7: Hiển thị thông tin người dùng

**User Story:** Là một người dùng đã đăng nhập, tôi muốn thấy thông tin tài khoản của mình, để biết mình đang đăng nhập với vai trò gì.

#### Acceptance Criteria

1. WHEN a user is authenticated, THE Admin_System SHALL display the username in the sidebar
2. WHEN a user is authenticated, THE Admin_System SHALL display the user role in the sidebar
3. THE Admin_System SHALL show a welcome message with the username
4. THE Admin_System SHALL provide visual indication of the current user's role (CEO or Nhân viên)
