"""
Thêm combo 4 trực tiếp vào production database qua Admin Panel API
"""
import requests
import time

# Wake up backend trước
print("⏳ Wake up backend...")
try:
    r = requests.get("https://ivie-backend.onrender.com/", timeout=60)
    print(f"✅ Backend ready: {r.status_code}")
except Exception as e:
    print(f"❌ Lỗi wake up: {e}")
    exit(1)

time.sleep(2)

# Kiểm tra combo hiện tại
print("\n📋 Kiểm tra combo hiện tại...")
try:
    r = requests.get("https://ivie-backend.onrender.com/pg/combo", timeout=30)
    if r.status_code == 200:
        combos = r.json()
        print(f"Hiện có {len(combos)} combo:")
        for c in combos:
            print(f"  - {c['ten']}: {c['gia']:,}đ")
        
        # Kiểm tra đã có combo 25tr chưa
        if any(c['gia'] == 25000000 for c in combos):
            print("\n✅ Combo 25 triệu đã tồn tại!")
            exit(0)
    else:
        print(f"❌ Lỗi: {r.status_code} - {r.text}")
        exit(1)
except Exception as e:
    print(f"❌ Lỗi: {e}")
    exit(1)

# Thêm combo mới
print("\n➕ Thêm COMBO PREMIUM LUXURY...")
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
        "https://ivie-backend.onrender.com/pg/combo",
        json=combo_data,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if r.status_code in [200, 201]:
        result = r.json()
        print(f"✅ Thành công!")
        print(f"   ID: {result['id']}")
        print(f"   Tên: {result['ten']}")
        print(f"   Giá: {result['gia']:,}đ")
        print(f"\n🎉 Combo đã được thêm! Kiểm tra tại:")
        print(f"   https://ivie-frontend.onrender.com")
    else:
        print(f"❌ Lỗi: {r.status_code}")
        print(f"   {r.text}")
except Exception as e:
    print(f"❌ Lỗi: {e}")
