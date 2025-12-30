# Hướng Dẫn Đăng Nhập Admin Panel

## 🔐 Tài Khoản Đăng Nhập

### 1. Tài khoản CEO (Quản trị viên)
- **Username:** `ceo`
- **Password:** `123456`
- **Quyền hạn:** Truy cập TẤT CẢ chức năng

### 2. Tài khoản Nhân viên
- **Username:** `nhanvien`
- **Password:** `12345`
- **Quyền hạn:** Bị hạn chế, KHÔNG được truy cập:
  - ⏳ Duyệt Đánh Giá
  - 👗 Quản lý Sản phẩm

## 📋 Danh Sách Quyền

### CEO - Full Access
✅ Tổng quan  
✅ Quản lý Đơn hàng  
✅ Liên hệ khách hàng  
✅ Tư vấn khách hàng  
✅ **Duyệt Đánh Giá** (Chỉ CEO)  
✅ Quản lý Banner  
✅ **Quản lý Sản phẩm** (Chỉ CEO)  
✅ Quản lý Combo  
✅ Đối tác & Khiếu nại  
✅ Thư viện ảnh mẫu  
✅ Dịch vụ Chuyên gia  
✅ Blog & Tin tức  
✅ Nội dung Trang chủ  

### Nhân viên - Restricted Access
✅ Tổng quan  
✅ Quản lý Đơn hàng  
✅ Liên hệ khách hàng  
✅ Tư vấn khách hàng  
❌ **Duyệt Đánh Giá** (Bị chặn)  
✅ Quản lý Banner  
❌ **Quản lý Sản phẩm** (Bị chặn)  
✅ Quản lý Combo  
✅ Đối tác & Khiếu nại  
✅ Thư viện ảnh mẫu  
✅ Dịch vụ Chuyên gia  
✅ Blog & Tin tức  
✅ Nội dung Trang chủ  

## 🚀 Cách Sử Dụng

1. **Truy cập Admin Panel:**
   - Local: http://localhost:8501
   - Production: https://ivie-admin.onrender.com

2. **Đăng nhập:**
   - Nhập username và password
   - Click "ĐĂNG NHẬP"

3. **Sau khi đăng nhập:**
   - Thông tin user hiển thị ở sidebar (username, vai trò)
   - Menu chỉ hiển thị các chức năng bạn có quyền truy cập
   - Nếu cố truy cập chức năng bị hạn chế → Hiển thị thông báo lỗi

4. **Đăng xuất:**
   - Click nút "🚪 Đăng xuất" ở sidebar

## 🔒 Bảo Mật

- Mật khẩu được mã hóa bằng **bcrypt** (không lưu plain text)
- Session được quản lý bởi Streamlit session state
- Mỗi request đều kiểm tra authentication
- Permission check trước khi hiển thị nội dung

## 🧪 Testing

Chạy tests để verify authentication:

```bash
cd admin-python
python test_auth.py
```

Tất cả 7 tests phải PASS:
- ✅ Password Hashing
- ✅ Valid Credentials
- ✅ Invalid Credentials
- ✅ CEO Permissions
- ✅ Nhân viên Permissions
- ✅ Menu Visibility
- ✅ Password Hashes Verification

## 📝 Lưu Ý

- **Không chia sẻ mật khẩu** với người không có quyền
- **CEO** nên thay đổi mật khẩu mặc định sau lần đăng nhập đầu tiên
- Nếu quên mật khẩu, liên hệ developer để reset
- Session tự động hết hạn khi đóng browser

## 🛠️ Troubleshooting

### Không thể đăng nhập?
- Kiểm tra username/password có đúng không
- Đảm bảo không có khoảng trắng thừa
- Thử refresh page và đăng nhập lại

### Menu items bị thiếu?
- Kiểm tra vai trò của bạn (CEO hay Nhân viên)
- Nhân viên không thấy "Quản lý Sản phẩm" và "Duyệt Đánh Giá"

### Thông báo "Không có quyền truy cập"?
- Bạn đang cố truy cập chức năng bị hạn chế
- Liên hệ CEO để được cấp quyền (nếu cần)
