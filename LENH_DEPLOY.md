# 🚀 LỆNH DEPLOY LÊN RENDER (BLUEPRINT)

## ✅ Tóm tắt kiểm tra

### File đã sẵn sàng:
- ✅ `render.yaml` - Blueprint đã tối ưu FREE TIER
- ✅ `backend/Dockerfile` - Tối ưu 200MB RAM
- ✅ `backend/start.sh` - 1 worker, timeout 60s
- ✅ `backend/requirements.txt` - Đầy đủ dependencies
- ✅ `frontend/package.json` - Build script OK
- ✅ `frontend/vite.config.js` - Tối ưu build
- ✅ `admin-python/Dockerfile` - Tối ưu 180MB RAM
- ✅ `admin-python/quan_tri_optimized_v2.py` - Main app
- ✅ `.gitignore` - Đã cấu hình đúng

### Repository:
- URL: `https://github.com/buidi2004/webbandocuoi.git`
- Branch: `main`
- Status: 1 commit chưa push

---

## 📝 BƯỚC 1: XÓA FILE KHÔNG CẦN THIẾT (OPTIONAL)

```bash
# Xóa file Python cache (nếu có)
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Xóa file test/demo không cần thiết
rm -f check_render_config.py
rm -f ivie.db 2>/dev/null
```

---

## 📦 BƯỚC 2: ADD VÀ COMMIT

```bash
# Di chuyển vào thư mục project
cd D:\webdichvumedia

# Kiểm tra status
git status

# Add tất cả file đã thay đổi
git add .

# Commit với message rõ ràng
git commit -m "Optimized for Render Free Tier - Blueprint ready

- Backend: 1 worker, 200MB RAM, timeout 60s
- Frontend: Static site, optimized build
- Admin: Streamlit optimized, 180MB RAM
- Database: PostgreSQL free tier
- Total: ~380MB RAM < 512MB limit
- Build time: 5-8 minutes per service
- Ready for production deployment"
```

---

## 🌐 BƯỚC 3: PUSH LÊN GITHUB

```bash
# Push lên GitHub repository
git push origin main

# Nếu bị lỗi authentication, sử dụng Personal Access Token
# Settings → Developer settings → Personal access tokens → Generate new token
```

---

## 🎯 BƯỚC 4: DEPLOY TRÊN RENDER

### Option A: Deploy qua Dashboard (Khuyến nghị)

1. **Mở Render Dashboard**
   - Truy cập: https://dashboard.render.com
   - Đăng nhập bằng GitHub (nếu chưa)

2. **Kết nối GitHub Repository**
   - Click nút **"New +"** ở góc trên bên phải
   - Chọn **"Blueprint"**
   - Chọn repository: **`buidi2004/webbandocuoi`**
   - Render sẽ tự động phát hiện file `render.yaml`

3. **Review Blueprint**
   - Xem qua các services sẽ được tạo:
     ```
     ✅ Database: ivie-db (PostgreSQL Free)
     ✅ Backend: ivie-backend (Docker, Free)
     ✅ Frontend: ivie-frontend (Static, Free)
     ✅ Admin: ivie-admin (Docker, Free)
     ```

4. **Click "Apply"**
   - Render bắt đầu tạo tất cả services
   - Theo dõi progress trong Dashboard

### Option B: Deploy qua Render CLI (Advanced)

```bash
# Cài đặt Render CLI
npm install -g @render/cli

# Đăng nhập
render login

# Deploy blueprint
render blueprint deploy --yes

# Theo dõi logs
render logs -s ivie-backend --tail
```

---

## ⏱️ BƯỚC 5: THEO DÕI QUẮT TRÌNH DEPLOY

### Thời gian dự kiến:
```
[1-2 phút]   🗄️  Database: ivie-db
[3-5 phút]   🔧  Backend: ivie-backend
[5-8 phút]   🌐  Frontend: ivie-frontend
[3-4 phút]   🎛️  Admin: ivie-admin
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[12-19 phút] ✅  Tất cả services LIVE
```

### Xem logs từng service:

**Database:**
```
Dashboard → ivie-db → Info
- Status: Available (màu xanh)
- Connection string: Internal Database URL
```

**Backend:**
```
Dashboard → ivie-backend → Logs
[Build] Installing dependencies...
[Build] Building Docker image...
[Deploy] Starting gunicorn...
[Deploy] Server started on port 8000
✅ Service live at: https://ivie-backend.onrender.com
```

**Frontend:**
```
Dashboard → ivie-frontend → Logs
[Build] npm ci --production=false
[Build] npm run build
[Build] Build complete: dist/
[Deploy] Deploying to CDN...
✅ Service live at: https://ivie-frontend.onrender.com
```

**Admin:**
```
Dashboard → ivie-admin → Logs
[Build] Installing Streamlit...
[Build] Building Docker image...
[Deploy] Starting Streamlit...
[Deploy] You can now view your Streamlit app
✅ Service live at: https://ivie-admin.onrender.com
```

---

## 🔍 BƯỚC 6: KIỂM TRA SAU KHI DEPLOY

### 1. Kiểm tra tất cả services LIVE
```bash
# Dashboard phải hiển thị:
✅ ivie-db: Available (màu xanh)
✅ ivie-backend: Live (màu xanh)
✅ ivie-frontend: Live (màu xanh)
✅ ivie-admin: Live (màu xanh)
```

### 2. Test Backend API
```bash
# Health check
curl https://ivie-backend.onrender.com/api/health

# Kết quả mong đợi:
{"status":"healthy","timestamp":"2024-01-15T10:30:00Z"}

# API Documentation
https://ivie-backend.onrender.com/docs
```

### 3. Test Frontend
```bash
# Truy cập trang chủ
https://ivie-frontend.onrender.com

# Kiểm tra:
✅ Trang chủ hiển thị đúng
✅ Menu navigation hoạt động
✅ Trang dịch vụ load được data từ API
✅ Trang combo hiển thị đúng
✅ Form liên hệ hoạt động
```

### 4. Test Admin Panel
```bash
# Truy cập admin
https://ivie-admin.onrender.com

# Login:
Username: admin
Password: admin123

# Kiểm tra:
✅ Dashboard hiển thị số liệu
✅ Quản lý dịch vụ (CRUD)
✅ Quản lý combo
✅ Xem đơn hàng
✅ Upload ảnh
```

### 5. Test Workflow Hoàn Chỉnh
```bash
Bước 1: Frontend → Chọn combo → Đặt hàng
Bước 2: Admin → Kiểm tra đơn hàng mới xuất hiện
Bước 3: Admin → Thêm dịch vụ mới
Bước 4: Frontend → Refresh → Dịch vụ mới hiển thị
```

---

## 🔧 BƯỚC 7: CẤU HÌNH SAU KHI DEPLOY

### 1. ĐỔI MẬT KHẨU ADMIN (BẮT BUỘC!)
```
1. Truy cập: https://ivie-admin.onrender.com
2. Login: admin / admin123
3. Vào Settings → Change Password
4. Đổi thành mật khẩu mạnh (ít nhất 8 ký tự)
5. Lưu lại
```

### 2. Setup Monitoring (UptimeRobot)
```
1. Đăng ký: https://uptimerobot.com (miễn phí)
2. Tạo Monitor cho Backend:
   - Name: IVIE Backend
   - URL: https://ivie-backend.onrender.com/api/health
   - Interval: 5 minutes
   - Monitor Type: HTTP(s)

3. Tạo Monitor cho Admin:
   - Name: IVIE Admin
   - URL: https://ivie-admin.onrender.com/_stcore/health
   - Interval: 5 minutes

4. Setup Email Alert:
   - Add email của bạn
   - Alert khi service down
```

### 3. Backup Database (Quan trọng!)
```bash
# Free tier KHÔNG có auto-backup
# Export database thủ công mỗi tuần:

# Lấy DATABASE_URL từ:
# Dashboard → ivie-db → Connect → Internal Database URL

# Export:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Hoặc dùng Render Dashboard:
Dashboard → ivie-db → Backups → Manual Backup
```

### 4. Kiểm tra Resource Usage
```
1. Dashboard → ivie-backend → Metrics
   - Memory Usage: Nên < 400MB ✅
   - CPU Usage: Nên < 50% ✅
   - Response Time: Nên < 500ms ✅

2. Dashboard → ivie-admin → Metrics
   - Memory Usage: Nên < 400MB ✅
   - CPU Usage: Nên < 50% ✅

3. Dashboard → ivie-db → Info
   - Disk Usage: Nên < 900MB ✅
   - Connections: < 90/97 ✅
```

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Auto-sleep sau 15 phút
- Backend và Admin sẽ sleep khi không có request trong 15 phút
- Cold start mất 20-40 giây
- Frontend (static site) KHÔNG bị sleep
- **Giải pháp**: Dùng UptimeRobot để ping mỗi 5 phút

### 2. Giới hạn 750 giờ/tháng
```
Tính toán:
- 3 services × 24h/day × 30 days = 2,160 giờ/tháng ❌
- Free tier = 750 giờ/tháng

Giải pháp:
✅ Frontend (static) KHÔNG tính giờ
✅ Để Backend + Admin sleep → ~400 giờ/tháng
✅ Hoặc chỉ giữ Backend active → ~720 giờ/tháng
```

### 3. Database Free Tier
```
Giới hạn:
- Storage: 1GB (đủ ~10,000 đơn hàng)
- Connections: 97 concurrent
- No automatic backups
- Expires sau 90 ngày không login

Khuyến nghị:
✅ Export backup mỗi tuần
✅ Monitor disk usage
✅ Clean up old data định kỳ
✅ Login Render mỗi tháng để giữ database
```

### 4. Environment Variables
```
Các biến đã được set trong render.yaml:
✅ DATABASE_URL (tự động từ ivie-db)
✅ SECRET_KEY (auto-generate)
✅ CORS_ORIGINS (frontend + admin URLs)
✅ API_BASE_URL (backend URL)

Nếu cần thêm:
Dashboard → Service → Environment → Add Environment Variable
```

---

## 🐛 TROUBLESHOOTING

### Lỗi: Build timeout (> 15 phút)
```yaml
# Sửa trong render.yaml, commit và push lại:
envVars:
  - key: NODE_OPTIONS
    value: --max-old-space-size=1024  # Giảm từ 1200
```

### Lỗi: Out of Memory (OOM)
```yaml
# Sửa trong render.yaml:
envVars:
  - key: MAX_REQUESTS
    value: "250"  # Giảm từ 500
```

### Lỗi: Service không start
```bash
# Xem logs để debug:
Dashboard → Service → Logs

# Kiểm tra health check:
curl https://ivie-backend.onrender.com/api/health
```

### Lỗi: CORS từ Frontend
```yaml
# Thêm domain vào CORS_ORIGINS:
envVars:
  - key: CORS_ORIGINS
    value: https://ivie-frontend.onrender.com,https://yourdomain.com
```

---

## 📊 URLs SAU KHI DEPLOY

```
🌐 Frontend (Trang chính):
https://ivie-frontend.onrender.com

🔧 Backend API:
https://ivie-backend.onrender.com

📖 API Documentation:
https://ivie-backend.onrender.com/docs

🎛️ Admin Panel:
https://ivie-admin.onrender.com

🗄️ Database:
Internal URL (chỉ các services khác truy cập)
```

---

## 🎉 HOÀN TẤT!

Chúc mừng! Bạn đã deploy thành công **IVIE Wedding Studio** lên Render!

### Checklist cuối cùng:
- [ ] Tất cả services status = Live
- [ ] Backend health check OK
- [ ] Frontend hiển thị đúng
- [ ] Admin login được
- [ ] Đã đổi mật khẩu admin
- [ ] Setup UptimeRobot monitoring
- [ ] Export database backup đầu tiên
- [ ] Test trên mobile devices

---

## 📞 HỖ TRỢ

- 📚 **Docs chi tiết**: `HUONG_DAN_DEPLOY_RENDER_FREE.md`
- 🚀 **Quick start**: `DEPLOY_RENDER_FREE_QUICKSTART.md`
- ✅ **Checklist**: `CHECKLIST_TRUOC_KHI_DEPLOY.md`
- 💡 **Tối ưu**: `RENDER_FREE_TIER_OPTIMIZATION.md`

**Render Support:**
- 🌐 https://render.com/docs
- 💬 https://community.render.com
- 📧 Dashboard → Help → Contact Support

---

**Happy Coding! 🚀💕**

*Made with ❤️ for IVIE Wedding Studio*