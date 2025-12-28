from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from ..co_so_du_lieu import lay_csdl, YeuThich as YeuThichDB, SanPham as SanPhamDB
from .nguoi_dung import lay_user_hien_tai

bo_dinh_tuyen = APIRouter(
    prefix="/api/yeu_thich",
    tags=["wishlist"]
)

# Pydantic models
class YeuThichItem(BaseModel):
    id: int
    product_id: int
    product_name: str | None = None
    product_image: str | None = None
    product_price: float | None = None
    created_at: datetime | None

# API endpoints
@bo_dinh_tuyen.get("/", response_model=List[YeuThichItem])
def lay_danh_sach_yeu_thich(token: str, csdl: Session = Depends(lay_csdl)):
    """Lấy danh sách sản phẩm yêu thích của user"""
    user = lay_user_hien_tai(token, csdl)
    
    items = csdl.query(YeuThichDB).filter(YeuThichDB.user_id == user.id).all()
    result = []
    for item in items:
        product = csdl.query(SanPhamDB).filter(SanPhamDB.id == item.product_id).first()
        result.append({
            "id": item.id,
            "product_id": item.product_id,
            "product_name": product.name if product else None,
            "product_image": product.image_url if product else None,
            "product_price": product.rental_price_day if product else None,
            "created_at": item.created_at
        })
    return result

@bo_dinh_tuyen.post("/them/{product_id}")
def them_yeu_thich(product_id: int, token: str, csdl: Session = Depends(lay_csdl)):
    """Thêm sản phẩm vào danh sách yêu thích"""
    user = lay_user_hien_tai(token, csdl)
    
    # Kiểm tra đã có trong wishlist chưa
    existing = csdl.query(YeuThichDB).filter(
        YeuThichDB.user_id == user.id,
        YeuThichDB.product_id == product_id
    ).first()
    
    if existing:
        return {"message": "Sản phẩm đã có trong danh sách yêu thích", "id": existing.id}
    
    # Kiểm tra sản phẩm tồn tại
    product = csdl.query(SanPhamDB).filter(SanPhamDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    yeu_thich = YeuThichDB(user_id=user.id, product_id=product_id)
    csdl.add(yeu_thich)
    csdl.commit()
    csdl.refresh(yeu_thich)
    
    return {"message": "Đã thêm vào yêu thích", "id": yeu_thich.id}

@bo_dinh_tuyen.delete("/xoa/{product_id}")
def xoa_yeu_thich(product_id: int, token: str, csdl: Session = Depends(lay_csdl)):
    """Xóa sản phẩm khỏi danh sách yêu thích"""
    user = lay_user_hien_tai(token, csdl)
    
    item = csdl.query(YeuThichDB).filter(
        YeuThichDB.user_id == user.id,
        YeuThichDB.product_id == product_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy trong danh sách yêu thích")
    
    csdl.delete(item)
    csdl.commit()
    return {"message": "Đã xóa khỏi yêu thích"}

@bo_dinh_tuyen.get("/kiem_tra/{product_id}")
def kiem_tra_yeu_thich(product_id: int, token: str, csdl: Session = Depends(lay_csdl)):
    """Kiểm tra sản phẩm có trong wishlist không"""
    user = lay_user_hien_tai(token, csdl)
    
    existing = csdl.query(YeuThichDB).filter(
        YeuThichDB.user_id == user.id,
        YeuThichDB.product_id == product_id
    ).first()
    
    return {"is_favorite": existing is not None}
