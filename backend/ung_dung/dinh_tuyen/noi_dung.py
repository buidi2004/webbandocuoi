from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..co_so_du_lieu import lay_csdl, GioiThieu as GioiThieuDB, DiemNhanHome as DiemNhanDB
from ..mo_hinh import GioiThieu, GioiThieuCoBan, DiemNhanHome, DiemNhanHomeTao

bo_dinh_tuyen = APIRouter(
    prefix="/api/noi_dung",
    tags=["noi_dung"]
)

# --- Giới thiệu (About Us) ---
@bo_dinh_tuyen.get("/gioi_thieu", response_model=GioiThieu)
def lay_gioi_thieu(csdl: Session = Depends(lay_csdl)):
    gt = csdl.query(GioiThieuDB).first()
    if not gt:
        # Tạo mặc định nếu chưa có
        gt = GioiThieuDB(
            title="Câu Chuyện Của IVIE",
            subtitle="Hơn 10 năm kinh nghiệm trong lĩnh vực cưới hỏi",
            description="Tại IVIE Studio, chúng tôi tin rằng mỗi cặp đôi đều có một câu chuyện tình yêu độc đáo xứng đáng được kể lại bằng ngôn ngữ hình ảnh tinh tế nhất.",
            image_url="/images/about-wedding.jpg",
            stat1_number="500+", stat1_label="Cặp Đôi",
            stat2_number="10+", stat2_label="Năm Kinh Nghiệm",
            stat3_number="100%", stat3_label="Hài Lòng"
        )
        csdl.add(gt)
        csdl.commit()
        csdl.refresh(gt)
    return gt

@bo_dinh_tuyen.put("/gioi_thieu", response_model=GioiThieu)
def cap_nhat_gioi_thieu(du_lieu: GioiThieuCoBan, csdl: Session = Depends(lay_csdl)):
    gt = csdl.query(GioiThieuDB).first()
    if not gt:
        gt = GioiThieuDB()
        csdl.add(gt)
    
    for khoa, gia_tri in du_lieu.dict().items():
        setattr(gt, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(gt)
    return gt

# --- Điểm nhấn trang chủ (Home Highlights) ---
@bo_dinh_tuyen.get("/diem_nhan", response_model=List[DiemNhanHome])
def lay_danh_sach_diem_nhan(csdl: Session = Depends(lay_csdl)):
    return csdl.query(DiemNhanDB).order_by(DiemNhanDB.order).all()

@bo_dinh_tuyen.post("/diem_nhan", response_model=DiemNhanHome)
def tao_diem_nhan(diem_nhan: DiemNhanHomeTao, csdl: Session = Depends(lay_csdl)):
    dn_moi = DiemNhanDB(**diem_nhan.dict())
    csdl.add(dn_moi)
    csdl.commit()
    csdl.refresh(dn_moi)
    return dn_moi

@bo_dinh_tuyen.put("/diem_nhan/{id_dn}", response_model=DiemNhanHome)
def cap_nhat_diem_nhan(id_dn: int, diem_nhan: DiemNhanHomeTao, csdl: Session = Depends(lay_csdl)):
    dn = csdl.query(DiemNhanDB).filter(DiemNhanDB.id == id_dn).first()
    if not dn:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục này")
    
    for khoa, gia_tri in diem_nhan.dict().items():
        setattr(dn, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(dn)
    return dn

@bo_dinh_tuyen.delete("/diem_nhan/{id_dn}")
def xoa_diem_nhan(id_dn: int, csdl: Session = Depends(lay_csdl)):
    dn = csdl.query(DiemNhanDB).filter(DiemNhanDB.id == id_dn).first()
    if not dn:
        raise HTTPException(status_code=404, detail="Không tìm thấy mục này")
    csdl.delete(dn)
    csdl.commit()
    return {"thong_bao": "Đã xóa thành công"}
