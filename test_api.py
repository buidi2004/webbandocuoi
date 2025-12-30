import requests
import json
import time

print("Đợi 60 giây để Render deploy...")
time.sleep(60)

print("\n=== TEST DATABASE CONNECTION ===")
url_db_test = "https://ivie-backend.onrender.com/api/db-test"
try:
    response = requests.get(url_db_test)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Lỗi: {e}")

# Test đăng ký
print("\n=== TEST ĐĂNG KÝ ===")
url_dang_ky = "https://ivie-backend.onrender.com/api/nguoi_dung/dang_ky"
data_dang_ky = {
    "username": f"testuser{int(time.time())}",  # Unique username
    "password": "test123456",
    "full_name": "Test User",
    "phone": "0123456789",
    "email": f"test{int(time.time())}@example.com",  # Unique email
    "address": "Ha Noi"
}

try:
    response = requests.post(url_dang_ky, json=data_dang_ky)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Lỗi: {e}")

print("\n=== TEST HEALTH CHECK ===")
url_health = "https://ivie-backend.onrender.com/api/health"
try:
    response = requests.get(url_health)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Lỗi: {e}")
