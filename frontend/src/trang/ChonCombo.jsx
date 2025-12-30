import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { sanPhamAPI, layUrlHinhAnh, comboAPI } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import { useToast } from '../thanh_phan/Toast';
import '../styles/combo.css';

const ChonCombo = () => {
    const navigate = useNavigate();
    const { addToast } = useToast();
    const [buoc, setBuoc] = useState(1);
    const [goiDaChon, setGoiDaChon] = useState(null);
    const [vayNu, setVayNu] = useState([]);
    const [vestNam, setVestNam] = useState([]);
    const [chonNu, setChonNu] = useState([]);
    const [chonNam, setChonNam] = useState([]);
    const [dangTai, setDangTai] = useState(false);
    const [danhSachCombo, setDanhSachCombo] = useState([]);

    useEffect(() => {
        taiDuLieu();
        taiCombo();
    }, []);

    const taiCombo = async () => {
        try {
            const res = await comboAPI.layTatCa();
            setDanhSachCombo(res.data || []);
        } catch (error) {
            console.error('Lỗi tải combo:', error);
            // Fallback to default combos if API fails
            setDanhSachCombo([
                {
                    id: 1,
                    ten: 'COMBO KHỞI ĐẦU',
                    gia: 2000000,
                    gioi_han: 2,
                    mo_ta: 'Gói cơ bản cho các cặp đôi',
                    quyen_loi: [
                        '2 Váy Cưới tùy chọn',
                        '2 Bộ Vest Nam tùy chọn',
                        'Miễn phí giặt ủi',
                        'Hỗ trợ chỉnh sửa kích cỡ'
                    ],
                    hinh_anh: 'https://images.unsplash.com/photo-1594552072238-b8a33785b261?auto=format&fit=crop&q=80&w=600'
                },
                {
                    id: 2,
                    ten: 'COMBO TIẾT KIỆM',
                    gia: 5000000,
                    gioi_han: 5,
                    mo_ta: 'Sự lựa chọn phổ biến nhất',
                    quyen_loi: [
                        '5 Váy Cưới tùy chọn',
                        '5 Bộ Vest Nam tùy chọn',
                        'Phụ kiện đi kèm miễn phí',
                        'Giữ đồ trong 3 ngày'
                    ],
                    hinh_anh: 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&q=80&w=600',
                    noi_bat: true
                },
                {
                    id: 3,
                    ten: 'COMBO VIP TOÀN NĂNG',
                    gia: 15000000,
                    gioi_han: 7,
                    mo_ta: 'Trọn gói ngày cưới hoàn hảo',
                    quyen_loi: [
                        '7 Váy Cưới tùy chọn (bao gồm dòng Luxury)',
                        '7 Bộ Vest Nam cao cấp',
                        'Trang điểm cô dâu & mẹ uyên ương',
                        'Chụp ảnh Pre-wedding & Tiệc cưới',
                        'Quay phim phóng sự cưới',
                        'Miễn phí chỉnh sửa ảnh & dựng phim'
                    ],
                    hinh_anh: 'https://images.unsplash.com/photo-1511285560982-1351cdeb9821?auto=format&fit=crop&q=80&w=600'
                },
                {
                    id: 4,
                    ten: 'COMBO PREMIUM LUXURY',
                    gia: 25000000,
                    gioi_han: 10,
                    mo_ta: 'Gói cao cấp với đội ngũ chuyên gia hàng đầu - Dành cho đám cưới hoàn hảo',
                    quyen_loi: [
                        '10 Váy Cưới cao cấp tùy chọn (bao gồm dòng Luxury & Designer)',
                        '10 Bộ Vest Nam cao cấp',
                        '🌟 Chuyên gia chụp ảnh HÀNG ĐẦU - Kinh nghiệm 10+ năm',
                        '🌟 Chuyên gia quay phim cinematic HÀNG ĐẦU',
                        '🌟 Dựng & chỉnh sửa ảnh bởi chuyên gia HÀNG ĐẦU',
                        '🌟 Dựng phim cưới điện ảnh (10-15 phút) - Đạo diễn chuyên nghiệp',
                        '🌟 Trang điểm cô dâu & gia đình bởi chuyên gia makeup HÀNG ĐẦU',
                        '🌟 Album ảnh cao cấp 40x60cm (50 trang) - Thiết kế độc quyền',
                        'Phụ kiện & trang sức đi kèm',
                        'Hỗ trợ tư vấn concept & styling bởi chuyên gia'
                    ],
                    hinh_anh: 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&q=80&w=600'
                }
            ]);
        }
    };

    const taiDuLieu = async () => {
        setDangTai(true);
        try {
            const [nuRes, namRes] = await Promise.all([
                sanPhamAPI.layTatCa({ gioi_tinh: 'female' }),
                sanPhamAPI.layTatCa({ gioi_tinh: 'male' })
            ]);
            setVayNu(nuRes.data);
            setVestNam(namRes.data);
        } catch (error) {
            console.error('Lỗi tải sản phẩm:', error);
        } finally {
            setDangTai(false);
        }
    };

    const chonGoiDichVu = (goi) => {
        setGoiDaChon(goi);
        setBuoc(2);
    };

    const xuLyChon = (item, danhSachDaChon, setDanhSachDaChon) => {
        const daCo = danhSachDaChon.find(i => i.id === item.id);
        if (daCo) {
            setDanhSachDaChon(danhSachDaChon.filter(i => i.id !== item.id));
        } else {
            if (danhSachDaChon.length < goiDaChon.gioi_han) {
                setDanhSachDaChon([...danhSachDaChon, item]);
            } else {
                addToast({ message: `Gói ${goiDaChon.ten} chỉ được chọn tối đa ${goiDaChon.gioi_han} sản phẩm mỗi loại.`, type: 'info' });
            }
        }
    };

    const StepIndicator = () => (
        <div className="combo-steps">
            {[1, 2, 3].map(s => (
                <div key={s} className={`step-indicator ${buoc === s ? 'active' : ''} ${buoc > s ? 'completed' : ''}`}>
                    <div className="step-number">{s}</div>
                    <span className="step-text">
                        {s === 1 ? 'Chọn Gói' : s === 2 ? 'Chọn Váy' : 'Chọn Vest'}
                    </span>
                </div>
            ))}
        </div>
    );

    return (
        <div className="combo-page">
            <section className="combo-hero">
                <div className="container">
                    <h1 className="page-title">Gói Dịch Vụ Cưới</h1>
                    <p className="page-subtitle">Giải pháp trọn gói, tiết kiệm tối đa</p>
                    <StepIndicator />
                </div>
            </section>

            <div className="combo-content">
                {/* BƯỚC 1: CHỌN GÓI */}
                {buoc === 1 && (
                    <div className="combo-intro fade-in">
                        <div className="pricing-grid">
                            {danhSachCombo.map(goi => (
                                <div key={goi.id} className={`pricing-card ${goi.noi_bat ? 'featured' : ''}`}>
                                    {goi.noi_bat && <div className="pricing-badge">BÁN CHẠY NHẤT</div>}
                                    <div className="pricing-image" style={{ backgroundImage: `url(${layUrlHinhAnh(goi.hinh_anh)})` }}></div>
                                    <div className="pricing-content">
                                        <h3 className="pricing-title">{goi.ten}</h3>
                                        <div className="pricing-price">{new Intl.NumberFormat('vi-VN').format(goi.gia)}đ</div>
                                        <p className="pricing-desc">{goi.mo_ta}</p>
                                        <ul className="pricing-features">
                                            {goi.quyen_loi.map((ql, idx) => (
                                                <li key={idx}>{ql}</li>
                                            ))}
                                        </ul>
                                        <NutBam
                                            variant="outline"
                                            className="btn-block"
                                            onClick={() => chonGoiDichVu(goi)}
                                        >
                                            CHỌN GÓI NÀY
                                        </NutBam>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* BƯỚC 2: CHỌN VÁY NỮ */}
                {buoc === 2 && (
                    <div className="selection-step fade-in">
                        <div className="selection-header">
                            <div>
                                <h3>Chọn Váy ({goiDaChon.gioi_han} mẫu)</h3>
                                <p style={{ fontSize: '14px', color: '#666' }}>Gói: {goiDaChon.ten}</p>
                            </div>
                            <span className="selection-counter">Đã chọn: {chonNu.length}/{goiDaChon.gioi_han}</span>
                        </div>
                        {dangTai ? <div className="loading">Đang tải sản phẩm...</div> : (
                            <div className="selection-grid">
                                {vayNu.map(sp => (
                                    <div
                                        key={sp.id}
                                        className={`selection-item ${chonNu.find(i => i.id === sp.id) ? 'selected' : ''}`}
                                        onClick={() => xuLyChon(sp, chonNu, setChonNu)}
                                    >
                                        <div className="selection-item-image">
                                            <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name} />
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="combo-actions">
                            <NutBam variant="outline" onClick={() => setBuoc(1)}>CHỌN LẠI GÓI</NutBam>
                            <NutBam onClick={() => setBuoc(3)}>TIẾP TỤC: CHỌN VEST</NutBam>
                        </div>
                    </div>
                )}

                {/* BƯỚC 3: CHỌN VEST NAM */}
                {buoc === 3 && (
                    <div className="selection-step fade-in">
                        <div className="selection-header">
                            <div>
                                <h3>Chọn Vest ({goiDaChon.gioi_han} mẫu)</h3>
                                <p style={{ fontSize: '14px', color: '#666' }}>Gói: {goiDaChon.ten}</p>
                            </div>
                            <span className="selection-counter">Đã chọn: {chonNam.length}/{goiDaChon.gioi_han}</span>
                        </div>
                        {dangTai ? <div className="loading">Đang tải sản phẩm...</div> : (
                            <div className="selection-grid">
                                {vestNam.map(sp => (
                                    <div
                                        key={sp.id}
                                        className={`selection-item ${chonNam.find(i => i.id === sp.id) ? 'selected' : ''}`}
                                        onClick={() => xuLyChon(sp, chonNam, setChonNam)}
                                    >
                                        <div className="selection-item-image">
                                            <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name} />
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="combo-actions">
                            <NutBam variant="outline" onClick={() => setBuoc(2)}>QUAY LẠI</NutBam>
                            <NutBam onClick={() => {
                                // Thêm combo vào giỏ hàng
                                const comboProduct = {
                                    id: `combo-${goiDaChon.id}`,
                                    name: goiDaChon.ten,
                                    code: `COMBO-${goiDaChon.id}`,
                                    category: 'combo',
                                    gender: 'unisex',
                                    description: goiDaChon.mo_ta,
                                    rental_price_day: goiDaChon.gia,
                                    rental_price_week: goiDaChon.gia,
                                    purchase_price: goiDaChon.gia,
                                    price_to_use: goiDaChon.gia,
                                    image_url: goiDaChon.hinh_anh,
                                    is_combo: true,
                                    quantity: 1,
                                    loai: 'mua',
                                    selected_items: {
                                        vay: chonNu.map(i => ({ id: i.id, name: i.name, code: i.code })),
                                        vest: chonNam.map(i => ({ id: i.id, name: i.name, code: i.code }))
                                    }
                                };
                                
                                const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
                                currentCart.push(comboProduct);
                                localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
                                
                                addToast({ 
                                    message: `Đã thêm ${goiDaChon.ten} vào giỏ hàng!`, 
                                    type: 'success' 
                                });
                                
                                setTimeout(() => {
                                    navigate('/gio-hang');
                                }, 500);
                            }}>THÊM VÀO GIỎ HÀNG</NutBam>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChonCombo;
