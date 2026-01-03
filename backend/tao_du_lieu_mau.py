"""
Script tạo dữ liệu mẫu cho IVIE Wedding Studio
Chạy: python tao_du_lieu_mau.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ung_dung.co_so_du_lieu import (
    PhienLamViec, khoi_tao_csdl,
    Banner, SanPham, ThuVien, GioiThieu, DiemNhanHome, DichVu, ChuyenGia
)

def tao_du_lieu_mau():
    """Tạo dữ liệu mẫu cho database"""
    
    # Khởi tạo database
    khoi_tao_csdl()
    
    db = PhienLamViec()
    
    try:
        # ========== BANNER ==========
        print("📸 Tạo banner...")
        banners = [
            Banner(
                title="Nơi Tình Yêu\nThăng Hoa",
                subtitle="Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với phong cách nghệ thuật độc đáo",
                image_url="/images/hero-wedding.jpg",
                is_active=True,
                order=1
            ),
            Banner(
                title="Bộ Sưu Tập\nVáy Cưới 2025",
                subtitle="Hơn 200 mẫu váy cưới cao cấp từ Luxury đến Minimalist",
                image_url="/images/wedding-dress-1.jpg",
                is_active=True,
                order=2
            ),
            Banner(
                title="Dịch Vụ\nTrọn Gói",
                subtitle="Chụp ảnh - Trang điểm - Váy cưới - Phụ kiện",
                image_url="/images/gallery-1.jpg",
                is_active=True,
                order=3
            ),
        ]
        
        for banner in banners:
            existing = db.query(Banner).filter(Banner.title == banner.title).first()
            if not existing:
                db.add(banner)
        
        # ========== SẢN PHẨM ==========
        print("👗 Tạo sản phẩm...")
        san_phams = [
            SanPham(
                name="Váy Cưới Luxury Đuôi Dài",
                code="VCD001",
                category="wedding_modern",
                sub_category="luxury",
                gender="female",
                description="Váy cưới cao cấp với đuôi dài 3m, chất liệu satin cao cấp, đính pha lê Swarovski",
                rental_price_day=2500000,
                rental_price_week=8000000,
                purchase_price=35000000,
                image_url="/images/wedding-dress-1.jpg",
                is_new=True,
                is_hot=True,
                fabric_type="Satin cao cấp",
                color="Trắng ngà",
                so_luong=5
            ),
            SanPham(
                name="Váy Cưới Minimalist",
                code="VCM001",
                category="wedding_modern",
                sub_category="minimalist",
                gender="female",
                description="Váy cưới phong cách tối giản, thanh lịch, phù hợp tiệc cưới ngoài trời",
                rental_price_day=1800000,
                rental_price_week=6000000,
                purchase_price=25000000,
                image_url="/images/wedding-dress-2.jpg",
                is_new=True,
                fabric_type="Organza",
                color="Trắng tinh",
                so_luong=8
            ),
            SanPham(
                name="Váy Cưới Công Chúa",
                code="VCCC001",
                category="wedding_modern",
                sub_category="princess",
                gender="female",
                description="Váy cưới phồng xòe kiểu công chúa, đính hoa 3D tinh xảo",
                rental_price_day=2200000,
                rental_price_week=7500000,
                purchase_price=32000000,
                image_url="/images/wedding-dress-3.jpg",
                is_hot=True,
                fabric_type="Tulle cao cấp",
                color="Trắng",
                so_luong=4
            ),
            SanPham(
                name="Áo Dài Cưới Nữ Đỏ",
                code="ADN001",
                category="traditional",
                sub_category="ao_dai",
                gender="female",
                description="Áo dài cưới truyền thống màu đỏ, thêu hoa sen vàng",
                rental_price_day=800000,
                rental_price_week=2500000,
                purchase_price=8000000,
                image_url="/images/aodai-nu-1.jpg",
                fabric_type="Lụa tơ tằm",
                color="Đỏ",
                so_luong=10
            ),
            SanPham(
                name="Áo Dài Cưới Nam",
                code="ADM001",
                category="traditional",
                sub_category="ao_dai",
                gender="male",
                description="Áo dài cưới nam truyền thống, chất liệu gấm cao cấp",
                rental_price_day=600000,
                rental_price_week=2000000,
                purchase_price=5000000,
                image_url="/images/aodai-nam-1.jpg",
                fabric_type="Gấm",
                color="Xanh đậm",
                so_luong=12
            ),
            SanPham(
                name="Vest Cưới Nam Đen",
                code="VCN001",
                category="wedding_modern",
                sub_category="suit",
                gender="male",
                description="Vest cưới nam cao cấp, cắt may theo số đo",
                rental_price_day=1200000,
                rental_price_week=4000000,
                purchase_price=15000000,
                image_url="/images/suit-1.jpg",
                is_new=True,
                fabric_type="Wool blend",
                color="Đen",
                so_luong=6
            ),
        ]
        
        for sp in san_phams:
            existing = db.query(SanPham).filter(SanPham.code == sp.code).first()
            if not existing:
                db.add(sp)
        
        # ========== THƯ VIỆN ẢNH ==========
        print("🖼️ Tạo thư viện ảnh...")
        thu_viens = [
            ThuVien(title="Bộ sưu tập Luxury", image_url="/images/gallery-1.jpg", order=1),
            ThuVien(title="Bộ sưu tập Minimalist", image_url="/images/gallery-2.jpg", order=2),
            ThuVien(title="Bộ sưu tập Vintage", image_url="/images/gallery-3.jpg", order=3),
        ]
        
        for tv in thu_viens:
            existing = db.query(ThuVien).filter(ThuVien.title == tv.title).first()
            if not existing:
                db.add(tv)
        
        # ========== GIỚI THIỆU ==========
        print("📝 Tạo giới thiệu...")
        existing_gt = db.query(GioiThieu).first()
        if not existing_gt:
            gioi_thieu = GioiThieu(
                title="Câu Chuyện Của IVIE",
                subtitle="Hơn 10 năm kinh nghiệm trong lĩnh vực cưới hỏi",
                description="Tại IVIE Studio, chúng tôi tin rằng mỗi cặp đôi đều có một câu chuyện tình yêu độc đáo xứng đáng được kể lại bằng ngôn ngữ hình ảnh tinh tế nhất. Với đội ngũ chuyên gia giàu kinh nghiệm và trang thiết bị hiện đại, chúng tôi cam kết mang đến cho bạn những khoảnh khắc đẹp nhất trong ngày trọng đại.",
                image_url="/images/hero-wedding.jpg",
                stat1_number="500+",
                stat1_label="Cặp Đôi Hạnh Phúc",
                stat2_number="10+",
                stat2_label="Năm Kinh Nghiệm",
                stat3_number="100%",
                stat3_label="Khách Hàng Hài Lòng"
            )
            db.add(gioi_thieu)
        
        # ========== ĐIỂM NHẤN TRANG CHỦ ==========
        print("⭐ Tạo điểm nhấn...")
        diem_nhans = [
            DiemNhanHome(
                title="Nhiếp Ảnh Nghệ Thuật",
                description="Ghi lại từng khoảnh khắc cảm xúc với phong cách blend màu độc quyền và góc máy sáng tạo.",
                image_url="/images/gallery-1.jpg",
                order=1
            ),
            DiemNhanHome(
                title="Trang Điểm Cô Dâu",
                description="Phong cách trang điểm tự nhiên, trong trẻo hoặc sắc sảo, tôn lên vẻ đẹp riêng của bạn.",
                image_url="/images/expert-1.jpg",
                order=2
            ),
            DiemNhanHome(
                title="Váy Cưới Thiết Kế",
                description="Bộ sưu tập hơn 200 mẫu váy cưới cao cấp, từ dòng Luxury đến Minimalist thanh lịch.",
                image_url="/images/wedding-dress-1.jpg",
                order=3
            ),
        ]
        
        for dn in diem_nhans:
            existing = db.query(DiemNhanHome).filter(DiemNhanHome.title == dn.title).first()
            if not existing:
                db.add(dn)
        
        # ========== DỊCH VỤ ==========
        print("🎯 Tạo dịch vụ...")
        dich_vus = [
            DichVu(
                name="Chụp Ảnh Cưới",
                description="Dịch vụ chụp ảnh cưới chuyên nghiệp với nhiều concept độc đáo",
                features='["Album 20x30", "100 ảnh gốc", "50 ảnh chỉnh sửa", "Trang điểm cô dâu"]',
                price_from=8000000,
                is_featured=True,
                icon="📸"
            ),
            DichVu(
                name="Thuê Váy Cưới",
                description="Bộ sưu tập váy cưới đa dạng từ Luxury đến Minimalist",
                features='["Váy cưới chính", "Váy dạ hội", "Phụ kiện đi kèm", "Chỉnh sửa miễn phí"]',
                price_from=2000000,
                is_featured=True,
                icon="👗"
            ),
            DichVu(
                name="Trang Điểm Cô Dâu",
                description="Dịch vụ makeup chuyên nghiệp cho ngày cưới",
                features='["Makeup cô dâu", "Làm tóc", "Phụ kiện", "Makeup tiệc tối"]',
                price_from=3000000,
                is_featured=True,
                icon="💄"
            ),
        ]
        
        for dv in dich_vus:
            existing = db.query(DichVu).filter(DichVu.name == dv.name).first()
            if not existing:
                db.add(dv)
        
        # ========== CHUYÊN GIA ==========
        print("👨‍🎨 Tạo chuyên gia...")
        chuyen_gias = [
            ChuyenGia(
                name="Nguyễn Thị Hương",
                title="Master Makeup Artist",
                bio="Hơn 15 năm kinh nghiệm trong lĩnh vực trang điểm cô dâu",
                years_experience=15,
                brides_count=500,
                specialties='["Makeup Hàn Quốc", "Makeup Châu Âu", "Makeup Vintage"]',
                image_url="/images/expert-1.jpg",
                category="makeup",
                level="master",
                is_top=True,
                price=5000000
            ),
            ChuyenGia(
                name="Trần Văn Minh",
                title="Senior Photographer",
                bio="Nhiếp ảnh gia chuyên nghiệp với phong cách nghệ thuật độc đáo",
                years_experience=10,
                brides_count=300,
                specialties='["Chụp phóng sự", "Chụp concept", "Chụp ngoại cảnh"]',
                image_url="/images/expert-2.jpg",
                category="photo",
                level="senior",
                is_top=True,
                price=8000000
            ),
        ]
        
        for cg in chuyen_gias:
            existing = db.query(ChuyenGia).filter(ChuyenGia.name == cg.name).first()
            if not existing:
                db.add(cg)
        
        db.commit()
        print("\n✅ Đã tạo dữ liệu mẫu thành công!")
        print("🔄 Hãy refresh lại trang web để xem kết quả.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    tao_du_lieu_mau()
