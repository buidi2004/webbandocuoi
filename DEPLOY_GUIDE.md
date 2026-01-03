# 🚀 HƯỚNG DẪN DEPLOY IVIE WEDDING STUDIO LÊN RENDER

## 📋 Tổng quan

Dự án IVIE Wedding Studio bao gồm 3 service cần deploy:

| Service | Công nghệ | Port | URL Example |
|---------|-----------|------|-------------|
| Backend API | FastAPI + Python 3.12 | 8000 | ivie-backend.onrender.com |
| Frontend | React + Vite + Nginx | 80 | ivie-frontend.onrender.com |
| Admin Panel | Streamlit + Python 3.11 | 8501 | ivie-admin.onrender.com |

---

## 🔧 Chuẩn bị trước khi Deploy

### 1. Tài khoản cần có
- [x] GitHub account
- [x] Render account (https://render.com)
- [x] (Optional) Gmail cho SMTP notifications
- [x] (Optional) Telegram Bot Token

### 2. Push code lên GitHub

```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit - IVIE Wedding Studio"

# Thêm remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push lên GitHub
git push -u origin main
```

---

## 📦 BƯỚC 1: Tạo Database PostgreSQL

1. Đăng nhập **Render Dashboard** → **New** → **PostgreSQL**

2. Điền thông tin:
   - **Name**: `ivie-db`
   - **Database**: `ivie_wedding`
   - **User**: `ivie_user`
   - **Region**: Singapore (gần Việt Nam nhất)
   - **Plan**: Free

3. Click **Create Database**

4. **Quan trọng**: Copy **Internal Database URL** để dùng cho Backend

---

## 🖥️ BƯỚC 2: Deploy Backend API

### 2.1 Tạo Web Service

1. **Render Dashboard** → **New** → **Web Service**

2. Kết nối GitHub repo của bạn

3. Cấu hình:
   ```
   Name: ivie-backend
   Region: Singapore
   Branch: main
   Root Directory: backend
   Runtime: Docker
   Plan: Free
   ```

### 2.2 Thiết lập Environment Variables

Trong tab **Environment**, thêm các biến sau:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Paste Internal Database URL từ bước 1) |
| `SECRET_KEY` | `your_super_secret_key_2024_random_string` |
| `CORS_ORIGINS` | `https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com` |
| `PYTHON_VERSION` | `3.12` |

**Optional (Email & Telegram notifications):**
| Key | Value |
|-----|-------|
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | `your_email@gmail.com` |
| `SMTP_PASSWORD` | `your_gmail_app_password` |
| `NOTIFY_RECEIVER_EMAIL` | `admin@yourdomain.com` |
| `TELEGRAM_BOT_TOKEN` | `your_telegram_bot_token` |
| `TELEGRAM_CHAT_ID` | `your_chat_id` |

### 2.3 Health Check

```
Health Check Path: /api/health
```

### 2.4 Click **Create Web Service**

⏳ Đợi 5-10 phút để build và deploy.

✅ Kiểm tra: Truy cập `https://ivie-backend.onrender.com/docs`

---

## 🌐 BƯỚC 3: Deploy Frontend

### 3.1 Tạo Web Service

1. **Render Dashboard** → **New** → **Web Service**

2. Cấu hình:
   ```
   Name: ivie-frontend
   Region: Singapore
   Branch: main
   Root Directory: frontend
   Runtime: Docker
   Plan: Free
   ```

### 3.2 Environment Variables

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://ivie-backend.onrender.com` |

### 3.3 Click **Create Web Service**

⏳ Đợi 3-5 phút.

✅ Kiểm tra: Truy cập `https://ivie-frontend.onrender.com`

---

## 👨‍💼 BƯỚC 4: Deploy Admin Panel

### 4.1 Tạo Web Service

1. **Render Dashboard** → **New** → **Web Service**

2. Cấu hình:
   ```
   Name: ivie-admin
   Region: Singapore
   Branch: main
   Root Directory: admin-python
   Runtime: Docker
   Plan: Free
   ```

### 4.2 Environment Variables

| Key | Value |
|-----|-------|
| `API_BASE_URL` | `https://ivie-backend.onrender.com` |

### 4.3 Health Check

```
Health Check Path: /_stcore/health
```

### 4.4 Click **Create Web Service**

⏳ Đợi 5-10 phút.

✅ Kiểm tra: Truy cập `https://ivie-admin.onrender.com`

---

## 🔄 BƯỚC 5: Cập nhật CORS (Backend)

Sau khi có URL thực của Frontend và Admin, quay lại Backend service:

1. Vào **Environment** tab
2. Cập nhật `CORS_ORIGINS`:
   ```
   https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com
   ```
3. Click **Save Changes** → Service sẽ tự động redeploy

---

## 📱 Deploy nhanh với render.yaml (Blueprint)

Nếu bạn muốn deploy tất cả cùng lúc, sử dụng file `render.yaml`:

1. Vào **Render Dashboard** → **Blueprints** → **New Blueprint Instance**

2. Kết nối GitHub repo

3. Render sẽ tự động đọc file `render.yaml` và tạo tất cả services

4. Chỉ cần điền các secret values và click **Apply**

---

## 🔐 Đăng nhập Admin Panel

**Tài khoản mặc định:**
- Username: `admin`
- Password: `admin123`

**⚠️ QUAN TRỌNG**: Đổi mật khẩu ngay sau khi deploy!

Để tạo password hash mới:
```python
import bcrypt
password = "your_new_password"
hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(hash.decode())
```

---

## 🐛 Xử lý lỗi thường gặp

### 1. Backend không kết nối được Database
```
Lỗi: could not connect to server
```
**Giải pháp**: Kiểm tra `DATABASE_URL` có đúng format không:
```
postgresql://user:password@host:5432/database
```

### 2. CORS Error
```
Lỗi: Access-Control-Allow-Origin
```
**Giải pháp**: Thêm URL frontend vào `CORS_ORIGINS` trong backend

### 3. Admin Panel load chậm
```
Lỗi: Timeout hoặc Server starting...
```
**Giải pháp**: Render Free tier sẽ sleep sau 15 phút không hoạt động. Lần đầu truy cập mất 30-60s để wake up.

### 4. Image upload không hoạt động
**Giải pháp**: Kiểm tra thư mục `tep_tin` có quyền write không. Trên Render, dùng CDN như Cloudinary hoặc ImgBB.

### 5. Build failed
```
Lỗi: ModuleNotFoundError
```
**Giải pháp**: Kiểm tra `requirements.txt` có đầy đủ packages không.

---

## 📊 Monitoring & Logs

### Xem logs realtime:
1. Vào service trên Render
2. Click tab **Logs**
3. Chọn **Live tail** để xem realtime

### Health check:
- Backend: `https://ivie-backend.onrender.com/api/health`
- Admin: `https://ivie-admin.onrender.com/_stcore/health`

---

## 🔄 Auto Deploy

Render tự động deploy khi bạn push code mới lên GitHub:

```bash
git add .
git commit -m "Update: your changes"
git push origin main
```

Sau 2-5 phút, service sẽ được cập nhật tự động.

---

## 💰 Nâng cấp lên Paid Plan

Free tier có giới hạn:
- Sleep sau 15 phút không hoạt động
- 750 giờ/tháng
- RAM 512MB

**Khuyến nghị cho Production:**
- Backend: Starter ($7/tháng) - Không sleep, 512MB RAM
- Frontend: Static Site (Free) - Vì build thành HTML/CSS/JS
- Admin: Starter ($7/tháng)
- Database: Starter ($7/tháng) - 1GB storage

---

## 📞 Hỗ trợ

Nếu gặp vấn đề khi deploy:
1. Kiểm tra **Logs** trên Render
2. Đọc lại hướng dẫn này
3. Tìm kiếm lỗi trên Google/Stack Overflow
4. Liên hệ support@render.com

---

**🎉 Chúc bạn deploy thành công!**