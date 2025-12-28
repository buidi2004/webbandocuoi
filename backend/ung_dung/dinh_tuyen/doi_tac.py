from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..co_so_du_lieu import lay_csdl, KhieuNai as KhieuNaiDB, HoSoDoiTac as HoSoDoiTacDB
from ..mo_hinh import KhieuNaiTao, KhieuNai, HoSoDoiTacTao, HoSoDoiTac
from ..tien_ich_email import gui_email_thong_bao

bo_dinh_tuyen = APIRouter(
    prefix="/api/doi_tac",
    tags=["doi_tac"]
)

# --- Khiếu nại ---
@bo_dinh_tuyen.post("/khieu_nai", response_model=dict)
def gui_khieu_nai(data: KhieuNaiTao, user_id: Optional[int] = None, csdl: Session = Depends(lay_csdl)):
    kn = KhieuNaiDB(
        user_id=user_id,
        customer_name=data.customer_name,
        customer_phone=data.customer_phone,
        title=data.title,
        content=data.content
    )
    csdl.add(kn)
    csdl.commit()
    
    # Thông báo email
    gui_email_thong_bao(
        f" Khiếu nại mới: {data.title}",
        f"<p>Khách hàng: {data.customer_name or 'Ẩn danh'}</p><p>Nội dung: {data.content}</p>"
    )
    return {"message": "Gửi khiếu nại thành công", "id": kn.id}

@bo_dinh_tuyen.get("/admin/khieu_nai", response_model=List[KhieuNai])
def lay_danh_sach_khieu_nai(csdl: Session = Depends(lay_csdl)):
    return csdl.query(KhieuNaiDB).order_by(KhieuNaiDB.created_at.desc()).all()

@bo_dinh_tuyen.post("/admin/khieu_nai/{id}/tra_loi")
def tra_loi_khieu_nai(id: int, reply: str, csdl: Session = Depends(lay_csdl)):
    kn = csdl.query(KhieuNaiDB).filter(KhieuNaiDB.id == id).first()
    if not kn:
        raise HTTPException(status_code=404, detail="Không tìm thấy khiếu nại")
    kn.admin_reply = reply
    kn.status = "resolved"
    csdl.commit()
    return {"message": "Đã phản hồi khiếu nại"}

# --- Đối tác ---
@bo_dinh_tuyen.post("/dang_ky", response_model=dict)
def dang_ky_doi_tac(data: HoSoDoiTacTao, user_id: int, csdl: Session = Depends(lay_csdl)):
    # Check if existing application
    existing = csdl.query(HoSoDoiTacDB).filter(HoSoDoiTacDB.user_id == user_id, HoSoDoiTacDB.status == "pending").first()
    if existing:
        raise HTTPException(status_code=400, detail="Bạn đã có một hồ sơ đang chờ duyệt")
        
    hoso = HoSoDoiTacDB(
        user_id=user_id,
        partner_type=data.partner_type,
        full_name=data.full_name,
        phone=data.phone,
        email=data.email,
        experience=data.experience,
        portfolio_url=data.portfolio_url,
        cv_url=data.cv_url
    )
    csdl.add(hoso)
    csdl.commit()
    
    gui_email_thong_bao(
        f" Hồ sơ đối tác mới ({data.partner_type}): {data.full_name}",
        f"<p>Họ tên: {data.full_name}</p><p>Kinh nghiệm: {data.experience}</p>"
    )
    return {"message": "Đã gửi hồ sơ ứng tuyển thành công", "id": hoso.id}

@bo_dinh_tuyen.get("/ho_so/{user_id}", response_model=List[HoSoDoiTac])
def lay_ho_so_user(user_id: int, csdl: Session = Depends(lay_csdl)):
    return csdl.query(HoSoDoiTacDB).filter(HoSoDoiTacDB.user_id == user_id).all()

@bo_dinh_tuyen.get("/admin/danh_sach")
def admin_lay_danh_sach_doi_tac(csdl: Session = Depends(lay_csdl)):
    try:
        results = csdl.query(HoSoDoiTacDB).order_by(HoSoDoiTacDB.created_at.desc()).all()
        # Convert datetime to string for serialization
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "partner_type": r.partner_type,
                "full_name": r.full_name,
                "phone": r.phone,
                "email": r.email,
                "experience": r.experience,
                "portfolio_url": r.portfolio_url,
                "cv_url": r.cv_url,
                "status": r.status,
                "admin_reply": r.admin_reply,
                "contract_content": r.contract_content,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lấy danh sách đối tác: {str(e)}")

@bo_dinh_tuyen.post("/admin/{id}/phe_duyet")
def admin_phe_duyet_doi_tac(id: int, status: str, reply: str = "", contract: str = "", csdl: Session = Depends(lay_csdl)):
    hoso = csdl.query(HoSoDoiTacDB).filter(HoSoDoiTacDB.id == id).first()
    if not hoso:
        raise HTTPException(status_code=404, detail="Không tìm thấy hồ sơ")
        
    hoso.status = status # rejected, interviewing, accepted
    hoso.admin_reply = reply
    if status == "accepted":
        hoso.contract_content = contract
        
    csdl.commit()
    return {"message": f"Đã cập nhật trạng thái hồ sơ: {status}"}
