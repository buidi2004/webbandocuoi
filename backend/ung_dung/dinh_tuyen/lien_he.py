from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel
from ..co_so_du_lieu import lay_csdl, LienHeGui as LienHeDB
from ..mo_hinh import LienHeTao, LienHePhanHoi, LienHe
from ..tien_ich_email import gui_email_thong_bao

class CapNhatTrangThai(BaseModel):
    status: str

bo_dinh_tuyen = APIRouter(
    prefix="/api/lien_he",
    tags=["lien_he"]
)

@bo_dinh_tuyen.get("/", response_model=List[LienHe])
def lay_danh_sach_lien_he(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả các liên hệ (dành cho admin)"""
    # Sắp xếp theo ID giảm dần để lấy mới nhất trước
    return csdl.query(LienHeDB).order_by(LienHeDB.id.desc()).all()

@bo_dinh_tuyen.get("/{id_lien_he}", response_model=LienHe)
def lay_lien_he(id_lien_he: int, csdl: Session = Depends(lay_csdl)):
    """Lấy liên hệ cụ thể theo ID"""
    lien_he = csdl.query(LienHeDB).filter(LienHeDB.id == id_lien_he).first()
    if not lien_he:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy liên hệ")
    return lien_he

@bo_dinh_tuyen.delete("/{id_lien_he}")
def xoa_lien_he(id_lien_he: int, csdl: Session = Depends(lay_csdl)):
    """Xóa liên hệ (dành cho admin)"""
    lien_he = csdl.query(LienHeDB).filter(LienHeDB.id == id_lien_he).first()
    if not lien_he:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy liên hệ")
    csdl.delete(lien_he)
    csdl.commit()
    return {"message": "Đã xóa liên hệ thành công"}

@bo_dinh_tuyen.patch("/{id_lien_he}/status", response_model=dict)
def cap_nhat_trang_thai(id_lien_he: int, data: CapNhatTrangThai, csdl: Session = Depends(lay_csdl)):
    """Cập nhật trạng thái liên hệ"""
    lien_he = csdl.query(LienHeDB).filter(LienHeDB.id == id_lien_he).first()
    if not lien_he:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy liên hệ")
    
    if data.status not in ["pending", "contacted", "completed"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Status không hợp lệ. Chỉ chấp nhận: pending, contacted, completed")
    
    lien_he.status = data.status
    csdl.commit()
    csdl.refresh(lien_he)
    return {"message": "Đã cập nhật trạng thái", "status": data.status, "id": id_lien_he}

@bo_dinh_tuyen.post("/", response_model=LienHePhanHoi)
def gui_lien_he(lien_he: LienHeTao, csdl: Session = Depends(lay_csdl)):
    """Gửi form liên hệ"""
    lh = LienHeDB(
        name=lien_he.name,
        email=lien_he.email,
        phone=lien_he.phone,
        address=lien_he.address, # New field
        message=lien_he.message,
        created_at=datetime.now().isoformat(),
        status="pending"
    )
    csdl.add(lh)
    csdl.commit()
    
    # Gửi email thông báo
    tieu_de = f"📩 Khách hàng liên hệ: {lien_he.name}"
    noi_dung = f"""
    <h3>Có tin nhắn mới từ khách hàng!</h3>
    <p><b>Họ tên:</b> {lien_he.name}</p>
    <p><b>Email:</b> {lien_he.email}</p>
    <p><b>Điện thoại:</b> {lien_he.phone}</p>
    <p><b>Địa chỉ:</b> {lien_he.address}</p>
    <p><b>Nội dung:</b> {lien_he.message}</p>
    <hr/>
    <p>Gửi từ hệ thống IVIE Wedding.</p>
    """
    gui_email_thong_bao(tieu_de, noi_dung)
    
    return LienHePhanHoi(
        message="Cảm ơn bạn đã liên hệ! Chúng tôi sẽ phản hồi trong thời gian sớm nhất.",
        success=True
    )

@bo_dinh_tuyen.post("/dat_lich", response_model=LienHePhanHoi)
def gui_dat_lich(lien_he: LienHeTao, csdl: Session = Depends(lay_csdl)):
    """Gửi yêu cầu đặt lịch"""
    lh = LienHeDB(
        name=lien_he.name,
        email=lien_he.email,
        phone=lien_he.phone,
        address=lien_he.address, # New field
        message=f"YÊU CẦU ĐẶT LỊCH: {lien_he.message}",
        created_at=datetime.now().isoformat()
    )
    csdl.add(lh)
    csdl.commit()
    
    # Gửi email thông báo
    tieu_de = f"🗓️ Khách đặt lịch mới: {lien_he.name}"
    noi_dung = f"""
    <h3>Có yêu cầu ĐẶT LỊCH mới!</h3>
    <p><b>Họ tên:</b> {lien_he.name}</p>
    <p><b>Email:</b> {lien_he.email}</p>
    <p><b>Điện thoại:</b> {lien_he.phone}</p>
    <p><b>Địa chỉ:</b> {lien_he.address}</p>
    <p><b>Ghi chú/Thời gian:</b> {lien_he.message}</p>
    <hr/>
    <p>Gần khách hàng hơn với IVIE Wedding.</p>
    """
    gui_email_thong_bao(tieu_de, noi_dung)
    
    return LienHePhanHoi(
        message="Đặt lịch thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.",
        success=True
    )
