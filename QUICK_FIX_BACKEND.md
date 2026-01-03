# 🚀 Quick Fix: Deploy Backend Lên Render

## ⚡ Các Bước Nhanh (5 phút)

### 1. Vào Render Dashboard
- URL: https://dashboard.render.com
- Đăng nhập bằng GitHub

### 2. Tạo Web Service
- Click **"New +"** → **"Web Service"**
- Click **"Build and deploy from a Git repository"**
- Click **"Next"**

### 3. Connect Repository
- Tìm repo: **webbandocuoi**
- Click **"Connect"**

### 4. Cấu Hình Service

**Điền chính xác:**

| Field | Giá Trị |
|-------|---------|
| Name | `ivie-backend` |
| Region | `Singapore` |
| Branch | `main` |
| Root Directory | `backend` ⚠️ |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn ung_dung.chinh:ung_dung --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 60` |
| Plan | **Free** |

### 5. Thêm Environment Variables

Click **"Add Environment Variable"** và thêm:

#### DATABASE_URL
```
Key: DATABASE_URL
Value: postgresql://ivie_user:vdaVborVkAZSCpYGqRFE8GYFXrc5MBgJ@dpg-d5cj5uvgi27c73f2jgag-a.singapore-postgres.render.com/ivie_wedding_3wcl
```

#### PORT
```
Key: PORT
Value: 8000
```

#### PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.12.0
```

#### CORS_ORIGINS (QUAN TRỌNG!)
```
Key: CORS_ORIGINS
Value: https://ivie-wedding-frontend.vercel.app,http://localhost:5173,http://localhost:3000
```

⚠️ **Thay `https://ivie-wedding-frontend.vercel.app` bằng URL Vercel thực tế của bạn!**

### 6. Create Service
- Click **"Create Web Service"**
- Chờ 5-10 phút để build

### 7. Kiểm Tra
Sau khi build xong:
- Copy URL Backend (ví dụ: `https://ivie-backend.onrender.com`)
- Mở browser, vào: `https://ivie-backend.onrender.com/api/health`
- Nếu thấy `{"status":"healthy"}` → Thành công!

---

## 🔗 Sau Khi Backend Chạy

### Cập Nhật Frontend (Vercel)

1. Vào Vercel Dashboard
2. Chọn project Frontend
3. Settings → Environment Variables
4. Thêm/Cập nhật:
```
Key: VITE_API_URL
Value: https://ivie-backend.onrender.com
```
5. Deployments → Redeploy

---

## ❌ Nếu Build Failed

### Lỗi Thường Gặp:

#### 1. "No module named 'ung_dung'"
**Nguyên nhân:** Root Directory sai
**Fix:** Đảm bảo Root Directory = `backend`

#### 2. "gunicorn: command not found"
**Nguyên nhân:** Thiếu gunicorn trong requirements.txt
**Fix:** Kiểm tra file `backend/requirements.txt` có dòng:
```
gunicorn==21.2.0
uvicorn[standard]==0.24.0
```

#### 3. "Database connection failed"
**Nguyên nhân:** DATABASE_URL sai
**Fix:** Kiểm tra lại DATABASE_URL trong Environment Variables

#### 4. "Port already in use"
**Nguyên nhân:** Start command sai
**Fix:** Đảm bảo Start Command có `$PORT` (không phải 8000 cố định)

---

## 📞 Cần Trợ Giúp?

Nếu vẫn gặp lỗi:
1. Chụp màn hình Logs tab
2. Chụp màn hình Environment Variables
3. Gửi cho tôi để debug
