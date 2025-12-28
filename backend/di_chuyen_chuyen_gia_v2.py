"""
Di chuyển CSDL v2: Thêm cột giá và top cho chuyên gia
"""
import sqlite3
import os

DUONG_DAN_CSDL = "ivie.db"

def di_chuyen():
    ket_noi = sqlite3.connect(DUONG_DAN_CSDL)
    con_tro = ket_noi.cursor()

    try:
        # Thêm cột 'price' (giá thuê chuyên gia)
        try:
            con_tro.execute("ALTER TABLE experts ADD COLUMN price REAL DEFAULT 1000000")
            print("Đã thêm cột 'price'.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'price' đã tồn tại.")
            else:
                raise loi

        # Thêm cột 'is_top' (gợi ý hàng đầu)
        try:
            con_tro.execute("ALTER TABLE experts ADD COLUMN is_top BOOLEAN DEFAULT 0")
            print("Đã thêm cột 'is_top'.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'is_top' đã tồn tại.")
            else:
                raise loi

        ket_noi.commit()
        print("Di chuyển chuyên gia v2 hoàn tất.")

    except Exception as loi:
        print(f"Di chuyển v2 thất bại: {loi}")
        ket_noi.rollback()
    finally:
        ket_noi.close()

if __name__ == "__main__":
    di_chuyen()
