"""
Di chuyển CSDL: Thêm các cột chi tiết cho sản phẩm
(Chất liệu, màu sắc, kích thước, tông trang điểm)
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

    cac_cot = [
        ("fabric_type", "TEXT"),      # Chất liệu vải
        ("color", "TEXT"),            # Màu sắc
        ("recommended_size", "TEXT"), # Kích thước đề xuất
        ("makeup_tone", "TEXT")       # Tông trang điểm phù hợp
    ]

    print("Đang di chuyển bảng products...")
    for ten_cot, kieu_cot in cac_cot:
        try:
            con_tro.execute(f"ALTER TABLE products ADD COLUMN {ten_cot} {kieu_cot}")
            print(f"Đã thêm cột {ten_cot}")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print(f"Cột {ten_cot} đã tồn tại.")
            else:
                print(f"Lỗi khi thêm {ten_cot}: {loi}")

    ket_noi.commit()
    ket_noi.close()
    print("Di chuyển chi tiết sản phẩm hoàn tất.")

if __name__ == "__main__":
    di_chuyen()
