"""
Script tạo bảng combo trong production database
"""
import requests
import time

API_URL = "https://ivie-backend.onrender.com"

print("🔧 Tạo bảng combo trong production database...")
print(f"   API: {API_URL}")

try:
    # Gọi endpoint khởi tạo bảng
    print("\n1️⃣ Đang gọi endpoint khởi tạo bảng...")
    response = requests.post(
        f"{API_URL}/pg/khoi-tao-bang",
        timeout=60
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✅ {response.json().get('thong_bao')}")
        
        # Đợi 2 giây
        time.sleep(2)
        
        # Kiểm tra lại endpoint combo
        print("\n2️⃣ Kiểm tra endpoint combo...")
        response = requests.get(f"{API_URL}/pg/combo", timeout=30)
        
        if response.status_code == 200:
            combos = response.json()
            print(f"   ✅ Endpoint combo hoạt động! Hiện có {len(combos)} combo")
            
            if len(combos) < 4:
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
                
                response = requests.post(
                    f"{API_URL}/pg/combo",
                    json=combo_data,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    print(f"   ✅ Đã thêm combo thành công!")
                    print(f"      ID: {result.get('id')}")
                    print(f"      Tên: {result.get('ten')}")
                    print(f"      Giá: {result.get('gia'):,}đ")
                else:
                    print(f"   ❌ Lỗi thêm combo: {response.status_code}")
                    print(f"      {response.text}")
            else:
                print("   ℹ️  Đã có đủ 4 combo")
        else:
            print(f"   ❌ Endpoint combo vẫn lỗi: {response.status_code}")
    else:
        print(f"   ❌ Lỗi: {response.text}")

except requests.Timeout:
    print("   ⏱️ Timeout: Server phản hồi quá lâu")
except Exception as e:
    print(f"   ❌ Lỗi: {e}")

print("\n🎉 Hoàn thành!")
