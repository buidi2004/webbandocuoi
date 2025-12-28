"""
Di chuyển CSDL v3: Cập nhật cấu trúc bảng người dùng
(Thêm username, phone, address)
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
        # Tắt khóa ngoại tạm thời
        con_tro.execute("PRAGMA foreign_keys=OFF")
        
        # Kiểm tra nếu users_old tồn tại (từ lần di chuyển thất bại trước)
        con_tro.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_old'")
        if con_tro.fetchone():
            # Nếu tồn tại, kiểm tra xem 'users' đã được cập nhật chưa
            con_tro.execute("PRAGMA table_info(users)")
            cac_cot = [c[1] for c in con_tro.fetchall()]
            if "username" in cac_cot:
                print("Bảng 'users' đã có cột 'username'. Đang dọn dẹp users_old.")
                con_tro.execute("DROP TABLE users_old")
                ket_noi.commit()
                return

        # Bắt đầu giao dịch
        con_tro.execute("BEGIN TRANSACTION")

        # 1. Xóa các index cũ để tránh xung đột tên
        con_tro.execute("DROP INDEX IF EXISTS ix_users_email")
        con_tro.execute("DROP INDEX IF EXISTS ix_users_id")
        con_tro.execute("DROP INDEX IF EXISTS ix_users_username")

        # 2. Đổi tên bảng hiện tại
        try:
            con_tro.execute("ALTER TABLE users RENAME TO users_old")
        except sqlite3.OperationalError:
            print("Lưu ý: Bảng 'users' không tìm thấy hoặc đã được đổi tên.")

        # 3. Tạo bảng mới với cấu trúc cập nhật
        con_tro.execute("""
            CREATE TABLE users (
                id INTEGER NOT NULL,
                username VARCHAR NOT NULL,
                email VARCHAR,
                full_name VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                hashed_password VARCHAR NOT NULL,
                is_active BOOLEAN,
                PRIMARY KEY (id)
            )
        """)
        con_tro.execute("CREATE UNIQUE INDEX ix_users_username ON users (username)")
        con_tro.execute("CREATE UNIQUE INDEX ix_users_email ON users (email)")
        con_tro.execute("CREATE INDEX ix_users_id ON users (id)")

        # 4. Sao chép dữ liệu (nếu có)
        con_tro.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users_old'")
        if con_tro.fetchone():
            # Sử dụng email làm username cho người dùng hiện có
            con_tro.execute("""
                INSERT INTO users (id, username, email, full_name, hashed_password, is_active)
                SELECT id, email, email, full_name, hashed_password, is_active FROM users_old
            """)
            con_tro.execute("DROP TABLE users_old")

        con_tro.execute("COMMIT")
        print("Di chuyển bảng người dùng (v3) hoàn tất thành công.")

    except Exception as loi:
        print(f"Di chuyển thất bại: {loi}")
        try:
            con_tro.execute("ROLLBACK")
        except:
            pass
    finally:
        con_tro.execute("PRAGMA foreign_keys=ON")
        ket_noi.close()

if __name__ == "__main__":
    di_chuyen()
