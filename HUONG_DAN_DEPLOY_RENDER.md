# 🚀 HƯỚNG DẪN DEPLOY LÊN RENDER (THỦ CÔNG)

## 📋 MỤC LỤC
1. [Chuẩn bị](#1-chuẩn-bị)
2. [Deploy Backend API](#2-deploy-backend-api)
3. [Deploy Frontend](#3-deploy-frontend)
4. [Deploy Admin Panel](#4-deploy-admin-panel)
5. [Cấu hình sau khi deploy](#5-cấu-hình-sau-khi-deploy)
6. [Kiểm tra và troubleshooting](#6-kiểm-tra-và-troubleshooting)

---

## 1. CHUẨN BỊ

### 1.1. Tài khoản cần thiết
- ✅ Tài khoản GitHub (đã có repository)
- ✅ Tài khoản Render.com (đăng ký miễn phí tại https://render.com)
- ✅ Code đã push lên GitHub

### 1.2. Kiểm tra repository
```bash
git status
git push origin main
```

### 1.3. Đảm bảo các file cần thiết
- ✅ `render.yaml` (đã có)
- ✅ `backend/requirements.txt` (đã có)
- ✅ `admin-python/requirements.txt` (đã có)
- ✅ `frontend/package.json` (đã có)

---

## 2. DEPLOY BACKEND API

### Bước 1: Tạo Web Service cho Backend
1. Đăng nhập vào https://dashboard.render.com
2. Click **"New +"** → Chọn **"Web Service"**
3. Chọn **"Build and deploy from a Git repository"**
4. Click **"Connect account"** để kết nối GitHub
5. Chọn repository: **`webbandocuoi`**
6. Click **"Connect"**

### Bước 2: Cấu hình Backend Service
Điền thông tin như sau:

**Basic Settings:**
- **Name**: `ivie-backend-api` (hoặc tên bạn muốn)
- **Region**: `Singapore` (gần Việt Nam nhất)
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Chọn **"Free"** (miễn phí)

**Environment Variables:**
Click **"Add Environment Variable"** và thêm:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.0` |
| `SECRET_KEY` | `ivie-secret-key-2024-production` |
| `CORS_ORIGINS` | `https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com` |
| `TELEGRAM_BOT_TOKEN` | `(token bot telegram của bạn)` |
| `TELEGRAM_CHAT_ID` | `(chat ID telegram của bạn)` |

**⚠️ LƯU Ý**: Sau khi tạo Frontend và Admin, bạn sẽ cập nhật lại `CORS_ORIGINS` với URL thực tế.

### Bước 3: Deploy
1. Click **"Create Web Service"**
2. Đợi 5-10 phút để Render build và deploy
3. Sau khi deploy xong, bạn sẽ có URL dạng: `https://ivie-backend-api.onrender.com`

### Bước 4: Kiểm tra Backend
Mở trình duyệt và truy cập:
```
https://ivie-backend-api.onrender.com/docs
```
Bạn sẽ thấy trang Swagger API documentation.

---

## 3. DEPLOY FRONTEND

### Bước 1: Cập nhật file .env.production
Trước khi deploy, cập nhật URL backend trong file `frontend/.env.production`:

```env
VITE_API_URL=https://ivie-backend-api.onrender.com
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
```

**Commit và push:**
```bash
git add frontend/.env.production
git commit -m "update: backend URL for production"
git push origin main
```

### Bước 2: Tạo Static Site cho Frontend
1. Vào https://dashboard.render.com
2. Click **"New +"** → Chọn **"Static Site"**
3. Chọn repository: **`webbandocuoi`**
4. Click **"Connect"**

### Bước 3: Cấu hình Frontend
**Basic Settings:**
- **Name**: `ivie-frontend`
- **Branch**: `main`
- **Root Directory**: `frontend`
- **Build Command**:
  ```bash
  npm install && npm run build
  ```
- **Publish Directory**: `dist`

**Environment Variables:**
Click **"Add Environment Variable"** và thêm:

| Key | Value |
|-----|-------|
| `NODE_VERSION` | `20.11.0` |
| `VITE_API_URL` | `https://ivie-backend-api.onrender.com` |

### Bước 4: Deploy
1. Click **"Create Static Site"**
2. Đợi 5-10 phút để build
3. Sau khi deploy xong, bạn sẽ có URL dạng: `https://ivie-frontend.onrender.com`

### Bước 5: Kiểm tra Frontend
Mở trình duyệt và truy cập URL frontend của bạn.

---

## 4. DEPLOY ADMIN PANEL

### Bước 1: Tạo Web Service cho Admin
1. Vào https://dashboard.render.com
2. Click **"New +"** → Chọn **"Web Service"**
3. Chọn repository: **`webbandocuoi`**
4. Click **"Connect"**

### Bước 2: Cấu hình Admin Service
**Basic Settings:**
- **Name**: `ivie-admin-panel`
- **Region**: `Singapore`
- **Branch**: `main`
- **Root Directory**: `admin-python`
- **Runtime**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```bash
  streamlit run quan_tri.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
  ```

**Instance Type:**
- Chọn **"Free"**

**Environment Variables:**
Click **"Add Environment Variable"** và thêm:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.12.0` |
| `API_BASE_URL` | `https://ivie-backend-api.onrender.com` |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `admin123` |

### Bước 3: Deploy
1. Click **"Create Web Service"**
2. Đợi 5-10 phút để deploy
3. Sau khi deploy xong, bạn sẽ có URL dạng: `https://ivie-admin-panel.onrender.com`

### Bước 4: Kiểm tra Admin
1. Mở trình duyệt và truy cập URL admin
2. Đăng nhập với:
   - Username: `admin`
   - Password: `admin123`

---

## 5. CẤU HÌNH SAU KHI DEPLOY

### 5.1. Cập nhật CORS_ORIGINS cho Backend
Sau khi có URL Frontend và Admin, cập nhật lại biến môi trường:

1. Vào Backend service trên Render Dashboard
2. Click tab **"Environment"**
3. Sửa `CORS_ORIGINS`:
   ```
   https://ivie-frontend.onrender.com,https://ivie-admin-panel.onrender.com
   ```
4. Click **"Save Changes"**
5. Service sẽ tự động restart

### 5.2. Cập nhật API URL trong Frontend (nếu cần)
Nếu URL backend thay đổi:
1. Sửa file `frontend/.env.production`
2. Commit và push
3. Frontend sẽ tự động rebuild

### 5.3. Tạo Custom Domain (Tùy chọn)
Nếu bạn có tên miền riêng:

**Cho Frontend:**
1. Vào Frontend service → Tab **"Settings"**
2. Scroll xuống **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Nhập domain: `www.iviestudio.vn`
5. Cấu hình DNS theo hướng dẫn của Render

**Cho Backend:**
1. Vào Backend service → Tab **"Settings"**
2. Add domain: `api.iviestudio.vn`

**Cho Admin:**
1. Vào Admin service → Tab **"Settings"**
2. Add domain: `admin.iviestudio.vn`

---

## 6. KIỂM TRA VÀ TROUBLESHOOTING

### 6.1. Kiểm tra các service
✅ **Backend API**: https://ivie-backend-api.onrender.com/docs
✅ **Frontend**: https://ivie-frontend.onrender.com
✅ **Admin**: https://ivie-admin-panel.onrender.com

### 6.2. Xem logs
Nếu có lỗi:
1. Vào service trên Render Dashboard
2. Click tab **"Logs"**
3. Xem log để debug

### 6.3. Các lỗi thường gặp

#### Lỗi 1: CORS Error
**Triệu chứng**: Frontend không kết nối được Backend
**Giải pháp**: 
- Kiểm tra `CORS_ORIGINS` trong Backend environment variables
- Đảm bảo có đúng URL của Frontend và Admin

#### Lỗi 2: Build Failed
**Triệu chứng**: Service không build được
**Giải pháp**:
- Kiểm tra logs để xem lỗi cụ thể
- Đảm bảo `requirements.txt` hoặc `package.json` đúng
- Kiểm tra Python/Node version

#### Lỗi 3: Service Sleep (Free Plan)
**Triệu chứng**: Service chậm khi truy cập lần đầu
**Giải pháp**:
- Đây là hạn chế của Free plan
- Service sẽ sleep sau 15 phút không hoạt động
- Lần truy cập đầu tiên sẽ mất 30-60 giây để wake up
- Nâng cấp lên Paid plan để tránh sleep

#### Lỗi 4: Database không có dữ liệu
**Triệu chứng**: Trang web không hiển thị sản phẩm
**Giải pháp**:
- Truy cập Admin panel
- Thêm dữ liệu mẫu (sản phẩm, combo, v.v.)

### 6.4. Monitoring
Render cung cấp:
- **Metrics**: CPU, Memory usage
- **Logs**: Real-time logs
- **Events**: Deploy history

---

## 7. CẬP NHẬT CODE

Khi bạn cập nhật code:

```bash
# 1. Commit changes
git add .
git commit -m "update: your changes"

# 2. Push to GitHub
git push origin main

# 3. Render sẽ tự động deploy lại
```

**Auto-deploy**: Render tự động deploy khi có commit mới trên branch `main`.

**Manual deploy**: 
1. Vào service trên Dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 8. BACKUP VÀ BẢO MẬT

### 8.1. Backup Database
```bash
# Download database từ backend
curl https://ivie-backend-api.onrender.com/api/backup/database -o backup.db
```

### 8.2. Thay đổi mật khẩu Admin
1. Vào Admin service → Environment
2. Sửa `ADMIN_PASSWORD`
3. Save và restart

### 8.3. Bảo mật SECRET_KEY
- Không commit SECRET_KEY vào Git
- Chỉ lưu trong Environment Variables trên Render

---

## 9. CHI PHÍ

### Free Plan (Hiện tại)
- ✅ Backend: Free (750 giờ/tháng)
- ✅ Frontend: Free (100GB bandwidth/tháng)
- ✅ Admin: Free (750 giờ/tháng)
- ⚠️ Service sleep sau 15 phút không hoạt động
- ⚠️ Shared CPU/RAM

### Paid Plan (Nếu cần)
- **Starter**: $7/tháng/service
  - Không sleep
  - Dedicated resources
  - Custom domain miễn phí

---

## 10. LIÊN HỆ HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra logs trên Render Dashboard
2. Xem documentation: https://render.com/docs
3. Liên hệ Render Support: https://render.com/support

---

## 📝 CHECKLIST HOÀN THÀNH

- [ ] Backend API đã deploy và chạy được
- [ ] Frontend đã deploy và hiển thị đúng
- [ ] Admin Panel đã deploy và đăng nhập được
- [ ] CORS đã cấu hình đúng
- [ ] Frontend kết nối được Backend
- [ ] Admin kết nối được Backend
- [ ] Đã thêm dữ liệu mẫu vào database
- [ ] Đã test các chức năng chính
- [ ] Đã cấu hình custom domain (nếu có)

---

**🎉 CHÚC MỪNG! Bạn đã deploy thành công ứng dụng lên Render!**
