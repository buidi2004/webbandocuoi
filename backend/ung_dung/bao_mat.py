from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import os
import hashlib
import base64
from dotenv import load_dotenv

load_dotenv()

# Cấu hình bảo mật
bi_mat = os.getenv("SECRET_KEY", "ivie_wedding_secret_key_super_secure_123")
thuat_toan = "HS256"
thoi_gian_het_han_phut = 60 * 24 * 7 # 7 ngày

ngu_canh_mat_khau = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

def xac_minh_mat_khau(mat_khau_tho: str, mat_khau_bam: str) -> bool:
    """Kiểm tra mật khẩu khớp với mã băm"""
    # Hash password with SHA256 and encode to base64 to ensure it's within bcrypt's 72 byte limit
    mat_khau_sha = hashlib.sha256(mat_khau_tho.encode('utf-8')).digest()
    mat_khau_b64 = base64.b64encode(mat_khau_sha).decode('utf-8')
    return ngu_canh_mat_khau.verify(mat_khau_b64, mat_khau_bam)

def bam_mat_khau(mat_khau: str) -> str:
    """Tạo mã băm cho mật khẩu"""
    # Hash password with SHA256 and encode to base64 to ensure it's within bcrypt's 72 byte limit
    mat_khau_sha = hashlib.sha256(mat_khau.encode('utf-8')).digest()
    mat_khau_b64 = base64.b64encode(mat_khau_sha).decode('utf-8')
    return ngu_canh_mat_khau.hash(mat_khau_b64)

def tao_token_truy_cap(du_lieu: dict, het_han_sau: Union[timedelta, None] = None) -> str:
    """Tạo JWT Token"""
    copy_du_lieu = du_lieu.copy()
    if het_han_sau:
        het_han = datetime.utcnow() + het_han_sau
    else:
        het_han = datetime.utcnow() + timedelta(minutes=thoi_gian_het_han_phut)
    
    copy_du_lieu.update({"exp": het_han})
    encoded_jwt = jwt.encode(copy_du_lieu, bi_mat, algorithm=thuat_toan)
    return encoded_jwt
