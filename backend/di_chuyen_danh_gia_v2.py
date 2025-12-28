"""
Di chuyển CSDL v2: Thêm cột ảnh và duyệt cho đánh giá
"""
import sqlite3
import os

DUONG_DAN_CSDL = "ivie.db"

def di_chuyen():
    if not os.path.exists(DUONG_DAN_CSDL):
        print(f"Không tìm thấy CSDL {DUONG_DAN_CSDL}.")
        return

    ket_noi = sqlite3.connect(DUONG_DAN_CSDL)
    con_tro = ket_noi.cursor()

    print("Đang thêm cột vào bảng product_reviews...")
    try:
        # Kiểm tra các cột đã tồn tại chưa
        con_tro.execute("PRAGMA table_info(product_reviews)")
        cac_cot = [cot[1] for cot in con_tro.fetchall()]
        
        if 'image_url' not in cac_cot:
            con_tro.execute("ALTER TABLE product_reviews ADD COLUMN image_url TEXT")
            print("Đã thêm cột 'image_url'.")
        
        if 'is_approved' not in cac_cot:
            con_tro.execute("ALTER TABLE product_reviews ADD COLUMN is_approved BOOLEAN DEFAULT 0")
            print("Đã thêm cột 'is_approved'.")
            
    except sqlite3.OperationalError as loi:
        print(f"Lỗi trong quá trình di chuyển: {loi}")

    ket_noi.commit()
    ket_noi.close()
    print("Di chuyển đánh giá v2 hoàn tất.")

if __name__ == "__main__":
    di_chuyen()
