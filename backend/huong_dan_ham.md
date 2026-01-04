# Tài Liệu Các Hàm Chính - Backend IVIE Wedding Studio

## 1. Cấu Trúc Tổng Quan

```
backend/ung_dung/
├── chinh.py              # FastAPI app chính, middleware, routing
├── co_so_du_lieu.py      # Database models (SQLAlchemy)
├── mo_hinh.py            # Pydantic schemas (request/response)
├── bao_mat.py            # JWT authentication, password hashing
├── cache_utils.py        # Cache middleware
└── dinh_tuyen/           # API routers (15 modules)
    ├── san_pham.py       # Sản phẩm
    ├── don_hang.py       # Đơn hàng
    ├── nguoi_dung.py     # Người dùng
    ├── lien_he.py        # Liên hệ
    ├── anh_bia.py        # Banner
    ├── thu_vien.py       # Thư viện ảnh
    ├── dich_vu.py        # Dịch vụ
    ├── bai_viet.py       # Blog
    ├── doi_tac.py        # Đối tác
    ├── yeu_thich.py      # Wishlist
    ├── tro_chuyen.py     # Chat
    ├── thong_ke.py       # Thống kê
    ├── noi_dung.py       # Nội dung trang
    ├── tep_tin.py        # Upload file
    └── api_postgresql.py # PostgreSQL utils
```

---

## 2. FastAPI App (`chinh.py`)

### 2.1 Khởi Tạo App

```python
ung_dung = FastAPI(
    title="IVIE Wedding Studio API (Tiếng Việt)",
    description="API cho website IVIE Wedding Studio",
    version="1.0.0",
)
```

### 2.2 Middleware

| Middleware | Mục đích |
|------------|----------|
| `GZipMiddleware` | Nén response > 500 bytes |
| `CacheControlMiddleware` | Tự động thêm cache headers |
| `CORSMiddleware` | Cho phép cross-origin requests |

### 2.3 Static Files

```python
# Thư mục ảnh sản phẩm
ung_dung.mount("/images", StaticFiles(directory=thu_muc_anh))

# Thư mục file upload
ung_dung.mount("/tep_tin", StaticFiles(directory="tep_tin"))
```

### 2.4 Startup Event

```python
@ung_dung.on_event("startup")
def su_kien_khoi_dong():
    """Khởi tạo CSDL khi server start"""
    khoi_tao_csdl()
```

### 2.5 Health Check Endpoints

| Endpoint | Mô tả |
|----------|-------|
| `GET /` | Welcome message |
| `GET /suckhoe` | Health check (tiếng Việt) |
| `GET /api/health` | Health check cho Render |
| `GET /api/db-test` | Test database connection |

---

## 3. Database Models (`co_so_du_lieu.py`)

### 3.1 Kết Nối Database

```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ivie.db")

# Fix Render's postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

dong_co = create_engine(DATABASE_URL)
PhienLamViec = sessionmaker(bind=dong_co)
```

### 3.2 Danh Sách Models (19 bảng)

| Model | Table | Mô tả |
|-------|-------|-------|
| `SanPham` | products | Sản phẩm (váy cưới, vest) |
| `ChuyenGia` | experts | Chuyên gia makeup/photo |
| `DichVu` | services | Dịch vụ |
| `Banner` | banners | Banner trang chủ |
| `GioiThieu` | about_us | Giới thiệu |
| `DiemNhanHome` | home_highlights | Điểm nhấn trang chủ |
| `ThuVien` | gallery | Thư viện ảnh |
| `LienHeGui` | contact_submissions | Form liên hệ |
| `NguoiDung` | users | Người dùng |
| `GioHang` | carts | Giỏ hàng |
| `ChiTietGioHang` | cart_items | Chi tiết giỏ hàng |
| `DonHang` | orders | Đơn hàng |
| `ChiTietDonHang` | order_items | Chi tiết đơn hàng |
| `TinNhanChat` | chat_messages | Tin nhắn chat |
| `MaGiamGia` | coupons | Mã giảm giá |
| `KhieuNai` | complaints | Khiếu nại |
| `HoSoDoiTac` | partner_applications | Hồ sơ đối tác |
| `DanhGia` | product_reviews | Đánh giá sản phẩm |
| `BaiViet` | blog_posts | Bài viết blog |
| `YeuThich` | wishlists | Danh sách yêu thích |
| `Combo` | combos | Gói combo |
| `LichTrong` | lich_trong | Lịch trống |

### 3.3 Dependency Injection

```python
def lay_csdl():
    """Dependency để inject database session"""
    db = PhienLamViec()
    try:
        yield db
    finally:
        db.close()
```

### 3.4 Hàm Khởi Tạo CSDL

```python
def khoi_tao_csdl():
    """
    - Tạo tables nếu chưa có
    - Auto migration cho PostgreSQL
    - Retry mechanism (5 lần, exponential backoff)
    """
```

---

## 4. API Sản Phẩm (`dinh_tuyen/san_pham.py`)

### 4.1 Endpoints

| Method | Endpoint | Hàm | Mô tả |
|--------|----------|-----|-------|
| GET | `/api/san_pham/` | `lay_danh_sach_san_pham()` | Lấy danh sách SP |
| GET | `/api/san_pham/{id}` | `lay_san_pham()` | Lấy chi tiết SP |
| POST | `/api/san_pham/` | `tao_san_pham()` | Tạo SP mới (admin) |
| PUT | `/api/san_pham/{id}` | `cap_nhat_san_pham()` | Cập nhật SP (admin) |
| DELETE | `/api/san_pham/{id}` | `xoa_san_pham()` | Xóa SP (admin) |

### 4.2 Query Parameters (GET /)

| Param | Type | Mô tả |
|-------|------|-------|
| `danh_muc` | string | Filter: wedding_modern, traditional, vest |
| `sub_category` | string | Filter tiểu mục |
| `gioi_tinh` | string | Filter: male, female |
| `sort_by` | string | Sắp xếp: price_asc, price_desc, hot, new |
| `bo_qua` | int | Offset (pagination) |
| `gioi_han` | int | Limit (pagination) |

### 4.3 Hàm Lấy Danh Sách

```python
@bo_dinh_tuyen.get("/", response_model=List[SanPham])
def lay_danh_sach_san_pham(
    danh_muc: Optional[str] = Query(None),
    sub_category: Optional[str] = Query(None),
    gioi_tinh: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    bo_qua: int = Query(0, ge=0),
    gioi_han: int = Query(0, ge=0, le=1000),
    csdl: Session = Depends(lay_csdl)
):
    truy_van = csdl.query(SanPhamDB)
    
    # Apply filters
    if danh_muc:
        truy_van = truy_van.filter(SanPhamDB.category == danh_muc)
    
    # Apply sorting
    if sort_by == "price_asc":
        truy_van = truy_van.order_by(SanPhamDB.rental_price_day.asc())
    elif sort_by == "hot":
        truy_van = truy_van.order_by(SanPhamDB.is_hot.desc())
    
    return truy_van.all()
```

### 4.4 API Đánh Giá

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/san_pham/{id}/danh_gia` | Lấy đánh giá đã duyệt |
| POST | `/api/san_pham/{id}/danh_gia` | Gửi đánh giá mới |
| GET | `/api/san_pham/admin/danh_gia_cho_duyet` | Lấy đánh giá chờ duyệt |
| POST | `/api/san_pham/admin/duyet_danh_gia/{id}` | Duyệt đánh giá |
| DELETE | `/api/san_pham/admin/xoa_danh_gia/{id}` | Xóa đánh giá |

---

## 5. API Đơn Hàng (`dinh_tuyen/don_hang.py`)

### 5.1 Endpoints

| Method | Endpoint | Hàm | Mô tả |
|--------|----------|-----|-------|
| POST | `/api/don_hang/` | `tao_don_hang()` | Tạo đơn hàng |
| GET | `/api/don_hang/` | `lay_danh_sach_don_hang()` | Lấy tất cả đơn |
| GET | `/api/don_hang/{id}` | `lay_don_hang()` | Chi tiết đơn |
| PUT | `/api/don_hang/{id}` | `cap_nhat_don_hang()` | Cập nhật trạng thái |

### 5.2 Request Body (POST /)

```python
class DonHangTao(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    total_amount: float
    items: List[ChiTietDonHangTao]
    payment_method: str = "cod"      # cod, bank_transfer
    delivery_type: str = "delivery"  # delivery, pickup
    note: Optional[str] = None
    user_id: Optional[int] = None
```

### 5.3 Trạng Thái Đơn Hàng

| Status | Mô tả |
|--------|-------|
| `pending` | Chờ xử lý |
| `processing` | Đang xử lý |
| `shipped` | Đang giao |
| `delivered` | Đã giao |
| `cancelled` | Đã hủy |

---

## 6. API Người Dùng (`dinh_tuyen/nguoi_dung.py`)

### 6.1 Endpoints

| Method | Endpoint | Hàm | Mô tả |
|--------|----------|-----|-------|
| POST | `/api/nguoi_dung/dang_ky` | `dang_ky()` | Đăng ký |
| POST | `/api/nguoi_dung/dang_nhap` | `dang_nhap()` | Đăng nhập |
| POST | `/api/nguoi_dung/dang_nhap_social` | `dang_nhap_social()` | Đăng nhập Google/FB |
| PUT | `/api/nguoi_dung/cap_nhat` | `cap_nhat_profile()` | Cập nhật profile |
| GET | `/api/nguoi_dung/don_hang` | `lay_lich_su_don_hang()` | Lịch sử đơn hàng |
| POST | `/api/nguoi_dung/kiem_tra_giam_gia` | `kiem_tra_giam_gia()` | Kiểm tra giảm giá |

### 6.2 Hàm Đăng Ký

```python
@bo_dinh_tuyen.post("/dang_ky", response_model=NguoiDungSchema)
def dang_ky(du_lieu: NguoiDungTao, csdl: Session = Depends(lay_csdl)):
    # Kiểm tra username đã tồn tại
    db_user = csdl.query(NguoiDungDB).filter(
        NguoiDungDB.username == du_lieu.username
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    
    # Hash password và tạo user
    mat_khau_ma_hoa = bam_mat_khau(du_lieu.password)
    user_moi = NguoiDungDB(
        username=du_lieu.username,
        hashed_password=mat_khau_ma_hoa,
        ...
    )
    csdl.add(user_moi)
    csdl.commit()
    return user_moi
```

### 6.3 Hàm Đăng Nhập

```python
@bo_dinh_tuyen.post("/dang_nhap", response_model=Token)
def dang_nhap(du_lieu: DangNhapForm, csdl: Session = Depends(lay_csdl)):
    user = csdl.query(NguoiDungDB).filter(
        NguoiDungDB.username == du_lieu.username
    ).first()
    
    if not user or not xac_minh_mat_khau(du_lieu.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Sai thông tin đăng nhập")
    
    access_token = tao_token_truy_cap(du_lieu={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": user}
```

### 6.4 Hàm Xác Thực Token

```python
def lay_user_tu_token(token: str, csdl: Session):
    """Giải mã JWT token và lấy user"""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user = csdl.query(NguoiDungDB).filter(
        NguoiDungDB.username == username
    ).first()
    return user
```

---

## 7. Pydantic Schemas (`mo_hinh.py`)

### 7.1 Pattern Naming

| Suffix | Mục đích |
|--------|----------|
| `CoBan` | Base schema (shared fields) |
| `Tao` | Create request |
| `CapNhat` | Update request |
| (none) | Response schema |

### 7.2 Ví Dụ Schema

```python
class SanPhamCoBan(BaseModel):
    name: str
    code: str
    category: str
    rental_price_day: float
    ...

class SanPhamTao(SanPhamCoBan):
    pass  # Inherit all fields

class SanPhamCapNhat(BaseModel):
    name: str | None = None  # All optional
    code: str | None = None
    ...

class SanPham(SanPhamCoBan):
    id: int
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('gallery_images', mode='before')
    def parse_json_fields(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v or []
```

---

## 8. Bảo Mật (`bao_mat.py`)

### 8.1 Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def bam_mat_khau(mat_khau: str) -> str:
    return pwd_context.hash(mat_khau)

def xac_minh_mat_khau(mat_khau: str, mat_khau_hash: str) -> bool:
    return pwd_context.verify(mat_khau, mat_khau_hash)
```

### 8.2 JWT Token

```python
from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "ivie_wedding_secret_key_super_secure_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def tao_token_truy_cap(du_lieu: dict):
    to_encode = du_lieu.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 9. Tổng Hợp API Endpoints

### 9.1 Public APIs (Không cần auth)

| Prefix | Mô tả |
|--------|-------|
| `/api/san_pham` | Sản phẩm |
| `/api/don_hang` | Đơn hàng |
| `/api/lien_he` | Liên hệ |
| `/api/banner` | Banner |
| `/api/thu_vien` | Thư viện ảnh |
| `/api/noi_dung` | Nội dung trang |
| `/api/dich_vu` | Dịch vụ |
| `/api/bai_viet` | Blog |
| `/api/combo` | Combo |

### 9.2 Protected APIs (Cần JWT token)

| Prefix | Mô tả |
|--------|-------|
| `/api/nguoi_dung/cap_nhat` | Cập nhật profile |
| `/api/nguoi_dung/don_hang` | Lịch sử đơn hàng |
| `/api/yeu_thich` | Wishlist |
| `/api/tro_chuyen` | Chat |
| `/api/doi_tac` | Đăng ký đối tác |

### 9.3 Admin APIs

| Prefix | Mô tả |
|--------|-------|
| `/api/san_pham/admin/*` | Quản lý đánh giá |
| `/api/thong_ke` | Thống kê |

---

## 10. Biến Môi Trường

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=ivie_wedding_secret_key_super_secure_123
CORS_ORIGINS=https://ivie-wedding-final.onrender.com
```

---

## 11. Thư Viện Sử Dụng

| Thư viện | Mục đích |
|----------|----------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `sqlalchemy` | ORM |
| `pydantic` | Data validation |
| `python-jose` | JWT tokens |
| `passlib` | Password hashing |
| `python-multipart` | File upload |
| `psycopg2-binary` | PostgreSQL driver |

---

## 12. Chạy Server

```bash
# Development
cd backend
uvicorn ung_dung.chinh:ung_dung --reload --port 8000

# Production (Render)
uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port $PORT
```

---

## 13. API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
