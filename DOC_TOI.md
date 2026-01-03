# IVIE WEDDING STUDIO - HE THONG QUAN LY

## Gioi thieu

Website va he thong quan ly cho IVIE Wedding Studio.
Bao gom: Website ban hang, API Backend, va Admin Panel.

---

## Cau truc du an

```
webdichvumedia/
├── backend/              # API Backend (FastAPI + Python)
├── frontend/             # Website (React + Vite)
├── admin-python/         # Admin Panel (Streamlit)
├── render.yaml           # Cau hinh deploy Render
└── docs/                 # Tai lieu
```

---

## Cong nghe su dung

### Backend
- FastAPI (Python 3.12)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Gunicorn (Production server)

### Frontend
- React 19
- Vite 7
- React Router
- Axios
- Three.js (Hieu ung 3D)

### Admin Panel
- Streamlit
- Pandas
- Plotly (Bieu do)
- Requests

---

## Chay tren local

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn ung_dung.chinh:ung_dung --reload
```

Truy cap: http://localhost:8000
API Docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Truy cap: http://localhost:5173

### 3. Admin Panel

```bash
cd admin-python
pip install -r requirements.txt
streamlit run quan_tri_optimized_v2.py
```

Truy cap: http://localhost:8501
Login: admin / admin123

---

## Deploy len Render

### Cach nhanh nhat

```bash
# 1. Push code
git add .
git commit -m "Deploy to Render"
git push origin main

# 2. Vao Render Dashboard
# https://dashboard.render.com
# New + -> Blueprint -> Chon repo -> Apply

# 3. Doi 15-20 phut
```

Chi tiet xem: `huong_dan_deploy.md`

---

## URLs sau khi deploy

- Frontend: https://ivie-frontend.onrender.com
- Backend: https://ivie-backend.onrender.com
- Admin: https://ivie-admin.onrender.com

---

## Tai lieu

- `huong_dan_deploy.md` - Huong dan deploy chi tiet
- `deploy_nhanh.txt` - Huong dan deploy nhanh
- `danh_sach_kiem_tra.md` - Checklist truoc deploy
- `kiem_tra_lien_ket.md` - Kiem tra lien ket API
- `toi_uu_goi_mien_phi.md` - Toi uu cho Render Free

---

## Tinh nang chinh

### Website (Frontend)
- Trang chu voi banner dong
- Danh sach dich vu
- Danh sach combo
- Chi tiet san pham
- Gio hang va dat hang
- Thu vien anh
- Lien he

### API (Backend)
- Quan ly san pham
- Quan ly dich vu
- Quan ly combo
- Quan ly don hang
- Quan ly nguoi dung
- Upload file
- API documentation (Swagger)

### Admin Panel
- Dashboard thong ke
- Quan ly san pham (CRUD)
- Quan ly dich vu (CRUD)
- Quan ly combo (CRUD)
- Quan ly don hang
- Quan ly banner
- Quan ly thu vien anh
- Quan ly nguoi dung
- Bao cao doanh thu

---

## Cau hinh moi truong

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
```

### Admin (.env)
```
API_BASE_URL=http://localhost:8000
STREAMLIT_SERVER_PORT=8501
```

Chi tiet xem: `.env.example` trong moi thu muc

---

## Toi uu cho Render Free Tier

Du an da duoc toi uu cho goi mien phi cua Render:

- RAM: 380MB (Backend 200MB + Admin 180MB) < 512MB
- Build time: 5-8 phut < 15 phut
- Workers: 1 worker de tiet kiem RAM
- Frontend: Static site khong tinh gio su dung
- Database: PostgreSQL 1GB mien phi

Chi tiet: `toi_uu_goi_mien_phi.md`

---

## Luu y quan trong

1. DOI MAT KHAU ADMIN sau khi deploy
   - Login mac dinh: admin / admin123
   - Doi ngay de bao mat

2. BACKUP DATABASE thuong xuyen
   - Render Free khong co auto-backup
   - Export thu cong moi tuan

3. SETUP MONITORING de tranh sleep
   - Dung UptimeRobot ping moi 5 phut
   - Services se sleep sau 15 phut khong dung

4. KIEM TRA RESOURCE USAGE
   - RAM nen < 400MB
   - CPU nen < 50%
   - Database < 900MB

---

## Xu ly loi

### Build timeout
Giam NODE_OPTIONS trong render.yaml xuong 1024MB

### Out of Memory
Giam MAX_REQUESTS xuong 250

### CORS error
Kiem tra CORS_ORIGINS trong Backend environment

### Database connection failed
Doi 30-60 giay cho database khoi dong

Chi tiet: `huong_dan_deploy.md` phan 6

---

## Ho tro

- GitHub: https://github.com/buidi2004/webbandocuoi
- Render Docs: https://render.com/docs
- Render Community: https://community.render.com

---

## Phien ban

- Backend: 1.0.0
- Frontend: 1.0.0
- Admin: 1.0.0

Last updated: 2024-01-15

---

Made for IVIE Wedding Studio