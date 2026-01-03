# 🎯 DEPLOY LÊN RENDER - CHỈ 3 BƯỚC

## ⚡ BƯỚC 1: Đăng nhập Render và kết nối GitHub

1. Truy cập: **<https://dashboard.render.com/register>**
2. Đăng ký/Đăng nhập bằng tài khoản GitHub
3. Cấp quyền cho Render truy cập repository của bạn

---

## 🚀 BƯỚC 2: Tạo Blueprint từ render.yaml

1. Vào Dashboard Render: **<https://dashboard.render.com>**
2. Click nút **"New +"** ở góc trên bên phải
3. Chọn **"Blueprint"**
4. Chọn repository: **`buidi2004/webbandocuoi`**
5. Render sẽ tự động phát hiện file `render.yaml`
6. Đặt tên cho Blueprint: **`ivie-wedding-studio`**
7. Click **"Apply"** hoặc **"Create Blueprint"**

✅ **Render sẽ tự động tạo:**

- ✅ Database PostgreSQL (ivie-db-final)
- ✅ Backend API (ivie-be-final)
- ✅ Frontend Static Site (ivie-fe-final)
- ✅ Admin Panel (ivie-ad-final)

---

## ⏱️ BƯỚC 3: Đợi deploy (5-10 phút)

### Theo dõi quá trình deploy

1. Vào tab **"Blueprint"** để xem tổng quan
2. Click vào từng service để xem logs chi tiết

### Trạng thái mỗi service

- 🔵 **Building** = Đang build
- 🟢 **Live** = Đã deploy thành công
- 🔴 **Failed** = Có lỗi (xem logs)

---

## 🎉 SAU KHI DEPLOY THÀNH CÔNG

### URLs của bạn

```
Backend:  https://ivie-be-final.onrender.com/docs
Frontend: https://ivie-fe-final.onrender.com
Admin:    https://ivie-ad-final.onrender.com
```

### Kiểm tra

1. **Backend**: Mở `/docs` để xem API documentation
2. **Frontend**: Truy cập trang chủ
3. **Admin**: Đăng nhập vào admin panel

### Đăng nhập Admin

- **URL**: <https://ivie-ad-final.onrender.com>
- **Username**: admin
- **Password**: admin123

---

## ⚠️ LƯU Ý QUAN TRỌNG VỀ GÓI MIỄN PHÍ

### 1. Service sẽ ngủ (Sleep) ⏰

- **Sau 15 phút không hoạt động** → Service tự động ngủ
- **Lần truy cập đầu tiên** → Chờ 30-60 giây để service "thức dậy"
- **Giải pháp**: Nâng cấp lên Paid Plan ($7/tháng/service)

### 2. Giới hạn tài nguyên 📊

- **RAM**: 512 MB mỗi service
- **CPU**: Shared (chia sẻ)
- **Bandwidth**: 100 GB/tháng (Frontend)
- **Storage**: 1 GB (Database)
- **Build time**: 500 giờ/tháng

### 3. Database riêng biệt 💾

- Mỗi service có SQLite riêng (trong free tier)
- Để dùng chung database PostgreSQL → Nâng cấp database lên Paid

---

## 🔧 CẬP NHẬT CODE

Sau khi deploy, mỗi lần bạn push code mới:

```bash
git add .
git commit -m "update: mô tả thay đổi"
git push origin main
```

✅ **Render sẽ tự động deploy lại** (Auto Deploy)

---

## 🚨 XỬ LÝ LỖI

### Lỗi: Build Failed

**Giải pháp:**

1. Vào service → Tab "Logs"
2. Tìm dòng lỗi màu đỏ
3. Sửa lỗi trong code
4. Push lại lên GitHub

### Lỗi: 502 Bad Gateway

**Giải pháp:**

- Đợi 1-2 phút (service đang khởi động)
- Nếu vẫn lỗi → Xem logs

### Lỗi: CORS Error

**Giải pháp:**

1. Vào Backend service → Tab "Environment"
2. Kiểm tra `CORS_ORIGINS` có đúng URL Frontend và Admin không
3. Save → Service tự động restart

---

## 📱 LIÊN HỆ HỖ TRỢ

- **Render Docs**: <https://render.com/docs>
- **Community**: <https://community.render.com>
- **Support**: <https://render.com/support>

---

## ✅ CHECKLIST

- [ ] Đã đăng ký tài khoản Render
- [ ] Đã kết nối GitHub với Render
- [ ] Đã tạo Blueprint từ render.yaml
- [ ] Backend đã deploy thành công (màu xanh)
- [ ] Frontend đã deploy thành công (màu xanh)
- [ ] Admin đã deploy thành công (màu xanh)
- [ ] Database đã tạo thành công
- [ ] Đã test truy cập 3 URLs
- [ ] Đã đăng nhập Admin panel

---

**🎊 CHÚC MỪNG! Bạn đã deploy thành công lên Render!**

**💡 TIP**: Bookmark 3 URLs của bạn để truy cập nhanh!
