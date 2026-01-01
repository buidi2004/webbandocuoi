import { useState, useEffect, useLayoutEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Link } from 'react-router-dom';
import { bannerAPI, noiDungAPI, thuVienAPI, layUrlHinhAnh } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import The from '../thanh_phan/The';
import HieuUngSong from '../thanh_phan/HieuUngSong';
import HieuUngHat from '../thanh_phan/HieuUngHat';
import WrapperAtropos from '../thanh_phan/WrapperAtropos';
import InstagramFeed from '../thanh_phan/InstagramFeed';
import LichTrong from '../thanh_phan/LichTrong';
import LazyImage from '../thanh_phan/LazyImage';
import '../styles/Home.css';

const TrangChu = () => {
    const [banners, setBanners] = useState([]);
    const [idxBanner, setIdxBanner] = useState(0);
    const [gioiThieu, setGioiThieu] = useState(null);
    const [diemNhan, setDiemNhan] = useState([]);
    const [thuVien, setThuVien] = useState([]);

    const containerRef = useRef(null);
    gsap.registerPlugin(ScrollTrigger);

    useEffect(() => {
        const layDuLieu = async () => {
            try {
                const [resBanner, resGT, resDN, resTV] = await Promise.all([
                    bannerAPI.layTatCa(),
                    noiDungAPI.layGioiThieu(),
                    noiDungAPI.layDiemNhan(),
                    thuVienAPI.layTatCa()
                ]);

                setBanners(resBanner.data || []);
                setGioiThieu(resGT.data);
                setDiemNhan(resDN.data || []);
                setThuVien(resTV.data || []);
            } catch (err) {
                console.error("Lỗi lấy dữ liệu:", err);
            }
        };
        layDuLieu();
    }, []);

    useLayoutEffect(() => {
        let ctx = gsap.context(() => {
            // Animate fade-in sections
            gsap.utils.toArray('.fade-in-section').forEach(section => {
                gsap.fromTo(section,
                    { opacity: 0, y: 50 },
                    {
                        opacity: 1,
                        y: 0,
                        duration: 1,
                        ease: "power3.out",
                        scrollTrigger: {
                            trigger: section,
                            start: "top 85%",
                            toggleActions: "play none none reverse"
                        }
                    }
                );
            });
        }, containerRef);
        return () => ctx.revert();
    }, [gioiThieu, diemNhan, thuVien]); // Re-run when data loads

    // Hiệu ứng chuyển Banner tự động
    useEffect(() => {
        if (banners.length <= 1) return;
        const timer = setInterval(() => {
            setIdxBanner(prev => (prev + 1) % banners.length);
        }, 6000);
        return () => clearInterval(timer);
    }, [banners]);

    const bannerHienTai = banners[idxBanner];

    return (
        <div className="home-page" ref={containerRef}>
            {/* Hero Section với Hiệu ứng động */}
            <section className="hero" id="home">
                {banners.length > 0 ? (
                    banners.map((b, i) => (
                        <div
                            key={b.id}
                            className={`hero-slide ${i === idxBanner ? 'active' : ''}`}
                            style={{
                                backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url(${layUrlHinhAnh(b.image_url)})`
                            }}
                        ></div>
                    ))
                ) : (
                    <div className="hero-slide active default-banner"></div>
                )}

                <div className="hero-content" key={idxBanner}>
                    <span className="hero-subtitle">IVIE STUDIO</span>
                    <h1 className="hero-title">
                        {bannerHienTai?.title ? (
                            <span dangerouslySetInnerHTML={{ __html: bannerHienTai.title.replace('\n', '<br/>') }} />
                        ) : (
                            <>
                                Nơi Tình Yêu<br />
                                <span className="highlight">Thăng Hoa</span>
                            </>
                        )}
                    </h1>
                    <p className="hero-description">
                        {bannerHienTai?.subtitle || "Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với phong cách nghệ thuật độc đáo và dịch vụ chuyên nghiệp hàng đầu."}
                    </p>
                    <div className="hero-buttons">
                        <Link to="/lien-he">
                            <NutBam variant="primary" style={{ minWidth: '180px' }}>ĐẶT LỊCH NGAY</NutBam>
                        </Link>
                        <Link to="/san-pham">
                            <NutBam variant="outline" className="btn-white" style={{ minWidth: '180px' }}>
                                XEM BỘ SƯU TẬP
                            </NutBam>
                        </Link>
                    </div>
                </div>

                {banners.length > 1 && (
                    <div className="banner-dots">
                        {banners.map((_, i) => (
                            <span key={i} className={`dot ${i === idxBanner ? 'active' : ''}`} onClick={() => setIdxBanner(i)}></span>
                        ))}
                    </div>
                )}

                <div className="scroll-indicator">
                    <span>Khám phá</span>
                    <div className="line"></div>
                </div>

                {/* Hiệu ứng sóng */}
                <HieuUngSong />
            </section>

            {/* Khung hiệu ứng hạt - responsive */}
            <section className="particle-section" style={{ 
                padding: '40px 20px',
                background: '#fff'
            }}>
                <div className="particle-container" style={{
                    position: 'relative',
                    width: '100%',
                    maxWidth: '1600px',
                    height: 'clamp(400px, 60vw, 800px)',
                    margin: '0 auto',
                    background: '#000',
                    borderRadius: '24px',
                    overflow: 'hidden'
                }}>
                    {/* Giảm số hạt - component sẽ tự giảm thêm trên mobile */}
                    <HieuUngHat particleCount={120} nenTrang={false} />
                    
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
                        justifyContent: 'center',
                        padding: 'clamp(20px, 5vw, 50px)',
                        pointerEvents: 'none'
                    }}>
                        <h2 style={{
                            color: '#fff',
                            fontSize: 'clamp(24px, 5vw, 36px)',
                            fontWeight: 400,
                            lineHeight: 1.3,
                            marginBottom: '20px',
                            fontFamily: 'Playfair Display, serif',
                            textShadow: '0 2px 4px rgba(0,0,0,0.5)'
                        }}>
                            Khám Phá<br/>
                            Vẻ Đẹp<br/>
                            Tinh Tế
                        </h2>
                        
                        <div style={{ display: 'flex', gap: '12px', pointerEvents: 'auto' }}>
                            <Link to="/san-pham" style={{
                                padding: '10px 20px',
                                background: 'transparent',
                                color: '#c9a86c',
                                fontSize: 'clamp(12px, 2vw, 14px)',
                                fontWeight: 500,
                                borderRadius: '50px',
                                border: '2px solid #c9a86c',
                                cursor: 'pointer',
                                textDecoration: 'none'
                            }}>
                                Xem Bộ Sưu Tập
                            </Link>
                        </div>
                    </div>
                </div>
                
                {/* CSS responsive cho particle section */}
                <style>{`
                    @media (max-width: 768px) {
                        .particle-section {
                            padding: 20px 15px !important;
                        }
                        .particle-container {
                            border-radius: 16px !important;
                        }
                    }
                `}</style>
            </section>
            <section className="section about-section">
                <div className="container">
                    <div className="about-grid">
                        <WrapperAtropos className="about-image fade-in-section">
                            <div data-atropos-offset="0">
                                <img src={layUrlHinhAnh(gioiThieu?.image_url) || '/images/about-wedding.jpg'} alt="Về chúng tôi" onError={(e) => e.target.src = 'https://placehold.co/600x800/d4a373/fff?text=IVIE+Studio'} data-atropos-offset="5" />
                            </div>
                        </WrapperAtropos>
                        <div className="about-content fade-in-section">
                            <h2 className="section-title" style={{ textAlign: 'left' }}>{gioiThieu?.title || "Câu Chuyện Của IVIE"}</h2>
                            <p className="section-subtitle" style={{ margin: '0 0 2rem 0', textAlign: 'left' }}>
                                {gioiThieu?.subtitle || "Hơn 10 năm kinh nghiệm trong lĩnh vực cưới hỏi"}
                            </p>
                            <p className="text-content">
                                {gioiThieu?.description || "Tại IVIE Studio, chúng tôi tin rằng mỗi cặp đôi đều có một câu chuyện tình yêu độc đáo xứng đáng được kể lại bằng ngôn ngữ hình ảnh tinh tế nhất."}
                            </p>
                            <div className="stats-grid">
                                <div className="stat-item">
                                    <span className="stat-number">{gioiThieu?.stat1_number || "500+"}</span>
                                    <span className="stat-label">{gioiThieu?.stat1_label || "Cặp Đôi"}</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-number">{gioiThieu?.stat2_number || "10+"}</span>
                                    <span className="stat-label">{gioiThieu?.stat2_label || "Năm Kinh Nghiệm"}</span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-number">{gioiThieu?.stat3_number || "100%"}</span>
                                    <span className="stat-label">{gioiThieu?.stat3_label || "Hài Lòng"}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Services Highlights Section (Dynamic) */}
            <section className="services section" id="services" style={{ backgroundColor: 'var(--secondary)' }}>
                <div className="container">
                    <div className="section-header fade-in-section">
                        <h2 className="section-title">Dịch Vụ Cao Cấp</h2>
                        <p className="section-subtitle">Trải nghiệm dịch vụ cưới trọn gói chuẩn quốc tế</p>
                    </div>

                    <div className="services-grid">
                        {diemNhan.length > 0 ? diemNhan.map(dn => (
                            <WrapperAtropos key={dn.id} className="fade-in-section">
                                <The className="service-card" style={{ height: '100%' }}>
                                    <div className="service-image" data-atropos-offset="0">
                                        <img src={layUrlHinhAnh(dn.image_url)} alt={dn.title} onError={(e) => e.target.src = 'https://placehold.co/400x300/e5e5e5/333?text=Highlight'} data-atropos-offset="5" />
                                    </div>
                                    <div className="service-info" data-atropos-offset="2">
                                        <h3 className="service-title">{dn.title}</h3>
                                        <p>{dn.description}</p>
                                    </div>
                                </The>
                            </WrapperAtropos>
                        )) : (
                            <>
                                {/* Fallback/Default if no highlights in DB */}
                                <WrapperAtropos className="fade-in-section">
                                    <The className="service-card" style={{ height: '100%' }}>
                                        <div className="service-image">
                                            <img src="/images/service-photo.jpg" alt="Chụp ảnh cưới" data-atropos-offset="5" />
                                        </div>
                                        <div className="service-info" data-atropos-offset="3">
                                            <h3 className="service-title">Nhiếp Ảnh Nghệ Thuật</h3>
                                            <p>Ghi lại từng khoảnh khắc cảm xúc với phong cách blend màu độc quyền và góc máy sáng tạo.</p>
                                        </div>
                                    </The>
                                </WrapperAtropos>

                                <WrapperAtropos className="fade-in-section">
                                    <The className="service-card" style={{ height: '100%' }}>
                                        <div className="service-image">
                                            <img src="/images/service-makeup.jpg" alt="Trang điểm" data-atropos-offset="5" />
                                        </div>
                                        <div className="service-info" data-atropos-offset="3">
                                            <h3 className="service-title">Trang Điểm Cô Dâu</h3>
                                            <p>Phong cách trang điểm tự nhiên, trong trẻo hoặc sắc sảo, tôn lên vẻ đẹp riêng của bạn.</p>
                                        </div>
                                    </The>
                                </WrapperAtropos>

                                <WrapperAtropos className="fade-in-section">
                                    <The className="service-card" style={{ height: '100%' }}>
                                        <div className="service-image">
                                            <img src="/images/service-dress.jpg" alt="Váy cưới" data-atropos-offset="5" />
                                        </div>
                                        <div className="service-info" data-atropos-offset="3">
                                            <h3 className="service-title">Váy Cưới Thiết Kế</h3>
                                            <p>Bộ sưu tập hơn 200 mẫu váy cưới cao cấp, từ dòng Luxury đến Minimalist thanh lịch.</p>
                                        </div>
                                    </The>
                                </WrapperAtropos>
                            </>
                        )}
                    </div>
                </div>
            </section>

            {/* Featured Products (Mini Gallery) */}
            <section className="section">
                <div className="container">
                    <div className="section-header fade-in-section">
                        <h2 className="section-title">Bộ Sưu Tập Mới</h2>
                        <p className="section-subtitle">Những thiết kế váy cưới được yêu thích nhất mùa này</p>
                    </div>
                    <div className="featured-grid fade-in-section">
                        {thuVien.length > 0 ? (
                            thuVien.slice(0, 3).map((item, idx) => (
                                <WrapperAtropos key={item.id} className={`featured-item ${idx === 0 ? 'large' : ''}`}>
                                    <div style={{ width: '100%', height: '100%' }} data-atropos-offset="0">
                                        <LazyImage
                                            src={layUrlHinhAnh(item.image_url)}
                                            alt={`${(item.title || 'bo-suu-tap').toLowerCase().replace(/\s+/g, '-')}-ivie-wedding-studio`}
                                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                        />
                                        <div className="collection-label">
                                            <h4>{item.title || `Bộ sưu tập ${idx + 1}`}</h4>
                                            <span>Xem chi tiết →</span>
                                        </div>
                                    </div>
                                </WrapperAtropos>
                            ))
                        ) : (
                            <>
                                <>
                                    <WrapperAtropos className="featured-item large">
                                        <div style={{ width: '100%', height: '100%' }} data-atropos-offset="0">
                                            <img src="/images/feat-1.jpg" alt="Váy cưới 1" loading="lazy" onError={(e) => e.target.src = 'https://placehold.co/600x800/e5e5e5/333?text=Collection+1'} data-atropos-offset="5" />
                                            <div className="collection-label">
                                                <h4>Váy Cưới Luxury</h4>
                                                <span>Xem chi tiết →</span>
                                            </div>
                                        </div>
                                    </WrapperAtropos>
                                    <WrapperAtropos className="featured-item">
                                        <div style={{ width: '100%', height: '100%' }} data-atropos-offset="0">
                                            <img src="/images/feat-2.jpg" alt="Váy cưới 2" loading="lazy" onError={(e) => e.target.src = 'https://placehold.co/400x400/e5e5e5/333?text=Collection+2'} data-atropos-offset="5" />
                                            <div className="collection-label">
                                                <h4>Minimalist</h4>
                                                <span>Xem chi tiết →</span>
                                            </div>
                                        </div>
                                    </WrapperAtropos>
                                    <WrapperAtropos className="featured-item">
                                        <div style={{ width: '100%', height: '100%' }} data-atropos-offset="0">
                                            <img src="/images/feat-3.jpg" alt="Váy cưới 3" loading="lazy" onError={(e) => e.target.src = 'https://placehold.co/400x400/e5e5e5/333?text=Collection+3'} data-atropos-offset="5" />
                                            <div className="collection-label">
                                                <h4>Vintage</h4>
                                                <span>Xem chi tiết →</span>
                                            </div>
                                        </div>
                                    </WrapperAtropos>
                                </>
                            </>
                        )}
                    </div>
                    <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                        <Link to="/san-pham">
                            <NutBam variant="outline">XEM TẤT CẢ SẢN PHẨM</NutBam>
                        </Link>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section" style={{ backgroundImage: 'url(/images/cta-bg.jpg)', backgroundSize: 'cover', backgroundBlendMode: 'overlay', backgroundColor: 'rgba(0,0,0,0.6)' }}>
                <div className="container">
                    <div className="cta-content fade-in-section">
                        <h2>Bạn Đã Sẵn Sàng Cho Ngày Trọng Đại?</h2>
                        <p>Liên hệ ngay với IVIE để nhận tư vấn chi tiết và ưu đãi đặc biệt cho mùa cưới này.</p>
                        <div className="cta-buttons">
                            <Link to="/lien-he">
                                <NutBam variant="primary" style={{ backgroundColor: 'var(--primary)', borderColor: 'var(--primary)' }}>NHẬN TƯ VẤN</NutBam>
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Social Proof - Đánh giá khách hàng */}
            <section className="section testimonials-section" style={{ background: '#faf8f5' }}>
                <div className="container">
                    <div className="section-header fade-in-section">
                        <h2 className="section-title">Khách Hàng Nói Gì Về IVIE</h2>
                        <p className="section-subtitle">Hơn 500+ cặp đôi đã tin tưởng lựa chọn chúng tôi</p>
                    </div>
                    
                    <div className="testimonials-grid fade-in-section">
                        <div className="testimonial-card">
                            <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
                            <p className="testimonial-text">"Mình rất hài lòng với dịch vụ của IVIE. Váy cưới đẹp, makeup tự nhiên, và đặc biệt là ekip rất nhiệt tình. Cảm ơn IVIE đã giúp ngày cưới của mình thật hoàn hảo!"</p>
                            <div className="testimonial-author">
                                <div className="author-avatar">👰</div>
                                <div className="author-info">
                                    <h4>Ngọc Trinh & Minh Khang</h4>
                                    <span>Cưới tháng 12/2025</span>
                                </div>
                            </div>
                        </div>
                        
                        <div className="testimonial-card">
                            <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
                            <p className="testimonial-text">"Chất lượng váy cưới tuyệt vời, nhiều mẫu đẹp để lựa chọn. Giá cả hợp lý so với chất lượng. Nhân viên tư vấn rất tận tâm và chuyên nghiệp."</p>
                            <div className="testimonial-author">
                                <div className="author-avatar">💑</div>
                                <div className="author-info">
                                    <h4>Thu Hà & Văn Đức</h4>
                                    <span>Cưới tháng 11/2025</span>
                                </div>
                            </div>
                        </div>
                        
                        <div className="testimonial-card">
                            <div className="testimonial-rating">⭐⭐⭐⭐⭐</div>
                            <p className="testimonial-text">"Album cưới của mình được chụp rất đẹp, góc máy sáng tạo và blend màu rất nghệ thuật. Mình đã giới thiệu IVIE cho nhiều bạn bè rồi!"</p>
                            <div className="testimonial-author">
                                <div className="author-avatar">📸</div>
                                <div className="author-info">
                                    <h4>Thanh Tâm & Hoàng Long</h4>
                                    <span>Cưới tháng 10/2025</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Stats bar */}
                    <div className="social-proof-stats fade-in-section">
                        <div className="proof-stat">
                            <span className="proof-number">500+</span>
                            <span className="proof-label">Cặp đôi hạnh phúc</span>
                        </div>
                        <div className="proof-stat">
                            <span className="proof-number">4.9/5</span>
                            <span className="proof-label">Đánh giá trung bình</span>
                        </div>
                        <div className="proof-stat">
                            <span className="proof-number">98%</span>
                            <span className="proof-label">Khách hàng giới thiệu</span>
                        </div>
                        <div className="proof-stat">
                            <span className="proof-number">10+</span>
                            <span className="proof-label">Năm kinh nghiệm</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* Availability Calendar - Lịch trống */}
            <LichTrong />

            {/* Instagram Feed */}
            <InstagramFeed />
        </div>
    );
};

export default TrangChu;
