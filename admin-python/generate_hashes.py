"""
Script để generate password hashes
"""
import bcrypt

def generate_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

# Generate hashes
ceo_hash = generate_hash("123456")
nv_hash = generate_hash("12345")

print("CEO password hash (123456):")
print(ceo_hash)
print()
print("Nhân viên password hash (12345):")
print(nv_hash)
print()

# Verify
print("Verifying CEO hash...")
assert bcrypt.checkpw("123456".encode(), ceo_hash.encode())
print("✓ CEO hash verified")

print("Verifying Nhân viên hash...")
assert bcrypt.checkpw("12345".encode(), nv_hash.encode())
print("✓ Nhân viên hash verified")
