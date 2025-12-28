from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..co_so_du_lieu import lay_csdl, ThuVien as ThuVienDB
from ..mo_hinh import ThuVien, ThuVienTao

bo_dinh_tuyen = APIRouter(
    prefix="/api/thu_vien",
    tags=["thu_vien"]
)

@bo_dinh_tuyen.get("/", response_model=List[ThuVien])
def lay_danh_sach_thu_vien(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả ảnh trong thư viện"""
    return csdl.query(ThuVienDB).order_by(ThuVienDB.order).all()

@bo_dinh_tuyen.post("/", response_model=ThuVien)
def tao_thu_vien(item: ThuVienTao, csdl: Session = Depends(lay_csdl)):
    """Thêm ảnh mới vào thư viện (Admin)"""
    moi = ThuVienDB(**item.dict())
    csdl.add(moi)
    csdl.commit()
    csdl.refresh(moi)
    return moi

@bo_dinh_tuyen.delete("/{id_item}")
def xoa_thu_vien(id_item: int, csdl: Session = Depends(lay_csdl)):
    """Xóa ảnh khỏi thư viện (Admin)"""
    item = csdl.query(ThuVienDB).filter(ThuVienDB.id == id_item).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")
    csdl.delete(item)
    csdl.commit()
    return {"thong_bao": "Đã xóa ảnh khỏi thư viện"}
