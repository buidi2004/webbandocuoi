"""
Script thêm combo thứ 4 qua API (cho production)
"""
import requests
import json

# API URL production
API_URL = "https://ivie-backend.onrender.com"

# Data combo thứ 4
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

print("🚀 Đang thêm COMBO PREMIUM LUXURY vào production...")
print(f"   API: {API_URL}")

try:
    # Kiểm tra xem combo đã tồn tại chưa
    print("\n1️⃣ Kiểm tra combo hiện có...")
    response = requests.get(f"{API_URL}/pg/combo", timeout=30)
    
    if response.status_code == 200:
        combos = response.json()
        print(f"   ✓ Hiện có {len(combos)} combo")
        
        # Kiểm tra xem đã có combo 25 triệu chưa
        has_premium = any(c.get('gia') == 25000000 for c in combos)
        
        if has_premium:
            print("   ⚠️  Combo 25 triệu đã tồn tại!")
            print("\n📋 Danh sách combo hiện tại:")
            for c in combos:
                print(f"   - {c.get('ten')}: {c.get('gia'):,}đ")
        else:
            # Thêm combo mới
            print("\n2️⃣ Thêm combo mới...")
            response = requests.post(
                f"{API_URL}/pg/combo",
                json=combo_data,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                print("   ✅ Đã thêm COMBO PREMIUM LUXURY thành công!")
                result = response.json()
                print(f"   ID: {result.get('id')}")
                print(f"   Tên: {result.get('ten')}")
                print(f"   Giá: {result.get('gia'):,}đ")
            else:
                print(f"   ❌ Lỗi: {response.status_code}")
                print(f"   {response.text}")
    else:
        print(f"   ❌ Không thể lấy danh sách combo: {response.status_code}")
        print(f"   {response.text}")

except requests.Timeout:
    print("   ⏱️ Timeout: Server phản hồi quá lâu (có thể đang sleep)")
    print("   💡 Thử lại sau 1-2 phút khi server đã wake up")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

print("\n🎉 Hoàn thành!")
