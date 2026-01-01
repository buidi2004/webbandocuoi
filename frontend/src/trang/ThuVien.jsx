import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { thuVienAPI, sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import BoSuuTapGach from '../thanh_phan/BoSuuTapGach';
import HieuUngHat from '../thanh_phan/HieuUngHat';
import ScrollLinkedGallery from '../thanh_phan/ScrollLinkedGallery';
import CardCarousel from '../thanh_phan/CardCarousel';

const ThuVien = () => {
    const [danhSachAnh, setDanhSachAnh] = useState([]);
    const [danhSachSanPham, setDanhSachSanPham] = useState([]);
    const [dangTai, setDangTai] = useState(true);

    useEffect(() => {
        layDuLieuThuVien();
        layDuLieuSanPham();
    }, []);

    const layDuLieuThuVien = async () => {
        try {
            const phanHoi = await thuVienAPI.layTatCa();
            setDanhSachAnh(phanHoi.data);
        } catch (loi) {
            console.error('Lỗi tải thư viện:', loi);
        } finally {
            setDangTai(false);
        }
    };

    const layDuLieuSanPham = async () => {
        try {
            const phanHoi = await sanPhamAPI.layTatCa();
            setDanhSachSanPham(phanHoi.data || []);
        } catch (loi) {
            console.error('Lỗi tải sản phẩm:', loi);
        }
    };

    const danhSachAnhGallery = danhSachAnh.map(item => ({
        url: layUrlHinhAnh(item.image_url),
        moTa: item.title || 'IVIE Studio - Khoảnh khắc hạnh phúc'
    }));

    // Hiệu ứng chữ
    const hieuUngTieuDe = {
        anDi: { opacity: 0 },
        hienThi: {
            opacity: 1,
            transition: {
                staggerChildren: 0.08,
            },
        },
    };

    const hieuUngChuCai = {
        anDi: { opacity: 0, y: 50 },
        hienThi: {
            opacity: 1,
            y: 0,
            transition: {
                duration: 0.5,
                ease: [0.25, 0.46, 0.45, 0.94],
            },
        },
    };

    const tieuDe = "Thư Viện Ảnh IVIE STUDIO";

    // Dữ liệu mặc định cho scroll sections
    const defaultSectionData = [
        {
            title: "Chụp Ảnh Cưới Chuyên Nghiệp",
            description: "Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với đội ngũ nhiếp ảnh gia giàu kinh nghiệm.",
            highlight: "500+ cặp đôi tin tưởng"
        },
        {
            title: "Studio Hiện Đại",
            description: "Không gian chụp ảnh sang trọng với ánh sáng tự nhiên và thiết bị cao cấp.",
            highlight: "3 studio tại Hà Nội"
        },
        {
            title: "Trang Điểm Cô Dâu",
            description: "Makeup artist chuyên nghiệp giúp bạn tỏa sáng trong ngày trọng đại.",
            highlight: "Top Artist được yêu thích"
        },
        {
            title: "Album & In Ấn Cao Cấp",
            description: "Album cưới cao cấp với chất liệu nhập khẩu, bền đẹp theo thời gian.",
            highlight: "Bảo hành trọn đời"
        }
    ];

    // Chuẩn bị dữ liệu cho scroll-linked animation - dùng 4 ảnh đầu từ thư viện
    const scrollSections = defaultSectionData.map((section, index) => ({
        id: index + 1,
        title: section.title,
        description: section.description,
        highlight: section.highlight,
        // Dùng ảnh từ thư viện nếu có, fallback về picsum
        image: danhSachAnh[index] 
            ? layUrlHinhAnh(danhSachAnh[index].image_url)
            : `https://picsum.photos/id/${1015 + index}/800/600`
    }));

    // Chuẩn bị dữ liệu cho CardCarousel - dùng 3 sản phẩm đầu hoặc fallback
    const defaultCarouselData = [
        {
            id: 1,
            title: "Gói Chụp Ảnh Cưới Premium",
            description: "Trọn gói chụp ảnh cưới cao cấp với 200+ ảnh đã chỉnh sửa",
            image: "https://picsum.photos/id/1011/800/600",
            price: "15.000.000đ"
        },
        {
            id: 2,
            title: "Gói Chụp Ảnh Gia Đình",
            description: "Lưu giữ khoảnh khắc hạnh phúc bên gia đình thân yêu",
            image: "https://picsum.photos/id/1012/800/600",
            price: "5.000.000đ"
        },
        {
            id: 3,
            title: "Gói Chụp Ảnh Kỷ Yếu",
            description: "Kỷ niệm tuổi học trò với bộ ảnh kỷ yếu độc đáo",
            image: "https://picsum.photos/id/1013/800/600",
            price: "3.000.000đ"
        }
    ];

    const carouselItems = danhSachSanPham.length >= 3 
        ? danhSachSanPham.slice(0, 3).map((sp, index) => ({
            id: sp.id || index + 1,
            title: sp.ten || sp.name || `Gói ${index + 1}`,
            description: sp.mo_ta || sp.description || 'Dịch vụ chụp ảnh chuyên nghiệp',
            image: layUrlHinhAnh(sp.hinh_anh || sp.image_url),
            price: sp.gia ? `${Number(sp.gia).toLocaleString('vi-VN')}đ` : null
        }))
        : defaultCarouselData;

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
            {/* Khung hiệu ứng hạt ở đầu trang - responsive */}
            <section style={{ 
                padding: '100px 15px 30px',
                background: '#fff',
                position: 'relative',
                overflow: 'hidden'
            }}>
                <div style={{
                    position: 'relative',
                    width: '100%',
                    maxWidth: '100%',
                    height: 'min(500px, 70vh)',
                    margin: '0 auto',
                    background: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    <HieuUngHat particleCount={800} nenTrang={true} />
                    
                    {/* Content overlay căn giữa - responsive mobile */}
                    <div style={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        zIndex: 10,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '20px',
                        pointerEvents: 'none',
                        textAlign: 'center'
                    }}>
                        <h1 style={{
                            color: '#1a1a1a',
                            fontSize: 'clamp(1.5rem, 6vw, 3.2rem)',
                            fontWeight: 700,
                            lineHeight: 1.2,
                            marginBottom: '12px',
                            fontFamily: "'Be Vietnam Pro', system-ui, sans-serif"
                        }}>
                            Thư Viện Ảnh IVIE
                        </h1>
                        <p style={{
                            color: '#666',
                            fontSize: 'clamp(0.9rem, 3vw, 1.1rem)',
                            maxWidth: '90%',
                            marginBottom: '20px'
                        }}>
                            Khoảnh khắc hạnh phúc của các cặp đôi
                        </p>
                        <div style={{ display: 'flex', gap: '10px', pointerEvents: 'auto', flexWrap: 'wrap', justifyContent: 'center' }}>
                            <a href="/lien-he" style={{
                                padding: '12px 20px',
                                background: '#1a1a1a',
                                color: '#fff',
                                fontSize: '0.85rem',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none'
                            }}>
                                Đặt Lịch Chụp
                            </a>
                            <a href="/san-pham" style={{
                                padding: '12px 20px',
                                background: 'transparent',
                                color: '#1a1a1a',
                                fontSize: '0.85rem',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none'
                            }}>
                                Xem Sản Phẩm →
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* Scroll-linked Animation Section - 4 ảnh local */}
            <ScrollLinkedGallery sections={scrollSections} />

            {/* Card Carousel Section - 3 sản phẩm đầu */}
            <CardCarousel items={carouselItems} />

            {/* Phần Gallery - responsive */}
            <div className="py-8 sm:py-12" style={{ marginTop: '40px' }}>
                <div className="container mx-auto px-3 sm:px-4">
                {/* Phần đầu với hiệu ứng chữ */}
                <div className="text-center mb-12 relative">
                    {/* Ảnh nền cho hiệu ứng chữ */}
                    <div className="absolute inset-0 -z-10 opacity-5">
                        <div
                            className="w-full h-full bg-cover bg-center"
                            style={{
                                backgroundImage: 'url(https://images.unsplash.com/photo-1519741497674-611481863552?w=1200)',
                            }}
                        />
                    </div>

                    {/* Tiêu đề với hiệu ứng - responsive */}
                    <motion.h1
                        className="text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-gray-900 via-[#b59410] to-gray-900 px-4"
                        variants={hieuUngTieuDe}
                        initial="anDi"
                        animate="hienThi"
                        style={{ wordBreak: 'break-word' }}
                    >
                        {tieuDe.split('').map((kyTu, viTri) => (
                            <motion.span key={viTri} variants={hieuUngChuCai}>
                                {kyTu === ' ' ? '\u00A0' : kyTu}
                            </motion.span>
                        ))}
                    </motion.h1>

                    {/* Phụ đề với hiệu ứng fade-in - responsive */}
                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.5 }}
                        className="text-sm sm:text-base lg:text-lg text-gray-600 max-w-2xl mx-auto px-4"
                    >
                        Khoảnh khắc hạnh phúc của các cặp đôi - Nơi lưu giữ những kỷ niệm đẹp nhất
                    </motion.p>

                    {/* Các nhãn với hiệu ứng lần lượt - responsive */}
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.7 }}
                        className="mt-4 sm:mt-6 flex items-center justify-center gap-2 sm:gap-3 flex-wrap text-xs sm:text-sm text-gray-500 px-4"
                    >
                        {[
                            { bieuTuong: '📸', noiDung: `${danhSachAnh.length} ảnh` },
                            { bieuTuong: '✨', noiDung: 'Bố cục Gạch' },
                            { bieuTuong: '💝', noiDung: 'Khoảnh khắc đẹp' },
                        ].map((nhan, viTri) => (
                            <motion.span
                                key={viTri}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ duration: 0.5, delay: 0.9 + viTri * 0.1 }}
                                whileHover={{ scale: 1.05, y: -2 }}
                                className="px-3 py-1.5 sm:px-4 sm:py-2 bg-white rounded-full shadow-sm hover:shadow-md transition-all cursor-pointer text-xs sm:text-sm"
                            >
                                {nhan.bieuTuong} {nhan.noiDung}
                            </motion.span>
                        ))}
                    </motion.div>

                    {/* Đường trang trí */}
                    <motion.div
                        initial={{ scaleX: 0 }}
                        animate={{ scaleX: 1 }}
                        transition={{ duration: 1, delay: 1.2 }}
                        className="w-24 h-1 bg-gradient-to-r from-transparent via-[#b59410] to-transparent mx-auto mt-8"
                    />
                </div>

                {/* Nội dung Gallery */}
                {dangTai ? (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="flex flex-col items-center justify-center py-20"
                    >
                        <motion.div
                            animate={{ rotate: 360 }}
                            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                            className="w-12 h-12 border-4 border-[#b59410] border-t-transparent rounded-full mb-4"
                        />
                        <p className="text-gray-600">Đang tải bộ sưu tập ảnh...</p>
                    </motion.div>
                ) : danhSachAnh.length > 0 ? (
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        className="bg-white/50 backdrop-blur-sm rounded-2xl shadow-xl p-6"
                    >
                        <BoSuuTapGach danhSachAnh={danhSachAnhGallery} />
                    </motion.div>
                ) : (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="text-center py-20 bg-white rounded-2xl shadow-lg"
                    >
                        <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="text-6xl mb-4"
                        >
                            📷
                        </motion.div>
                        <p className="text-gray-500 text-lg">Chưa có ảnh trong thư viện</p>
                        <p className="text-gray-400 text-sm mt-2">
                            Hãy quay lại sau để xem những khoảnh khắc đẹp
                        </p>
                    </motion.div>
                )}

                {/* Thông tin cuối trang */}
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.8, delay: 1.5 }}
                    className="text-center mt-12 py-8 border-t border-gray-200"
                >
                    <p className="text-gray-600 mb-2">
                        💡 <strong>Mẹo:</strong> Di chuột vào ảnh để xem hiệu ứng, click để phóng to
                    </p>
                    <p className="text-gray-500 text-sm">
                        © 2024 IVIE STUDIO - Lưu giữ khoảnh khắc hạnh phúc
                    </p>
                </motion.div>
            </div>
        </div>
        </div>
    );
};

export default ThuVien;
