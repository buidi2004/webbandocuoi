# Hướng Dẫn Thêm Combo PREMIUM LUXURY vào Production

## Vấn Đề
- Combo thứ 4 (PREMIUM LUXURY 25 triệu) chưa hiện trên frontend production
- Nguyên nhân: Migration script chỉ chạy khi database trống, nhưng production đã có 3 combo
- Bảng `combos` đã được tạo nhưng chưa có dữ liệu combo thứ 4

## Giải Pháp: Thêm Combo qua Admin Panel

### Bước 1: Đăng nhập Admin Panel
1. Truy cập: https://ivie-admin.onrender.com
2. Đăng nhập với tài khoản CEO:
   - Username: `ceo`
   - Password: `123456`

### Bước 2: Vào Quản lý Combo
1. Trong menu bên trái, chọn **"🎁 Quản lý Combo"**
2. Chọn tab **"THÊM/SỬA COMBO"**

### Bước 3: Điền Thông Tin Combo

**Thông tin cơ bản:**
- **Tên Combo**: `COMBO PREMIUM LUXURY`
- **Giá (VNĐ)**: `25000000`
- **Giới hạn sản phẩm**: `10`
- **Mô tả**: `Gói cao cấp với đội ngũ chuyên gia hàng đầu - Dành cho đám cưới hoàn hảo`

**Quyền lợi (10 dòng):**
1. `10 Váy Cưới cao cấp tùy chọn (bao gồm dòng Luxury & Designer)`
2. `10 Bộ Vest Nam cao cấp`
3. `🌟 Chuyên gia chụp ảnh HÀNG ĐẦU - Kinh nghiệm 10+ năm`
4. `🌟 Chuyên gia quay phim cinematic HÀNG ĐẦU`
5. `🌟 Dựng & chỉnh sửa ảnh bởi chuyên gia HÀNG ĐẦU`
6. `🌟 Dựng phim cưới điện ảnh (10-15 phút) - Đạo diễn chuyên nghiệp`
7. `🌟 Trang điểm cô dâu & gia đình bởi chuyên gia makeup HÀNG ĐẦU`
8. `🌟 Album ảnh cao cấp 40x60cm (50 trang) - Thiết kế độc quyền`
9. `Phụ kiện & trang sức đi kèm`
10. `Hỗ trợ tư vấn concept & styling bởi chuyên gia`

**Hình ảnh:**
- **URL**: `https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600`

**Trạng thái:**
- ☐ Nổi bật (không check)
- ☑ Hoạt động (check)

### Bước 4: Lưu Combo
1. Click nút **"💾 Thêm Combo"**
2. Đợi thông báo thành công

### Bước 5: Kiểm Tra
1. Quay lại tab **"DANH SÁCH COMBO"**
2. Xác nhận combo mới đã xuất hiện
3. Truy cập frontend: https://ivie-frontend.onrender.com
4. Vào trang **"Chọn Gói Dịch Vụ"**
5. Xác nhận combo PREMIUM LUXURY 25 triệu đã hiển thị

## Lưu Ý
- Nếu backend đang sleep, lần đầu truy cập sẽ mất 30-60 giây
- Sau khi thêm combo, frontend sẽ tự động load từ API
- Không cần clear cache hay restart service

## Giải Pháp Thay Thế (Nếu Admin Panel Không Hoạt Động)

### Option 1: Chạy Script Python
```bash
python add_combo_via_api.py
```

### Option 2: Thêm Trực Tiếp vào Database
Nếu có quyền truy cập database production, chạy SQL:
```sql
INSERT INTO combos (ten, gia, gioi_han, mo_ta, quyen_loi, hinh_anh, noi_bat, hoat_dong, ngay_tao)
VALUES (
    'COMBO PREMIUM LUXURY',
    25000000,
    10,
    'Gói cao cấp với đội ngũ chuyên gia hàng đầu - Dành cho đám cưới hoàn hảo',
    '["10 Váy Cưới cao cấp tùy chọn (bao gồm dòng Luxury & Designer)", "10 Bộ Vest Nam cao cấp", "🌟 Chuyên gia chụp ảnh HÀNG ĐẦU - Kinh nghiệm 10+ năm", "🌟 Chuyên gia quay phim cinematic HÀNG ĐẦU", "🌟 Dựng & chỉnh sửa ảnh bởi chuyên gia HÀNG ĐẦU", "🌟 Dựng phim cưới điện ảnh (10-15 phút) - Đạo diễn chuyên nghiệp", "🌟 Trang điểm cô dâu & gia đình bởi chuyên gia makeup HÀNG ĐẦU", "🌟 Album ảnh cao cấp 40x60cm (50 trang) - Thiết kế độc quyền", "Phụ kiện & trang sức đi kèm", "Hỗ trợ tư vấn concept & styling bởi chuyên gia"]',
    'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600',
    false,
    true,
    NOW()
);
```

## Tóm Tắt
✅ Code đã được push lên GitHub
✅ Render sẽ tự động deploy
✅ Bảng combos đã được tạo trong production
⏳ Cần thêm dữ liệu combo thứ 4 qua Admin Panel
