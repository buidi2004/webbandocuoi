# IVIE Wedding Studio - Backend API

API Backend cho website IVIE Wedding Studio sử dụng FastAPI.

## Cài Đặt

### 1. Cài Đặt Thư Viện

```bash
cd backend
pip install -r requirements.txt
```

### 2. Khởi Tạo Cơ Sở Dữ Liệu

```bash
python khoi_tao_du_lieu.py
```

### 3. Chạy Server

```bash
uvicorn ung_dung.chinh:ung_dung --reload
```

API sẽ chạy tại: `http://localhost:8000`

### 4. Xem Tài Liệu API

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Các Endpoint API

### Sản Phẩm (san_pham)
- `GET /api/san_pham` - Lấy tất cả sản phẩm (có bộ lọc tùy chọn)
  - Tham số: `danh_muc`, `gioi_tinh`, `sort_by`
- `GET /api/san_pham/{id}` - Lấy sản phẩm theo ID
- `POST /api/san_pham` - Tạo sản phẩm mới
- `PUT /api/san_pham/{id}` - Cập nhật sản phẩm
- `DELETE /api/san_pham/{id}` - Xóa sản phẩm

### Đánh Giá (danh_gia)
- `GET /api/san_pham/{id}/danh_gia` - Lấy đánh giá đã duyệt
- `POST /api/san_pham/{id}/danh_gia` - Gửi đánh giá mới
- `GET /api/san_pham/admin/danh_gia_cho_duyet` - Lấy đánh giá chờ duyệt
- `POST /api/san_pham/admin/duyet_danh_gia/{id}` - Duyệt đánh giá
- `DELETE /api/san_pham/admin/xoa_danh_gia/{id}` - Xóa đánh giá

### Người Dùng (nguoi_dung)
- `POST /api/nguoi_dung/dang_ky` - Đăng ký tài khoản
- `POST /api/nguoi_dung/dang_nhap` - Đăng nhập
- `PUT /api/nguoi_dung/cap_nhat` - Cập nhật thông tin
- `GET /api/nguoi_dung/don_hang` - Lấy lịch sử đơn hàng
- `POST /api/nguoi_dung/kiem_tra_giam_gia` - Kiểm tra quyền giảm giá

### Dịch Vụ (dich_vu)
- `GET /api/dich_vu` - Lấy tất cả dịch vụ
- `GET /api/dich_vu/chuyen_gia` - Lấy danh sách chuyên gia
- `GET /api/dich_vu/chuyen_gia/{id}` - Lấy chuyên gia theo ID

### Liên Hệ (lien_he)
- `POST /api/lien_he` - Gửi form liên hệ
- `GET /api/lien_he` - Lấy danh sách liên hệ (admin)

### Thư Viện (thu_vien)
- `GET /api/thu_vien` - Lấy tất cả ảnh thư viện
- `POST /api/thu_vien` - Thêm ảnh mới
- `DELETE /api/thu_vien/{id}` - Xóa ảnh

### Banner
- `GET /api/banner` - Lấy tất cả banner
- `POST /api/banner` - Thêm banner mới
- `PUT /api/banner/{id}` - Cập nhật banner
- `DELETE /api/banner/{id}` - Xóa banner

### Blog (bai_viet)
- `GET /api/blog` - Lấy tất cả bài viết
- `GET /api/blog/{slug}` - Lấy bài viết theo slug
- `POST /api/blog` - Tạo bài viết mới
- `PUT /api/blog/{id}` - Cập nhật bài viết
- `DELETE /api/blog/{id}` - Xóa bài viết

### Đối Tác (doi_tac)
- `POST /api/doi_tac/nop_ho_so` - Nộp hồ sơ đối tác
- `GET /api/doi_tac/ho_so` - Lấy hồ sơ của mình
- `GET /api/doi_tac/admin/danh_sach` - Lấy tất cả hồ sơ (admin)

### Yêu Thích (yeu_thich)
- `GET /api/yeu_thich` - Lấy danh sách yêu thích
- `POST /api/yeu_thich/{id_san_pham}` - Thêm vào yêu thích
- `DELETE /api/yeu_thich/{id_san_pham}` - Xóa khỏi yêu thích

### Chat
- `GET /api/chat/tin_nhan` - Lấy tin nhắn
- `POST /api/chat/gui` - Gửi tin nhắn

### Tệp Tin (tap_tin)
- `POST /api/tap_tin/tai_len` - Tải lên tệp tin
- `GET /tep_tin/{ten_tep}` - Lấy tệp tin

### Thống Kê (thong_ke)
- `GET /api/thong_ke/tong_quan` - Thống kê tổng quan
- `GET /api/thong_ke/doanh_thu` - Thống kê doanh thu

## Biến Môi Trường

Tạo file `.env` trong thư mục backend:

```env
DATABASE_URL=sqlite:///./ivie.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
SECRET_KEY=khoa_bi_mat_cua_ban_rat_dai_va_bao_mat_123
```

## Cơ Sở Dữ Liệu

Ứng dụng sử dụng SQLite cho môi trường phát triển. CSDL sẽ được tạo tự động khi chạy script khởi tạo.

### Các Bảng Dữ Liệu:

| Tên Bảng | Mô Tả |
|----------|-------|
| `products` | Sản phẩm (váy cưới, vest, áo dài) |
| `experts` | Chuyên gia trang điểm |
| `services` | Dịch vụ |
| `contact_submissions` | Liên hệ từ khách hàng |
| `users` | Người dùng |
| `carts` | Giỏ hàng |
| `cart_items` | Chi tiết giỏ hàng |
| `orders` | Đơn hàng |
| `order_items` | Chi tiết đơn hàng |
| `product_reviews` | Đánh giá sản phẩm |
| `banners` | Banner trang chủ |
| `gallery` | Thư viện ảnh |
| `blog_posts` | Bài viết blog |
| `wishlists` | Danh sách yêu thích |
| `chat_messages` | Tin nhắn chat |
| `coupons` | Mã giảm giá |
| `complaints` | Khiếu nại |
| `partner_applications` | Hồ sơ đối tác |

## Cấu Trúc Thư Mục

```
backend/
├── ung_dung/
│   ├── __init__.py
│   ├── chinh.py              # Ứng dụng FastAPI chính
│   ├── co_so_du_lieu.py      # Mô hình CSDL và kết nối
│   ├── mo_hinh.py            # Pydantic schemas
│   ├── bao_mat.py            # Xác thực và mã hóa
│   ├── tien_ich_email.py     # Tiện ích gửi email
│   ├── dinh_tuyen/           # Các route API
│   │   ├── san_pham.py       # API sản phẩm
│   │   ├── nguoi_dung.py     # API người dùng
│   │   ├── dich_vu.py        # API dịch vụ
│   │   ├── lien_he.py        # API liên hệ
│   │   ├── thu_vien.py       # API thư viện
│   │   ├── banner.py         # API banner
│   │   ├── blog.py           # API blog
│   │   ├── doi_tac.py        # API đối tác
│   │   ├── yeu_thich.py      # API yêu thích
│   │   ├── chat.py           # API chat
│   │   ├── tap_tin.py        # API tệp tin
│   │   └── thong_ke.py       # API thống kê
│   └── static/               # Tệp tĩnh
├── tep_tin/                  # Thư mục lưu tệp tải lên
├── requirements.txt          # Thư viện cần thiết
├── khoi_tao_du_lieu.py       # Script khởi tạo dữ liệu
├── .env                      # Biến môi trường
└── HUONG_DAN.md              # Tài liệu hướng dẫn
```

## Bảo Mật

### Xác Thực JWT
- Sử dụng JWT Token để xác thực người dùng
- Token có thời hạn 7 ngày
- Mật khẩu được mã hóa bằng bcrypt

### Quét Virus
- Tệp tin tải lên được quét virus trước khi lưu
- Chỉ chấp nhận các định dạng: `.jpg`, `.jpeg`, `.png`, `.webp`

## Tác Giả

IVIE Studio - © 2024
