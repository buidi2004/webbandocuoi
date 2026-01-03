# 🚀 Hướng Dẫn Deploy IVIE Wedding lên Render (Free Tier)

## 📋 Yêu Cầu Trước Khi Deploy

1. **Tài khoản GitHub** - Code đã push lên repo
2. **Tài khoản Render** - Đăng ký miễn phí tại [render.com](https://render.com)

---

## 🎯 Deploy Tự Động với Blueprint

### Bước 1: Push code lên GitHub

```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Bước 2: Tạo Blueprint trên Render

1. Đăng nhập [Render Dashboard](https://dashboard.render.com)
2. Click **"New"** → **"Blueprint"**
3. Chọn **"Connect a repository"**
4. Authorize GitHub nếu chưa kết nối
5. Chọn repo **webbandocuoi** (hoặc tên repo của bạn)
6. Render sẽ tự động phát hiện file `render.yaml`
7. Click **"Apply"** để bắt đầu deploy

### Bước 3: Chờ Deploy (~10-15 phút)

Render sẽ tự động tạo theo thứ tự:
1. ✅ **Database** (ivie-db) - ~2 phút
2. ✅ **Backend** (ivie-backend) - ~5 phút  
3. ✅ **Frontend** (ivie-frontend) - ~5 phút
4. ✅ **Admin** (ivie-admin) - ~3 phút

---

## 🌐 URL Sau Khi Deploy

| Service | URL |
|---------|-----|
| Frontend | https://ivie-frontend.onrender.com |
| Backend API | https://ivie-backend.onrender.com |
| Admin Panel | https://ivie-admin.onrender.com |
| API Docs | https://ivie-backend.onrender.com/docs |

---

## ⚠️ Lưu Ý Quan Trọng (Free Tier)

### Giới hạn Free Tier:
- **RAM**: 512MB per service
- **Auto-sleep**: Service ngủ sau 15 phút không dùng
- **Cold start**: 20-40 giây để wake up
- **Build time**: Max 15 phút
- **Hours**: 750 giờ/tháng TỔNG (mỗi service tối đa 500 giờ)
- **Static site**: Frontend không tính giờ sử dụng
- **Lưu ý**: Backend + Admin = 2 services, để auto-sleep để tiết kiệm

### Giữ Service Active (Tùy chọn):
Dùng [UptimeRobot](https://uptimerobot.com) (miễn phí) để ping mỗi 5 phút:
- Monitor 1: `https://ivie-backend.onrender.com/api/health`
- Monitor 2: `https://ivie-admin.onrender.com/_stcore/health`

---

## 🔧 Xử Lý Lỗi Thường Gặp

### 1. Build Failed - Out of Memory
```
Error: JavaScript heap out of memory
```
**Giải pháp**: Đã cấu hình `NODE_OPTIONS=--max-old-space-size=1536` trong render.yaml

### 2. Database Connection Error
```
Error: could not connect to server
```
**Giải pháp**: 
- Chờ database khởi tạo xong (~2 phút)
- Kiểm tra DATABASE_URL trong Environment Variables

### 3. Health Check Failed
```
Error: Health check failed
```
**Giải pháp**:
- Backend: Kiểm tra endpoint `/api/health`
- Admin: Kiểm tra endpoint `/_stcore/health`

### 4. CORS Error
```
Error: Access-Control-Allow-Origin
```
**Giải pháp**: Cập nhật `CORS_ORIGINS` trong backend với URL frontend chính xác

---

## 📊 Kiểm Tra Sau Deploy

1. **Test Backend API**:
   ```
   curl https://ivie-backend.onrender.com/api/health
   ```
   Expected: `{"status":"healthy"}`

2. **Test Frontend**: Mở https://ivie-frontend.onrender.com

3. **Test Admin**: Mở https://ivie-admin.onrender.com
   - Đăng nhập với tài khoản admin

---

## 🔄 Cập Nhật Code

Mỗi khi push code mới lên GitHub, Render sẽ tự động:
1. Detect changes
2. Rebuild service bị thay đổi
3. Deploy version mới

```bash
git add .
git commit -m "Update feature X"
git push origin main
# Render tự động deploy
```

---

## 💡 Tips Tối Ưu Free Tier

1. **Frontend là Static Site** → Không tính giờ sử dụng
2. **Chỉ dùng 1 worker** cho Backend/Admin → Tiết kiệm RAM
3. **Tắt file watcher** trong Streamlit → Giảm 30-50MB RAM
4. **Giảm max upload size** → Tránh OOM khi upload ảnh lớn
5. **Dùng UptimeRobot** → Giữ service không bị sleep

---

## 📞 Hỗ Trợ

- Render Docs: https://render.com/docs
- Render Status: https://status.render.com
- Community: https://community.render.com
