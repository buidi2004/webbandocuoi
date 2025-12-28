"""
Seed database with initial data
Run this file once to populate the database
"""
import json
from ung_dung.co_so_du_lieu import PhienLamViec, khoi_tao_csdl, SanPham, ChuyenGia, DichVu

def seed_data():
    # Initialize database
    khoi_tao_csdl()
    
    db = PhienLamViec()
    
    # Check if data already exists
    if db.query(SanPham).first():
        print("Database already seeded!")
        return
    
    # Seed Products - Wedding Dresses
    products = [
        # Modern Wedding Dresses - Female
        SanPham(
            name="Váy Cưới Công Chúa Ren Pháp",
            code="WD-001",
            category="wedding_modern",
            gender="female",
            description="Váy cưới công chúa với ren Pháp cao cấp, đuôi dài cathedral",
            rental_price_day=3000000,
            rental_price_week=15000000,
            purchase_price=50000000,
            image_url="/images/wedding-dress-1.jpg",
            is_new=True,
            is_hot=False
        ),
        SanPham(
            name="Váy Cưới Đuôi Cá Pha Lê",
            code="WD-002",
            category="wedding_modern",
            gender="female",
            description="Váy cưới đuôi cá với pha lê và đá quý đính kết",
            rental_price_day=3500000,
            rental_price_week=18000000,
            purchase_price=65000000,
            image_url="/images/wedding-dress-2.jpg",
            is_new=False,
            is_hot=True
        ),
        SanPham(
            name="Váy Cưới Minimalist Tối Giản",
            code="WD-003",
            category="wedding_modern",
            gender="female",
            description="Váy cưới minimalist với đường cắt hiện đại",
            rental_price_day=2500000,
            rental_price_week=12000000,
            purchase_price=45000000,
            image_url="/images/wedding-dress-3.jpg",
            is_new=False,
            is_hot=False
        ),
        
        # Modern Suits - Male
        SanPham(
            name="Vest Cưới Ý Cao Cấp",
            code="MS-001",
            category="wedding_modern",
            gender="male",
            description="Vest cưới Ý với chất liệu cao cấp",
            rental_price_day=1500000,
            rental_price_week=7000000,
            purchase_price=25000000,
            image_url="/images/suit-1.jpg",
            is_new=True,
            is_hot=False
        ),
        SanPham(
            name="Tuxedo Đen Sang Trọng",
            code="MS-002",
            category="wedding_modern",
            gender="male",
            description="Tuxedo đen sang trọng cho chú rể",
            rental_price_day=2000000,
            rental_price_week=9000000,
            purchase_price=35000000,
            image_url="/images/suit-2.jpg",
            is_new=False,
            is_hot=True
        ),
        SanPham(
            name="Vest Xám Modern Fit",
            code="MS-003",
            category="wedding_modern",
            gender="male",
            description="Vest xám modern fit thanh lịch",
            rental_price_day=1200000,
            rental_price_week=5500000,
            purchase_price=20000000,
            image_url="/images/suit-3.jpg",
            is_new=False,
            is_hot=False
        ),
        
        # Traditional Ao Dai - Female
        SanPham(
            name="Áo Dài Đỏ Thêu Rồng Phượng",
            code="AD-F001",
            category="traditional",
            gender="female",
            description="Áo dài đỏ với họa tiết thêu rồng phượng tinh xảo",
            rental_price_day=1500000,
            rental_price_week=7000000,
            purchase_price=18000000,
            image_url="/images/aodai-nu-1.jpg",
            is_new=True,
            is_hot=False
        ),
        SanPham(
            name="Áo Dài Vàng Thêu Hoa Sen",
            code="AD-F002",
            category="traditional",
            gender="female",
            description="Áo dài vàng với họa tiết hoa sen",
            rental_price_day=1800000,
            rental_price_week=8500000,
            purchase_price=22000000,
            image_url="/images/aodai-nu-2.jpg",
            is_new=False,
            is_hot=True
        ),
        SanPham(
            name="Áo Dài Trắng Ren Cao Cấp",
            code="AD-F003",
            category="traditional",
            gender="female",
            description="Áo dài trắng với ren cao cấp",
            rental_price_day=1200000,
            rental_price_week=5500000,
            purchase_price=15000000,
            image_url="/images/aodai-nu-3.jpg",
            is_new=False,
            is_hot=False
        ),
        
        # Traditional Ao Dai - Male
        SanPham(
            name="Áo Dài Nam Đỏ Thêu Rồng",
            code="AD-M001",
            category="traditional",
            gender="male",
            description="Áo dài nam đỏ với họa tiết rồng thêu tay",
            rental_price_day=1000000,
            rental_price_week=4500000,
            purchase_price=12000000,
            image_url="/images/aodai-nam-1.jpg",
            is_new=True,
            is_hot=False
        ),
        SanPham(
            name="Áo Dài Nam Xanh Gấm",
            code="AD-M002",
            category="traditional",
            gender="male",
            description="Áo dài nam xanh với chất liệu gấm",
            rental_price_day=1200000,
            rental_price_week=5500000,
            purchase_price=15000000,
            image_url="/images/aodai-nam-2.jpg",
            is_new=False,
            is_hot=True
        ),
        SanPham(
            name="Áo Dài Nam Đen Lịch Lãm",
            code="AD-M003",
            category="traditional",
            gender="male",
            description="Áo dài nam đen lịch lãm",
            rental_price_day=900000,
            rental_price_week=4000000,
            purchase_price=10000000,
            image_url="/images/aodai-nam-3.jpg",
            is_new=False,
            is_hot=False
        ),
    ]
    
    # Seed Experts
    experts = [
        ChuyenGia(
            name="Minh Anh",
            title="Trưởng Phòng Makeup",
            bio="Chuyên gia trang điểm cưới với hơn 15 năm kinh nghiệm. Từng làm việc tại New York Fashion Week và các show thời trang lớn.",
            years_experience=15,
            brides_count=500,
            specialties=json.dumps(["Bridal Makeup", "HD Makeup", "Korean Style"]),
            image_url="/images/expert-1.jpg",
            social_facebook="https://facebook.com/minhanh.makeup",
            social_instagram="https://instagram.com/minhanh.makeup"
        ),
        ChuyenGia(
            name="Thu Hà",
            title="Makeup Artist Cao Cấp",
            bio="Chuyên về phong cách trang điểm Hàn Quốc tự nhiên. Đã được đào tạo bởi các chuyên gia hàng đầu tại Seoul.",
            years_experience=12,
            brides_count=400,
            specialties=json.dumps(["K-Beauty", "Natural Look", "Skin Care"]),
            image_url="/images/expert-2.jpg",
            social_facebook="https://facebook.com/thuha.makeup",
            social_instagram="https://instagram.com/thuha.makeup"
        ),
        ChuyenGia(
            name="Phương Linh",
            title="Hair Stylist Chuyên Nghiệp",
            bio="Chuyên gia làm tóc cưới với phong cách sáng tạo và độc đáo. Giải nhất cuộc thi Hair Stylist 2022.",
            years_experience=10,
            brides_count=350,
            specialties=json.dumps(["Bridal Hair", "Updo Styles", "Hair Extensions"]),
            image_url="/images/expert-3.jpg",
            social_facebook="https://facebook.com/phuonglinh.hair",
            social_instagram="https://instagram.com/phuonglinh.hair"
        ),
        ChuyenGia(
            name="Quỳnh Anh",
            title="Makeup Artist & Educator",
            bio="Chuyên gia trang điểm với phong cách hiện đại và táo bạo. Giảng viên tại nhiều trường đào tạo makeup hàng đầu.",
            years_experience=8,
            brides_count=300,
            specialties=json.dumps(["Artistic Makeup", "Glam Look", "Editorial"]),
            image_url="/images/expert-4.jpg",
            social_facebook="https://facebook.com/quynhanh.makeup",
            social_instagram="https://instagram.com/quynhanh.makeup"
        ),
    ]
    
    # Seed Services
    services = [
        DichVu(
            name="Trang Điểm Cô Dâu",
            description="Tạo phong cách trang điểm hoàn hảo cho cô dâu trong ngày cưới",
            features=json.dumps(["Tư vấn phong cách", "Makeup HD cao cấp", "Làm tóc cô dâu", "Thử makeup trước"]),
            price_from=5000000,
            is_featured=False,
            icon="💄"
        ),
        DichVu(
            name="Gói Cưới Trọn Gói",
            description="Dịch vụ trang điểm toàn diện cho cả đám cưới",
            features=json.dumps([
                "Makeup cô dâu + chú rể",
                "Makeup 4 phù dâu/phù rể",
                "Thử makeup 2 lần",
                "Hỗ trợ tại gia/venue",
                "Touch-up trong ngày"
            ]),
            price_from=15000000,
            is_featured=True,
            icon="👰"
        ),
        DichVu(
            name="Dịch Vụ Làm Đẹp",
            description="Chăm sóc toàn diện cho vẻ đẹp hoàn hảo",
            features=json.dumps(["Chăm sóc da mặt", "Làm móng tay chân", "Nối mi", "Spa thư giãn"]),
            price_from=2000000,
            is_featured=False,
            icon="💅"
        ),
    ]
    
    # Add to database
    db.add_all(products)
    db.add_all(experts)
    db.add_all(services)
    db.commit()
    
    print("✅ Database seeded successfully!")
    print(f"   - {len(products)} products added")
    print(f"   - {len(experts)} experts added")
    print(f"   - {len(services)} services added")
    
    db.close()

if __name__ == "__main__":
    seed_data()
