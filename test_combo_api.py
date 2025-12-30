"""
Test combo API với thông tin chi tiết
"""
import requests
import json

API_URL = "https://ivie-backend.onrender.com"

print("🔍 Test 1: Kiểm tra health của backend...")
try:
    r = requests.get(f"{API_URL}/", timeout=60)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

print("\n🔍 Test 2: Kiểm tra endpoint combo...")
try:
    r = requests.get(f"{API_URL}/pg/combo", timeout=60)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        combos = r.json()
        print(f"   ✅ Có {len(combos)} combo")
        for c in combos:
            print(f"      - {c.get('ten')}: {c.get('gia'):,}đ")
    else:
        print(f"   Response: {r.text[:500]}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

print("\n🔍 Test 3: Thử thêm combo mới...")
combo_data = {
    "ten": "COMBO PREMIUM LUXURY",
    "gia": 25000000,
    "gioi_han": 10,
    "mo_ta": "Gói cao cấp với đội ngũ chuyên gia hàng đầu - Dành cho đám cưới hoàn hảo",
    "quyen_loi": [
        "10 Váy Cưới cao cấp tùy chọn (bao gồm dòng Luxury & Designer)",
        "10 Bộ Vest Nam cao cấp",
        "🌟 Chuyên gia chụp ảnh HÀNG ĐẦU - Kinh nghiệm 10+ năm",
        "🌟 Chuyên gia quay phim cinematic HÀNG ĐẦU",
        "🌟 Dựng & chỉnh sửa ảnh bởi chuyên gia HÀNG ĐẦU",
        "🌟 Dựng phim cưới điện ảnh (10-15 phút) - Đạo diễn chuyên nghiệp",
        "🌟 Trang điểm cô dâu & gia đình bởi chuyên gia makeup HÀNG ĐẦU",
        "🌟 Album ảnh cao cấp 40x60cm (50 trang) - Thiết kế độc quyền",
        "Phụ kiện & trang sức đi kèm",
        "Hỗ trợ tư vấn concept & styling bởi chuyên gia"
    ],
    "hinh_anh": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600",
    "noi_bat": False,
    "hoat_dong": True
}

try:
    r = requests.post(
        f"{API_URL}/pg/combo",
        json=combo_data,
        headers={"Content-Type": "application/json"},
        timeout=60
    )
    print(f"   Status: {r.status_code}")
    if r.status_code in [200, 201]:
        print(f"   ✅ Thành công!")
        print(f"   Response: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"   Response: {r.text[:500]}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")
