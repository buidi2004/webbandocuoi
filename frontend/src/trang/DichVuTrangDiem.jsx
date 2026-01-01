import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { dichVuAPI, layUrlHinhAnh } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import { useToast } from '../thanh_phan/Toast';
import '../styles/makeup.css';

const DichVuTrangDiem = () => {
    const [dichVu, setDichVu] = useState([]);
    const [chuyenGia, setChuyenGia] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const [activeBeforeAfter, setActiveBeforeAfter] = useState(0);
    const { addToast } = useToast();
    const navigate = useNavigate();

    // Dữ liệu Before & After mẫu
    const beforeAfterData = [
        {
            id: 1,
            title: 'Cô dâu Ngọc Trinh',
            style: 'Phong cách Hàn Quốc',
            before: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400',
            after: 'https://images.unsplash.com/photo-1595959183082-7b570b7e08e2?w=400'
        },
        {
            id: 2,
            title: 'Cô dâu Thu Hà',
            style: 'Phong cách Châu Âu',
            before: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400',
            after: 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400'
        },
        {
            id: 3,
            title: 'Cô dâu Minh Anh',
            style: 'Phong cách Tự nhiên',
            before: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400',
            after: 'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400'
        }
    ];

    useEffect(() => {
        layDuLieu();
    }, []);

    const layDuLieu = async () => {
        try {
            const [dichVuRes, chuyenGiaRes] = await Promise.all([
                dichVuAPI.layTatCa(),
                dichVuAPI.layChuyenGia()
            ]);
            setDichVu(dichVuRes.data);
            setChuyenGia(chuyenGiaRes.data);
        } catch (loi) {
            console.error('Lỗi khi tải dữ liệu:', loi);
            addToast({ message: 'Không thể tải dữ liệu chuyên gia', type: 'error' });
        } finally {
            setDangTai(false);
        }
    };

    const dinhDangGia = (gia) => {
        return new Intl.NumberFormat('vi-VN').format(gia) + 'đ';
    };

    const addToCart = (expert) => {
        const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        const existingItemIndex = currentCart.findIndex(item => item.id === expert.id && item.type === 'expert');

        const itemToAdd = {
            id: expert.id,
            name: `Chuyên gia: ${expert.name}`,
            image_url: expert.image_url,
            rental_price_day: expert.price || 1000000,
            code: `EXP-${expert.id}`,
            type: 'expert'
        };

        if (existingItemIndex > -1) {
            currentCart[existingItemIndex].quantity = (currentCart[existingItemIndex].quantity || 1) + 1;
        } else {
            currentCart.push({ ...itemToAdd, quantity: 1 });
        }

        localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
        addToast({ message: `Đã chọn chuyên gia ${expert.name}`, type: 'success' });
    };

    const bookNow = (expert) => {
        addToCart(expert);
        navigate('/gio-hang');
    };

    if (dangTai) {
        return <div className="loading" style={{ textAlign: 'center', padding: '50px' }}>Đang tải đội ngũ chuyên gia...</div>;
    }

    // Filter experts
    const makeupArtists = chuyenGia.filter(cg => !cg.category || cg.category === 'makeup');
    const photographers = chuyenGia.filter(cg => cg.category === 'photo');
    const topArtists = chuyenGia.filter(cg => cg.is_top);

    const renderExpertCard = (cg) => (
        <div key={cg.id} className="expert-card-wrapper" style={{ transition: 'transform 0.3s' }}>
            <div className="expert-card" style={{ height: '100%', margin: 0, position: 'relative' }}>
                {cg.is_top && <div className="expert-badge top">TOP ARTIST</div>}
                {cg.level === 'master' && <div className="expert-badge master">MASTER</div>}

                <div className="expert-image">
                    <img src={layUrlHinhAnh(cg.image_url)} alt={cg.name}
                        onError={(e) => e.target.src = 'https://placehold.co/400x500/333/fff?text=Expert'} />
                </div>
                <div className="expert-info">
                    <div className="expert-header-row">
                        <h3 className="expert-name">{cg.name}</h3>
                        <span className="expert-location">📍 {cg.location || 'Hà Nội'}</span>
                    </div>
                    <p className="expert-title">{cg.title}</p>

                    <div className="expert-stats">
                        <div className="stat">
                            <span className="stat-number">{cg.years_experience}+</span>
                            <span className="stat-label">Năm KN</span>
                        </div>
                        <div className="stat">
                            <span className="stat-number">{cg.brides_count}+</span>
                            <span className="stat-label">Show</span>
                        </div>
                    </div>

                    <p className="expert-bio">{cg.bio}</p>

                    <div className="expert-price-row">
                        <span className="price-label">Booking:</span>
                        <span className="expert-price">{dinhDangGia(cg.price || 1000000)}</span>
                    </div>

                    <div className="expert-actions" style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                        <NutBam variant="outline" onClick={() => addToCart(cg)} style={{ flex: 1, fontSize: '0.9rem', padding: '8px' }}>+ GIỎ</NutBam>
                        <NutBam variant="primary" onClick={() => bookNow(cg)} style={{ flex: 1, fontSize: '0.9rem', padding: '8px' }}>ĐẶT LỊCH</NutBam>
                    </div>
                </div>
            </div>
        </div>
    );

    return (
        <div className="makeup-services-page">
            <section className="page-hero makeup-hero">
                <div className="page-hero-overlay"></div>
                <div className="page-hero-content">
                    <h1 className="page-title fade-in">Nghệ Thuật Cưới</h1>
                    <p className="page-subtitle fade-in">Đội Ngũ Chuyên Gia & Dịch Vụ Đẳng Cấp</p>
                </div>
            </section>

            {/* Top Artists Recommendation */}
            {topArtists.length > 0 && (
                <section className="expert-team section" style={{ background: '#0a0a0a' }}>
                    <div className="container">
                        <div className="section-header">
                            <h2 className="section-title gold-text">Gợi Ý Hàng Đầu</h2>
                            <p className="section-subtitle">Những gương mặt xuất sắc nhất tháng</p>
                        </div>
                        <div className="experts-grid">
                            {topArtists.map(renderExpertCard)}
                        </div>
                    </div>
                </section>
            )}

            {/* Makeup Artists Section */}
            <section className="expert-team section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Chuyên Gia Trang Điểm</h2>
                        <p className="section-subtitle">Phù thủy nhan sắc cho ngày trọng đại</p>
                    </div>
                    <div className="experts-grid">
                        {makeupArtists.map(renderExpertCard)}
                    </div>
                </div>
            </section>

            {/* Video Showcase Section - Redesigned */}
            <section className="video-showcase-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Nghệ Sĩ Tiêu Biểu</h2>
                        <p className="section-subtitle">Xem video giới thiệu từ các chuyên gia hàng đầu</p>
                    </div>
                    <div className="video-showcase-grid">
                        <div className="video-container-wrapper">
                            <div className="video-overlay-blur"></div>
                            <div className="video-frame">
                                <iframe
                                    src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=0&mute=1"
                                    title="Artist Introduction"
                                    frameBorder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                    allowFullScreen
                                ></iframe>
                            </div>
                            <div className="video-info-overlay">
                                <h3>Hồ Văn Phi</h3>
                                <p>Master Makeup Artist</p>
                            </div>
                        </div>
                        <div className="video-description">
                            <h3>Hồ Văn Phi - Master Artist</h3>
                            <p>Với hơn 10 năm kinh nghiệm trong ngành makeup cưới, Hồ Văn Phi đã tạo nên hàng ngàn diện mạo hoàn hảo cho các cô dâu.</p>
                            <ul className="artist-highlights">
                                <li>✨ Top 10 Makeup Artist Việt Nam 2024</li>
                                <li>💄 Chuyên gia trang điểm phong cách Hàn Quốc</li>
                                <li>🏆 Giải nhất cuộc thi Makeup Artist toàn quốc</li>
                                <li>📸 Hợp tác với 50+ nhiếp ảnh gia hàng đầu</li>
                            </ul>
                            <NutBam variant="primary" onClick={() => navigate('/lien-he')}>ĐẶT LỊCH NGAY</NutBam>
                        </div>
                    </div>
                </div>
            </section>

            {/* Before & After Section */}
            <section className="before-after-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Trước & Sau Trang Điểm</h2>
                        <p className="section-subtitle">Sự thay đổi kỳ diệu từ bàn tay nghệ sĩ</p>
                    </div>
                    <div className="before-after-showcase">
                        <div className="before-after-main">
                            <div className="ba-image-container">
                                <div className="ba-before">
                                    <img src={beforeAfterData[activeBeforeAfter].before} alt="Before" />
                                    <span className="ba-label">TRƯỚC</span>
                                </div>
                                <div className="ba-divider">
                                    <span>→</span>
                                </div>
                                <div className="ba-after">
                                    <img src={beforeAfterData[activeBeforeAfter].after} alt="After" />
                                    <span className="ba-label">SAU</span>
                                </div>
                            </div>
                            <div className="ba-info">
                                <h4>{beforeAfterData[activeBeforeAfter].title}</h4>
                                <p>{beforeAfterData[activeBeforeAfter].style}</p>
                            </div>
                        </div>
                        <div className="before-after-thumbnails">
                            {beforeAfterData.map((item, idx) => (
                                <div 
                                    key={item.id}
                                    className={`ba-thumb ${idx === activeBeforeAfter ? 'active' : ''}`}
                                    onClick={() => setActiveBeforeAfter(idx)}
                                >
                                    <img src={item.after} alt={item.title} />
                                    <span>{item.title}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* Photographers Section */}
            <section className="expert-team section" style={{ background: '#f9f9f9', color: '#333' }}>
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title" style={{ color: '#333' }}>Đội Ngũ Nhiếp Ảnh & Quay Phim</h2>
                        <p className="section-subtitle" style={{ color: '#666' }}>Ghi lại khoảnh khắc - Lưu giữ thanh xuân</p>
                    </div>
                    <div className="experts-grid">
                        {photographers.length > 0 ? photographers.map(renderExpertCard) : (
                            <p style={{ textAlign: 'center', width: '100%', color: '#666' }}>Đang cập nhật đội ngũ nhiếp ảnh...</p>
                        )}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default DichVuTrangDiem;
