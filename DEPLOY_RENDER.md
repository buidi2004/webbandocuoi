# 🚀 Hướng Dẫn Deploy IVIE Wedding lên Render (Thủ Công)

## 📋 Chuẩn Bị

1. **Tài khoản GitHub** - Code đã push lên repo
2. **Tài khoản Render** - Đăng ký miễn phí tại [render.com](https://render.com)

---

## 🗄️ BƯỚC 1: Tạo PostgreSQL Database

### 1.1. Đăng nhập Render
- Truy cập: https://dashboard.render.com
- Đăng nhập bằng GitHub hoặc email

### 1.2. Tạo Database
1. Click nút **"New +"** ở góc trên bên phải
2. Chọn **"PostgreSQL"**
3. Điền thông tin:
   - **Name**: `ivie-db-final` (hoặc tên bạn muốn)
   - **Database**: `ivie_wedding`
   - **User**: `ivie_user`
   - **Region**: **Singapore** (gần Việt Nam nhất)
   - **PostgreSQL Version**: 16 (mặc định)
   - **Datadog API Key**: Để trống
   - **Plan**: Chọn **Free**
4. Click **"Create Database"**
5. Chờ ~2-3 phút để database khởi tạo

### 1.3. Lưu Database URL
- Sau khi tạo xong, vào tab **"Info"**
- Tìm phần **"Connections"**
- Copy **"Internal Database URL"** (dạng: `postgresql://ivie_user:...@...`)
- **LƯU LẠI URL NÀY** - sẽ dùng cho Backend

---

## 🔧 BƯỚC 2: Deploy Backend (FastAPI)

### 2.1. Tạo Web Service
1. Click **"New +"** → **"Web Service"**
2. Chọn **"Build and deploy from a Git repository"**
3. Click **"Connect"** 
4. Nếu chưa kết nối GitHub:
   - Click **"Connect GitHub"**
   - Authorize Render truy cập GitHub
5. Chọn repository **webbandocuoi** (hoặc tên repo của bạn)
6. Click **"Connect"**

### 2.2. Cấu hình Backend Service

**Basic Settings:**
- **Name**: `ivie-be-final` (hoặc tên bạn muốn)
- **Region**: **Singapore**
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: **Docker**
- **Instance Type**: **Free**

**Build Settings:**
- **Dockerfile Path**: `./Dockerfile` (tự động detect)

### 2.3. Thêm Environment Variables

Scroll xuống phần **"Environment Variables"**

Click **"Add Environment Variable"** và thêm từng biến sau:

```
Key: DATABASE_URL
Value: [Paste Internal Database URL từ bước 1.3]

Key: PORT
Value: 8000

Key: SECRET_KEY
Value: [Click "Generate" để tự động tạo]

Key: CORS_ORIGINS
Value: *

Key: PYTHONUNBUFFERED
Value: 1
```

**Lưu ý:** 
- `DATABASE_URL`: Paste URL từ database đã tạo
- `SECRET_KEY`: Click nút "Generate" để Render tự tạo
- `CORS_ORIGINS`: Tạm thời dùng `*`, sau sẽ cập nhật

### 2.4. Deploy Backend
1. Scroll xuống cuối
2. Click **"Create Web Service"**
3. Chờ build (~5-10 phút)
4. Theo dõi logs để xem tiến trình

### 2.5. Kiểm tra Backend
Sau khi deploy xong (status: **Live**):
- URL sẽ là: `https://ivie-be-final.onrender.com`
- Mở trình duyệt, test:
  ```
  https://ivie-be-final.onrender.com/api/health
  ```
- Kết quả mong đợi: `{"status":"healthy"}`

---

## 🌐 BƯỚC 3: Deploy Frontend (Static Site)

### 3.1. Tạo Static Site
1. Click **"New +"** → **"Static Site"**
2. Chọn repository **webbandocuoi**
3. Click **"Connect"**

### 3.2. Cấu hình Frontend

**Basic Settings:**
- **Name**: `ivie-fe-final`
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `./dist`

### 3.3. Thêm Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

```
Key: VITE_API_BASE_URL
Value: https://ivie-be-final.onrender.com

Key: NODE_ENV
Value: production

Key: NODE_OPTIONS
Value: --max-old-space-size=1536
```

**Lưu ý:** Thay `ivie-be-final` bằng tên backend service của bạn

### 3.4. Cấu hình Redirects/Rewrites

Scroll xuống phần **"Redirects/Rewrites"**

Click **"Add Rule"** và điền:

```
Source: /*
Destination: /index.html
Action: Rewrite
```

Điều này đảm bảo React Router hoạt động đúng.

### 3.5. Deploy Frontend
1. Click **"Create Static Site"**
2. Chờ build (~5-8 phút)
3. Frontend sẽ có URL: `https://ivie-fe-final.onrender.com`

### 3.6. Test Frontend
- Mở: `https://ivie-fe-final.onrender.com`
- Kiểm tra trang chủ có hiển thị không
- Kiểm tra có lỗi CORS không (mở Console)

---

## 👨‍💼 BƯỚC 4: Deploy Admin Panel (Streamlit)

### 4.1. Tạo Web Service
1. Click **"New +"** → **"Web Service"**
2. Chọn repository **webbandocuoi**
3. Click **"Connect"**

### 4.2. Cấu hình Admin Service

**Basic Settings:**
- **Name**: `ivie-ad-final`
- **Region**: **Singapore**
- **Branch**: `main`
- **Root Directory**: `admin-python`
- **Runtime**: **Docker**
- **Instance Type**: **Free**

**Build Settings:**
- **Dockerfile Path**: `./Dockerfile`

### 4.3. Thêm Environment Variables

```
Key: API_BASE_URL
Value: https://ivie-be-final.onrender.com

Key: STREAMLIT_SERVER_PORT
Value: 8501

Key: STREAMLIT_SERVER_ADDRESS
Value: 0.0.0.0

Key: STREAMLIT_SERVER_HEADLESS
Value: true

Key: STREAMLIT_SERVER_FILE_WATCHER_TYPE
Value: none

Key: STREAMLIT_SERVER_MAX_UPLOAD_SIZE
Value: 3

Key: STREAMLIT_BROWSER_GATHER_USAGE_STATS
Value: false

Key: STREAMLIT_SERVER_ENABLE_CORS
Value: false

Key: STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION
Value: false

Key: STREAMLIT_THEME_BASE
Value: dark

Key: STREAMLIT_THEME_PRIMARY_COLOR
Value: #b59410
```

### 4.4. Deploy Admin
1. Click **"Create Web Service"**
2. Chờ build (~3-5 phút)
3. Admin URL: `https://ivie-ad-final.onrender.com`

### 4.5. Test Admin
- Mở: `https://ivie-ad-final.onrender.com`
- Đăng nhập với tài khoản admin
- Kiểm tra kết nối với Backend

---

## ✅ BƯỚC 5: Cập Nhật CORS

### 5.1. Lấy URL chính xác
Ghi lại 3 URL:
- Frontend: `https://ivie-fe-final.onrender.com`
- Backend: `https://ivie-be-final.onrender.com`
- Admin: `https://ivie-ad-final.onrender.com`

### 5.2. Cập nhật Backend CORS
1. Vào service **ivie-be-final**
2. Click tab **"Environment"**
3. Tìm biến `CORS_ORIGINS`
4. Click **Edit** (icon bút chì)
5. Sửa value thành:
   ```
   https://ivie-fe-final.onrender.com,https://ivie-ad-final.onrender.com
   ```
6. Click **"Save Changes"**
7. Backend sẽ tự động redeploy (~2 phút)

---

## 🧪 BƯỚC 6: Kiểm Tra Toàn Bộ Hệ Thống

### 6.1. Test Backend API
```
https://ivie-be-final.onrender.com/api/health
→ {"status":"healthy"}

https://ivie-be-final.onrender.com/api/banner/
→ [] hoặc danh sách banner

https://ivie-be-final.onrender.com/docs
→ Swagger UI
```

### 6.2. Test Frontend
- Mở: `https://ivie-fe-final.onrender.com`
- Kiểm tra:
  - ✅ Trang chủ hiển thị
  - ✅ Menu hoạt động
  - ✅ Không có lỗi CORS trong Console
  - ✅ API calls thành công

### 6.3. Test Admin Panel
- Mở: `https://ivie-ad-final.onrender.com`
- Đăng nhập
- Kiểm tra:
  - ✅ Dashboard hiển thị
  - ✅ Có thể xem/thêm/sửa dữ liệu
  - ✅ Upload ảnh hoạt động

---

## 📊 BƯỚC 7: Thêm Dữ Liệu Mẫu (Tùy chọn)

### Cách 1: Qua Backend Shell
1. Vào service **ivie-be-final**
2. Click tab **"Shell"**
3. Click **"Launch Shell"**
4. Chạy lệnh:
   ```bash
   python tao_du_lieu_mau.py
   ```
5. Chờ script chạy xong

### Cách 2: Qua Admin Panel
1. Mở Admin Panel
2. Thêm dữ liệu thủ công qua giao diện

---

## ⚠️ Lưu Ý Quan Trọng (Free Tier)

### Giới hạn Free Tier:
- **RAM**: 512MB per service
- **Auto-sleep**: Service ngủ sau 15 phút không dùng
- **Cold start**: 20-40 giây để wake up lần đầu
- **Build time**: Max 15 phút
- **Hours**: 750 giờ/tháng TỔNG cho tất cả services
- **Mỗi service**: Tối đa 500 giờ/tháng
- **Static site**: Frontend KHÔNG tính giờ sử dụng ✅
- **Lưu ý**: Backend + Admin = 2 services web, cần quản lý giờ sử dụng

### Tính toán giờ sử dụng:
- Backend: ~500 giờ/tháng (max)
- Admin: ~250 giờ/tháng (để dư)
- Frontend: 0 giờ (static site)
- **Tổng**: 750 giờ/tháng

### Giữ Service Active (Tùy chọn):

Dùng **UptimeRobot** (miễn phí) để ping services:

1. Đăng ký tại: https://uptimerobot.com
2. Tạo 2 monitors:
   - **Monitor 1**: 
     - URL: `https://ivie-be-final.onrender.com/api/health`
     - Interval: 5 phút
   - **Monitor 2**: 
     - URL: `https://ivie-ad-final.onrender.com/_stcore/health`
     - Interval: 5 phút

**Lưu ý:** Giữ service active sẽ tốn nhiều giờ hơn!

---

## 🔄 Cập Nhật Code

### Khi có code mới:
```bash
git add .
git commit -m "Update feature X"
git push origin main
```

Render sẽ tự động:
1. Detect thay đổi trong repo
2. Rebuild service bị ảnh hưởng
3. Deploy version mới

### Xem logs deploy:
1. Vào service cần xem
2. Click tab **"Logs"**
3. Theo dõi real-time

---

## 🐛 Xử Lý Lỗi Thường Gặp

### 1. Build Failed - Out of Memory
```
Error: JavaScript heap out of memory
```
**Nguyên nhân**: Frontend build vượt quá 512MB RAM

**Giải pháp**: 
- Đã cấu hình `NODE_OPTIONS=--max-old-space-size=1536`
- Nếu vẫn lỗi, thử build local rồi push `dist/` folder

### 2. Database Connection Failed
```
Error: could not connect to server
```
**Nguyên nhân**: 
- DATABASE_URL sai
- Database chưa sẵn sàng

**Giải pháp**: 
- Kiểm tra DATABASE_URL trong Environment Variables
- Chờ database khởi động xong (~2 phút)
- Dùng **Internal Database URL**, không dùng External

### 3. Health Check Failed
```
Error: Health check failed
```
**Nguyên nhân**: Service không phản hồi đúng endpoint

**Giải pháp**:
- Backend: Kiểm tra endpoint `/api/health` có hoạt động
- Admin: Kiểm tra endpoint `/_stcore/health`
- Xem logs để tìm lỗi cụ thể

### 4. CORS Error
```
Error: Access-Control-Allow-Origin
```
**Nguyên nhân**: Frontend không được phép gọi Backend

**Giải pháp**: 
- Cập nhật `CORS_ORIGINS` trong Backend
- Dùng URL chính xác (không có dấu `/` cuối)
- Redeploy Backend sau khi sửa

### 5. Service Sleep (Cold Start)
```
Service is starting...
```
**Nguyên nhân**: Service ngủ sau 15 phút không dùng

**Giải pháp**: 
- Chờ 20-40 giây để service wake up
- Dùng UptimeRobot để giữ service active
- Hoặc chấp nhận cold start (tiết kiệm giờ)

### 6. 404 Not Found trên Frontend
**Nguyên nhân**: React Router không hoạt động

**Giải pháp**: 
- Kiểm tra Redirects/Rewrites đã cấu hình đúng
- Source: `/*`, Destination: `/index.html`, Action: `Rewrite`

---

## 📈 Monitoring & Logs

### Xem Logs:
1. Vào service cần xem
2. Click tab **"Logs"**
3. Chọn time range
4. Search logs nếu cần

### Xem Metrics:
1. Click tab **"Metrics"**
2. Xem:
   - CPU usage
   - Memory usage
   - Request count
   - Response time

### Alerts:
1. Click tab **"Settings"**
2. Scroll xuống **"Notifications"**
3. Thêm email để nhận thông báo khi:
   - Deploy failed
   - Service down
   - Health check failed

---

## 🎯 Checklist Hoàn Thành

- [ ] Database đã tạo và running
- [ ] Backend deployed và health check OK
- [ ] Frontend deployed và hiển thị trang chủ
- [ ] Admin deployed và đăng nhập được
- [ ] CORS đã cấu hình đúng
- [ ] Không có lỗi trong logs
- [ ] Dữ liệu mẫu đã thêm (nếu cần)
- [ ] UptimeRobot đã setup (nếu muốn)

---

## 📞 Hỗ Trợ

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Community**: https://community.render.com
- **Support**: support@render.com

---

## 🎉 Hoàn Tất!

Sau khi hoàn thành tất cả bước, bạn sẽ có:

✅ **Frontend**: https://ivie-fe-final.onrender.com  
✅ **Backend API**: https://ivie-be-final.onrender.com  
✅ **Admin Panel**: https://ivie-ad-final.onrender.com  
✅ **Database**: PostgreSQL Free Tier  

**Chúc mừng! Website của bạn đã online! 🚀**
