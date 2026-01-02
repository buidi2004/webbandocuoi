# 🚀 HƯỚNG DẪN TỐI ƯU HÓA ADMIN PANEL - IVIE WEDDING STUDIO

## 📋 Tổng Quan

Tài liệu này hướng dẫn cách tối ưu hóa hiệu suất cho Backend và Admin Panel của IVIE Wedding Studio.

## 🎯 Mục Tiêu Tối Ưu

- **Response Time**: Giảm từ >2s xuống <500ms
- **Database Queries**: Tối ưu với indexing và caching
- **Memory Usage**: Giảm 30-50% với connection pooling
- **Concurrent Users**: Hỗ trợ nhiều admin truy cập đồng thời

---

## 📁 Cấu Trúc Files Tối Ưu

```
backend/ung_dung/
├── cache_advanced.py          # Advanced caching layer
├── cache_utils.py             # Basic cache utilities  
├── co_so_du_lieu_optimized.py # Database với connection pooling
├── chinh_optimized.py         # FastAPI app tối ưu
└── dinh_tuyen/
    └── san_pham_optimized.py  # API endpoints tối ưu

admin-python/
└── quan_tri_optimized.py      # Streamlit admin tối ưu

optimize_admin.py              # Script monitoring & optimization
```

---

## 🔧 Cài Đặt

### 1. Cập nhật Dependencies

```bash
# Backend
cd backend
pip install -r requirements_optimized.txt

# Hoặc cài các package quan trọng
pip install redis hiredis psutil asyncpg aiofiles
```

### 2. Cấu hình Environment Variables

Thêm vào file `.env`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis Cache (Optional - nếu có)
REDIS_URL=redis://localhost:6379/0

# Performance Settings
DEBUG=false
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

### 3. Khởi động với Optimized Version

```bash
# Thay thế chinh.py bằng chinh_optimized.py
# Hoặc update import trong chinh.py

# Chạy uvicorn với workers
uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port 8000 --workers 4
```

---

## 💾 DATABASE OPTIMIZATION

### Indexes Tự Động

File `co_so_du_lieu_optimized.py` tự động tạo các indexes:

```sql
-- Sản phẩm
CREATE INDEX idx_san_pham_category ON san_pham(category);
CREATE INDEX idx_san_pham_category_gender ON san_pham(category, gender);
CREATE INDEX idx_san_pham_price ON san_pham(rental_price_day);

-- Đơn hàng  
CREATE INDEX idx_don_hang_status ON don_hang(status);
CREATE INDEX idx_don_hang_status_date ON don_hang(status, order_date);

-- Đánh giá
CREATE INDEX idx_danh_gia_product_approved ON danh_gia(product_id, is_approved);
```

### Connection Pooling

```python
from co_so_du_lieu_optimized import get_engine, lay_csdl_optimized

# Cấu hình pool
engine = create_engine(
    url,
    pool_size=5,          # Số connection cơ bản
    max_overflow=10,      # Connection thêm khi cần
    pool_timeout=30,      # Timeout khi đợi
    pool_recycle=1800,    # Recycle sau 30 phút
    pool_pre_ping=True,   # Kiểm tra trước khi dùng
)
```

### SQLite Optimization (Development)

```python
# Tự động áp dụng PRAGMA
PRAGMA journal_mode=WAL;     # Concurrent reads
PRAGMA cache_size=-64000;    # 64MB cache
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=268435456;  # 256MB mmap
```

---

## 🗄️ CACHING STRATEGY

### Cache Layers

1. **Response Cache**: Cache HTTP responses
2. **Query Cache**: Cache database queries
3. **Application Cache**: Cache computed data

### Cache TTL Settings

```python
CACHE_TTL = {
    "INSTANT": 30,      # Real-time data
    "SHORT": 60,        # Frequently changing
    "MEDIUM": 300,      # Product lists (5 phút)
    "LONG": 900,        # Category data (15 phút)
    "EXTENDED": 3600,   # Static content (1 giờ)
}
```

### Sử dụng Cache

```python
from cache_advanced import cached, redis_client, invalidator

# Decorator caching
@cached("products", ttl=300)
def get_products(category=None):
    return db.query(Product).filter(...).all()

# Manual caching
data = redis_client.get("my_key")
if not data:
    data = expensive_operation()
    redis_client.set("my_key", data, ttl=300)

# Invalidate sau khi update
invalidator.invalidate_products()
```

### Cache Rules (Response)

```python
CACHE_RULES = {
    "/api/san_pham": 300,    # 5 phút
    "/api/banner": 900,      # 15 phút
    "/api/thu_vien": 3600,   # 1 giờ
    "/api/thong_ke": 60,     # 1 phút
}
```

---

## ⚡ API OPTIMIZATION

### Pagination

```python
# New pagination format
GET /api/san_pham/?page=1&page_size=20

# Response
{
    "items": [...],
    "pagination": {
        "total": 100,
        "page": 1,
        "page_size": 20,
        "total_pages": 5,
        "has_next": true,
        "has_prev": false
    }
}
```

### Bulk Operations

```python
# Tạo nhiều sản phẩm
POST /api/san_pham/bulk
Body: [{"name": "SP1", ...}, {"name": "SP2", ...}]

# Cập nhật nhiều sản phẩm
PUT /api/san_pham/bulk
Body: [{"id": 1, "price": 100}, {"id": 2, "price": 200}]

# Xóa nhiều sản phẩm
DELETE /api/san_pham/bulk
Body: [1, 2, 3, 4, 5]
```

### Quick Toggle

```python
# Toggle hot status
PATCH /api/san_pham/123/toggle-hot

# Toggle new status
PATCH /api/san_pham/123/toggle-new
```

---

## 🖥️ STREAMLIT ADMIN OPTIMIZATION

### Session State

```python
# Khởi tạo một lần
if "products_cache" not in st.session_state:
    st.session_state.products_cache = None

# Cache data trong session
@st.cache_data(ttl=300)
def fetch_products():
    return api_request("/api/san_pham/")
```

### Parallel Requests

```python
from concurrent.futures import ThreadPoolExecutor

# Fetch nhiều endpoints cùng lúc
def fetch_parallel(endpoints):
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch, ep): ep for ep in endpoints}
        return {futures[f]: f.result() for f in as_completed(futures)}
```

### Lazy Image Loading

```python
@st.cache_data(ttl=3600)
def get_image_thumbnail(url, size=(100, 100)):
    # Download và resize ảnh
    # Cache kết quả
    pass
```

### Skeleton Loading

```python
def show_loading_skeleton():
    st.markdown("""
    <style>
    .skeleton {
        background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
        animation: shimmer 1.5s infinite;
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## 📊 MONITORING & BENCHMARKING

### Health Check

```bash
python optimize_admin.py health-check

# Output
✅ API server: OK (0.123s)
✅ Database: OK (0.045s)
✅ Cache: OK (0.012s)
```

### Performance Benchmark

```bash
# Sequential benchmark
python optimize_admin.py benchmark --iterations 20

# Concurrent benchmark
python optimize_admin.py benchmark --concurrent --concurrency 10

# Output
/api/san_pham/    avg: 45.23ms    success: 100%
/api/banner/      avg: 12.45ms    success: 100%
/api/thu_vien/    avg: 89.12ms    success: 100%
```

### Cache Management

```bash
# Xem cache stats
python optimize_admin.py cache-stats

# Clear cache
python optimize_admin.py cache-clear
python optimize_admin.py cache-clear --pattern products

# Warm up cache
python optimize_admin.py cache-warmup
```

### Full Report

```bash
python optimize_admin.py report
# Tạo file: monitoring_report_20240115_143022.json
```

---

## 🎛️ CONFIGURATION TUNING

### Uvicorn Settings (Production)

```bash
uvicorn ung_dung.chinh:ung_dung \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http httptools \
    --limit-concurrency 100 \
    --timeout-keep-alive 30
```

### Gunicorn Settings (Alternative)

```bash
gunicorn ung_dung.chinh:ung_dung \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 5
```

### Nginx (Reverse Proxy)

```nginx
upstream backend {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    location /api/ {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering on;
        proxy_cache_valid 200 5m;
    }
}
```

---

## 📈 Performance Checklist

### Backend

- [ ] Database indexes đã được tạo
- [ ] Connection pooling đã cấu hình
- [ ] GZip compression enabled
- [ ] Cache headers được set
- [ ] Slow query logging enabled
- [ ] Response time monitoring

### Admin Panel

- [ ] `@st.cache_data` cho API calls
- [ ] `@st.cache_resource` cho HTTP session
- [ ] Pagination cho lists lớn
- [ ] Lazy loading cho images
- [ ] Parallel API requests
- [ ] Session state optimization

### Infrastructure

- [ ] Redis cache (production)
- [ ] Multiple workers (uvicorn/gunicorn)
- [ ] Nginx reverse proxy
- [ ] CDN cho static files
- [ ] Database connection limits

---

## 🐛 Troubleshooting

### Slow Responses

1. Check database indexes: `EXPLAIN ANALYZE <query>`
2. Check cache hit rate: `/api/cache/stats`
3. Check slow query log
4. Profile với `cProfile`

### Memory Issues

1. Check connection pool: `/api/health/detailed`
2. Reduce `pool_size` nếu cần
3. Enable `expire_on_commit=False`

### Cache Issues

1. Clear cache: `python optimize_admin.py cache-clear`
2. Check Redis connection
3. Verify cache TTL settings

---

## 📚 Tài Liệu Tham Khảo

- [FastAPI Performance](https://fastapi.tiangolo.com/deployment/concepts/)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [Streamlit Caching](https://docs.streamlit.io/library/advanced-features/caching)
- [Redis Documentation](https://redis.io/documentation)

---

## ✅ Kết Luận

Áp dụng các tối ưu hóa này sẽ giúp:

| Metric | Before | After |
|--------|--------|-------|
| API Response Time | 500ms - 2s | 50ms - 200ms |
| Page Load (Admin) | 3-5s | 1-2s |
| Concurrent Users | 10-20 | 50-100 |
| Memory Usage | High | Optimized |
| Database Queries | N+1 | Optimized |

**Lưu ý**: Luôn test trên staging trước khi deploy production!