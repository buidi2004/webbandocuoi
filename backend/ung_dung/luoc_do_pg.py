"""
Pydantic Schemas cho PostgreSQL API - IVIE Studio
Đã cập nhật để khớp với tên cột trong database (tiếng Anh)
"""
from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
import json


# ============ SẢN PHẨM ============
class SanPhamCoSo(BaseModel):
    name: str
    code: str
    category: str
    sub_category: Optional[str] = None
    gender: str
    description: Optional[str] = None
    rental_price_day: float
    rental_price_week: float
    purchase_price: float
    image_url: Optional[str] = None
    is_new: bool = False
    is_hot: bool = False
    fabric_type: Optional[str] = None
    color: Optional[str] = None
    recommended_size: Optional[str] = None
    makeup_tone: Optional[str] = None
    so_luong: Optional[int] = 10
    het_hang: Optional[bool] = False
    gallery_images: Optional[List[str]] = None
    accessories: Optional[List[Any]] = None


class SanPhamTao(SanPhamCoSo):
    pass


class SanPhamCapNhat(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    rental_price_day: Optional[float] = None
    rental_price_week: Optional[float] = None
    purchase_price: Optional[float] = None
    image_url: Optional[str] = None
    is_new: Optional[bool] = None
    is_hot: Optional[bool] = None
    fabric_type: Optional[str] = None
    color: Optional[str] = None
    recommended_size: Optional[str] = None
    makeup_tone: Optional[str] = None
    so_luong: Optional[int] = None
    het_hang: Optional[bool] = None
    gallery_images: Optional[List[str]] = None
    accessories: Optional[List[Any]] = None


class SanPhamPhanHoi(SanPhamCoSo):
    id: int

    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('gallery_images', 'accessories', mode='before')
    @classmethod
    def parse_json_fields(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        if isinstance(v, list):
            return v
        return []


# ============ NGƯỜI DÙNG ============
class NguoiDungCoSo(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class NguoiDungTao(NguoiDungCoSo):
    password: str


class NguoiDungCapNhat(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class NguoiDungPhanHoi(NguoiDungCoSo):
    id: int
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


# ============ ĐƠN HÀNG ============
class DonHangCoSo(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    total_amount: float


class DonHangTao(DonHangCoSo):
    user_id: Optional[int] = None


class DonHangCapNhat(BaseModel):
    status: Optional[str] = None
    shipping_address: Optional[str] = None


class DonHangPhanHoi(DonHangCoSo):
    id: int
    user_id: Optional[int] = None
    status: str = "pending"
    order_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ============ CHI TIẾT ĐƠN HÀNG ============
class ChiTietDonHangCoSo(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float


class ChiTietDonHangTao(ChiTietDonHangCoSo):
    pass


class ChiTietDonHangPhanHoi(ChiTietDonHangCoSo):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============ LIÊN HỆ ============
class LienHeCoSo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    message: str


class LienHeTao(LienHeCoSo):
    pass


class LienHeCapNhat(BaseModel):
    status: Optional[str] = None


class LienHePhanHoi(LienHeCoSo):
    id: int
    status: str = "pending"
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============ THƯ VIỆN ẢNH ============
class ThuVienAnhCoSo(BaseModel):
    image_url: str
    title: Optional[str] = None
    order: int = 0


class ThuVienAnhTao(ThuVienAnhCoSo):
    pass


class ThuVienAnhCapNhat(BaseModel):
    image_url: Optional[str] = None
    title: Optional[str] = None
    order: Optional[int] = None


class ThuVienAnhPhanHoi(ThuVienAnhCoSo):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============ COMBO ============
class ComboCoSo(BaseModel):
    ten: str
    gia: float
    gioi_han: int
    mo_ta: Optional[str] = None
    quyen_loi: Optional[List[str]] = []
    hinh_anh: Optional[str] = None
    noi_bat: bool = False
    hoat_dong: bool = True


class ComboTao(ComboCoSo):
    pass


class ComboCapNhat(BaseModel):
    ten: Optional[str] = None
    gia: Optional[float] = None
    gioi_han: Optional[int] = None
    mo_ta: Optional[str] = None
    quyen_loi: Optional[List[str]] = None
    hinh_anh: Optional[str] = None
    noi_bat: Optional[bool] = None
    hoat_dong: Optional[bool] = None


class ComboPhanHoi(ComboCoSo):
    id: int
    ngay_tao: Optional[datetime] = None

    @field_validator('quyen_loi', mode='before')
    @classmethod
    def parse_quyen_loi(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        return v or []

    model_config = ConfigDict(from_attributes=True)
