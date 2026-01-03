# ⚡ DEPLOY LÊN RENDER - HƯỚNG DẪN TỪNG BƯỚC CÓ HÌNH ẢNH

## 🎬 VIDEO HƯỚNG DẪN (Nếu bạn thích xem video)

- Tìm kiếm trên YouTube: "How to deploy to Render using render.yaml"
- Hoặc xem docs chính thức: <https://render.com/docs/infrastructure-as-code>

---

## 📍 BƯỚC 1: ĐĂNG KÝ TÀI KHOẢN RENDER

### 1.1. Truy cập Render.com

```
🔗 Link: https://dashboard.render.com/register
```

### 1.2. Đăng ký bằng GitHub

✅ Click nút **"Continue with GitHub"**
✅ Đăng nhập vào GitHub của bạn
✅ Cấp quyền cho Render truy cập repositories

### 1.3. Xác nhận email (nếu cần)

📧 Kiểm tra email và click link xác nhận

---

## 📍 BƯỚC 2: TẠO BLUEPRINT

### 2.1. Vào Dashboard

```
🔗 Link: https://dashboard.render.com
```

### 2.2. Tạo Blueprint mới

1. Click nút **"New +"** ở góc trên bên phải
2. Trong menu dropdown, chọn **"Blueprint"**

### 2.3. Kết nối Repository

1. Tìm và chọn repository: **`buidi2004/webbandocuoi`**
2. Click nút **"Connect"**

### 2.4. Cấu hình Blueprint

Render sẽ tự động:

- ✅ Phát hiện file `render.yaml`
- ✅ Đọc cấu hình
- ✅ Hiển thị preview các services sẽ được tạo

Bạn sẽ thấy:

```
📦 Services sẽ được tạo:
├── 💾 Database: ivie-db-final (PostgreSQL Free)
├── 🔧 Web Service: ivie-be-final (Backend API)
├── 🎨 Static Site: ivie-fe-final (Frontend)
└── 👨‍💼 Web Service: ivie-ad-final (Admin Panel)
```

### 2.5. Đặt tên và Deploy

1. **Blueprint Name**: Để mặc định hoặc đặt tên: `ivie-wedding-studio`
2. Click nút **"Apply"** hoặc **"Create Blueprint"**
3. ✅ Xác nhận tạo Blueprint

---

## 📍 BƯỚC 3: CHỜ DEPLOY (5-10 PHÚT)

### 3.1. Theo dõi quá trình Deploy

Render sẽ bắt đầu tạo các services theo thứ tự:

#### 1️⃣ Database (1-2 phút)

```
🔵 Creating... → 🟢 Available
```

#### 2️⃣ Backend API (3-5 phút)

```
🔵 Building (pip install...)
🔵 Starting (gunicorn...)
🟢 Live!
```

#### 3️⃣ Frontend (3-5 phút)

```
🔵 Building (npm install && npm run build...)
🟢 Live!
```

#### 4️⃣ Admin Panel (3-5 phút)

```
🔵 Building (pip install...)
🔵 Starting (streamlit run...)
🟢 Live!
```

### 3.2. Xem Logs

Nếu muốn xem chi tiết:

1. Click vào từng service
2. Tab **"Logs"** → Xem quá trình build và deploy
3. Tab **"Events"** → Xem lịch sử deploy

---

## 🎉 BƯỚC 4: KIỂM TRA SAU KHI DEPLOY

### 4.1. Lấy URLs của các services

Sau khi deploy xong, bạn sẽ có 3 URLs:

#### Backend API

```
https://ivie-be-final.onrender.com
```

**Test**: Mở trình duyệt và truy cập:

```
https://ivie-be-final.onrender.com/docs
```

✅ Bạn sẽ thấy trang Swagger API Documentation

#### Frontend

```
https://ivie-fe-final.onrender.com
```

**Test**: Mở trình duyệt và truy cập URL trên
✅ Bạn sẽ thấy trang chủ website

#### Admin Panel

```
https://ivie-ad-final.onrender.com
```

**Test**: Mở trình duyệt, đăng nhập với:

- Username: `admin`
- Password: `admin123`
✅ Bạn sẽ vào được Admin Dashboard

### 4.2. Bookmark các URLs

💡 Lưu lại 3 URLs này để truy cập nhanh!

---

## 🔧 CẤU HÌNH BỔ SUNG (TÙY CHỌN)

### Thêm biến môi trường riêng

Nếu bạn muốn thêm API keys hoặc secrets:

1. Vào service → Tab **"Environment"**
2. Click **"Add Environment Variable"**
3. Thêm key-value
4. Click **"Save Changes"**
5. Service sẽ tự động restart

Ví dụ:

```
TELEGRAM_BOT_TOKEN = your_bot_token_here
TELEGRAM_CHAT_ID = your_chat_id_here
```

---

## ⚠️ ĐIỀU CẦN BIẾT VỀ GÓI MIỄN PHÍ

### ✅ Ưu điểm

- Hoàn toàn miễn phí
- Không cần thẻ tín dụng
- SSL/HTTPS tự động
- Auto deploy khi push code
- 750 giờ/tháng cho Web Services
- 100GB bandwidth cho Static Sites

### ⚠️ Hạn chế

1. **Service Sleep**:
   - Sau 15 phút không hoạt động → Service ngủ
   - Lần đầu truy cập → Chờ 30-60 giây để "wake up"

2. **Tài nguyên hạn chế**:
   - RAM: 512 MB/service
   - CPU: Shared
   - Database: 1 GB storage

3. **Bandwidth**:
   - Frontend: 100 GB/tháng
   - Vượt quá → Service tạm dừng

### 💡 Giải pháp

Nếu traffic cao, nâng cấp lên **Paid Plan**:

- $7/tháng/service
- Không sleep
- Dedicated resources
- Custom domain miễn phí

---

## 🔄 CẬP NHẬT CODE SAU NÀY

Mỗi khi bạn sửa code:

```bash
# 1. Commit changes
git add .
git commit -m "update: mô tả thay đổi của bạn"

# 2. Push lên GitHub
git push origin main

# 3. Render tự động deploy lại (Auto Deploy)
# → Vào Dashboard để theo dõi
```

**⏱️ Thời gian deploy lại**: 3-5 phút

---

## 🚨 XỬ LÝ LỖI

### Lỗi 1: Build Failed ❌

**Triệu chứng**: Service màu đỏ, status "Failed"

**Cách xử lý**:

```
1. Vào service → Tab "Logs"
2. Tìm dòng lỗi (màu đỏ)
3. Thường là:
   - requirements.txt thiếu package
   - Python/Node version không tương thích
   - Syntax error trong code
4. Sửa lỗi trong code local
5. Push lại lên GitHub
```

### Lỗi 2: 502 Bad Gateway ⚠️

**Triệu chứng**: Truy cập website hiện "502 Bad Gateway"

**Cách xử lý**:

```
✅ Đợi 1-2 phút (service đang khởi động)
✅ Refresh trang
✅ Nếu vẫn lỗi → Xem Logs để debug
```

### Lỗi 3: CORS Error 🔒

**Triệu chứng**: Frontend không kết nối được Backend

**Cách xử lý**:

```
1. Vào Backend service → Tab "Environment"
2. Kiểm tra biến CORS_ORIGINS:
   CORS_ORIGINS = https://ivie-fe-final.onrender.com,https://ivie-ad-final.onrender.com
3. Đảm bảo có đúng URL của Frontend và Admin
4. Save Changes → Service restart
```

### Lỗi 4: Service Sleep 💤

**Triệu chứng**: Truy cập lần đầu rất chậm (30-60s)

**Cách xử lý**:

```
✅ Đây là hành vi bình thường của Free Plan
✅ Đợi service "wake up"
✅ Lần truy cập tiếp theo sẽ nhanh hơn
⚠️ Hoặc nâng cấp lên Paid Plan ($7/tháng)
```

---

## 📊 MONITORING

### Theo dõi trạng thái Services

Vào Dashboard → Bạn sẽ thấy:

```
📈 Metrics:
├── CPU Usage
├── Memory Usage
├── Request Count
└── Response Time

📜 Logs:
├── Real-time logs
├── Error logs
└── Access logs

🕐 Events:
├── Deploy history
├── Manual deploys
└── Auto deploys
```

---

## 🔐 BẢO MẬT

### Thay đổi mật khẩu Admin

```
1. Vào Admin Service → Tab "Environment"
2. Sửa biến:
   ADMIN_PASSWORD = matkhau-moi-cua-ban
3. Save Changes
4. Service tự động restart
```

### Thêm JWT Secret (Nâng cao)

```
1. Vào Backend Service → Tab "Environment"
2. Thêm:
   JWT_SECRET_KEY = random-string-dai-va-phuc-tap
3. Save Changes
```

---

## 📞 HỖ TRỢ

### Tài liệu chính thức

- 📖 **Render Docs**: <https://render.com/docs>
- 💬 **Community**: <https://community.render.com>
- 📧 **Support**: <https://render.com/support>

### Tìm kiếm lỗi

- Google: "Render [tên lỗi]"
- Stack Overflow
- Render Community Forum

---

## ✅ CHECKLIST HOÀN THÀNH

Deploy thành công khi tất cả đều ✅:

**Setup:**

- [ ] Đã đăng ký Render
- [ ] Đã kết nối GitHub với Render
- [ ] Đã tạo Blueprint từ render.yaml

**Services:**

- [ ] Database màu xanh (Available)
- [ ] Backend màu xanh (Live)
- [ ] Frontend màu xanh (Live)
- [ ] Admin màu xanh (Live)

**Testing:**

- [ ] Backend API /docs hiển thị đúng
- [ ] Frontend trang chủ hiển thị đúng
- [ ] Admin login thành công
- [ ] Frontend kết nối được Backend (không có CORS error)

**Hoàn tất:**

- [ ] Đã bookmark 3 URLs
- [ ] Đã test thêm dữ liệu trong Admin
- [ ] Đã hiểu về Service Sleep
- [ ] Đã biết cách update code (git push)

---

## 🎊 CHÚC MỪNG

**Bạn đã deploy thành công ứng dụng lên Render!** 🚀

### URLs của bạn

```
🔧 Backend:  https://ivie-be-final.onrender.com/docs
🎨 Frontend: https://ivie-fe-final.onrender.com
👨‍💼 Admin:    https://ivie-ad-final.onrender.com
```

### Bước tiếp theo

1. ✅ Thêm dữ liệu sản phẩm trong Admin
2. ✅ Test các chức năng chính
3. ✅ Chia sẻ link với khách hàng/bạn bè
4. ✅ Theo dõi logs và metrics

---

**💡 PRO TIP**: Lưu file này lại để tham khảo khi cần!
