"""
Di chuyển CSDL: Thêm các cột mới cho bảng chuyên gia
"""
import sqlite3
import os

DUONG_DAN_CSDL = "ivie.db"

def di_chuyen():
    if not os.path.exists(DUONG_DAN_CSDL):
        print(f"Không tìm thấy CSDL tại {DUONG_DAN_CSDL}")
        return

    ket_noi = sqlite3.connect(DUONG_DAN_CSDL)
    con_tro = ket_noi.cursor()

    try:
        # Thêm cột 'category' (danh mục)
        try:
            con_tro.execute("ALTER TABLE experts ADD COLUMN category TEXT DEFAULT 'makeup'")
            print("Đã thêm cột 'category'.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'category' đã tồn tại.")
            else:
                raise loi

        # Thêm cột 'level' (cấp độ)
        try:
            con_tro.execute("ALTER TABLE experts ADD COLUMN level TEXT DEFAULT 'senior'")
            print("Đã thêm cột 'level'.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'level' đã tồn tại.")
            else:
                raise loi

        # Thêm cột 'location' (địa điểm)
        try:
            con_tro.execute("ALTER TABLE experts ADD COLUMN location TEXT DEFAULT 'Hà Nội'")
            print("Đã thêm cột 'location'.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'location' đã tồn tại.")
            else:
                raise loi

        ket_noi.commit()
        print("Di chuyển chuyên gia hoàn tất thành công.")

    except Exception as loi:
        print(f"Di chuyển thất bại: {loi}")
        ket_noi.rollback()
    finally:
        ket_noi.close()

if __name__ == "__main__":
    di_chuyen()
