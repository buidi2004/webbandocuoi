"""
Script cập nhật combo PREMIUM để nhấn mạnh chuyên gia hàng đầu
"""
import sys
sys.path.insert(0, 'backend')

from ung_dung.co_so_du_lieu import PhienLamViec, Combo
import json

phien = PhienLamViec()

# Tìm combo 25 triệu
combo = phien.query(Combo).filter(Combo.gia == 25000000).first()

if not combo:
    print("❌ Không tìm thấy combo 25 triệu!")
    phien.close()
    sys.exit(1)

print(f"📝 Đang cập nhật combo: {combo.ten}")

# Cập nhật mô tả và quyền lợi với nhấn mạnh chuyên gia hàng đầu
combo.mo_ta = "Gói cao cấp với đội ngũ chuyên gia hàng đầu - Dành cho đám cưới hoàn hảo"
combo.quyen_loi = json.dumps([
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
])

phien.commit()

print("✅ Đã cập nhật combo PREMIUM LUXURY!")
print(f"   Mô tả mới: {combo.mo_ta}")
print(f"   Quyền lợi: {len(json.loads(combo.quyen_loi))} items")
print("\n📋 Chi tiết quyền lợi:")
for idx, ql in enumerate(json.loads(combo.quyen_loi), 1):
    print(f"   {idx}. {ql}")

phien.close()
print("\n🎉 Hoàn thành!")
