"""
Migration script để tạo bảng combo - chạy tự động khi deploy
"""
import os
import sys

# Thêm đường dẫn backend vào sys.path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from ung_dung.co_so_du_lieu import CoSo, dong_co, Combo, PhienLamViec
    import json
    
    print("🔄 Đang kiểm tra và tạo bảng combo...")
    
    # Tạo bảng nếu chưa có
    CoSo.metadata.create_all(bind=dong_co)
    print("✅ Đã tạo/kiểm tra bảng combo!")
    
    # Kiểm tra xem đã có combo chưa
    phien = PhienLamViec()
    existing = phien.query(Combo).first()
    
    if not existing:
        print("📝 Đang thêm dữ liệu combo mẫu...")
        
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
            },
            {
                "ten": "COMBO PREMIUM LUXURY",
                "gia": 25000000,
                "gioi_han": 10,
                "mo_ta": "Gói cao cấp dành cho đám cưới hoàn hảo",
                "quyen_loi": json.dumps([
                    "10 Váy Cưới cao cấp tùy chọn (bao gồm dòng Luxury & Designer)",
                    "10 Bộ Vest Nam cao cấp",
                    "Chuyên gia chụp ảnh chuyên nghiệp",
                    "Chuyên gia quay phim cinematic",
                    "Dựng & chỉnh sửa ảnh chuyên nghiệp",
                    "Dựng phim cưới điện ảnh (10-15 phút)",
                    "Trang điểm cô dâu & gia đình bởi chuyên gia cao cấp",
                    "Album ảnh cao cấp 40x60cm (50 trang)",
                    "Phụ kiện & trang sức đi kèm",
                    "Hỗ trợ tư vấn concept & styling"
                ]),
                "hinh_anh": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600",
                "noi_bat": False,
                "hoat_dong": True
            }
        ]
        
        for combo_data in combos_mau:
            combo = Combo(**combo_data)
            phien.add(combo)
        
        phien.commit()
        print("✅ Đã thêm 4 combo mẫu!")
    else:
        print("ℹ️  Đã có combo trong database")
    
    phien.close()
    print("🎉 Migration hoàn thành!")
    
except Exception as e:
    print(f"❌ Lỗi migration: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
