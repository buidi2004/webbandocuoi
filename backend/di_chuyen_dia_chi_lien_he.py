"""
Di chuyển CSDL: Thêm cột địa chỉ vào bảng liên hệ
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
        # Thêm cột 'address' vào bảng contact_submissions
        try:
            con_tro.execute("ALTER TABLE contact_submissions ADD COLUMN address TEXT")
            print("Đã thêm cột 'address' vào bảng contact_submissions.")
        except sqlite3.OperationalError as loi:
            if "duplicate column name" in str(loi):
                print("Cột 'address' đã tồn tại.")
            else:
                raise loi

        ket_noi.commit()
        print("Di chuyển địa chỉ liên hệ hoàn tất thành công.")

    except Exception as loi:
        print(f"Di chuyển thất bại: {loi}")
        ket_noi.rollback()
    finally:
        ket_noi.close()

if __name__ == "__main__":
    di_chuyen()
