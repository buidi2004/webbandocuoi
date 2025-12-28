"""
Di chuyển CSDL: Tạo bảng đánh giá sản phẩm
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

    print("Đang tạo bảng product_reviews...")
    try:
        con_tro.execute("""
            CREATE TABLE IF NOT EXISTS product_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        print("Bảng product_reviews đã được tạo thành công.")
    except sqlite3.OperationalError as loi:
        print(f"Lỗi khi tạo bảng: {loi}")

    ket_noi.commit()
    ket_noi.close()
    print("Di chuyển đánh giá hoàn tất.")

if __name__ == "__main__":
    di_chuyen()
