# 🏯 IVIE Wedding Studio

> Website cho thuê và bán váy cưới, vest, áo dài cao cấp

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Node](https://img.shields.io/badge/node-20+-green.svg)

## 📋 Tổng quan

IVIE Wedding Studio là nền tảng thương mại điện tử chuyên về trang phục cưới hỏi, bao gồm:

- 🛍️ **Website khách hàng** - Xem sản phẩm, đặt hàng, đánh giá
- 👨‍💼 **Admin Panel** - Quản lý sản phẩm, đơn hàng, khách hàng
- 🔗 **Backend API** - RESTful API xử lý nghiệp vụ

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │   Admin Panel   │    │   PostgreSQL    │
│  React + Vite   │───▶│    Streamlit    │───▶│    Database     │
│     (Nginx)     │    │                 │    │                 │
└────────┬────────┘    └────────┬────────┘    └────────▲────────┘
         │                      │                      │
         │                      │                      │
         └──────────────────────┴──────────────────────┘
                                │
                       ┌────────▼────────┐
                       │   Backend API   │
                       │     FastAPI     │
                       └─────────────────┘
```

## 📁 Cấu trúc dự án

```
webdichvumedia/
├── backend/                 # Backend API (FastAPI)
│   ├── ung_dung/           # Application modules
│   │   ├── dinh_tuyen/     # API routes
│   │   ├── chinh.py        # Main FastAPI app
│   │   ├── co_so_du_lieu.py # Database models
│   │   └── mo_hinh.py      # Pydantic schemas
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         
│   └── start.sh            # Startup script
│
├── frontend/               # Frontend (React + Vite)
│   ├── src/
│   │   ├── api/           # API clients
│   │   ├── trang/         # Page components
│   │   ├── thanh_phan/    # Shared components
│   │   └── styles/        # CSS styles
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
│
├── admin-python/          # Admin Panel (Streamlit)
│   ├── modules/           # Modular components
│   ├── quan_tri.py        # Main admin app
│   ├── auth.py            # Authentication
│   ├── requirements.txt
│   └── Dockerfile
│
├── render.yaml            # Render deployment config
├── DEPLOY_GUIDE.md        # Deployment guide
└── README.md              # This file
```

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- Python 3.12+
- Node.js 20+
- PostgreSQL (production) hoặc SQLite (development)

### 1. Clone repository

```bash
git clone https://github.com/buidi2004/webbandocuoi.git
cd webbandocuoi
```

### 2. Cài đặt Backend

```bash
cd backend

# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Copy file env mẫu
cp .env.example .env
# Chỉnh sửa .env theo cấu hình của bạn
```

### 3. Cài đặt Frontend

```bash
cd frontend

# Cài đặt dependencies
npm install

# Copy file env mẫu
cp .env.example .env
```

### 4. Cài đặt Admin Panel

```bash
cd admin-python

# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Copy file env mẫu
cp .env.example .env
```

## 🏃 Chạy ứng dụng (Development)

### Chạy tất cả cùng lúc (Windows)

```bash
# Từ thư mục gốc
chay_server.bat
```

### Chạy riêng từng service

**Backend API** (Port 8000):
```bash
cd backend
uvicorn ung_dung.chinh:ung_dung --reload --host 0.0.0.0 --port 8000
```

**Frontend** (Port 5173):
```bash
cd frontend
npm run dev
```

**Admin Panel** (Port 8501):
```bash
cd admin-python
streamlit run quan_tri.py
```

### Truy cập

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API Docs | http://localhost:8000/docs |
| Admin Panel | http://localhost:8501 |

## 🌐 Deploy lên Render

Xem hướng dẫn chi tiết tại [DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)

### Deploy nhanh

1. Fork repository này về GitHub của bạn
2. Đăng nhập [Render Dashboard](https://dashboard.render.com)
3. Tạo **Blueprint** → Connect GitHub repo
4. Render sẽ tự động đọc `render.yaml` và deploy

### Deploy bằng script

```bash
# Windows
scripts\deploy.bat "Commit message"

# Linux/Mac
chmod +x scripts/deploy.sh
./scripts/deploy.sh "Commit message"
```

## 🔐 Tài khoản Admin mặc định

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ **Lưu ý**: Hãy đổi mật khẩu ngay sau khi deploy!

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI** - Framework API hiệu năng cao
- **SQLAlchemy** - ORM cho database
- **PostgreSQL** - Database chính (production)
- **SQLite** - Database phát triển (development)
- **Pydantic** - Data validation
- **JWT** - Authentication

### Frontend
- **React 19** - UI Framework
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Framer Motion** - Animations
- **GSAP** - Advanced animations
- **Firebase** - Social login (Google/Facebook)

### Admin Panel
- **Streamlit** - Dashboard framework
- **Pandas** - Data processing
- **Plotly** - Charts & visualization
- **Pillow** - Image processing

### DevOps
- **Docker** - Containerization
- **Nginx** - Web server (frontend)
- **Gunicorn** - WSGI server (backend)
- **Render** - Cloud hosting

## 📊 Tính năng

### 👥 Khách hàng
- [x] Xem danh sách sản phẩm với bộ lọc
- [x] Xem chi tiết sản phẩm
- [x] Thêm vào giỏ hàng
- [x] Đặt hàng online
- [x] Đăng ký/Đăng nhập (Email, Google, Facebook)
- [x] Đánh giá sản phẩm
- [x] Danh sách yêu thích
- [x] Lịch sử đơn hàng
- [x] Chat hỗ trợ

### 👨‍💼 Admin
- [x] Dashboard thống kê
- [x] Quản lý sản phẩm (CRUD)
- [x] Quản lý đơn hàng
- [x] Quản lý khách hàng
- [x] Quản lý banner
- [x] Quản lý chuyên gia
- [x] Quản lý blog
- [x] Duyệt đánh giá
- [x] Quản lý đối tác
- [x] Quản lý combo
- [x] Chat với khách hàng
- [x] Xuất báo cáo Excel

## 🔧 API Endpoints

### Sản phẩm
```
GET    /api/san_pham/           # Danh sách sản phẩm
GET    /api/san_pham/{id}       # Chi tiết sản phẩm
POST   /api/san_pham/           # Tạo sản phẩm (Admin)
PUT    /api/san_pham/{id}       # Cập nhật sản phẩm (Admin)
DELETE /api/san_pham/{id}       # Xóa sản phẩm (Admin)
```

### Đơn hàng
```
GET    /api/don_hang/           # Danh sách đơn hàng
POST   /api/don_hang/           # Tạo đơn hàng
PUT    /api/don_hang/{id}       # Cập nhật trạng thái
```

### Người dùng
```
POST   /api/nguoi_dung/dang_ky      # Đăng ký
POST   /api/nguoi_dung/dang_nhap    # Đăng nhập
POST   /api/nguoi_dung/dang_nhap_social  # Đăng nhập Social
```

📚 Xem đầy đủ API tại: `http://localhost:8000/docs`

## 🐛 Xử lý sự cố

### Backend không chạy
```bash
# Kiểm tra port 8000 đã được sử dụng chưa
netstat -ano | findstr :8000

# Kill process nếu cần
taskkill /PID <PID> /F
```

### Frontend build lỗi
```bash
# Xóa cache và cài lại
rm -rf node_modules package-lock.json
npm install
```

### Database lỗi
```bash
# Xóa database SQLite và chạy lại
rm backend/ivie.db
# Restart backend - database sẽ được tạo lại tự động
```

## 📝 License

MIT License - Xem file [LICENSE](./LICENSE) để biết thêm chi tiết.

## 👨‍💻 Tác giả

**IVIE Wedding Studio Team**

- GitHub: [@buidi2004](https://github.com/buidi2004)

---

<p align="center">
  Made with ❤️ for Vietnamese Wedding Industry
</p>