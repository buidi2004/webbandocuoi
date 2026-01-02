import { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { thuVienAPI, sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import HieuUngHat from '../thanh_phan/HieuUngHat';
import ScrollLinkedGallery from '../thanh_phan/ScrollLinkedGallery';
import CardCarousel from '../thanh_phan/CardCarousel';
import MasonryGrid from '../thanh_phan/MasonryGrid';
import GalleryLightbox from '../thanh_phan/GalleryLightbox';
import PetalBackground from '../thanh_phan/PetalBackground';
import GalleryFloatingCTA from '../thanh_phan/GalleryFloatingCTA';

const ThuVien = () => {
    const [danhSachAnh, setDanhSachAnh] = useState([]);
    const [danhSachSanPham, setDanhSachSanPham] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    
    // Lightbox state
    const [lightboxOpen, setLightboxOpen] = useState(false);
    const [lightboxIndex, setLightboxIndex] = useState(0);

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

    // Prepare gallery images for MasonryGrid
    const galleryImages = danhSachAnh.map((item, index) => ({
        id: item.id || index,
        url: layUrlHinhAnh(item.image_url),
        title: item.title || 'IVIE Studio - Khoảnh khắc hạnh phúc'
    }));

    // Lightbox handlers
    const handleImageClick = useCallback((index) => {
        setLightboxIndex(index);
        setLightboxOpen(true);
    }, []);

    const handleLightboxClose = useCallback(() => {
        setLightboxOpen(false);
    }, []);

    const handleLightboxNavigate = useCallback((direction) => {
        setLightboxIndex(prev => {
            const total = galleryImages.length;
            if (direction === 'prev') {
                return prev === 0 ? total - 1 : prev - 1;
            } else {
                return prev === total - 1 ? 0 : prev + 1;
            }
        });
    }, [galleryImages.length]);

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

    // Chuẩn bị dữ liệu cho scroll-linked animation
    const scrollSections = defaultSectionData.map((section, index) => ({
        id: index + 1,
        title: section.title,
        description: section.description,
        highlight: section.highlight,
        image: danhSachAnh[index] 
            ? layUrlHinhAnh(danhSachAnh[index].image_url)
            : `https://picsum.photos/id/${1015 + index}/800/600`
    }));

    // Chuẩn bị dữ liệu cho CardCarousel
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
        <div className="min-h-screen bg-white">
            {/* Khung hiệu ứng hạt ở đầu trang */}
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
                    
                    {/* Content overlay */}
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
                            color: '#333333',
                            fontSize: 'clamp(1.5rem, 6vw, 3.2rem)',
                            fontWeight: 700,
                            lineHeight: 1.2,
                            marginBottom: '12px',
                            fontFamily: "'Playfair Display', Georgia, serif"
                        }}>
                            Thư Viện Ảnh IVIE
                        </h1>
                        <p style={{
                            color: '#666',
                            fontSize: 'clamp(0.9rem, 3vw, 1.1rem)',
                            maxWidth: '90%',
                            marginBottom: '20px',
                            fontFamily: "'Montserrat', sans-serif"
                        }}>
                            Khoảnh khắc hạnh phúc của các cặp đôi
                        </p>
                        <div style={{ display: 'flex', gap: '10px', pointerEvents: 'auto', flexWrap: 'wrap', justifyContent: 'center' }}>
                            <a href="/lien-he" style={{
                                padding: '12px 20px',
                                background: '#D4AF37',
                                color: '#fff',
                                fontSize: '0.85rem',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none',
                                fontFamily: "'Montserrat', sans-serif"
                            }}>
                                Đặt Lịch Chụp
                            </a>
                            <a href="/san-pham" style={{
                                padding: '12px 20px',
                                background: 'transparent',
                                color: '#333333',
                                fontSize: '0.85rem',
                                fontWeight: 600,
                                borderRadius: '8px',
                                border: 'none',
                                cursor: 'pointer',
                                textDecoration: 'none',
                                fontFamily: "'Montserrat', sans-serif"
                            }}>
                                Xem Sản Phẩm →
                            </a>
                        </div>
                    </div>
                </div>
            </section>

            {/* Scroll-linked Animation Section */}
            <ScrollLinkedGallery sections={scrollSections} />

            {/* Card Carousel Section */}
            <CardCarousel items={carouselItems} />

            {/* Gallery Section với Petal Background */}
            <section className="py-12 sm:py-16" style={{ 
                marginTop: '40px',
                position: 'relative',
                overflow: 'hidden',
                background: '#FFFFFF'
            }}>
                {/* Petal Animation Background */}
                <PetalBackground petalCount={20} />

                <div className="container mx-auto px-4 sm:px-6" style={{ position: 'relative', zIndex: 1 }}>
                    {/* Section Header */}
                    <div className="text-center mb-12">
                        <motion.h2
                            className="mb-4"
                            style={{
                                fontFamily: "'Playfair Display', Georgia, serif",
                                fontSize: 'clamp(1.75rem, 5vw, 3rem)',
                                fontWeight: 700,
                                color: '#333333'
                            }}
                            variants={hieuUngTieuDe}
                            initial="anDi"
                            whileInView="hienThi"
                            viewport={{ once: true }}
                        >
                            {tieuDe.split('').map((kyTu, viTri) => (
                                <motion.span key={viTri} variants={hieuUngChuCai}>
                                    {kyTu === ' ' ? '\u00A0' : kyTu}
                                </motion.span>
                            ))}
                        </motion.h2>

                        <motion.p
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.8, delay: 0.5 }}
                            style={{
                                fontFamily: "'Montserrat', sans-serif",
                                fontSize: 'clamp(0.9rem, 2.5vw, 1.1rem)',
                                color: '#666',
                                maxWidth: '600px',
                                margin: '0 auto'
                            }}
                        >
                            Khoảnh khắc hạnh phúc của các cặp đôi - Nơi lưu giữ những kỷ niệm đẹp nhất
                        </motion.p>

                        {/* Tags */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.8, delay: 0.7 }}
                            className="mt-6 flex items-center justify-center gap-3 flex-wrap"
                        >
                            {[
                                { icon: '📸', text: `${danhSachAnh.length} ảnh` },
                                { icon: '✨', text: 'Masonry Grid' },
                                { icon: '💝', text: 'Khoảnh khắc đẹp' },
                            ].map((tag, index) => (
                                <span
                                    key={index}
                                    style={{
                                        padding: '8px 16px',
                                        background: 'white',
                                        borderRadius: '50px',
                                        boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
                                        fontSize: '0.85rem',
                                        fontFamily: "'Montserrat', sans-serif",
                                        color: '#333'
                                    }}
                                >
                                    {tag.icon} {tag.text}
                                </span>
                            ))}
                        </motion.div>

                        {/* Decorative line */}
                        <motion.div
                            initial={{ scaleX: 0 }}
                            whileInView={{ scaleX: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 1, delay: 1 }}
                            style={{
                                width: '80px',
                                height: '3px',
                                background: 'linear-gradient(90deg, transparent, #D4AF37, transparent)',
                                margin: '24px auto 0'
                            }}
                        />
                    </div>

                    {/* Gallery Content */}
                    {dangTai ? (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="flex flex-col items-center justify-center py-20"
                        >
                            <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                                style={{
                                    width: '48px',
                                    height: '48px',
                                    border: '4px solid #D4AF37',
                                    borderTopColor: 'transparent',
                                    borderRadius: '50%',
                                    marginBottom: '16px'
                                }}
                            />
                            <p style={{ color: '#666', fontFamily: "'Montserrat', sans-serif" }}>
                                Đang tải bộ sưu tập ảnh...
                            </p>
                        </motion.div>
                    ) : galleryImages.length > 0 ? (
                        <motion.div
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.8 }}
                        >
                            <MasonryGrid 
                                images={galleryImages} 
                                gap={20}
                                onImageClick={handleImageClick}
                            />
                        </motion.div>
                    ) : (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center py-20"
                            style={{
                                background: '#f9f9f9',
                                borderRadius: '16px'
                            }}
                        >
                            <div style={{ fontSize: '4rem', marginBottom: '16px', opacity: 0.5 }}>📷</div>
                            <p style={{ color: '#666', fontSize: '1.1rem', fontFamily: "'Montserrat', sans-serif" }}>
                                Chưa có ảnh trong thư viện
                            </p>
                            <p style={{ color: '#999', fontSize: '0.9rem', marginTop: '8px', fontFamily: "'Montserrat', sans-serif" }}>
                                Hãy quay lại sau để xem những khoảnh khắc đẹp
                            </p>
                        </motion.div>
                    )}

                    {/* Footer info */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8, delay: 0.5 }}
                        className="text-center mt-12 pt-8"
                        style={{ borderTop: '1px solid #eee' }}
                    >
                        <p style={{ color: '#666', fontFamily: "'Montserrat', sans-serif", marginBottom: '8px' }}>
                            💡 <strong>Mẹo:</strong> Di chuột vào ảnh để xem hiệu ứng, click để phóng to
                        </p>
                        <p style={{ color: '#999', fontSize: '0.85rem', fontFamily: "'Montserrat', sans-serif" }}>
                            © 2024 IVIE STUDIO - Lưu giữ khoảnh khắc hạnh phúc
                        </p>
                    </motion.div>
                </div>
            </section>

            {/* Lightbox */}
            <GalleryLightbox
                images={galleryImages}
                currentIndex={lightboxIndex}
                isOpen={lightboxOpen}
                onClose={handleLightboxClose}
                onNavigate={handleLightboxNavigate}
            />

            {/* Floating CTA */}
            <GalleryFloatingCTA />
        </div>
    );
};

export default ThuVien;
