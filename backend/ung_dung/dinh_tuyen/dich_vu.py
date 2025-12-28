from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from ..co_so_du_lieu import lay_csdl, ChuyenGia as ChuyenGiaDB, DichVu as DichVuDB
from ..mo_hinh import ChuyenGia, ChuyenGiaTao, DichVu, DichVuTao

bo_dinh_tuyen = APIRouter(
    prefix="/api/dich_vu",
    tags=["dich_vu"]
)

# --- Chuyên gia ---
@bo_dinh_tuyen.get("/chuyen_gia", response_model=List[ChuyenGia])
def lay_danh_sach_chuyen_gia(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả hồ sơ chuyên gia"""
    chuyen_gia = csdl.query(ChuyenGiaDB).all()
    # Deserialize JSON strings
    for cg in chuyen_gia:
        if isinstance(cg.specialties, str):
            cg.specialties = json.loads(cg.specialties)
    return chuyen_gia

@bo_dinh_tuyen.get("/chuyen_gia/{id_chuyen_gia}", response_model=ChuyenGia)
def lay_chuyen_gia(id_chuyen_gia: int, csdl: Session = Depends(lay_csdl)):
    """Lấy chuyên gia cụ thể theo ID"""
    chuyen_gia = csdl.query(ChuyenGiaDB).filter(ChuyenGiaDB.id == id_chuyen_gia).first()
    if not chuyen_gia:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyên gia")
    # Deserialize JSON string
    if isinstance(chuyen_gia.specialties, str):
        chuyen_gia.specialties = json.loads(chuyen_gia.specialties)
    return chuyen_gia

@bo_dinh_tuyen.post("/chuyen_gia", response_model=ChuyenGia)
def tao_chuyen_gia(chuyen_gia: ChuyenGiaTao, csdl: Session = Depends(lay_csdl)):
    """Tạo chuyên gia mới (Admin)"""
    du_lieu = chuyen_gia.dict()
    if du_lieu.get("specialties"):
        du_lieu["specialties"] = json.dumps(du_lieu["specialties"])
    cg_moi = ChuyenGiaDB(**du_lieu)
    csdl.add(cg_moi)
    csdl.commit()
    csdl.refresh(cg_moi)
    # Re-parse for response
    if isinstance(cg_moi.specialties, str):
        cg_moi.specialties = json.loads(cg_moi.specialties)
    return cg_moi

@bo_dinh_tuyen.put("/chuyen_gia/{id_chuyen_gia}", response_model=ChuyenGia)
def cap_nhat_chuyen_gia(id_chuyen_gia: int, chuyen_gia: ChuyenGiaTao, csdl: Session = Depends(lay_csdl)):
    """Cập nhật chuyên gia (Admin)"""
    cg = csdl.query(ChuyenGiaDB).filter(ChuyenGiaDB.id == id_chuyen_gia).first()
    if not cg:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyên gia")
    
    du_lieu = chuyen_gia.dict()
    if du_lieu.get("specialties"):
        du_lieu["specialties"] = json.dumps(du_lieu["specialties"])
        
    for khoa, gia_tri in du_lieu.items():
        setattr(cg, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(cg)
    if isinstance(cg.specialties, str):
        cg.specialties = json.loads(cg.specialties)
    return cg

@bo_dinh_tuyen.delete("/chuyen_gia/{id_chuyen_gia}")
def xoa_chuyen_gia(id_chuyen_gia: int, csdl: Session = Depends(lay_csdl)):
    """Xóa chuyên gia (Admin)"""
    cg = csdl.query(ChuyenGiaDB).filter(ChuyenGiaDB.id == id_chuyen_gia).first()
    if not cg:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy chuyên gia")
    csdl.delete(cg)
    csdl.commit()
    return {"thong_bao": "Đã xóa chuyên gia thành công"}

# --- Dịch vụ ---
@bo_dinh_tuyen.get("/", response_model=List[DichVu])
def lay_danh_sach_dich_vu(csdl: Session = Depends(lay_csdl)):
    """Lấy tất cả dịch vụ trang điểm"""
    dich_vu = csdl.query(DichVuDB).all()
    # Deserialize JSON strings
    for dv in dich_vu:
        if isinstance(dv.features, str):
            dv.features = json.loads(dv.features)
    return dich_vu

@bo_dinh_tuyen.post("/", response_model=DichVu)
def tao_dich_vu(dich_vu: DichVuTao, csdl: Session = Depends(lay_csdl)):
    """Tạo dịch vụ mới (Admin)"""
    du_lieu = dich_vu.dict()
    if du_lieu.get("features"):
        du_lieu["features"] = json.dumps(du_lieu["features"])
    dv_moi = DichVuDB(**du_lieu)
    csdl.add(dv_moi)
    csdl.commit()
    csdl.refresh(dv_moi)
    if isinstance(dv_moi.features, str):
        dv_moi.features = json.loads(dv_moi.features)
    return dv_moi

@bo_dinh_tuyen.put("/{id_dich_vu}", response_model=DichVu)
def cap_nhat_dich_vu(id_dich_vu: int, dich_vu: DichVuTao, csdl: Session = Depends(lay_csdl)):
    """Cập nhật dịch vụ (Admin)"""
    dv = csdl.query(DichVuDB).filter(DichVuDB.id == id_dich_vu).first()
    if not dv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ")
    
    du_lieu = dich_vu.dict()
    if du_lieu.get("features"):
        du_lieu["features"] = json.dumps(du_lieu["features"])
        
    for khoa, gia_tri in du_lieu.items():
        setattr(dv, khoa, gia_tri)
    
    csdl.commit()
    csdl.refresh(dv)
    if isinstance(dv.features, str):
        dv.features = json.loads(dv.features)
    return dv

@bo_dinh_tuyen.delete("/{id_dich_vu}")
def xoa_dich_vu(id_dich_vu: int, csdl: Session = Depends(lay_csdl)):
    """Xóa dịch vụ (Admin)"""
    dv = csdl.query(DichVuDB).filter(DichVuDB.id == id_dich_vu).first()
    if not dv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Không tìm thấy dịch vụ")
    csdl.delete(dv)
    csdl.commit()
    return {"thong_bao": "Đã xóa dịch vụ thành công"}
