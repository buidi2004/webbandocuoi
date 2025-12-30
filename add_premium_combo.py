"""
Script thêm combo PREMIUM 25 triệu vào database
"""
import sys
sys.path.insert(0, 'backend')

from ung_dung.co_so_du_lieu import PhienLamViec, Combo
import json

phien = PhienLamViec()

# Kiểm tra xem combo 25 triệu đã tồn tại chưa
existing = phien.query(Combo).filter(Combo.gia == 25000000).first()

if existing:
    print("⚠️  Combo 25 triệu đã tồn tại!")
    print(f"   ID: {existing.id}, Tên: {existing.ten}")
    phien.close()
    sys.exit(0)

print("📝 Đang thêm COMBO PREMIUM 25 triệu...")

combo_premium = Combo(
    ten="COMBO PREMIUM LUXURY",
    gia=25000000,
    gioi_han=10,
    mo_ta="Gói cao cấp dành cho đám cưới hoàn hảo",
    quyen_loi=json.dumps([
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
    hinh_anh="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600",
    noi_bat=False,
    hoat_dong=True
)

phien.add(combo_premium)
phien.commit()

print("✅ Đã thêm COMBO PREMIUM LUXURY - 25.000.000đ!")
print(f"   ID: {combo_premium.id}")
print(f"   Giới hạn: {combo_premium.gioi_han} bộ đồ")
print(f"   Quyền lợi: {len(json.loads(combo_premium.quyen_loi))} items")

phien.close()
print("🎉 Hoàn thành!")
