import hashlib
from passlib.context import CryptContext

# Test bcrypt locally
ngu_canh_mat_khau = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

password = "test123456"
print(f"Original password: {password}")
print(f"Password length: {len(password)} chars, {len(password.encode('utf-8'))} bytes")

# Hash with SHA256 first
mat_khau_sha = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(f"\nSHA256 hash: {mat_khau_sha}")
print(f"SHA256 length: {len(mat_khau_sha)} chars, {len(mat_khau_sha.encode('utf-8'))} bytes")

# Then bcrypt
try:
    hashed = ngu_canh_mat_khau.hash(mat_khau_sha)
    print(f"\nBcrypt hash: {hashed}")
    print("SUCCESS!")
except Exception as e:
    print(f"\nERROR: {e}")
