<p align="center">
  <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Version-2.0.1-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

# 💒 BÁO CÁO DỰ ÁN WEBSITE IVIE WEDDING STUDIO

<p align="center">
  <strong>🌐 Website thương mại điện tử cho thuê và bán trang phục cưới</strong>
</p>

---

## 📋 MỤC LỤC

1. [Tổng quan dự án](#-1-tổng-quan-dự-án)
2. [Công nghệ sử dụng](#-2-công-nghệ-sử-dụng)
3. [Kiến trúc hệ thống](#-3-kiến-trúc-hệ-thống)
4. [Cấu trúc thư mục](#-4-cấu-trúc-thư-mục)
5. [Cơ sở dữ liệu](#-5-cơ-sở-dữ-liệu)
6. [API Endpoints](#-6-api-endpoints)
7. [Tính năng chính](#-7-tính-năng-chính)
8. [Triển khai](#-8-triển-khai)
9. [Hướng dẫn cài đặt](#-9-hướng-dẫn-cài-đặt)
10. [Bảo mật & Hiệu năng](#-10-bảo-mật--hiệu-năng)

---

## 🎯 1. TỔNG QUAN DỰ ÁN

### 1.1 Giới thiệu
**IVIE Wedding Studio** là website thương mại điện tử chuyên cho thuê và bán váy cưới, vest, áo dài. Hệ thống bao gồm 3 thành phần chính:
- 🖥️ **Website khách hàng** - Giao diện người dùng
- ⚙️ **API Server** - Xử lý logic nghiệp vụ
- 📊 **Trang quản trị** - Dashboard admin

### 1.2 URLs Production

| Thành phần | URL | Status |
|------------|-----|--------|
| 🌐 Frontend | https://ivie-wedding-final.onrender.com | ![](https://img.shields.io/badge/Live-brightgreen) |
| ⚡ Backend | https://ivie-be-final.onrender.com | ![](https://img.shields.io/badge/Live-brightgreen) |
| 🔧 Admin | https://ivie-ad-final.onrender.com | ![](https://img.shields.io/badge/Live-brightgreen) |

---

## 🛠️ 2. CÔNG NGHỆ SỬ DỤNG

### 2.1 Frontend

| Công nghệ | Icon | Phiên bản | Mô tả |
|-----------|------|-----------|-------|
| React | ![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB) | 18.x | Thư viện UI |
| Vite | ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white) | 5.x | Build tool siêu nhanh |
| React Router | ![React Router](https://img.shields.io/badge/React_Router-CA4245?style=flat&logo=react-router&logoColor=white) | 6.x | Routing SPA |
| CSS3 | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) | - | Styling |
| JavaScript | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | ES6+ | Ngôn ngữ lập trình |

### 2.2 Backend

| Công nghệ | Icon | Phiên bản | Mô tả |
|-----------|------|-----------|-------|
| Python | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | 3.12 | Ngôn ngữ lập trình |
| FastAPI | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) | 0.100+ | Web framework |
| SQLAlchemy | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white) | 2.x | ORM |
| Pydantic | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white) | 2.x | Data validation |
| Gunicorn | ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat&logo=gunicorn&logoColor=white) | - | WSGI Server |
| Uvicorn | ![Uvicorn](https://img.shields.io/badge/Uvicorn-2C3E50?style=flat&logo=uvicorn&logoColor=white) | - | ASGI Server |

### 2.3 Admin Panel

| Công nghệ | Icon | Phiên bản | Mô tả |
|-----------|------|-----------|-------|
| Streamlit | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | 1.x | Dashboard framework |
| Pandas | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | - | Data analysis |
| Plotly | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) | - | Charts |

### 2.4 Database & Hosting

| Công nghệ | Icon | Mô tả |
|-----------|------|-------|
| PostgreSQL | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) | Database chính |
| Render | ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) | Cloud hosting |
| ImgBB | ![ImgBB](https://img.shields.io/badge/ImgBB-02569B?style=flat&logo=imgur&logoColor=white) | Image hosting |

### 2.5 Tools & DevOps

| Công nghệ | Icon | Mô tả |
|-----------|------|-------|
| Git | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) | Version control |
| GitHub | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) | Repository |
| npm | ![npm](https://img.shields.io/badge/npm-CB3837?style=flat&logo=npm&logoColor=white) | Package manager |
| pip | ![pip](https://img.shields.io/badge/pip-3775A9?style=flat&logo=pypi&logoColor=white) | Python packages |

---

## 🏗️ 3. KIẾN TRÚC HỆ THỐNG

### 3.1 Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           🌐 INTERNET (HTTPS)                           │
└─────────────────────────────────────────────────────────────────────────┘
              │                        │                        │
              ▼                        ▼                        ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│   🖥️ FRONTEND        │  │   ⚡ BACKEND          │  │   📊 ADMIN           │
│   ━━━━━━━━━━━━━━━━   │  │   ━━━━━━━━━━━━━━━━   │  │   ━━━━━━━━━━━━━━━━   │
│   React + Vite       │──│   FastAPI            │──│   Streamlit          │
│                      │  │                      │  │                      │
│   📱 Responsive UI   │  │   🔌 REST API        │  │   📈 Dashboard       │
│   🛒 Shopping Cart   │  │   🔐 JWT Auth        │  │   📦 CRUD Products   │
│   👤 User Account    │  │   📁 File Upload     │  │   📋 Order Mgmt      │
│   💳 Checkout        │  │   🗜️ GZip            │  │   👥 User Mgmt       │
└──────────────────────┘  └──────────┬───────────┘  └──────────────────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │   🗄️ POSTGRESQL      │
                          │   ━━━━━━━━━━━━━━━━   │
                          │   Render Database    │
                          │                      │
                          │   📊 15+ Tables      │
                          │   🔒 SSL Enabled     │
                          │   💾 Auto Backup     │
                          └──────────────────────┘
```

### 3.2 Luồng dữ liệu

```
👤 User ──▶ 🖥️ Frontend ──▶ ⚡ Backend API ──▶ 🗄️ PostgreSQL
                │                  │
                │                  ▼
                │            📁 File Storage
                │                  │
                ◀──────────────────┘
```

---

## 📁 4. CẤU TRÚC THƯ MỤC

```
ivie-wedding/
│
├── 🖥️ frontend/                    # WEBSITE KHÁCH HÀNG
│   ├── 📂 src/
│   │   ├── 📂 api/                 # API clients
│   │   │   ├── 📄 khach_hang.js    # API sản phẩm, đơn hàng
│   │   │   └── 📄 nguoi_dung.js    # API đăng nhập/đăng ký
│   │   │
│   │   ├── 📂 trang/               # 📄 Các trang chính
│   │   │   ├── 🏠 TrangChu.jsx     # Trang chủ
│   │   │   ├── 👗 SanPham.jsx      # Danh sách sản phẩm
│   │   │   ├── 🛒 GioHang.jsx      # Giỏ hàng
│   │   │   ├── 💳 ThanhToan.jsx    # Thanh toán
│   │   │   ├── 👤 TaiKhoan.jsx     # Tài khoản
│   │   │   ├── 🔐 DangNhap.jsx     # Đăng nhập
│   │   │   ├── 🖼️ ThuVien.jsx      # Thư viện ảnh
│   │   │   ├── 📞 LienHe.jsx       # Liên hệ
│   │   │   ├── 📦 ChonCombo.jsx    # Chọn combo
│   │   │   └── 📜 ChinhSach.jsx    # Chính sách
│   │   │
│   │   ├── 📂 thanh_phan/          # 🧩 Components
│   │   │   ├── 🧭 ThanhDieuHuong.jsx  # Header
│   │   │   ├── 📍 ChanTrang.jsx       # Footer
│   │   │   ├── 🃏 TheSanPham.jsx      # Product card
│   │   │   ├── 🔍 ThanhTimKiem.jsx    # Search bar
│   │   │   ├── 📅 LichTrong.jsx       # Calendar
│   │   │   └── 📝 FormLienHeNhanh.jsx # Quick contact
│   │   │
│   │   ├── 📂 styles/              # 🎨 CSS files
│   │   └── 📄 UngDung.jsx          # App root
│   │
│   ├── 📂 public/                  # Static assets
│   └── 📄 package.json
│
├── ⚡ backend/                      # API SERVER
│   ├── 📂 ung_dung/
│   │   ├── 📄 chinh.py             # 🚀 Main FastAPI app
│   │   ├── 📄 co_so_du_lieu.py     # 🗄️ Database models
│   │   ├── 📄 mo_hinh.py           # 📋 Pydantic schemas
│   │   ├── 📄 cache_utils.py       # ⚡ Caching
│   │   │
│   │   └── 📂 dinh_tuyen/          # 🔌 API Routes
│   │       ├── 👗 san_pham.py      # Products API
│   │       ├── 📦 don_hang.py      # Orders API
│   │       ├── 👤 nguoi_dung.py    # Users API
│   │       ├── 📞 lien_he.py       # Contact API
│   │       ├── 🖼️ anh_bia.py       # Banners API
│   │       ├── 📸 thu_vien.py      # Gallery API
│   │       ├── 📝 bai_viet.py      # Blog API
│   │       ├── ❤️ yeu_thich.py     # Wishlist API
│   │       └── 📊 thong_ke.py      # Statistics API
│   │
│   └── 📄 requirements.txt
│
├── 📊 admin-python/                 # TRANG QUẢN TRỊ
│   ├── 📄 quan_tri.py              # 🎛️ Main Streamlit app
│   ├── 📄 xac_thuc.py              # 🔐 Authentication
│   ├── 📄 phan_tich.py             # 📈 Analytics
│   └── 📄 requirements.txt
│
├── 📄 render.yaml                   # ☁️ Render config
└── 📄 README.md                     # 📖 Documentation
```

---

## 🗄️ 5. CƠ SỞ DỮ LIỆU

### 5.1 Sơ đồ ERD

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   👤 users      │       │   📦 orders     │       │ 📋 order_items  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)      │◀──┐   │ 🔑 id (PK)      │◀──┐   │ 🔑 id (PK)      │
│ 👤 username     │   │   │ 🔗 user_id (FK) │───┘   │ 🔗 order_id(FK) │───┐
│ 📧 email        │   │   │ 📝 customer_*   │       │ 🔗 product_id   │   │
│ 🔒 password     │   │   │ 💰 total_amount │       │ 🔢 quantity     │   │
│ 📱 phone        │   │   │ 📊 status       │       │ 💵 price        │   │
└─────────────────┘   │   └─────────────────┘       └─────────────────┘   │
                      │                                                   │
┌─────────────────┐   │   ┌─────────────────┐       ┌─────────────────┐   │
│   ❤️ wishlists  │   │   │   👗 products   │◀──────│ ⭐ reviews      │   │
├─────────────────┤   │   ├─────────────────┤       ├─────────────────┤   │
│ 🔑 id (PK)      │   │   │ 🔑 id (PK)      │◀──────│ 🔗 product_id   │   │
│ 🔗 user_id (FK) │───┘   │ 📝 name         │       │ 👤 user_name    │   │
│ 🔗 product_id   │───────│ 🏷️ code         │       │ ⭐ rating       │   │
└─────────────────┘       │ 📂 category     │       │ 💬 comment      │   │
                          │ 💰 price_*      │       │ ✅ is_approved  │   │
                          │ 🖼️ image_url    │       └─────────────────┘   │
                          │ 🆕 is_new/hot   │◀────────────────────────────┘
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   🖼️ banners    │       │   📸 gallery    │       │   📝 blog_posts │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)      │       │ 🔑 id (PK)      │       │ 🔑 id (PK)      │
│ 🖼️ image_url    │       │ 🖼️ image_url    │       │ 📝 title        │
│ 📝 title        │       │ 📝 title        │       │ 🔗 slug         │
│ ✅ is_active    │       │ 🔢 order        │       │ 📄 content      │
└─────────────────┘       └─────────────────┘       │ ✅ is_published │
                                                    └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   📦 combos     │       │  📅 lich_trong  │       │ 📞 contact_sub  │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)      │       │ 🔑 id (PK)      │       │ 🔑 id (PK)      │
│ 📝 ten          │       │ 📅 date         │       │ 👤 name         │
│ 💰 gia          │       │ 📊 status       │       │ 📧 email        │
│ 🔢 gioi_han     │       │ 🔢 slots        │       │ 💬 message      │
│ ⭐ noi_bat      │       └─────────────────┘       │ 📊 status       │
└─────────────────┘                                 └─────────────────┘
```

### 5.2 Chi tiết bảng Products

| Cột | Kiểu | Icon | Mô tả |
|-----|------|------|-------|
| id | SERIAL | 🔑 | Khóa chính |
| name | VARCHAR | 📝 | Tên sản phẩm |
| code | VARCHAR | 🏷️ | Mã sản phẩm (unique) |
| category | VARCHAR | 📂 | wedding_modern, vest, aodai |
| sub_category | VARCHAR | 📁 | xoe, duoi_ca, ngan... |
| gender | VARCHAR | 👤 | male, female |
| rental_price_day | FLOAT | 💰 | Giá thuê/ngày |
| rental_price_week | FLOAT | 💵 | Giá thuê/tuần |
| purchase_price | FLOAT | 💎 | Giá mua |
| image_url | VARCHAR | 🖼️ | Ảnh chính |
| gallery_images | TEXT | 📸 | JSON array ảnh |
| is_new | BOOLEAN | 🆕 | Sản phẩm mới |
| is_hot | BOOLEAN | 🔥 | Sản phẩm hot |
| so_luong | INTEGER | 📦 | Số lượng tồn |

---

## 🔌 6. API ENDPOINTS

### 6.1 👗 Sản phẩm (`/api/san_pham`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/` | Danh sách sản phẩm | ❌ |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/{id}` | Chi tiết sản phẩm | ❌ |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat) | `/` | Tạo sản phẩm | 🔐 Admin |
| ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat) | `/{id}` | Cập nhật sản phẩm | 🔐 Admin |
| ![DELETE](https://img.shields.io/badge/DELETE-F93E3E?style=flat) | `/{id}` | Xóa sản phẩm | 🔐 Admin |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/{id}/danh_gia` | Đánh giá sản phẩm | ❌ |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat) | `/{id}/danh_gia` | Gửi đánh giá | ❌ |

### 6.2 📦 Đơn hàng (`/api/don_hang`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/` | Danh sách đơn hàng | 🔐 Admin |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/{id}` | Chi tiết đơn hàng | 🔐 User |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat) | `/` | Tạo đơn hàng | ❌ |
| ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat) | `/{id}` | Cập nhật trạng thái | 🔐 Admin |

### 6.3 👤 Người dùng (`/api/nguoi_dung`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat) | `/dang_ky` | Đăng ký tài khoản | ❌ |
| ![POST](https://img.shields.io/badge/POST-49CC90?style=flat) | `/dang_nhap` | Đăng nhập | ❌ |
| ![GET](https://img.shields.io/badge/GET-61AFFE?style=flat) | `/thong_tin/{id}` | Thông tin user | 🔐 User |
| ![PUT](https://img.shields.io/badge/PUT-FCA130?style=flat) | `/cap_nhat/{id}` | Cập nhật thông tin | 🔐 User |

### 6.4 📋 Các API khác

| Prefix | Icon | Mô tả |
|--------|------|-------|
| `/api/anh_bia` | 🖼️ | Quản lý banner |
| `/api/thu_vien` | 📸 | Thư viện ảnh |
| `/api/lien_he` | 📞 | Form liên hệ |
| `/api/bai_viet` | 📝 | Blog/Tin tức |
| `/api/yeu_thich` | ❤️ | Danh sách yêu thích |
| `/api/combo` | 📦 | Gói combo |
| `/api/lich_trong` | 📅 | Lịch đặt |
| `/api/thong_ke` | 📊 | Thống kê |

---

## ✨ 7. TÍNH NĂNG CHÍNH

### 7.1 🖥️ Website Khách hàng

| # | Tính năng | Icon | Mô tả |
|---|-----------|------|-------|
| 1 | Trang chủ | 🏠 | Banner, sản phẩm nổi bật, combo |
| 2 | Danh sách SP | 👗 | Lọc, sắp xếp, phân trang |
| 3 | Chi tiết SP | 🔍 | Gallery, thông tin, đánh giá |
| 4 | Giỏ hàng | 🛒 | Thêm/xóa/cập nhật số lượng |
| 5 | Thanh toán | 💳 | Form đặt hàng |
| 6 | Tài khoản | 👤 | Đăng ký, đăng nhập, lịch sử |
| 7 | Thư viện | 📸 | Gallery với lightbox |
| 8 | Liên hệ | 📞 | Form gửi tin nhắn |
| 9 | Blog | 📝 | Tin tức, bài viết |
| 10 | Yêu thích | ❤️ | Lưu sản phẩm yêu thích |
| 11 | Lịch đặt | 📅 | Xem lịch trống |
| 12 | Combo | 📦 | Chọn gói combo |

### 7.2 📊 Trang Quản trị

| # | Tính năng | Icon | Mô tả |
|---|-----------|------|-------|
| 1 | Dashboard | 📈 | Thống kê tổng quan |
| 2 | Sản phẩm | 👗 | CRUD sản phẩm |
| 3 | Đơn hàng | 📦 | Xem, cập nhật trạng thái |
| 4 | Khách hàng | 👥 | Danh sách users |
| 5 | Banner | 🖼️ | CRUD banner |
| 6 | Thư viện | 📸 | Upload/xóa ảnh |
| 7 | Blog | 📝 | CRUD bài viết |
| 8 | Combo | 📦 | CRUD combo |
| 9 | Đánh giá | ⭐ | Approve/reject reviews |
| 10 | Liên hệ | 📞 | Xem tin nhắn |
| 11 | Báo cáo | 📊 | Doanh thu, thống kê |

---

## ☁️ 8. TRIỂN KHAI

### 8.1 Nền tảng Render.com

```yaml
# render.yaml
databases:
  - name: ivie-db-final
    plan: free
    region: singapore

services:
  # ⚡ Backend
  - type: web
    name: ivie-be-final
    runtime: python
    
  # 🖥️ Frontend  
  - type: web
    name: ivie-wedding-final
    runtime: static
    
  # 📊 Admin
  - type: web
    name: ivie-ad-final
    runtime: python
```

### 8.2 🔐 Biến môi trường

**⚡ Backend:**
```env
DATABASE_URL=postgresql://user:pass@host/db
CORS_ORIGINS=https://ivie-wedding-final.onrender.com
SECRET_KEY=your_secret_key
```

**🖥️ Frontend:**
```env
VITE_API_BASE_URL=https://ivie-be-final.onrender.com
VITE_IMGBB_API_KEY=your_imgbb_key
```

**📊 Admin:**
```env
API_BASE_URL=https://ivie-be-final.onrender.com
SECRET_KEY=your_secret_key
```

### 8.3 🚀 Quy trình Deploy

```
1️⃣ Push code lên GitHub
   git add .
   git commit -m "message"
   git push

2️⃣ Render tự động build
   ⚡ Backend: pip install → gunicorn start
   🖥️ Frontend: npm install → npm build
   📊 Admin: pip install → streamlit run

3️⃣ Database auto-migrate
```

---

## 💻 9. HƯỚNG DẪN CÀI ĐẶT

### 9.1 📋 Yêu cầu

| Công cụ | Phiên bản | Icon |
|---------|-----------|------|
| Python | 3.11+ | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| Node.js | 18+ | ![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=node.js&logoColor=white) |
| PostgreSQL | 15 | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) |

### 9.2 ⚡ Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn ung_dung.chinh:ung_dung --reload --port 8000
```
📍 Mở: http://localhost:8000/docs

### 9.3 🖥️ Frontend

```bash
cd frontend
npm install
npm run dev
```
📍 Mở: http://localhost:5173

### 9.4 📊 Admin

```bash
cd admin-python
pip install -r requirements.txt
streamlit run quan_tri.py --server.port 8501
```
📍 Mở: http://localhost:8501

---

## 🔒 10. BẢO MẬT & HIỆU NĂNG

### 10.1 🛡️ Bảo mật

| Tính năng | Icon | Mô tả |
|-----------|------|-------|
| Password Hashing | 🔐 | bcrypt |
| CORS | 🌐 | Chỉ cho phép domain cụ thể |
| Input Validation | ✅ | Pydantic schemas |
| SQL Injection | 🛡️ | SQLAlchemy ORM |
| File Upload | 📁 | Kiểm tra extension |
| HTTPS | 🔒 | SSL trên Render |

### 10.2 ⚡ Hiệu năng

| Tối ưu | Icon | Mô tả |
|--------|------|-------|
| GZip | 🗜️ | Nén response > 500 bytes |
| Cache | 💾 | Cache static assets |
| Lazy Loading | 🖼️ | Load ảnh khi cần |
| Pagination | 📄 | Phân trang API |
| Indexing | 🔍 | Index database |

---

## 📊 THỐNG KÊ DỰ ÁN

<p align="center">

| Metric | Value |
|--------|-------|
| 📁 Tổng số files | 100+ |
| 📂 Frontend components | 30+ |
| 🔌 API endpoints | 50+ |
| 🗄️ Database tables | 15+ |
| 📝 Lines of code | 10,000+ |

</p>

---

<p align="center">
  <strong>📅 Ngày tạo báo cáo:</strong> 04/01/2026<br>
  <strong>📌 Phiên bản:</strong> 2.0.1<br><br>
  
  Made with ❤️ by IVIE Wedding Studio Team
</p>
