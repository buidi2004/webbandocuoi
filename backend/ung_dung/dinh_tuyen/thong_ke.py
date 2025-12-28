from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..co_so_du_lieu import (
    lay_csdl, 
    SanPham as SanPhamDB, 
    DonHang as DonHangDB, 
    LienHeGui as LienHeDB,
    NguoiDung as NguoiDungDB,
    BaiViet as BaiVietDB
)

bo_dinh_tuyen = APIRouter(
    prefix="/api/thong_ke",
    tags=["statistics"]
)

@bo_dinh_tuyen.get("/tong_quan")
def thong_ke_tong_quan(csdl: Session = Depends(lay_csdl)):
    """Thống kê tổng quan cho Admin Dashboard"""
    
    # Đếm tổng số
    tong_san_pham = csdl.query(func.count(SanPhamDB.id)).scalar()
    tong_don_hang = csdl.query(func.count(DonHangDB.id)).scalar()
    tong_nguoi_dung = csdl.query(func.count(NguoiDungDB.id)).scalar()
    tong_lien_he = csdl.query(func.count(LienHeDB.id)).scalar()
    
    # Đơn hàng theo trạng thái
    don_hang_pending = csdl.query(func.count(DonHangDB.id)).filter(DonHangDB.status == "pending").scalar()
    don_hang_completed = csdl.query(func.count(DonHangDB.id)).filter(DonHangDB.status == "delivered").scalar()
    
    # Tổng doanh thu
    tong_doanh_thu = csdl.query(func.sum(DonHangDB.total_amount)).filter(
        DonHangDB.status.in_(["delivered", "processing", "shipped"])
    ).scalar() or 0
    
    # Liên hệ chưa xử lý
    lien_he_moi = csdl.query(func.count(LienHeDB.id)).filter(LienHeDB.status == "pending").scalar()
    
    return {
        "tong_san_pham": tong_san_pham,
        "tong_don_hang": tong_don_hang,
        "tong_nguoi_dung": tong_nguoi_dung,
        "tong_lien_he": tong_lien_he,
        "don_hang_cho_xu_ly": don_hang_pending,
        "don_hang_hoan_thanh": don_hang_completed,
        "tong_doanh_thu": tong_doanh_thu,
        "lien_he_chua_xu_ly": lien_he_moi
    }

@bo_dinh_tuyen.get("/don_hang_theo_thang")
def thong_ke_don_hang_theo_thang(csdl: Session = Depends(lay_csdl)):
    """Thống kê đơn hàng theo 6 tháng gần nhất"""
    results = []
    
    for i in range(5, -1, -1):
        ngay = datetime.now() - timedelta(days=i*30)
        thang = ngay.strftime("%m/%Y")
        
        start_date = datetime(ngay.year, ngay.month, 1)
        if ngay.month == 12:
            end_date = datetime(ngay.year + 1, 1, 1)
        else:
            end_date = datetime(ngay.year, ngay.month + 1, 1)
        
        so_don = csdl.query(func.count(DonHangDB.id)).filter(
            DonHangDB.order_date >= start_date,
            DonHangDB.order_date < end_date
        ).scalar()
        
        doanh_thu = csdl.query(func.sum(DonHangDB.total_amount)).filter(
            DonHangDB.order_date >= start_date,
            DonHangDB.order_date < end_date,
            DonHangDB.status.in_(["delivered", "processing", "shipped"])
        ).scalar() or 0
        
        results.append({
            "thang": thang,
            "so_don_hang": so_don,
            "doanh_thu": doanh_thu
        })
    
    return results

@bo_dinh_tuyen.get("/san_pham_ban_chay")
def san_pham_ban_chay(limit: int = 5, csdl: Session = Depends(lay_csdl)):
    """Top sản phẩm bán chạy"""
    from ..co_so_du_lieu import ChiTietDonHang as ChiTietDB
    
    result = csdl.query(
        SanPhamDB.id,
        SanPhamDB.name,
        SanPhamDB.code,
        func.sum(ChiTietDB.quantity).label('total_sold')
    ).join(ChiTietDB, SanPhamDB.id == ChiTietDB.product_id)\
     .group_by(SanPhamDB.id)\
     .order_by(func.sum(ChiTietDB.quantity).desc())\
     .limit(limit)\
     .all()
    
    return [
        {
            "id": r[0],
            "name": r[1],
            "code": r[2],
            "total_sold": r[3] or 0
        }
        for r in result
    ]
