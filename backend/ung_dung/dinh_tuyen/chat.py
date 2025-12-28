from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..co_so_du_lieu import lay_csdl, TinNhanChat as TinNhanDB
from ..mo_hinh import TinNhanChatTao, TinNhanChat as TinNhanSchema
from .nguoi_dung import lay_user_hien_tai

bo_dinh_tuyen = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)

@bo_dinh_tuyen.post("/gui", response_model=TinNhanSchema)
def gui_tin_nhan(du_lieu: TinNhanChatTao, token: str, csdl: Session = Depends(lay_csdl)):
    """Gửi tin nhắn lên admin"""
    user = lay_user_hien_tai(token, csdl)
    
    tin_moi = TinNhanDB(
        user_id=user.id,
        tin_nhan=du_lieu.tin_nhan,
        is_from_admin=False
    )
    csdl.add(tin_moi)
    csdl.commit()
    csdl.refresh(tin_moi)
    return tin_moi

@bo_dinh_tuyen.get("/lich_su", response_model=list[TinNhanSchema])
def lay_lich_su_chat(token: str, csdl: Session = Depends(lay_csdl)):
    """Lấy lịch sử chat của người dùng"""
    user = lay_user_hien_tai(token, csdl)
    
    tin_nhans = csdl.query(TinNhanDB).filter(TinNhanDB.user_id == user.id).order_by(TinNhanDB.thoi_gian.asc()).all()
    return tin_nhans

@bo_dinh_tuyen.get("/admin/cac_phien_chat")
def lay_cac_phien_chat_admin(csdl: Session = Depends(lay_csdl)):
    """Admin: Lấy danh sách người dùng đã chat"""
    from ..co_so_du_lieu import NguoiDung
    from sqlalchemy import func
    
    # Lấy các user_id duy nhất từ bảng tin nhắn
    subquery = csdl.query(TinNhanDB.user_id).distinct().subquery()
    users = csdl.query(NguoiDung).filter(NguoiDung.id.in_(subquery)).all()
    
    res = []
    for u in users:
        # Lấy tin nhắn cuối cùng
        last_msg = csdl.query(TinNhanDB).filter(TinNhanDB.user_id == u.id).order_by(TinNhanDB.thoi_gian.desc()).first()
        res.append({
            "id": u.id,
            "username": u.username,
            "full_name": u.full_name,
            "last_message": last_msg.tin_nhan if last_msg else "",
            "last_time": last_msg.thoi_gian if last_msg else None
        })
    return sorted(res, key=lambda x: x["last_time"] or "", reverse=True)

@bo_dinh_tuyen.get("/admin/lich_su/{user_id}", response_model=list[TinNhanSchema])
def lay_lich_su_chat_admin(user_id: int, csdl: Session = Depends(lay_csdl)):
    """Admin: Lấy lịch sử chat với một user cụ thể"""
    return csdl.query(TinNhanDB).filter(TinNhanDB.user_id == user_id).order_by(TinNhanDB.thoi_gian.asc()).all()

@bo_dinh_tuyen.post("/admin/tra_loi/{user_id}", response_model=TinNhanSchema)
def admin_tra_loi(user_id: int, du_lieu: TinNhanChatTao, csdl: Session = Depends(lay_csdl)):
    """Admin: Trả lời tin nhắn cho người dùng"""
    tin_moi = TinNhanDB(
        user_id=user_id,
        tin_nhan=du_lieu.tin_nhan,
        is_from_admin=True
    )
    csdl.add(tin_moi)
    csdl.commit()
    csdl.refresh(tin_moi)
    return tin_moi
