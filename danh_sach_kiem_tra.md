# ✅ CHECKLIST TRƯỚC KHI DEPLOY LÊN RENDER

## 📋 Kiểm tra File Cần Thiết

### 1. Root Directory
- [x] `render.yaml` - Blueprint configuration
- [x] `.gitignore` - Đã cấu hình đúng
- [x] `README.md` hoặc docs

### 2. Backend (FastAPI)
- [x] `backend/Dockerfile` - ✅ Đã tối ưu FREE TIER
- [x] `backend/start.sh` - ✅ Có quyền execute (chmod +x)
- [x] `backend/requirements.txt` - ✅ Đầy đủ dependencies
- [x] `backend/ung_dung/chinh.py` - Main FastAPI app
- [x] `backend/ung_dung/co_so_du_lieu.py` - Database models

### 3. Frontend (React/Vite)
- [x] `frontend/package.json` - ✅ Có build script
- [x] `frontend/vite.config.js` - ✅ Đã tối ưu
- [x] `frontend/src/` - Source code
- [x] Build output: `dist/` (sẽ tạo khi build)

### 4. Admin Panel (Streamlit)
- [x] `admin-python/Dockerfile` - ✅ Đã tối ưu FREE TIER
- [x] `admin-python/requirements.txt` - ✅ Đầy đủ dependencies
- [x] `admin-python/quan_tri_optimized_v2.py` - ✅ Main app

---

## 🔧 Kiểm tra Cấu hình render.yaml

### Database
```yaml
✅ name: ivie-db
✅ plan: free
✅ region: singapore
```

### Backend
```yaml
✅ runtime: docker
✅ healthCheckPath: /api/health
✅ WEB_CONCURRENCY: "1"
✅ WORKERS: "1"
✅ GUNICORN_TIMEOUT: "60"
✅ MAX_REQUESTS: "500"
```

### Frontend
```yaml
✅ runtime: static
✅ buildCommand: npm ci --production=false && npm run build
✅ staticPublishPath: ./dist
✅ NODE_OPTIONS: --max-old-space-size=1200
✅ GENERATE_SOURCEMAP: "false"
```

### Admin
```yaml
✅ runtime: docker
✅ healthCheckPath: /_stcore/health
✅ STREAMLIT_SERVER_FILE_WATCHER_TYPE: "none"
✅ STREAMLIT_SERVER_MAX_UPLOAD_SIZE: "3"
```

---

## 🌐 Kiểm tra GitHub Repository

### Repository URL trong render.yaml
```bash
Current: https://github.com/buidi2004/webbandocuoi.git
Branch: main
```

- [x] URL đúng với GitHub repo của bạn
- [x] Branch = main
- [x] Repo visibility: Public hoặc Private (Render hỗ trợ cả 2)

### Git Status
```bash
✅ Đang ở branch: main
⚠️  Có 1 commit chưa push
⚠️  Có file chưa track: check_render_config.py
```

---

## 📦 Kiểm tra Dependencies

### Backend (Python)
```bash
✅ fastapi>=0.115.0
✅ uvicorn[standard]>=0.32.0
✅ sqlalchemy>=2.0.0
✅ psycopg2-binary>=2.9.0
✅ gunicorn>=21.2.0
✅ pydantic>=2.9.0
```

### Frontend (Node.js)
```bash
✅ react: ^19.2.0
✅ react-dom: ^19.2.0
✅ react-router-dom: ^7.11.0
✅ vite: ^7.2.4
✅ axios: ^1.13.2
```

### Admin (Python)
```bash
✅ streamlit==1.39.0
✅ requests==2.32.3
✅ pandas==2.2.3
✅ plotly==5.24.1
```

---

## 🚀 LỆNH DEPLOY

### Bước 1: Add tất cả file mới
```bash
git add .
```

### Bước 2: Commit changes
```bash
git commit -m "Optimized for Render Free Tier - Ready to deploy"
```

### Bước 3: Push lên GitHub
```bash
git push origin main
```

### Bước 4: Deploy trên Render
1. Vào https://render.com
2. Đăng nhập bằng GitHub
3. Click "New +" → "Blueprint"
4. Chọn repository: `buidi2004/webbandocuoi`
5. Render tự động đọc `render.yaml`
6. Click "Apply" để deploy

---

## ⏱️ Thời Gian Deploy Dự Kiến

| Service | Thời gian | Status |
|---------|-----------|--------|
| Database | 1-2 phút | Khởi tạo PostgreSQL |
| Backend | 3-5 phút | Build Docker + Install deps |
| Frontend | 5-8 phút | npm install + build |
| Admin | 3-4 phút | Build Docker + Install deps |
| **TỔNG** | **12-19 phút** | Tất cả services live |

---

## 📊 Resource Usage Dự Kiến

### Giới hạn FREE TIER
- RAM: 512MB per service
- Build time: Max 15 phút
- Hours: 750 giờ/tháng
- Database: 1GB storage

### Dự án này sử dụng
- Backend RAM: ~200MB ✅
- Admin RAM: ~180MB ✅
- Frontend: Static (không tính RAM) ✅
- Build time: 5-8 phút mỗi service ✅
- **TỔNG RAM: ~380MB < 512MB** ✅

---

## 🔍 Sau Khi Deploy - Kiểm Tra

### 1. Kiểm tra tất cả services LIVE
```
Render Dashboard → Services
- ivie-db: Available (màu xanh)
- ivie-backend: Live (màu xanh)
- ivie-frontend: Live (màu xanh)
- ivie-admin: Live (màu xanh)
```

### 2. Test các endpoints

#### Backend Health Check
```bash
curl https://ivie-backend.onrender.com/api/health

# Kết quả mong đợi:
{"status":"healthy","timestamp":"..."}
```

#### Backend API Docs
```
https://ivie-backend.onrender.com/docs
```

#### Frontend
```
https://ivie-frontend.onrender.com
- Trang chủ hiển thị
- Menu navigation hoạt động
- Trang dịch vụ/combo load được
```

#### Admin Panel
```
https://ivie-admin.onrender.com
- Login: admin / admin123
- Dashboard hiển thị
- CRUD operations hoạt động
```

### 3. Test workflow hoàn chỉnh
- [ ] Vào Frontend → Chọn combo → Đặt hàng
- [ ] Vào Admin → Kiểm tra đơn hàng mới
- [ ] Thêm dịch vụ mới từ Admin
- [ ] Kiểm tra Frontend hiển thị dịch vụ mới

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Đổi mật khẩu Admin ngay!
```
Login: https://ivie-admin.onrender.com
User: admin
Pass: admin123
→ Settings → Change Password
```

### 2. Backup Database
```bash
# Free tier không có auto-backup
# Export thủ công mỗi tuần:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### 3. Setup Monitoring (UptimeRobot)
```
1. Đăng ký: https://uptimerobot.com
2. Tạo 2 monitors:
   - https://ivie-backend.onrender.com/api/health (5 phút)
   - https://ivie-admin.onrender.com/_stcore/health (5 phút)
```

### 4. Auto-sleep sau 15 phút
- Backend và Admin sẽ sleep khi không dùng
- Cold start: 20-40 giây
- Frontend (static) không bị sleep
- Dùng UptimeRobot để giữ services active

### 5. Giới hạn 750 giờ/tháng
- 3 services × 24h × 30 days = 2,160 giờ ❌
- Frontend (static) không tính giờ ✅
- Để Backend + Admin sleep → ~400 giờ/tháng ✅
- Hoặc chỉ giữ Backend active → ~720 giờ/tháng ✅

---

## 🐛 Nếu Gặp Lỗi

### Build timeout (> 15 phút)
```yaml
# Giảm NODE_OPTIONS trong render.yaml
NODE_OPTIONS: --max-old-space-size=1024
```

### Out of Memory (OOM)
```yaml
# Giảm MAX_REQUESTS
MAX_REQUESTS: "250"
```

### Database connection failed
```bash
# Kiểm tra DATABASE_URL trong Backend Environment
# Đợi 30-60 giây cho database khởi động
```

### CORS error
```yaml
# Thêm domain vào CORS_ORIGINS
CORS_ORIGINS: https://ivie-frontend.onrender.com,https://yourdomain.com
```

---

## 📞 Hỗ Trợ

- 📚 Docs chi tiết: `HUONG_DAN_DEPLOY_RENDER_FREE.md`
- 🚀 Quick start: `DEPLOY_RENDER_FREE_QUICKSTART.md`
- 💡 Tối ưu: `RENDER_FREE_TIER_OPTIMIZATION.md`
- 🌐 Render Docs: https://render.com/docs
- 💬 Community: https://community.render.com

---

## ✅ READY TO DEPLOY!

Tất cả file đã được kiểm tra và tối ưu cho Render Free Tier!

**Lệnh cuối cùng:**
```bash
# 1. Add files
git add .

# 2. Commit
git commit -m "Optimized for Render Free Tier - Ready to deploy"

# 3. Push
git push origin main

# 4. Vào Render Dashboard → New + → Blueprint → Select repo → Apply
```

**🎉 Chúc bạn deploy thành công!**

---

**Made with ❤️ for IVIE Wedding Studio**