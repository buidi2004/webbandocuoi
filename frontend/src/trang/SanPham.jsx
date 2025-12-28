import { useState, useEffect, useLayoutEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useNavigate } from 'react-router-dom';
import api, { sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import The from '../thanh_phan/The';
import { useToast } from '../thanh_phan/Toast';
import '../styles/products.css';

const SanPham = () => {
    // ... existing code ...

    // ... (skipping to render part for brevity in tool call, but strictly targeting lines)
    // actually I need TWO replace calls or one multi_replace because imports are at top and code at bottom.
    // I will use multi_replace.
    const [danhSachSanPham, setDanhSachSanPham] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const [loi, setLoi] = useState(null);
    const [boLoc, setBoLoc] = useState('all');
    const [tieuMuc, setTieuMuc] = useState('all');
    const [sapXep, setSapXep] = useState('new');

    const containerRef = useRef(null);

    gsap.registerPlugin(ScrollTrigger);

    useLayoutEffect(() => {
        if (danhSachSanPham.length > 0) {
            let ctx = gsap.context(() => {
                // Hero Animation
                gsap.from(".page-title", { opacity: 0, y: -30, duration: 1, ease: "power3.out" });
                gsap.from(".page-subtitle", { opacity: 0, y: 30, duration: 1, delay: 0.3, ease: "power3.out" });

                gsap.fromTo(".product-card",
                    { opacity: 0, y: 50 },
                    {
                        opacity: 1,
                        y: 0,
                        duration: 0.8,
                        stagger: 0.1,
                        ease: "power3.out",
                        scrollTrigger: {
                            trigger: ".products-grid",
                            start: "top 80%",
                        }
                    }
                );
            }, containerRef);
            return () => ctx.revert();
        }
    }, [danhSachSanPham]);

    useEffect(() => {
        laySanPham();
    }, [boLoc, tieuMuc, sapXep]);

    const laySanPham = async () => {
        setDangTai(true);
        setLoi(null);
        try {
            const thamSo = { sort_by: sapXep };
            if (boLoc !== 'all') thamSo.danh_muc = boLoc;
            if (tieuMuc !== 'all') thamSo.sub_category = tieuMuc;

            const phanHoi = await sanPhamAPI.layTatCa(thamSo);
            if (Array.isArray(phanHoi.data)) {
                setDanhSachSanPham(phanHoi.data);
            } else {
                setDanhSachSanPham([]);
            }
        } catch (loi) {
            console.error('Lỗi khi tải sản phẩm:', loi);
            setLoi('Không thể tải dữ liệu sản phẩm.');
        } finally {
            setDangTai(false);
        }
    };

    const dinhDangGia = (gia) => {
        return new Intl.NumberFormat('vi-VN').format(gia) + 'đ';
    };

    const navigate = useNavigate();
    const { addToast } = useToast();

    const addToCart = (product) => {
        const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        const existingItemIndex = currentCart.findIndex(item => item.id === product.id);
        if (existingItemIndex > -1) {
            currentCart[existingItemIndex].quantity = (currentCart[existingItemIndex].quantity || 1) + 1;
        } else {
            currentCart.push({ ...product, quantity: 1 });
        }
        localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
        addToast({ message: 'Đã thêm vào giỏ hàng!', type: 'success' });
    };

    const buyNow = (product) => {
        const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        const existingItemIndex = currentCart.findIndex(item => item.id === product.id);
        if (existingItemIndex > -1) {
            currentCart[existingItemIndex].quantity = (currentCart[existingItemIndex].quantity || 1) + 1;
        } else {
            currentCart.push({ ...product, quantity: 1 });
        }
        localStorage.setItem('ivie_cart', JSON.stringify(currentCart));
        navigate('/gio-hang');
    };


    const layBoLocTieuMuc = () => {
        if (boLoc === 'wedding_modern') return [
            { id: 'all', nhan: 'Tất cả váy' },
            { id: 'xoe', nhan: 'Váy Xòe' },
            { id: 'ngan', nhan: 'Váy Ngắn' }
        ];
        if (boLoc === 'aodai') return [
            { id: 'all', nhan: 'Tất cả áo dài' },
            { id: 'nam', nhan: 'Áo dài Nam' },
            { id: 'nu', nhan: 'Áo dài Nữ' }
        ];
        if (boLoc === 'vest') return [
            { id: 'all', nhan: 'Tất cả Vest' },
            { id: 'hien_dai', nhan: 'Vest Hiện đại' },
            { id: 'truyen_thong', nhan: 'Vest Hàn Quốc' }
        ];
        return [];
    };

    return (
        <div className="products-page" ref={containerRef}>
            <section className="page-hero">
                <div className="page-hero-overlay"></div>
                <div className="page-hero-content container">
                    <h1 className="page-title">Bộ Sưu Tập</h1>
                    <p className="page-subtitle">Váy Cưới & Trang Phục Lễ Hội Cao Cấp</p>
                </div>
            </section>

            <section className="products-filter">
                <div className="container">
                    <div className="filter-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', flexWrap: 'wrap', gap: '15px' }}>
                        <div className="filter-tabs">
                            {[
                                { id: 'all', nhan: 'Tất Cả' },
                                { id: 'wedding_modern', nhan: 'Váy Cưới Hiện Đại' },
                                { id: 'vest', nhan: 'Vest Nam' },
                                { id: 'aodai', nhan: 'Áo Dài' }
                            ].map(tab => (
                                <button
                                    key={tab.id}
                                    className={`filter-tab ${boLoc === tab.id ? 'active' : ''}`}
                                    onClick={() => { setBoLoc(tab.id); setTieuMuc('all'); }}
                                >
                                    {tab.nhan}
                                </button>
                            ))}
                        </div>

                        <div className="sort-box">
                            <select
                                value={sapXep}
                                onChange={(e) => setSapXep(e.target.value)}
                                className="sort-select"
                            >
                                <option value="new">Mới nhất</option>
                                <option value="hot">Nổi bật</option>
                                <option value="price_asc">Giá: Thấp đến Cao</option>
                                <option value="price_desc">Giá: Cao đến Thấp</option>
                            </select>
                        </div>
                    </div>

                    {layBoLocTieuMuc().length > 0 && (
                        <div className="sub-filter-tabs" style={{ display: 'flex', gap: '10px', marginBottom: '20px', overflowX: 'auto', paddingBottom: '10px' }}>
                            {layBoLocTieuMuc().map(sub => (
                                <button
                                    key={sub.id}
                                    className={`sub-tab ${tieuMuc === sub.id ? 'active' : ''}`}
                                    onClick={() => setTieuMuc(sub.id)}
                                >
                                    {sub.nhan}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </section>


            {/* Products Grid */}
            <section className="products-section section">
                <div className="container">
                    {loi && (
                        <div className="alert error" style={{ color: 'red', textAlign: 'center', margin: '20px 0' }}>
                            {loi}
                        </div>
                    )}
                    {dangTai ? (
                        <div className="loading" style={{ textAlign: 'center', padding: '50px', fontSize: '20px' }}>Đang tải bộ sưu tập mới nhất...</div>
                    ) : (
                        <div className="products-grid">
                            {danhSachSanPham.length > 0 ? danhSachSanPham.map((sp, idx) => (
                                <The
                                    key={sp.id}
                                    className="product-card"
                                >
                                    <div className="product-image" onClick={() => navigate(`/san-pham/${sp.id}`)} style={{ cursor: 'pointer' }}>
                                        <img src={layUrlHinhAnh(sp.image_url)} alt={sp.name}
                                            onError={(e) => e.target.src = 'https://placehold.co/400x600/e5e5e5/333?text=IVIE+Product'} />
                                        {sp.is_new && <div className="product-badge">NEW</div>}
                                        {sp.is_hot && <div className="product-badge hot">HOT</div>}
                                    </div>
                                    <div className="product-info">
                                        <div className="product-header">
                                            <h3 className="product-name" onClick={() => navigate(`/san-pham/${sp.id}`)} style={{ cursor: 'pointer' }}>{sp.name}</h3>
                                            <span className="product-code">#{sp.code}</span>
                                        </div>

                                        <div className="product-pricing">
                                            <div className="price-row">
                                                <span className="price-label">Thuê ngày:</span>
                                                <span className="price-value">{dinhDangGia(sp.rental_price_day)}</span>
                                            </div>
                                            <div className="price-row">
                                                <span className="price-label">Mua:</span>
                                                <span className="price-value highlight">{dinhDangGia(sp.purchase_price)}</span>
                                            </div>
                                        </div>

                                        <div className="product-actions">
                                            <NutBam
                                                variant="outline"
                                                onClick={() => addToCart(sp)}
                                            >
                                                THÊM GIỎ
                                            </NutBam>
                                            <NutBam
                                                variant="primary"
                                                onClick={() => buyNow(sp)}
                                            >
                                                MUA NGAY
                                            </NutBam>
                                        </div>
                                    </div>
                                </The>
                            )) : (
                                <div className="no-products">
                                    <p>Không tìm thấy sản phẩm nào trong danh mục này.</p>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default SanPham;
