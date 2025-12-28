"""
Di chuyển CSDL: Thêm cột trạng thái vào bảng liên hệ
Chạy script này một lần để thêm cột status vào database
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy import text
from ung_dung.co_so_du_lieu import dong_co

def di_chuyen_them_cot_trang_thai():
    """Thêm cột trạng thái vào bảng contact_submissions"""
    
    with dong_co.connect() as ket_noi:
        ket_qua = ket_noi.execute(text("PRAGMA table_info(contact_submissions)"))
        cac_cot = [dong[1] for dong in ket_qua.fetchall()]
        
        if 'status' in cac_cot:
            print("OK: Cột 'status' đã tồn tại")
            return True
        
        try:
            # Thêm cột status với giá trị mặc định là 'pending'
            ket_noi.execute(text("ALTER TABLE contact_submissions ADD COLUMN status VARCHAR DEFAULT 'pending'"))
            ket_noi.commit()
            print("OK: Đã thêm cột 'status' thành công!")
            
            # Cập nhật các bản ghi cũ (nếu có)
            ket_noi.execute(text("UPDATE contact_submissions SET status = 'pending' WHERE status IS NULL"))
            ket_noi.commit()
            print("OK: Đã cập nhật các bản ghi cũ")
            
            return True
            
        except Exception as loi:
            print(f"LỖI: {loi}")
            ket_noi.rollback()
            return False

if __name__ == "__main__":
    print("=" * 50)
    print("Di chuyển CSDL: Thêm cột trạng thái")
    print("=" * 50)
    
    thanh_cong = di_chuyen_them_cot_trang_thai()
    
    if thanh_cong:
        print("\nOK: Di chuyển hoàn tất!")
    else:
        print("\nLỖI: Di chuyển thất bại!")
