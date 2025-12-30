"""
Đợi Render deploy xong và test combo API
"""
import requests
import time
import json

API_URL = "https://ivie-backend.onrender.com"

print("⏳ Đợi Render deploy... (khoảng 2-3 phút)")
print("   Bạn có thể theo dõi tại: https://dashboard.render.com/")
print()

# Đợi 2 phút
for i in range(120, 0, -10):
    print(f"   Còn {i} giây...", end="\r")
    time.sleep(10)

print("\n\n🔍 Bắt đầu test...")

# Test 1: Wake up backend
print("\n1️⃣ Wake up backend...")
try:
    r = requests.get(f"{API_URL}/", timeout=60)
    print(f"   ✅ Backend đã sẵn sàng: {r.status_code}")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")
    exit(1)

time.sleep(2)

# Test 2: Kiểm tra endpoint combo
print("\n2️⃣ Kiểm tra endpoint combo...")
try:
    r = requests.get(f"{API_URL}/pg/combo", timeout=30)
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        combos = r.json()
        print(f"   ✅ Endpoint hoạt động! Hiện có {len(combos)} combo:")
        for c in combos:
            print(f"      - {c.get('ten')}: {c.get('gia'):,}đ")
        
        # Kiểm tra xem đã có combo 25 triệu chưa
        has_premium = any(c.get('gia') == 25000000 for c in combos)
        
        if has_premium:
            print("\n   🎉 Combo PREMIUM LUXURY đã tồn tại!")
        else:
            print("\n3️⃣ Thêm combo PREMIUM LUXURY...")
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
            
            r = requests.post(
                f"{API_URL}/pg/combo",
                json=combo_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if r.status_code in [200, 201]:
                result = r.json()
                print(f"   ✅ Đã thêm combo thành công!")
                print(f"      ID: {result.get('id')}")
                print(f"      Tên: {result.get('ten')}")
                print(f"      Giá: {result.get('gia'):,}đ")
                
                print("\n4️⃣ Kiểm tra frontend...")
                print(f"   🌐 Truy cập: https://ivie-frontend.onrender.com")
                print(f"   📍 Vào trang 'Chọn Gói Dịch Vụ'")
                print(f"   ✅ Combo PREMIUM LUXURY sẽ hiển thị!")
            else:
                print(f"   ❌ Lỗi thêm combo: {r.status_code}")
                print(f"      {r.text}")
    else:
        print(f"   ❌ Endpoint combo lỗi: {r.status_code}")
        print(f"      {r.text[:500]}")
        print("\n   💡 Thử thêm qua Admin Panel:")
        print(f"      1. Truy cập: https://ivie-admin.onrender.com")
        print(f"      2. Đăng nhập: ceo / 123456")
        print(f"      3. Vào 'Quản lý Combo' > 'THÊM/SỬA COMBO'")
        print(f"      4. Xem file HUONG_DAN_THEM_COMBO_PRODUCTION.md")
        
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

print("\n🎉 Hoàn thành!")
