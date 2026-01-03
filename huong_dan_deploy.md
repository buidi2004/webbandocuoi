# HUONG DAN DEPLOY LEN RENDER (GOI MIEN PHI)

## Muc luc
1. Gioi thieu ve Render Free Tier
2. Chuan bi truoc khi deploy
3. Cac buoc deploy
4. Kiem tra sau khi deploy
5. Cau hinh quan trong
6. Xu ly loi thuong gap

---

## 1. GIOI THIEU VE RENDER FREE TIER

### Gioi han goi mien phi
- RAM: 512MB moi service
- CPU: Shared
- Build time: Toi da 15 phut
- Storage: 1GB cho PostgreSQL
- Bandwidth: 100GB/thang
- Hours: 750 gio/thang mien phi
- Auto-sleep: Sau 15 phut khong hoat dong
- Cold start: 20-40 giay khi danh thuc

### Du an nay da toi uu
- Backend: khoang 200MB RAM (dung 1 worker)
- Admin: khoang 180MB RAM (tat file watcher)
- Frontend: Static site (khong tinh gio)
- Build time: 3-8 phut moi service
- Tong RAM: khoang 380MB < 512MB

---

## 2. CHUAN BI TRUOC KHI DEPLOY

### Buoc 1: Push code len GitHub

```bash
# Neu chua co Git repository
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"

# Tao repo tren GitHub (vi du: webbandocuoi)
git remote add origin https://github.com/USERNAME/webbandocuoi.git
git branch -M main
git push -u origin main
```

### Buoc 2: Kiem tra cac file can thiet

Dam bao co cac file sau trong repository:
- render.yaml (blueprint cho Render)
- backend/Dockerfile
- backend/start.sh
- backend/requirements.txt
- admin-python/Dockerfile
- admin-python/requirements.txt
- frontend/package.json

### Buoc 3: Dang ky tai khoan Render

- Truy cap: https://render.com
- Dang ky bang GitHub (khuyen nghi)
- Xac nhan email

---

## 3. CAC BUOC DEPLOY

### Buoc 1: Dang nhap Render

1. Vao https://render.com/login
2. Chon "Sign up with GitHub"
3. Cho phep Render truy cap repositories

### Buoc 2: Ket noi repository

1. Vao Dashboard -> "New +"
2. Chon "Blueprint"
3. Chon repository cua ban
4. Render se tu dong phat hien file render.yaml

### Buoc 3: Deploy tu Blueprint

1. Render se hien thi cac services se duoc tao:
   - Database: ivie-db (PostgreSQL Free)
   - Backend: ivie-backend (Docker, Free)
   - Frontend: ivie-frontend (Static, Free)
   - Admin: ivie-admin (Docker, Free)

2. Click "Apply" de bat dau deploy

### Buoc 4: Theo doi qua trinh deploy

Thoi gian du kien:
- Database: 1-2 phut
- Backend: 3-5 phut
- Frontend: 5-8 phut
- Admin: 3-4 phut
- Tong cong: 12-19 phut

---

## 4. KIEM TRA SAU KHI DEPLOY

### Kiem tra tat ca services LIVE

Trong Render Dashboard -> Services
- ivie-db: Available (mau xanh)
- ivie-backend: Live (mau xanh)
- ivie-frontend: Live (mau xanh)
- ivie-admin: Live (mau xanh)

### Test Backend API

```bash
# Health check
curl https://ivie-backend.onrender.com/api/health

# Ket qua mong doi:
{"status":"healthy","timestamp":"..."}

# API Documentation
https://ivie-backend.onrender.com/docs
```

### Test Frontend

Truy cap: https://ivie-frontend.onrender.com

Kiem tra:
- Trang chu hien thi dung
- Menu navigation hoat dong
- Trang dich vu load duoc data tu API
- Trang combo hien thi dung
- Form lien he hoat dong

### Test Admin Panel

Truy cap: https://ivie-admin.onrender.com

Login mac dinh:
- Username: admin
- Password: admin123
- LUU Y: Doi mat khau ngay sau khi login!

Kiem tra:
- Dashboard hien thi so lieu
- Quan ly dich vu (CRUD)
- Quan ly combo
- Xem don hang
- Upload anh

### Test Workflow Hoan Chinh

1. Frontend -> Chon combo -> Dat hang
2. Admin -> Kiem tra don hang moi xuat hien
3. Admin -> Them dich vu moi
4. Frontend -> Refresh -> Dich vu moi hien thi

---

## 5. CAU HINH QUAN TRONG

### 1. DOI MAT KHAU ADMIN (BAT BUOC)

1. Truy cap: https://ivie-admin.onrender.com
2. Login: admin / admin123
3. Vao Settings -> Change Password
4. Doi thanh mat khau manh (it nhat 8 ky tu)
5. Luu lai

### 2. Setup Monitoring (UptimeRobot)

1. Dang ky: https://uptimerobot.com (mien phi)

2. Tao Monitor cho Backend:
   - Name: IVIE Backend
   - URL: https://ivie-backend.onrender.com/api/health
   - Interval: 5 minutes
   - Monitor Type: HTTP(s)

3. Tao Monitor cho Admin:
   - Name: IVIE Admin
   - URL: https://ivie-admin.onrender.com/_stcore/health
   - Interval: 5 minutes

4. Setup Email Alert:
   - Add email cua ban
   - Alert khi service down

### 3. Backup Database (Quan trong)

Free tier KHONG co auto-backup. Export thu cong moi tuan:

```bash
# Lay DATABASE_URL tu:
# Dashboard -> ivie-db -> Connect -> Internal Database URL

# Export:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Hoac dung Render Dashboard:
# Dashboard -> ivie-db -> Backups -> Manual Backup
```

### 4. Kiem tra Resource Usage

1. Dashboard -> ivie-backend -> Metrics
   - Memory Usage: Nen < 400MB
   - CPU Usage: Nen < 50%
   - Response Time: Nen < 500ms

2. Dashboard -> ivie-admin -> Metrics
   - Memory Usage: Nen < 400MB
   - CPU Usage: Nen < 50%

3. Dashboard -> ivie-db -> Info
   - Disk Usage: Nen < 900MB
   - Connections: < 90/97

---

## 6. XU LY LOI THUONG GAP

### Loi 1: Build timeout (vuot qua 15 phut)

Trieu chung:
```
Error: Build exceeded 15 minutes
Build cancelled
```

Giai phap:
1. Giam NODE_OPTIONS trong render.yaml:
```yaml
- key: NODE_OPTIONS
  value: --max-old-space-size=1024
```

2. Kiem tra requirements.txt xoa dependencies khong can thiet

### Loi 2: Out of Memory (OOM)

Trieu chung:
```
Error: Process killed (signal 9)
Worker process died unexpectedly
```

Giai phap:
1. Kiem tra WEB_CONCURRENCY=1 (da cau hinh)

2. Giam MAX_REQUESTS de restart worker thuong xuyen hon:
```yaml
- key: MAX_REQUESTS
  value: "250"
```

### Loi 3: Database connection failed

Trieu chung:
```
Error: could not connect to server
FATAL: password authentication failed
```

Giai phap:
1. Kiem tra DATABASE_URL trong Backend environment
2. Kiem tra database da khoi dong chua (Status = Available)
3. Tang thoi gian cho trong start.sh (sleep 10 giay)

### Loi 4: CORS error tu Frontend

Trieu chung:
```
Access to fetch has been blocked by CORS policy
```

Giai phap:
1. Kiem tra CORS_ORIGINS trong Backend:
```yaml
- key: CORS_ORIGINS
  value: https://ivie-frontend.onrender.com,https://ivie-admin.onrender.com
```

2. Them custom domain neu co

### Loi 5: Service keeps restarting

Trieu chung:
```
Service restarted due to health check failure
Logs show repeated restart cycles
```

Giai phap:
1. Kiem tra health endpoint hoat dong:
```bash
curl https://ivie-backend.onrender.com/api/health
```

2. Tang start-period trong Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3
```

3. Xem logs de tim loi

---

## LUU Y QUAN TRONG

### 1. Auto-sleep sau 15 phut
- Backend va Admin se sleep khi khong co request trong 15 phut
- Cold start mat 20-40 giay
- Frontend (static) KHONG bi sleep
- Giai phap: Dung UptimeRobot de ping moi 5 phut

### 2. Gioi han 750 gio/thang

Tinh toan:
- 3 services x 24h/day x 30 days = 2,160 gio/thang (Vuot qua!)
- Free tier = 750 gio/thang

Giai phap:
- Frontend (static) KHONG tinh gio
- De Backend + Admin sleep -> khoang 400 gio/thang
- Hoac chi giu Backend active -> khoang 720 gio/thang

### 3. Database Free Tier

Gioi han:
- Storage: 1GB (du khoang 10,000 don hang)
- Connections: 97 concurrent
- No automatic backups
- Expires sau 90 ngay khong login

Khuyen nghi:
- Export backup moi tuan
- Monitor disk usage
- Clean up old data dinh ky
- Login Render moi thang de giu database

---

## URLS SAU KHI DEPLOY

```
Frontend (Trang chinh):
https://ivie-frontend.onrender.com

Backend API:
https://ivie-backend.onrender.com

API Documentation:
https://ivie-backend.onrender.com/docs

Admin Panel:
https://ivie-admin.onrender.com
```

---

## CHECKLIST SAU DEPLOY

- [ ] Tat ca services status = Live
- [ ] Backend health check OK
- [ ] Frontend hien thi dung
- [ ] Admin login duoc
- [ ] Da doi mat khau admin
- [ ] Setup UptimeRobot monitoring
- [ ] Export database backup dau tien
- [ ] Test tren mobile devices

---

## HO TRO

Render Support:
- Docs: https://render.com/docs
- Community: https://community.render.com
- Support: dashboard.render.com -> Help

---

Chuc ban deploy thanh cong!

Last updated: 2024-01-15