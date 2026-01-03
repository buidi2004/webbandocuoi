import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from .cache_utils import CacheControlMiddleware
from .co_so_du_lieu import khoi_tao_csdl
from .dinh_tuyen import (
    api_pg,
    banner,
    blog,
    chat,
    dich_vu,
    doi_tac,
    don_hang,
    lien_he,
    nguoi_dung,
    noi_dung,
    san_pham,
    tap_tin,
    thong_ke,
    thu_vien,
    yeu_thich,
)

load_dotenv()

ung_dung = FastAPI(
    title="IVIE Wedding Studio API (Tiếng Việt)",
    description="API cho website IVIE Wedding Studio",
    version="1.0.0",
)

# GZip Middleware - nén response > 500 bytes để giảm TTFB
ung_dung.add_middleware(GZipMiddleware, minimum_size=500)

# Cache Control Middleware - tự động thêm cache headers cho GET requests
ung_dung.add_middleware(CacheControlMiddleware)

# Cấu hình CORS
# Lấy từ biến môi trường CORS_ORIGINS (cấu hình trong render.yaml)
# Development: cho phép localhost
# Production: giới hạn domain cụ thể từ Render
cors_origins_env = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
)
nguon_goc = [origin.strip() for origin in cors_origins_env.split(",")]

# Nếu không có CORS_ORIGINS trong env (development), cho phép tất cả
if not os.getenv("CORS_ORIGINS"):
    nguon_goc = ["*"]

ung_dung.add_middleware(
    CORSMiddleware,
    allow_origins=nguon_goc,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

# Gắn thư mục tĩnh cho hình ảnh (để Admin panel và API có thể truy cập)
# Đường dẫn tính từ backend/ung_dung/chinh.py -> ../../frontend/public/images
thu_muc_anh = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../frontend/public/images")
)
if os.path.exists(thu_muc_anh):
    ung_dung.mount("/images", StaticFiles(directory=thu_muc_anh), name="images")
else:
    print(f"Lưu ý: Không tìm thấy thư mục ảnh tại {thu_muc_anh}")

# Gắn thư mục tep_tin cho ảnh người dùng tải lên
thu_muc_tep_tin = "tep_tin"
os.makedirs(thu_muc_tep_tin, exist_ok=True)
ung_dung.mount("/tep_tin", StaticFiles(directory=thu_muc_tep_tin), name="tep_tin")

# Bao gồm các bộ định tuyến
ung_dung.include_router(san_pham.bo_dinh_tuyen)
ung_dung.include_router(dich_vu.bo_dinh_tuyen)
ung_dung.include_router(lien_he.bo_dinh_tuyen)
ung_dung.include_router(tap_tin.bo_dinh_tuyen)
ung_dung.include_router(banner.bo_dinh_tuyen)
ung_dung.include_router(noi_dung.bo_dinh_tuyen)
ung_dung.include_router(thu_vien.bo_dinh_tuyen)
ung_dung.include_router(nguoi_dung.bo_dinh_tuyen)
ung_dung.include_router(chat.bo_dinh_tuyen)
ung_dung.include_router(doi_tac.bo_dinh_tuyen)
ung_dung.include_router(blog.bo_dinh_tuyen)
ung_dung.include_router(yeu_thich.bo_dinh_tuyen)
ung_dung.include_router(thong_ke.bo_dinh_tuyen)
ung_dung.include_router(api_pg.bo_dinh_tuyen)
ung_dung.include_router(don_hang.bo_dinh_tuyen)


@ung_dung.on_event("startup")
def su_kien_khoi_dong():
    """Khởi tạo cơ sở dữ liệu khi khởi động"""
    khoi_tao_csdl()


@ung_dung.get("/")
def doc_goc():
    return {
        "thong_bao": "Chào mừng đến với API IVIE Wedding Studio",
        "tai_lieu": "/docs",
        "phien_ban": "1.0.0",
    }


@ung_dung.get("/suckhoe")
def kiem_tra_suc_khoe():
    return {"trang_thai": "khoe_manh"}


@ung_dung.get("/api/health")
def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy"}


@ung_dung.get("/api/db-test")
def test_database():
    """Test database connection and table creation"""
    import os

    from sqlalchemy import text

    from .co_so_du_lieu import NguoiDung, PhienLamViec, dong_co

    try:
        # Test connection
        with dong_co.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            conn_status = "OK"

        # Test table exists
        db = PhienLamViec()
        try:
            user_count = db.query(NguoiDung).count()
            table_status = f"OK - {user_count} users"
        except Exception as e:
            table_status = f"ERROR - {str(e)}"
        finally:
            db.close()

        return {
            "database_url": os.getenv("DATABASE_URL", "Not set")[:50] + "...",
            "connection": conn_status,
            "users_table": table_status,
        }
    except Exception as e:
        return {
            "error": str(e),
            "database_url": os.getenv("DATABASE_URL", "Not set")[:50] + "...",
        }
