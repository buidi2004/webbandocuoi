import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { sanPhamAPI, layUrlHinhAnh, comboAPI } from '../api/khach_hang';
import '../styles/search.css';

const ThanhTimKiem = ({ isOpen, onClose }) => {
    const [tuKhoa, setTuKhoa] = useState('');
    const [sanPham, setSanPham] = useState([]);
    const [danhSachCombo, setDanhSachCombo] = useState([]);
    const [ketQua, setKetQua] = useState({ sanPham: [], combo: [] });
    const [dangTai, setDangTai] = useState(false);
    const [phongCach, setPhongCach] = useState('all');
    const [khoangGia, setKhoangGia] = useState('all');
    const inputRef = useRef(null);
    const navigate = useNavigate();

    const goiYTimKiem = [
        'Váy cưới hiện đại',
        'Áo dài truyền thống',
        'Combo Album',
        'Vest nam',
        'Váy đuôi cá',
    ];

    const phongCachOptions = [
        { id: 'all', nhan: 'Tất cả' },
        { id: 'minimalist', nhan: 'Minimalist' },
        { id: 'princess', nhan: 'Công chúa' },
        { id: 'vintage', nhan: 'Vintage' },
        { id: 'sexy', nhan: 'Quyến rũ' },
        { id: 'classic', nhan: 'Cổ điển' },
    ];

    const khoangGiaOptions = [
        { id: 'all', nhan: 'Tất cả giá' },
        { id: 'duoi_500k', nhan: 'Dưới 500K' },
        { id: '500k_1tr', nhan: '500K - 1 triệu' },
        { id: '1tr_2tr', nhan: '1 - 2 triệu' },
        { id: 'tren_2tr', nhan: 'Trên 2 triệu' },
    ];

    useEffect(() => {
        if (isOpen && sanPham.length === 0) {
            taiSanPham();
            taiCombo();
        }
        if (isOpen) {
            setTimeout(() => {
                inputRef.current?.focus();
            }, 100);
        } else {
            setTuKhoa('');
            setKetQua({ sanPham: [], combo: [] });
            setPhongCach('all');
            setKhoangGia('all');
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

    const taiCombo = async () => {
        try {
            const res = await comboAPI.layTatCa();
            if (res.data) setDanhSachCombo(res.data);
        } catch (error) {
            console.error("Lỗi tải combo:", error);
            setDanhSachCombo([
                { id: 1, ten: 'COMBO KHỞI ĐẦU', gia: 2000000, mo_ta: 'Gói cơ bản cho các cặp đôi', hinh_anh: 'https://images.unsplash.com/photo-1594552072238-b8a33785b261?auto=format&fit=crop&q=80&w=600' },
                { id: 2, ten: 'COMBO TIẾT KIỆM', gia: 5000000, mo_ta: 'Sự lựa chọn phổ biến nhất', hinh_anh: 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?auto=format&fit=crop&q=80&w=600' },
                { id: 3, ten: 'COMBO VIP TOÀN NĂNG', gia: 15000000, mo_ta: 'Trọn gói ngày cưới hoàn hảo', hinh_anh: 'https://images.unsplash.com/photo-1511285560982-1351cdeb9821?auto=format&fit=crop&q=80&w=600' }
            ]);
        }
    };

    useEffect(() => {
        const tuKhoaThuong = tuKhoa.toLowerCase().trim();

        let spTimThay = sanPham;

        // Lọc theo từ khóa
        if (tuKhoaThuong) {
            spTimThay = spTimThay.filter(sp =>
                sp.name.toLowerCase().includes(tuKhoaThuong) ||
                sp.code.toLowerCase().includes(tuKhoaThuong)
            );
        }

        // Lọc theo phong cách
        if (phongCach !== 'all') {
            spTimThay = spTimThay.filter(sp => sp.style === phongCach);
        }

        // Lọc theo khoảng giá
        if (khoangGia !== 'all') {
            spTimThay = spTimThay.filter(sp => {
                const gia = sp.rental_price_day || 0;
                switch (khoangGia) {
                    case 'duoi_500k': return gia < 500000;
                    case '500k_1tr': return gia >= 500000 && gia < 1000000;
                    case '1tr_2tr': return gia >= 1000000 && gia < 2000000;
                    case 'tren_2tr': return gia >= 2000000;
                    default: return true;
                }
            });
        }

        const cbTimThay = tuKhoaThuong ? danhSachCombo.filter(cb =>
            cb.ten.toLowerCase().includes(tuKhoaThuong) ||
            cb.mo_ta.toLowerCase().includes(tuKhoaThuong)
        ).slice(0, 5) : [];

        setKetQua({ sanPham: spTimThay.slice(0, 10), combo: cbTimThay });
    }, [tuKhoa, sanPham, danhSachCombo, phongCach, khoangGia]);

    const dinhDangGia = (gia) => new Intl.NumberFormat('vi-VN').format(gia) + 'đ';

    if (!isOpen) return null;

    return (
        <div className={`search-overlay ${isOpen ? 'active' : ''}`} onClick={(e) => {
            if (e.target === e.currentTarget) onClose();
        }}>
            <div className="search-container">
                {/* Search Input - Tối giản, bo góc tròn */}
                <div className="search-bar-wrapper">
                    <svg className="search-icon-large" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="11" cy="11" r="8"/>
                        <path d="m21 21-4.35-4.35"/>
                    </svg>
                    <input
                        ref={inputRef}
                        type="text"
                        className="search-input"
                        placeholder="Bạn đang tìm kiếm điều gì?"
                        value={tuKhoa}
                        onChange={(e) => setTuKhoa(e.target.value)}
                    />
                    {tuKhoa && (
                        <button className="search-clear-btn" onClick={() => setTuKhoa('')}>×</button>
                    )}
                    <button className="close-search-btn" onClick={onClose}>×</button>
                </div>

                {/* Chips gợi ý */}
                <div className="search-chips-wrapper">
                    {goiYTimKiem.map((goiY, index) => (
                        <button
                            key={index}
                            className={`search-chip ${tuKhoa === goiY ? 'active' : ''}`}
                            onClick={() => setTuKhoa(goiY)}
                        >
                            {goiY}
                        </button>
                    ))}
                </div>

                {/* Bộ lọc - Flexbox */}
                <div className="search-filters">
                    <div className="filter-group">
                        <span className="filter-label">Phong cách:</span>
                        <div className="filter-options">
                            {phongCachOptions.map(pc => (
                                <button
                                    key={pc.id}
                                    className={`filter-btn ${phongCach === pc.id ? 'active' : ''}`}
                                    onClick={() => setPhongCach(pc.id)}
                                >
                                    {pc.nhan}
                                </button>
                            ))}
                        </div>
                    </div>
                    <div className="filter-group">
                        <span className="filter-label">Khoảng giá:</span>
                        <div className="filter-options">
                            {khoangGiaOptions.map(kg => (
                                <button
                                    key={kg.id}
                                    className={`filter-btn ${khoangGia === kg.id ? 'active' : ''}`}
                                    onClick={() => setKhoangGia(kg.id)}
                                >
                                    {kg.nhan}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Kết quả tìm kiếm */}
                <div className="search-content-grid">
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
                        )) : !dangTai && (
                            <div className="no-results">Không tìm thấy sản phẩm phù hợp</div>
                        )}
                    </div>

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
                                    <h4 className="card-name">{cb.ten}</h4>
                                    <span className="card-price">{dinhDangGia(cb.gia)}</span>
                                </div>
                            </Link>
                        )) : tuKhoa && !dangTai && (
                            <div className="no-results">Không tìm thấy gói dịch vụ</div>
                        )}
                    </div>
                </div>

                {dangTai && <div className="search-loading">Đang tìm kiếm...</div>}
            </div>
        </div>
    );
};

export default ThanhTimKiem;
