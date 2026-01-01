import { useState, useEffect, useRef } from 'react';
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
    const [showComboDetail, setShowComboDetail] = useState(null);
    const [showCompareTable, setShowCompareTable] = useState(false);
    const stickyBarRef = useRef(null);

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
                    <div className="step-number">{buoc > s ? '✓' : s}</div>
                    <span className="step-text">
                        {s === 1 ? 'Chọn Gói' : s === 2 ? 'Chọn Váy' : 'Chọn Vest'}
                    </span>
                </div>
            ))}
        </div>
    );

    // Progress Bar cho bước chọn sản phẩm
    const SelectionProgress = ({ current, max, type }) => {
        const percentage = (current / max) * 100;
        const slots = Array.from({ length: max }, (_, i) => i < current);
        
        return (
            <div className="selection-progress">
                <div className="progress-header">
                    <span className="progress-label">
                        {type === 'vay' ? '👗 Váy cưới' : '🤵 Vest nam'}
                    </span>
                    <span className="progress-count">{current}/{max}</span>
                </div>
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${percentage}%` }}></div>
                </div>
                <div className="progress-slots">
                    {slots.map((filled, idx) => (
                        <div key={idx} className={`slot ${filled ? 'filled' : 'empty'}`}>
                            {filled ? '✓' : idx + 1}
                        </div>
                    ))}
                </div>
                {current < max && (
                    <p className="progress-hint">Còn {max - current} vị trí trống</p>
                )}
                {current === max && (
                    <p className="progress-complete">✅ Đã chọn đủ!</p>
                )}
            </div>
        );
    };

    // Modal xem chi tiết combo
    const ComboDetailModal = ({ combo, onClose }) => {
        if (!combo) return null;
        
        const quyenLoiChiTiet = {
            'Hỗ trợ chỉnh sửa kích cỡ': 'Đội ngũ thợ may chuyên nghiệp sẽ chỉnh sửa váy/vest theo số đo của bạn, đảm bảo vừa vặn hoàn hảo.',
            'Miễn phí giặt ủi': 'Sau khi sử dụng, chúng tôi sẽ giặt ủi miễn phí trước khi bạn trả lại.',
            'Phụ kiện đi kèm miễn phí': 'Bao gồm: khăn voan, găng tay, vương miện, hoa cài áo vest.',
            'Giữ đồ trong 3 ngày': 'Bạn có thể giữ váy/vest trong 3 ngày để chụp ảnh và tiệc cưới.',
            'Trang điểm cô dâu & mẹ uyên ương': 'Chuyên gia makeup sẽ trang điểm cho cô dâu và 2 mẹ trong ngày cưới.',
            'Chụp ảnh Pre-wedding & Tiệc cưới': 'Gói chụp ảnh cưới ngoại cảnh + phóng sự tiệc cưới.',
            'Quay phim phóng sự cưới': 'Quay phim full HD, dựng clip highlight 3-5 phút.',
            'Miễn phí chỉnh sửa ảnh & dựng phim': 'Chỉnh sửa màu, retouch da, dựng phim chuyên nghiệp.'
        };
        
        return (
            <div className="combo-modal-overlay" onClick={onClose}>
                <div className="combo-modal" onClick={e => e.stopPropagation()}>
                    <button className="modal-close" onClick={onClose}>×</button>
                    <div className="modal-header">
                        <img src={layUrlHinhAnh(combo.hinh_anh)} alt={combo.ten} />
                        <div className="modal-title-section">
                            <h2>{combo.ten}</h2>
                            <div className="modal-price">{new Intl.NumberFormat('vi-VN').format(combo.gia)}đ</div>
                            <p>{combo.mo_ta}</p>
                        </div>
                    </div>
                    <div className="modal-content">
                        <h3>📋 Chi tiết quyền lợi</h3>
                        <div className="benefits-detail-list">
                            {combo.quyen_loi.map((ql, idx) => (
                                <div key={idx} className="benefit-detail-item">
                                    <div className="benefit-name">✓ {ql}</div>
                                    {quyenLoiChiTiet[ql] && (
                                        <div className="benefit-desc">{quyenLoiChiTiet[ql]}</div>
                                    )}
                                </div>
                            ))}
                        </div>
                        <div className="modal-policy">
                            <h4>📌 Chính sách đổi/hủy</h4>
                            <ul>
                                <li>Đổi lịch miễn phí trước 7 ngày</li>
                                <li>Hoàn 80% cọc nếu hủy trước 14 ngày</li>
                                <li>Hoàn 50% cọc nếu hủy trước 7 ngày</li>
                            </ul>
                        </div>
                    </div>
                    <div className="modal-footer">
                        <NutBam variant="primary" onClick={() => { onClose(); chonGoiDichVu(combo); }}>
                            CHỌN GÓI NÀY
                        </NutBam>
                    </div>
                </div>
            </div>
        );
    };

    // Bảng so sánh combo
    const CompareTable = () => (
        <div className="compare-table-section">
            <h3 className="compare-title">📊 So sánh các gói dịch vụ</h3>
            <div className="compare-table-wrapper">
                <table className="compare-table">
                    <thead>
                        <tr>
                            <th>Quyền lợi</th>
                            {danhSachCombo.map(c => (
                                <th key={c.id} className={c.noi_bat ? 'featured-col' : ''}>
                                    {c.ten}
                                    <div className="th-price">{new Intl.NumberFormat('vi-VN').format(c.gia)}đ</div>
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Số váy cưới</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gioi_han}</td>)}
                        </tr>
                        <tr>
                            <td>Số vest nam</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gioi_han}</td>)}
                        </tr>
                        <tr>
                            <td>Phụ kiện miễn phí</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gia >= 5000000 ? '✓' : '—'}</td>)}
                        </tr>
                        <tr>
                            <td>Trang điểm</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gia >= 15000000 ? '✓' : '—'}</td>)}
                        </tr>
                        <tr>
                            <td>Chụp ảnh cưới</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gia >= 15000000 ? '✓' : '—'}</td>)}
                        </tr>
                        <tr>
                            <td>Quay phim</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gia >= 15000000 ? '✓' : '—'}</td>)}
                        </tr>
                        <tr>
                            <td>Chuyên gia hàng đầu</td>
                            {danhSachCombo.map(c => <td key={c.id}>{c.gia >= 25000000 ? '⭐' : '—'}</td>)}
                        </tr>
                        <tr className="action-row">
                            <td></td>
                            {danhSachCombo.map(c => (
                                <td key={c.id}>
                                    <NutBam 
                                        variant={c.noi_bat ? 'primary' : 'outline'} 
                                        onClick={() => chonGoiDichVu(c)}
                                        style={{ fontSize: '12px', padding: '8px 16px' }}
                                    >
                                        CHỌN
                                    </NutBam>
                                </td>
                            ))}
                        </tr>
                    </tbody>
                </table>
            </div>
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
                        {/* Toggle bảng so sánh */}
                        <div className="compare-toggle">
                            <button 
                                className={`toggle-btn ${showCompareTable ? 'active' : ''}`}
                                onClick={() => setShowCompareTable(!showCompareTable)}
                            >
                                {showCompareTable ? '📋 Ẩn bảng so sánh' : '📊 Xem bảng so sánh'}
                            </button>
                        </div>

                        {showCompareTable && <CompareTable />}

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
                                            {goi.quyen_loi.slice(0, 4).map((ql, idx) => (
                                                <li key={idx}>{ql}</li>
                                            ))}
                                            {goi.quyen_loi.length > 4 && (
                                                <li className="more-features">+{goi.quyen_loi.length - 4} quyền lợi khác</li>
                                            )}
                                        </ul>
                                        <div className="pricing-actions">
                                            <button 
                                                className="btn-detail"
                                                onClick={() => setShowComboDetail(goi)}
                                            >
                                                Xem chi tiết
                                            </button>
                                            <NutBam
                                                variant={goi.noi_bat ? 'primary' : 'outline'}
                                                className="btn-block"
                                                onClick={() => chonGoiDichVu(goi)}
                                            >
                                                CHỌN GÓI NÀY
                                            </NutBam>
                                        </div>
                                        
                                        {/* Trust signals */}
                                        <div className="pricing-trust">
                                            <span>⭐ 4.9/5</span>
                                            <span>👥 {50 + goi.id * 30}+ đã chọn</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Chính sách */}
                        <div className="combo-policy-banner">
                            <div className="policy-item">
                                <span className="policy-icon">🔄</span>
                                <div>
                                    <strong>Đổi lịch miễn phí</strong>
                                    <p>Trước 7 ngày</p>
                                </div>
                            </div>
                            <div className="policy-item">
                                <span className="policy-icon">💰</span>
                                <div>
                                    <strong>Hoàn tiền cọc</strong>
                                    <p>Lên đến 80%</p>
                                </div>
                            </div>
                            <div className="policy-item">
                                <span className="policy-icon">📞</span>
                                <div>
                                    <strong>Hỗ trợ 24/7</strong>
                                    <p>Hotline: 0909.xxx.xxx</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Modal chi tiết combo */}
                {showComboDetail && (
                    <ComboDetailModal 
                        combo={showComboDetail} 
                        onClose={() => setShowComboDetail(null)} 
                    />
                )}

                {/* BƯỚC 2: CHỌN VÁY NỮ */}
                {buoc === 2 && (
                    <div className="selection-step fade-in">
                        {/* Sticky header với progress */}
                        <div className="selection-header-sticky" ref={stickyBarRef}>
                            <div className="sticky-left">
                                <h3>👗 Chọn Váy Cưới</h3>
                                <p className="package-name">Gói: {goiDaChon.ten}</p>
                            </div>
                            <div className="sticky-right">
                                <SelectionProgress current={chonNu.length} max={goiDaChon.gioi_han} type="vay" />
                            </div>
                        </div>

                        {/* Thông báo giá đã bao gồm */}
                        <div className="included-notice">
                            <span className="notice-icon">💡</span>
                            <span>Tất cả váy cưới dưới đây đều <strong>ĐÃ BAO GỒM</strong> trong gói {goiDaChon.ten}. Bạn chỉ cần chọn mẫu yêu thích!</span>
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
                                            {chonNu.find(i => i.id === sp.id) && (
                                                <div className="selected-order">
                                                    {chonNu.findIndex(i => i.id === sp.id) + 1}
                                                </div>
                                            )}
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                            <p className="included-price">Đã bao gồm trong combo</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Sticky bottom bar */}
                        <div className="combo-actions-sticky">
                            <div className="actions-left">
                                <NutBam variant="outline" onClick={() => setBuoc(1)}>← Chọn lại gói</NutBam>
                            </div>
                            <div className="actions-right">
                                <div className="selection-summary">
                                    Đã chọn: <strong>{chonNu.length}/{goiDaChon.gioi_han}</strong> váy
                                </div>
                                <NutBam 
                                    onClick={() => setBuoc(3)}
                                    disabled={chonNu.length === 0}
                                    className={chonNu.length === 0 ? 'btn-disabled' : ''}
                                >
                                    TIẾP TỤC: CHỌN VEST →
                                </NutBam>
                            </div>
                        </div>
                    </div>
                )}

                {/* BƯỚC 3: CHỌN VEST NAM */}
                {buoc === 3 && (
                    <div className="selection-step fade-in">
                        {/* Sticky header với progress */}
                        <div className="selection-header-sticky">
                            <div className="sticky-left">
                                <h3>🤵 Chọn Vest Nam</h3>
                                <p className="package-name">Gói: {goiDaChon.ten}</p>
                            </div>
                            <div className="sticky-right">
                                <SelectionProgress current={chonNam.length} max={goiDaChon.gioi_han} type="vest" />
                            </div>
                        </div>

                        {/* Thông báo giá đã bao gồm */}
                        <div className="included-notice">
                            <span className="notice-icon">💡</span>
                            <span>Tất cả vest dưới đây đều <strong>ĐÃ BAO GỒM</strong> trong gói {goiDaChon.ten}. Bạn chỉ cần chọn mẫu yêu thích!</span>
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
                                            {chonNam.find(i => i.id === sp.id) && (
                                                <div className="selected-order">
                                                    {chonNam.findIndex(i => i.id === sp.id) + 1}
                                                </div>
                                            )}
                                        </div>
                                        <div className="selection-item-info">
                                            <h4>{sp.name}</h4>
                                            <p className="included-price">Đã bao gồm trong combo</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Sticky bottom bar */}
                        <div className="combo-actions-sticky">
                            <div className="actions-left">
                                <NutBam variant="outline" onClick={() => setBuoc(2)}>← Quay lại</NutBam>
                            </div>
                            <div className="actions-right">
                                <div className="selection-summary">
                                    <span>👗 {chonNu.length} váy</span>
                                    <span>🤵 {chonNam.length} vest</span>
                                </div>
                                <NutBam 
                                    onClick={() => {
                                        // Thêm combo vào giỏ hàng
                                        const comboProduct = {
                                            id: `combo-${goiDaChon.id}-${Date.now()}`,
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
                                                vay: chonNu.map(i => ({ id: i.id, name: i.name, code: i.code, image_url: i.image_url })),
                                                vest: chonNam.map(i => ({ id: i.id, name: i.name, code: i.code, image_url: i.image_url }))
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
                                    }}
                                    disabled={chonNu.length === 0 && chonNam.length === 0}
                                    className={chonNu.length === 0 && chonNam.length === 0 ? 'btn-disabled' : ''}
                                >
                                    🛒 THÊM VÀO GIỎ HÀNG
                                </NutBam>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChonCombo;
