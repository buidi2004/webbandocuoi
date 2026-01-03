from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Port 2014 là port PostgreSQL của bạn
DUONG_DAN_CSDL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:2014/postgres"
)

# Render dùng postgres:// nhưng SQLAlchemy cần postgresql://
if DUONG_DAN_CSDL.startswith("postgres://"):
    DUONG_DAN_CSDL = DUONG_DAN_CSDL.replace("postgres://", "postgresql://", 1)

dong_co = create_engine(DUONG_DAN_CSDL, echo=False, pool_pre_ping=True)
PhienLamViec = sessionmaker(autocommit=False, autoflush=False, bind=dong_co)
CoSo = declarative_base()

def kiem_tra_ket_noi():
    try:
        with dong_co.connect() as ket_noi:
            ket_noi.execute(text("SELECT 1"))
            print("Ket noi PostgreSQL thanh cong!")
            return True
    except Exception as loi:
        print(f"Loi ket noi: {loi}")
        return False

if __name__ == "__main__":
    kiem_tra_ket_noi()
