import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { layUrlHinhAnh } from '../api/khach_hang';
import { useToast } from './Toast';
import './QuickViewModal.css';

const QuickViewModal = ({ sanPham, onClose }) => {
    const [hinhHienTai, setHinhHienTai] = useState(0);
    const [dangTai, setDangTai] = useState(true);
    const navigate = useNavigate();
    const { addToast } = useToast();

    // Danh sách hình ảnh (main + gallery nếu có)
    const danhSachHinh = sanPham?.gallery_images 
        ? [sanPham.image_url, ...sanPham.gallery_images.split(',').filter(Boolean)]
        : [sanPham?.image_url];

    useEffect(() => {
        // Disable body scroll khi modal mở
        document.body.style.overflow = 'hidden';
        setDangTai(false);
        
        return () => {
            document.body.style.overflow = 'unset';
        };
    }, []);

    // Đóng modal khi nhấn ESC
    useEffect(() => {
        const handleEsc = (e) => {
            if (e.key === 'Escape') onClose();
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, [onClose]);

    if (!sanPham) return null;

    const dinhDangGia = (gia) => new Intl.NumberFormat('vi-VN').format(gia) + 'đ';

    const themGioHang = () => {
        const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        const item = {
            id: sanPham.id,
            name: sanPham.name,
            code: sanPham.code,
            image_url: sanPham.image_url,
            purchase_price: sanPham.purchase_price,
            rental_price_day: sanPham.rental_price_day,
            price_to_use: sanPham.purchase_price,
            quantity: 1,
            loai: 'mua',
            so_luong: sanPham.so_luong
        };
        const existing = currentCart.findIndex(i => i.id === item.id && i.loai === 'mua');
        if (existing > -1) {
            currentCart[existing].quantity = (currentCart[existing].quantity || 1) + 1;
        } else {
            currentCart.push(item);
        }
        localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
        addToast({ message: 'Đã thêm vào giỏ hàng!', type: 'success' });
    };

    const muaNgay = () => {
        themGioHang();
        navigate('/gio-hang');
    };

    const xemChiTiet = () => {
        onClose();
        navigate(`/san-pham/${sanPham.id}`);
    };

    return (
        <div className="quick-view-overlay" onClick={onClose}>
            <div className="quick-view-modal" onClick={(e) => e.stopPropagation()}>
                <button className="qv-close" onClick={onClose}>×</button>
                
                <div className="qv-content">
                    {/* Gallery bên trái */}
                    <div className="qv-gallery">
                        <div className="qv-main-image">
                            {sanPham.is_hot && <span className="qv-badge hot">Hot Deal 🔥</span>}
                            {sanPham.is_new && <span className="qv-badge new">Mới ✨</span>}
                            <img 
                                src={layUrlHinhAnh(danhSachHinh[hinhHienTai])} 
                                alt={sanPham.name}
                                loading="lazy"
                                onError={(e) => e.target.src = 'https://placehold.co/500x600/f5f5f5/333?text=IVIE'}
                            />
                        </div>
                        
                        {danhSachHinh.length > 1 && (
                            <div className="qv-thumbnails">
                                {danhSachHinh.map((hinh, idx) => (
                                    <div 
                                        key={idx}
                                        className={`qv-thumb ${idx === hinhHienTai ? 'active' : ''}`}
                                        onClick={() => setHinhHienTai(idx)}
                                    >
                                        <img 
                                            src={layUrlHinhAnh(hinh)} 
                                            alt={`${sanPham.name} ${idx + 1}`}
                                            loading="lazy"
                                        />
                                    </div>
                                ))}
                            </div>
                        )}
                        
                        {/* Navigation arrows */}
                        {danhSachHinh.length > 1 && (
                            <>
                                <button 
                                    className="qv-nav prev"
                                    onClick={() => setHinhHienTai(prev => prev === 0 ? danhSachHinh.length - 1 : prev - 1)}
                                >
                                    ‹
                                </button>
                                <button 
                                    className="qv-nav next"
                                    onClick={() => setHinhHienTai(prev => prev === danhSachHinh.length - 1 ? 0 : prev + 1)}
                                >
                                    ›
                                </button>
                            </>
                        )}
                    </div>
                    
                    {/* Thông tin bên phải */}
                    <div className="qv-info">
                        <h2 className="qv-title">{sanPham.name}</h2>
                        
                        <div className="qv-rating">
                            <span className="stars">⭐⭐⭐⭐⭐</span>
                            <span className="count">(128 đánh giá)</span>
                        </div>
                        
                        <div className="qv-prices">
                            <div className="qv-price-row">
                                <span className="label">Thuê:</span>
                                <span className="price rental">{dinhDangGia(sanPham.rental_price_day)}</span>
                                <span className="unit">/ngày</span>
                            </div>
                            {sanPham.purchase_price > 0 && (
                                <div className="qv-price-row">
                                    <span className="label">Mua:</span>
                                    <span className="price purchase">{dinhDangGia(sanPham.purchase_price)}</span>
                                </div>
                            )}
                        </div>
                        
                        {sanPham.description && (
                            <p className="qv-description">{sanPham.description}</p>
                        )}
                        
                        <div className="qv-meta">
                            {sanPham.style && (
                                <span className="meta-item">
                                    <strong>Phong cách:</strong> {sanPham.style}
                                </span>
                            )}
                            {sanPham.so_luong !== undefined && (
                                <span className={`meta-item ${sanPham.so_luong <= 5 ? 'low-stock' : ''}`}>
                                    <strong>Còn lại:</strong> {sanPham.so_luong} sản phẩm
                                </span>
                            )}
                        </div>
                        
                        <div className="qv-actions">
                            <button className="qv-btn add-cart" onClick={themGioHang}>
                                🛒 Thêm giỏ hàng
                            </button>
                            <button className="qv-btn buy-now" onClick={muaNgay}>
                                Mua ngay
                            </button>
                        </div>
                        
                        <button className="qv-detail-link" onClick={xemChiTiet}>
                            Xem chi tiết sản phẩm →
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuickViewModal;
