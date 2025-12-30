"""
Script để tạo bảng combo trong database
"""
import sys
sys.path.insert(0, 'backend')

from ung_dung.co_so_du_lieu import CoSo, dong_co, Combo
import json

# Tạo bảng
print("Đang tạo bảng combo...")
CoSo.metadata.create_all(bind=dong_co)
print("✅ Đã tạo bảng combo thành công!")

# Thêm dữ liệu mẫu
from ung_dung.co_so_du_lieu import PhienLamViec

phien = PhienLamViec()

# Kiểm tra xem đã có combo chưa
existing = phien.query(Combo).first()
if not existing:
    print("\nĐang thêm dữ liệu mẫu...")
    
    combos_mau = [
        {
            "ten": "COMBO KHỞI ĐẦU",
            "gia": 2000000,
            "gioi_han": 2,
            "mo_ta": "Gói cơ bản cho các cặp đôi",
            "quyen_loi": json.dumps([
                "2 Váy Cưới tùy chọn",
                "2 Bộ Vest Nam tùy chọn",
                "Miễn phí giặt ủi",
                "Hỗ trợ chỉnh sửa kích cỡ"
            ]),
            "hinh_anh": "https://images.unsplash.com/photo-1594552072238-b8a33785b261?auto=format&fit=crop&q=80&w=600",
            "noi_bat": False,
            "hoat_dong": True
        },
        {
            "ten": "COMBO TIẾT KIỆM",
            "gia": 5000000,
            "gioi_han": 5,
            "mo_ta": "Sự lựa chọn phổ biến nhất",
            "quyen_loi": json.dumps([
                "5 Váy Cưới tùy chọn",
                "5 Bộ Vest Nam tùy chọn",
                "Phụ kiện đi kèm miễn phí",
                "Giữ đồ trong 3 ngày"
            ]),
            "hinh_anh": "https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&q=80&w=600",
            "noi_bat": True,
            "hoat_dong": True
        },
        {
            "ten": "COMBO VIP TOÀN NĂNG",
            "gia": 15000000,
            "gioi_han": 7,
            "mo_ta": "Trọn gói ngày cưới hoàn hảo",
            "quyen_loi": json.dumps([
                "7 Váy Cưới tùy chọn (bao gồm dòng Luxury)",
                "7 Bộ Vest Nam cao cấp",
                "Trang điểm cô dâu & mẹ uyên ương",
                "Chụp ảnh Pre-wedding & Tiệc cưới",
                "Quay phim phóng sự cưới",
                "Miễn phí chỉnh sửa ảnh & dựng phim"
            ]),
            "hinh_anh": "https://images.unsplash.com/photo-1511285560982-1351cdeb9821?auto=format&fit=crop&q=80&w=600",
            "noi_bat": False,
            "hoat_dong": True
        }
    ]
    
    for combo_data in combos_mau:
        combo = Combo(**combo_data)
        phien.add(combo)
    
    phien.commit()
    print("✅ Đã thêm 3 combo mẫu!")
else:
    print("\n⚠️ Đã có combo trong database, bỏ qua thêm dữ liệu mẫu")

phien.close()
print("\n🎉 Hoàn thành!")
