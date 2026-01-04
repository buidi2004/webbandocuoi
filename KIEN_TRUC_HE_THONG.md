# Kiến Trúc Hệ Thống IVIE Wedding Studio

## Tổng Quan

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  FRONTEND   │────▶│   BACKEND   │────▶│  DATABASE   │
│   (React)   │◀────│  (FastAPI)  │◀────│ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
                           ▲
                           │
                    ┌──────┴──────┐
                    │    ADMIN    │
                    │ (Streamlit) │
                    └─────────────┘
```

## Luồng Hoạt Động

### 1. Khách Hàng Xem Sản Phẩm

```
Frontend (SanPham.jsx)
    │
    ▼ GET /api/san_pham?danh_muc=wedding_modern
    │
Backend (san_pham.py)
    │
    ▼ SELECT * FROM products WHERE category='wedding_modern'
    │
Database (PostgreSQL)
    │
    ▼ Trả về JSON [{id, name, price, image_url...}]
    │
Frontend hiển thị danh sách sản phẩm
```

### 2. Khách Hàng Đặt Hàng

```
Frontend (GioHang.jsx)
    │
    ▼ POST /api/don_hang {customer_name, items[], total}
    │
Backend (don_hang.py)
    │
    ▼ INSERT INTO orders + INSERT INTO order_items
    │
Database lưu đơn hàng
    │
    ▼ Trả về {id: 123, status: "pending"}
    │
Frontend chuyển trang "Cảm ơn"
```

### 3. Admin Quản Lý Sản Phẩm

```
Admin (Streamlit)
    │
    ▼ POST /api/san_pham {name, price, image_url}
    │
Backend (san_pham.py)
    │
    ▼ INSERT INTO products
    │
Database lưu sản phẩm mới
    │
    ▼ Frontend tự động hiển thị khi refresh
```

## Chi Tiết Từng Thành Phần

### Frontend (React + Vite)

| File | Chức năng |
|------|-----------|
| `api/khach_hang.js` | Gọi API backend (axios) |
| `trang/SanPham.jsx` | Hiển thị danh sách SP |
| `trang/GioHang.jsx` | Giỏ hàng + đặt hàng |
| `trang/TrangChu.jsx` | Trang chủ + banner |

**Lưu trữ local:**
- `localStorage.ivie_cart` - Giỏ hàng
- `localStorage.ivie_token` - JWT token đăng nhập

### Backend (FastAPI + SQLAlchemy)

| File | Chức năng |
|------|-----------|
| `chinh.py` | App chính, middleware, routing |
| `co_so_du_lieu.py` | Models (19 bảng) |
| `dinh_tuyen/san_pham.py` | CRUD sản phẩm |
| `dinh_tuyen/don_hang.py` | CRUD đơn hàng |
| `dinh_tuyen/nguoi_dung.py` | Đăng ký/đăng nhập |

**API chính:**
- `GET /api/san_pham` - Lấy sản phẩm
- `POST /api/don_hang` - Tạo đơn hàng
- `POST /api/nguoi_dung/dang_nhap` - Đăng nhập

### Admin (Streamlit)

| Tab | Chức năng |
|-----|-----------|
| Dashboard | Thống kê tổng quan |
| Sản phẩm | Thêm/sửa/xóa SP |
| Đơn hàng | Xem + cập nhật trạng thái |
| Người dùng | Quản lý tài khoản |
| Liên hệ | Xem form liên hệ |

**Đăng nhập:** `admin` / `ivie2024`

### Database (PostgreSQL)

**Bảng chính:**
- `products` - Sản phẩm
- `orders` + `order_items` - Đơn hàng
- `users` - Người dùng
- `banners` - Banner trang chủ
- `gallery` - Thư viện ảnh

## URLs Production

| Service | URL |
|---------|-----|
| Frontend | https://ivie-wedding-final.onrender.com |
| Backend | https://ivie-be-final.onrender.com |
| Admin | https://ivie-ad-final.onrender.com |
| API Docs | https://ivie-be-final.onrender.com/docs |

## Chạy Local

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn ung_dung.chinh:ung_dung --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev

# Admin
cd admin-python
pip install -r requirements.txt
streamlit run quan_tri.py --server.port 8501
```

## Sơ Đồ Database (Rút Gọn)

```
USERS ──────┬──── ORDERS ──── ORDER_ITEMS ──── PRODUCTS
            │
            ├──── WISHLISTS ──── PRODUCTS
            │
            └──── CHAT_MESSAGES

PRODUCTS ──── PRODUCT_REVIEWS

BANNERS, GALLERY, CONTACT_SUBMISSIONS (độc lập)
```
