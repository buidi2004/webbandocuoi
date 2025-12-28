import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import { DANH_SACH_GOI } from '../trang/ChonCombo';
import '../styles/search.css';

const ThanhTimKiem = ({ isOpen, onClose }) => {
    const [tuKhoa, setTuKhoa] = useState('');
    const [sanPham, setSanPham] = useState([]);
    const [ketQua, setKetQua] = useState({ sanPham: [], combo: [] });
    const [dangTai, setDangTai] = useState(false);
    const inputRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (isOpen && sanPham.length === 0) {
            taiSanPham();
        }
        if (isOpen) {
            setTimeout(() => {
                inputRef.current?.focus();
            }, 100);
        } else {
            setTuKhoa('');
            setKetQua({ sanPham: [], combo: [] });
        }
    }, [isOpen]);

    const taiSanPham = async () => {
        setDangTai(true);
        try {
            const res = await sanPhamAPI.layTatCa();
            if (res.data) setSanPham(res.data);
        } catch (error) {
            console.error("Lỗi tải sản phẩm tìm kiếm:", error);
        } finally {
            setDangTai(false);
        }
    };

    useEffect(() => {
        if (!tuKhoa.trim()) {
            setKetQua({ sanPham: [], combo: [] });
            return;
        }

        const tuKhoaThuong = tuKhoa.toLowerCase();

        const spTimThay = sanPham.filter(sp =>
            sp.name.toLowerCase().includes(tuKhoaThuong) ||
            sp.code.toLowerCase().includes(tuKhoaThuong)
        ).slice(0, 10);

        const cbTimThay = DANH_SACH_GOI.filter(cb =>
            cb.ten.toLowerCase().includes(tuKhoaThuong) ||
            cb.mo_ta.toLowerCase().includes(tuKhoaThuong)
        ).slice(0, 5);

        setKetQua({ sanPham: spTimThay, combo: cbTimThay });
    }, [tuKhoa, sanPham]);

    const dinhDangGia = (gia) => {
        return new Intl.NumberFormat('vi-VN').format(gia) + 'đ';
    };

    if (!isOpen) return null;

    const QuickTag = ({ text }) => (
        <button className="tag-btn" onClick={() => setTuKhoa(text)}>
            {text}
        </button>
    );

    return (
        <div className={`search-overlay ${isOpen ? 'active' : ''}`} onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
        }}>
            <div className="search-container">
                {/* Search Bar Wrapper */}
                <div className="search-bar-wrapper">
                    <svg className="search-icon-large" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input
                        ref={inputRef}
                        type="text"
                        className="search-input"
                        placeholder="Bạn đang tìm kiếm điều gì?"
                        value={tuKhoa}
                        onChange={(e) => setTuKhoa(e.target.value)}
                    />
                    <button className="close-search-btn" onClick={onClose}>&times;</button>
                </div>

                {/* Suggestions / Quick Tags */}
                {!tuKhoa && (
                    <div className="quick-tags">
                        <span style={{ color: '#999', fontSize: '0.9rem', marginRight: '10px' }}>Gợi ý:</span>
                        <QuickTag text="Váy cưới hiện đại" />
                        <QuickTag text="Áo dài truyền thống" />
                        <QuickTag text="Combo Album" />
                        <QuickTag text="Vest nam" />
                    </div>
                )}

                {/* Search Results Grid */}
                <div className="search-content-grid">
                    {/* Left: Products */}
                    <div className="results-column">
                        <div className="section-title-modern">Sản phẩm ({ketQua.sanPham.length})</div>
                        {ketQua.sanPham.length > 0 ? ketQua.sanPham.map((sp, index) => (
                            <Link
                                to={`/san-pham/${sp.id}`}
                                key={sp.id}
                                className="modern-card"
                                onClick={onClose}
                                style={{ animationDelay: `${index * 0.05}s` }}
                            >
                                <div className="card-img-wrapper">
                                    <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name}
                                        onError={(e) => e.target.src = 'https://placehold.co/100x150?text=IVIE'} />
                                </div>
                                <div className="card-details">
                                    <h4 className="card-name">{sp.name}</h4>
                                    <span className="card-meta">Mã: #{sp.code}</span>
                                    <span className="card-price">Thuê: {dinhDangGia(sp.rental_price_day)}</span>
                                </div>
                            </Link>
                        )) : tuKhoa && !dangTai && (
                            <div className="no-results" style={{ fontSize: '1rem', padding: '20px 0' }}>Không thấy sản phẩm nào...</div>
                        )}
                    </div>

                    {/* Right: Combos */}
                    <div className="results-column">
                        <div className="section-title-modern">Gói dịch vụ ({ketQua.combo.length})</div>
                        {ketQua.combo.length > 0 ? ketQua.combo.map((cb, index) => (
                            <Link
                                to="/chon-combo"
                                key={index}
                                className="modern-card"
                                onClick={onClose}
                                style={{ animationDelay: `${(index + 3) * 0.05}s` }}
                            >
                                <div className="card-img-wrapper">
                                    <img src={cb.hinh_anh} alt={cb.ten} />
                                </div>
                                <div className="card-details">
                                    <h4 className="card-name" style={{ fontSize: '1rem' }}>{cb.ten}</h4>
                                    <span className="card-price">{dinhDangGia(cb.gia)}</span>
                                </div>
                            </Link>
                        )) : tuKhoa && !dangTai && (
                            <div className="no-results" style={{ fontSize: '1rem', padding: '20px 0' }}>Không thấy gói nào...</div>
                        )}
                    </div>
                </div>

                {dangTai && <div style={{ textAlign: 'center', color: '#b59410', padding: '40px' }}>Đang tìm kiếm...</div>}
                {!tuKhoa && !dangTai && (
                    <div className="no-results">Bắt đầu gõ để khám phá bộ sưu tập của chúng tôi</div>
                )}
            </div>
        </div>
    );
};

export default ThanhTimKiem;
