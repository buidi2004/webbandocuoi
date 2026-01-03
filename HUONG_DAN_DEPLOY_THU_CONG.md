# 🚀 Hướng Dẫn Deploy Thủ Công lên Render (Free Tier)

## 📋 Chuẩn Bị

1. Tài khoản GitHub (đã push code)
2. Tài khoản Render (đăng ký miễn phí tại render.com)

---

## 🗄️ BƯỚC 1: Tạo PostgreSQL Database

### 1.1. Vào Render Dashboard
- Truy cập: https://dashboard.render.com
- Đăng nhập tài khoản

### 1.2. Tạo Database
1. Click **"New"** → **"PostgreSQL"**
2. Điền thông tin:
   - **Name**: `ivie-db`
   - **Database**: `ivie_wedding`
   - **User**: `ivie_user`
   - **Region**: `Singapore`
   - **Plan**: **Free**
3. Click **"Create Database"**
4. Chờ ~2 phút để database khởi tạo

### 1.3. Lưu Database URL
- Sau khi tạo xong, vào tab **"Info"**
- Copy **"Internal Database URL"** (dạng: `postgresql://...`)
- Lưu lại để dùng cho Backend

---

## 🔧 BƯỚC 2: Deploy Backend (FastAPI)

### 2.1. Tạo Web Service
1. Click **"New"** → **"Web Service"**
2. Chọn **"Build and deploy from a Git repository"**
3. Click **"Connect"** → Chọn repo **webbandocuoi**

### 2.2. Cấu hình Backend
Điền thông tin:

**Basic:**
- **Name**: `ivie-backend`
- **Region**: `Singapore`
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Docker`
- **Plan**: **Free**

**Build & Deploy:**
- **Dockerfile Path**: `./Dockerfile`

### 2.3. Thêm Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Thêm các biến sau:

```
DATABASE_URL = [Paste Internal Database URL từ bước 1.3]
SECRET_KEY = [Click "Generate" để tự động tạo]
CORS_ORIGINS = https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com
PORT = 8000
WEB_CONCURRENCY = 1
WORKERS = 1
GUNICORN_TIMEOUT = 60
MAX_REQUESTS = 500
MAX_REQUESTS_JITTER = 50
```

### 2.4. Deploy
1. Click **"Create Web Service"**
2. Chờ build (~5-7 phút)
3. Sau khi deploy xong, URL sẽ là: `https://ivie-backend.onrender.com`

### 2.5. Kiểm tra Backend
Mở trình duyệt, truy cập:
```
https://ivie-backend.onrender.com/api/health
```
Kết quả: `{"status":"healthy"}`

---

## 🌐 BƯỚC 3: Deploy Frontend (Static Site)

### 3.1. Tạo Static Site
1. Click **"New"** → **"Static Site"**
2. Chọn repo **webbandocuoi**

### 3.2. Cấu hình Frontend
Điền thông tin:

**Basic:**
- **Name**: `ivie-frontend`
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Build Command**: `npm ci && npm run build`
- **Publish Directory**: `./dist`

### 3.3. Thêm Environment Variables
```
VITE_API_BASE_URL = https://ivie-backend.onrender.com
NODE_ENV = production
NODE_OPTIONS = --max-old-space-size=1536
```

### 3.4. Cấu hình Redirects/Rewrites
Scroll xuống **"Redirects/Rewrites"** → Click **"Add Rule"**

```
Source: /*
Destination: /index.html
Action: Rewrite
```

### 3.5. Deploy
1. Click **"Create Static Site"**
2. Chờ build (~5-8 phút)
3. URL: `https://ivie-frontend.onrender.com`

---

## 👨‍💼 BƯỚC 4: Deploy Admin Panel (Streamlit)

### 4.1. Tạo Web Service
1. Click **"New"** → **"Web Service"**
2. Chọn repo **webbandocuoi**

### 4.2. Cấu hình Admin
**Basic:**
- **Name**: `ivie-admin`
- **Region**: `Singapore`
- **Branch**: `main`
- **Root Directory**: `admin-python`
- **Runtime**: `Docker`
- **Plan**: **Free**

**Build & Deploy:**
- **Dockerfile Path**: `./Dockerfile`

### 4.3. Thêm Environment Variables
```
API_BASE_URL = https://ivie-backend.onrender.com
STREAMLIT_SERVER_PORT = 8501
STREAMLIT_SERVER_ADDRESS = 0.0.0.0
STREAMLIT_SERVER_HEADLESS = true
STREAMLIT_SERVER_FILE_WATCHER_TYPE = none
STREAMLIT_SERVER_MAX_UPLOAD_SIZE = 3
STREAMLIT_BROWSER_GATHER_USAGE_STATS = false
STREAMLIT_SERVER_ENABLE_CORS = false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION = false
STREAMLIT_THEME_BASE = dark
STREAMLIT_THEME_PRIMARY_COLOR = #b59410
```

### 4.4. Deploy
1. Click **"Create Web Service"**
2. Chờ build (~3-5 phút)
3. URL: `https://ivie-admin.onrender.com`

---

## ✅ BƯỚC 5: Cập Nhật CORS

### 5.1. Cập nhật Backend CORS
1. Vào service **ivie-backend**
2. Tab **"Environment"**
3. Sửa biến `CORS_ORIGINS`:
```
CORS_ORIGINS = https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com
```
4. Click **"Save Changes"**
5. Backend sẽ tự động redeploy

---

## 🧪 BƯỚC 6: Kiểm Tra

### 6.1. Test Backend
```
https://ivie-backend.onrender.com/api/health
→ {"status":"healthy"}

https://ivie-backend.onrender.com/api/banner/
→ [] (hoặc danh sách banner)
```

### 6.2. Test Frontend
- Mở: `https://ivie-frontend.onrender.com`
- Kiểm tra trang chủ hiển thị

### 6.3. Test Admin
- Mở: `https://ivie-admin.onrender.com`
- Đăng nhập với tài khoản admin

---

## 📊 BƯỚC 7: Thêm Dữ Liệu Mẫu (Tùy chọn)

### 7.1. Truy cập Backend Shell
1. Vào service **ivie-backend**
2. Tab **"Shell"**
3. Click **"Launch Shell"**

### 7.2. Chạy Script Tạo Dữ Liệu
```bash
python tao_du_lieu_mau.py
```

Hoặc tạo dữ liệu qua Admin Panel.

---

## ⚠️ Lưu Ý Quan Trọng (Free Tier)

### Giới hạn:
- **RAM**: 512MB per service
- **Auto-sleep**: 15 phút không dùng
- **Cold start**: 20-40 giây
- **Build time**: Max 15 phút
- **Hours**: 750 giờ/tháng TỔNG (mỗi service tối đa 500 giờ)
- **Static site**: Frontend không tính giờ sử dụng
- **Lưu ý**: Backend + Admin = 2 services, cần để auto-sleep để tiết kiệm giờ

### Giữ Service Active:
Dùng [UptimeRobot](https://uptimerobot.com) (miễn phí):
1. Đăng ký tài khoản
2. Tạo 2 monitors:
   - `https://ivie-backend.onrender.com/api/health` (mỗi 5 phút)
   - `https://ivie-admin.onrender.com/_stcore/health` (mỗi 5 phút)

---

## 🔄 Cập Nhật Code

Mỗi khi push code mới:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render tự động detect và redeploy service bị thay đổi.

---

## 🐛 Xử Lý Lỗi

### Lỗi: Build Failed (Out of Memory)
**Nguyên nhân**: Frontend build vượt quá RAM
**Giải pháp**: Đã cấu hình `NODE_OPTIONS=--max-old-space-size=1536`

### Lỗi: Database Connection Failed
**Nguyên nhân**: DATABASE_URL sai hoặc database chưa sẵn sàng
**Giải pháp**: 
- Kiểm tra DATABASE_URL trong Environment Variables
- Chờ database khởi động xong (~2 phút)

### Lỗi: Health Check Failed
**Nguyên nhân**: Service không phản hồi đúng endpoint
**Giải pháp**:
- Backend: Kiểm tra `/api/health`
- Admin: Kiểm tra `/_stcore/health`

### Lỗi: CORS Error
**Nguyên nhân**: Frontend không được phép gọi Backend
**Giải pháp**: Cập nhật `CORS_ORIGINS` trong Backend với URL frontend chính xác

---

## 📞 Hỗ Trợ

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Community: https://community.render.com

---

## 🎉 Hoàn Tất!

Sau khi hoàn thành tất cả bước, bạn sẽ có:
- ✅ Frontend: https://ivie-frontend.onrender.com
- ✅ Backend: https://ivie-backend.onrender.com
- ✅ Admin: https://ivie-admin.onrender.com
- ✅ Database: PostgreSQL Free Tier
