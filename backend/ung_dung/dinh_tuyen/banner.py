from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..co_so_du_lieu import lay_csdl, Banner as BannerDB
from ..mo_hinh import Banner, BannerTao

bo_dinh_tuyen = APIRouter(
    prefix="/api/banner",
    tags=["banner"]
)

@bo_dinh_tuyen.get("/", response_model=List[Banner])
def lay_danh_sach_banner(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả banner (công khai)"""
    return csdl.query(BannerDB).filter(BannerDB.is_active == True).order_by(BannerDB.order).all()

@bo_dinh_tuyen.get("/tat_ca", response_model=List[Banner])
def lay_tat_ca_banner_admin(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả banner bao gồm cả banner bị ẩn (Admin)"""
    return csdl.query(BannerDB).order_by(BannerDB.order).all()

@bo_dinh_tuyen.post("/", response_model=Banner)
def tao_banner(banner: BannerTao, csdl: Session = Depends(lay_csdl)):
    """Tạo banner mới (Admin)"""
    banner_moi = BannerDB(**banner.dict())
    csdl.add(banner_moi)
    csdl.commit()
    csdl.refresh(banner_moi)
    return banner_moi

@bo_dinh_tuyen.put("/{id_banner}", response_model=Banner)
def cap_nhat_banner(id_banner: int, banner: BannerTao, csdl: Session = Depends(lay_csdl)):
    """Cập nhật banner (Admin)"""
    bn = csdl.query(BannerDB).filter(BannerDB.id == id_banner).first()
    if not bn:
        raise HTTPException(status_code=404, detail="Không tìm thấy banner")
    
    du_lieu = banner.dict()
    for khoa, gia_tri in du_lieu.items():
        setattr(bn, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(bn)
    return bn

@bo_dinh_tuyen.delete("/{id_banner}")
def xoa_banner(id_banner: int, csdl: Session = Depends(lay_csdl)):
    """Xóa banner (Admin)"""
    bn = csdl.query(BannerDB).filter(BannerDB.id == id_banner).first()
    if not bn:
        raise HTTPException(status_code=404, detail="Không tìm thấy banner")
    csdl.delete(bn)
    csdl.commit()
    return {"thong_bao": "Đã xóa banner thành công"}
