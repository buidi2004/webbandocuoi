import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { sanPhamAPI, layUrlHinhAnh } from '../api/khach_hang';
import NutBam from '../thanh_phan/NutBam';
import The from '../thanh_phan/The';
import { useToast } from '../thanh_phan/Toast';
import '../styles/product_detail.css';

const ChiTietSanPham = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { addToast } = useToast();
    const [sanPham, setSanPham] = useState(null);
    const [dangTai, setDangTai] = useState(true);
    const [soNgayThue, setSoNgayThue] = useState(1);
    const [goiYNam, setGoiYNam] = useState([]);

    // Review states
    const [danhGia, setDanhGia] = useState([]);
    const [tenNguoiDung, setTenNguoiDung] = useState('');
    const [soSao, setSoSao] = useState(5);
    const [binhLuan, setBinhLuan] = useState('');
    const [hinhAnh, setHinhAnh] = useState(null); // New state for image file
    const [previewUrl, setPreviewUrl] = useState(''); // Preview for UI
    const [dangGuiDanhGia, setDangGuiDanhGia] = useState(false);

    useEffect(() => {
        const layDuLieu = async () => {
            setDangTai(true);
            try {
                const res = await sanPhamAPI.layTheoId(id);
                setSanPham(res.data);

                const resGoiY = await sanPhamAPI.layTatCa({ gioi_tinh: 'male' });
                if (resGoiY.data) setGoiYNam(resGoiY.data.slice(0, 4));

                const resDanhGia = await sanPhamAPI.layDanhGia(id);
                if (resDanhGia.data) setDanhGia(resDanhGia.data);

            } catch (err) {
                console.error("Lỗi tải chi tiết sản phẩm:", err);
                addToast({ message: "Không tìm thấy sản phẩm", type: "error" });
                navigate('/san-pham');
            } finally {
                setDangTai(false);
            }
        };
        layDuLieu();
        window.scrollTo(0, 0);
    }, [id]);

    const handleHinhAnhChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setHinhAnh(file);
            setPreviewUrl(URL.createObjectURL(file));
        }
    };

    const handleGuiDanhGia = async (e) => {
        e.preventDefault();
        if (!tenNguoiDung || !binhLuan) {
            addToast({ message: "Vui lòng nhập tên và nhận xét", type: "info" });
            return;
        }

        setDangGuiDanhGia(true);
        try {
            const formData = new FormData();
            formData.append('user_name', tenNguoiDung);
            formData.append('rating', soSao);
            formData.append('comment', binhLuan);
            if (hinhAnh) {
                formData.append('image', hinhAnh);
            }

            const res = await sanPhamAPI.guiDanhGia(id, formData);
            if (res.data) {
                setBinhLuan('');
                setTenNguoiDung('');
                setHinhAnh(null);
                setPreviewUrl('');

                addToast({
                    message: "Đánh giá đã được gửi! Vui lòng chờ Admin duyệt để hiển thị.",
                    type: "success"
                });
            }
        } catch (error) {
            const errorMsg = error.response?.data?.detail || "Lỗi khi gửi đánh giá";
            addToast({ message: `Lỗi: ${errorMsg}`, type: "error" });
        } finally {
            setDangGuiDanhGia(false);
        }
    };

    const dinhDangGia = (gia) => {
        return new Intl.NumberFormat('vi-VN').format(gia) + 'đ';
    };

    const addToCart = (buyNow = false) => {
        const currentCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        const existingItemIndex = currentCart.findIndex(item => item.id === sanPham.id && item.rental_days === (buyNow ? 0 : soNgayThue));

        const itemToAdd = {
            ...sanPham,
            rental_days: buyNow ? 0 : soNgayThue,
            quantity: 1,
            price_to_use: buyNow ? sanPham.purchase_price : (sanPham.rental_price_day * soNgayThue)
        };

        if (existingItemIndex > -1) {
            currentCart[existingItemIndex].quantity += 1;
        } else {
            currentCart.push(itemToAdd);
        }

        localStorage.setItem('ivie_cart', JSON.stringify(currentCart));

        if (buyNow) navigate('/gio-hang');
        else addToast({ message: 'Đã thêm vào giỏ hàng!', type: 'success' });
    };

    if (dangTai) return <div className="loading" style={{ textAlign: 'center', padding: '100px' }}>Đang tải sản phẩm cao cấp...</div>;
    if (!sanPham) return null;

    // Lấy danh sách ảnh: ưu tiên gallery_images, fallback về image_url
    const gallery = Array.isArray(sanPham.gallery_images) && sanPham.gallery_images.length > 0
        ? sanPham.gallery_images
        : [sanPham.image_url];
    const [galleryIndex, setGalleryIndex] = useState(0);

    return (
        <div className="product-detail-page">
            <div className="container">
                <div className="product-detail-container">
                    <div className="product-detail-gallery">
                        <div className="product-detail-image-wrapper" style={{position:'relative'}}>
                            <img
                                src={layUrlHinhAnh(gallery[galleryIndex])}
                                alt={sanPham.name}
                                onError={(e) => e.target.src = 'https://placehold.co/600x800?text=IVIE+Studio'}
                                style={{maxHeight:'520px',objectFit:'contain',background:'#f9f9f9'}}
                            />
                            {gallery.length > 1 && (
                                <>
                                    <button
                                        style={{position:'absolute',left:10,top:'50%',transform:'translateY(-50%)',background:'#fff',border:'1px solid #eee',borderRadius:8,padding:'6px 10px',cursor:'pointer',zIndex:2}}
                                        onClick={()=>setGalleryIndex(i=>i===0?gallery.length-1:i-1)}
                                        aria-label="Ảnh trước"
                                    >&#8592;</button>
                                    <button
                                        style={{position:'absolute',right:10,top:'50%',transform:'translateY(-50%)',background:'#fff',border:'1px solid #eee',borderRadius:8,padding:'6px 10px',cursor:'pointer',zIndex:2}}
                                        onClick={()=>setGalleryIndex(i=>(i+1)%gallery.length)}
                                        aria-label="Ảnh sau"
                                    >&#8594;</button>
                                </>
                            )}
                        </div>
                        {gallery.length > 1 && (
                            <div style={{display:'flex',gap:10,marginTop:14,justifyContent:'center'}}>
                                {gallery.map((img,idx)=>(
                                    <div 
                                        key={img+idx}
                                        style={{position:'relative',cursor:'pointer'}}
                                        onClick={()=>setGalleryIndex(idx)}
                                    >
                                        <img
                                            src={layUrlHinhAnh(img)}
                                            alt={`thumb-${idx+1}`}
                                            style={{width:60,height:60,objectFit:'cover',borderRadius:8,border:galleryIndex===idx?'2.5px solid #b59410':'1.5px solid #eee',boxShadow:galleryIndex===idx?'0 2px 8px #b5941033':'none',background:'#fff'}}
                                        />
                                        <div style={{
                                            position:'absolute',
                                            bottom:'4px',
                                            left:'50%',
                                            transform:'translateX(-50%)',
                                            background:'rgba(0,0,0,0.75)',
                                            color:'white',
                                            padding:'2px 6px',
                                            borderRadius:'8px',
                                            fontSize:'0.65rem',
                                            fontWeight:'600',
                                            pointerEvents:'none',
                                            whiteSpace:'nowrap'
                                        }}>
                                            Mẫu {idx+1}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="product-detail-info">
                        <span className="product-detail-category">
                            {sanPham.category === 'wedding_modern' ? 'Váy Cưới Hiện Đại' :
                                sanPham.category === 'traditional' ? 'Áo Dài Truyền Thống' : 'Phụ Kiện'}
                        </span>
                        <h1 className="product-detail-name">{sanPham.name}</h1>
                        <span className="product-detail-code">Sản phẩm thủ công độc quyền • Mã #{sanPham.code}</span>

                        <div className="product-detail-price-box">
                            <div className="price-item"><span className="price-label">Giá thuê (Ưu đãi ngày):</span><span className="price-value">{dinhDangGia(sanPham.rental_price_day)}</span></div>
                            <div className="price-item"><span className="price-label">Sở hữu vĩnh viễn:</span><span className="price-value highlight">{dinhDangGia(sanPham.purchase_price)}</span></div>
                        </div>

                        <div className="product-attributes">
                            <div className="attribute-card"><span className="attribute-label">Chất liệu cao cấp</span><span className="attribute-value">{sanPham.fabric_type || 'Ren Pháp & Lụa tơ tằm'}</span></div>
                            <div className="attribute-card"><span className="attribute-label">Sắc màu chủ đạo</span><span className="attribute-value">{sanPham.color || 'Trắng Ivory / Ngọc trai'}</span></div>
                            <div className="attribute-card"><span className="attribute-label">Form dáng gợi ý</span><span className="attribute-value">{sanPham.recommended_size || 'Cao: 1m55-1m75 | Nặng: 45-65kg'}</span></div>
                            <div className="attribute-card"><span className="attribute-label">Phong cách Makeup</span><span className="attribute-value">{sanPham.makeup_tone || 'Tone Tây sang trọng / Hàn Quốc'}</span></div>
                        </div>

                        <div className="product-description" style={{ marginBottom: '40px', color: '#666', lineHeight: '1.8', fontSize: '1.1rem' }}>
                            <h4 style={{ color: '#1a1a1a', marginBottom: '15px', fontWeight: '600' }}>Chi tiết tuyệt phẩm</h4>
                            <p>{sanPham.description || "Mẫu thiết kế tinh xảo đến từng đường kim mũi chỉ, sử dụng những chất liệu tốt nhất để tôn vinh vẻ đẹp kiêu sa của bạn trong ngày trọng đại nhất cuộc đời."}</p>
                        </div>

                        <div className="rental-options">
                            <h4>Thời gian trải nghiệm ({soNgayThue} ngày)</h4>
                            <div className="days-selector">
                                {[1, 2, 3, 4, 5, 6, 7].map(day => (
                                    <button key={day} className={`day-btn ${soNgayThue === day ? 'active' : ''}`} onClick={() => setSoNgayThue(day)}>{day}</button>
                                ))}
                            </div>
                        </div>

                        <div className="product-detail-actions">
                            <button
                                onClick={() => {
                                    addToCart(false);
                                    navigate('/gio-hang');
                                }}
                                style={{ 
                                    padding: '18px', 
                                    fontSize: '1rem', 
                                    backgroundColor: '#b59410',
                                    color: '#ffffff',
                                    width: '100%',
                                    display: 'block',
                                    border: 'none',
                                    borderRadius: '50px',
                                    fontWeight: '600',
                                    cursor: 'pointer',
                                    textTransform: 'uppercase',
                                    letterSpacing: '1px',
                                    transition: 'all 0.3s ease',
                                    marginBottom: '15px'
                                }}
                                className="btn btn-thue-ngay"
                            >
                                THUÊ NGAY
                            </button>
                            <NutBam
                                variant="primary"
                                className="btn-rent-now"
                                onClick={() => {
                                    addToCart(false);
                                    navigate('/gio-hang');
                                }}
                                style={{ padding: '20px', fontSize: '1.1rem' }}
                            >
                                ĐẶT THUÊ NGAY • {dinhDangGia(sanPham.rental_price_day * soNgayThue)}
                            </NutBam>
                            <NutBam
                                variant="outline"
                                onClick={() => addToCart(false)}
                                style={{ padding: '18px', borderColor: '#1a1a1a', color: '#1a1a1a' }}
                            >
                                THÊM GIỎ HÀNG
                            </NutBam>
                            <NutBam
                                variant="outline"
                                onClick={() => addToCart(true)}
                                style={{ padding: '18px', borderColor: '#1a1a1a', color: '#1a1a1a' }}
                            >
                                MUA SỞ HỮU
                            </NutBam>
                        </div>
                    </div>
                </div>

                {goiYNam.length > 0 && (
                    <section className="recommendations-section">
                        <div className="section-header"><h2>Kết Hợp Hoàn Hảo</h2><p>Đề xuất các mẫu Vest nam phù hợp để sánh đôi cùng nàng</p></div>
                        <div className="recommendations-grid">
                            {goiYNam.map(sp => (
                                <The key={sp.id} className="product-card" style={{ background: '#fff', border: '1px solid #eee' }}>
                                    <div className="product-image" onClick={() => navigate(`/san-pham/${sp.id}`)} style={{ cursor: 'pointer' }}><img src={layUrlHinhAnh(sp.image_url)} alt={sp.name} /></div>
                                    <div className="product-info" style={{ padding: '15px' }}><h4 style={{ fontSize: '1rem', margin: '0 0 5px 0' }}>{sp.name}</h4><p style={{ color: '#b59410', fontWeight: 'bold', margin: 0 }}>{dinhDangGia(sp.rental_price_day)}</p></div>
                                </The>
                            ))}
                        </div>
                    </section>
                )}

                <section className="reviews-section">
                    <div className="reviews-container">
                        <div className="section-header"><h2>Cảm Nhận Khách Hàng</h2><p>Chia sẻ trải nghiệm tuyệt vời của bạn cùng IVIE STUDIO</p></div>

                        <form className="review-form" onSubmit={handleGuiDanhGia}>
                            <h3>Gửi đánh giá của bạn</h3>
                            <div className="rating-input">
                                {[1, 2, 3, 4, 5].map(star => (
                                    <button key={star} type="button" className={`star-btn ${soSao >= star ? 'active' : ''}`} onClick={() => setSoSao(star)}>★</button>
                                ))}
                            </div>
                            <div className="form-group">
                                <label>Tên của bạn</label>
                                <input type="text" value={tenNguoiDung} onChange={(e) => setTenNguoiDung(e.target.value)} placeholder="Nhập tên..." required />
                            </div>
                            <div className="form-group">
                                <label>Nhận xét về sản phẩm</label>
                                <textarea rows="4" value={binhLuan} onChange={(e) => setBinhLuan(e.target.value)} placeholder="Chia sẻ cảm nhận của bạn về chất liệu, form dáng..." required></textarea>
                            </div>

                            {/* New Image Upload */}
                            <div className="form-group">
                                <label>Hình ảnh thực tế (không bắt buộc)</label>
                                <input type="file" accept="image/*" onChange={handleHinhAnhChange} />
                                {previewUrl && (
                                    <div className="image-preview" style={{ marginTop: '10px' }}>
                                        <img src={previewUrl} alt="Preview" style={{ width: '100px', height: '100px', objectFit: 'cover', borderRadius: '8px' }} />
                                    </div>
                                )}
                            </div>

                            <NutBam variant="primary" type="submit" disabled={dangGuiDanhGia}>
                                {dangGuiDanhGia ? 'ĐANG GỬI...' : 'GỬI ĐÁNH GIÁ'}
                            </NutBam>
                        </form>

                        <div className="review-list">
                            {danhGia.length > 0 ? danhGia.map(dg => (
                                <div key={dg.id} className="review-card">
                                    <div className="review-header">
                                        <span className="reviewer-name">{dg.user_name}</span>
                                        <div className="review-stars">{[...Array(dg.rating)].map((_, i) => <span key={i}>★</span>)}</div>
                                    </div>
                                    <p className="review-comment">{dg.comment}</p>

                                    {/* Display Review Image */}
                                    {dg.image_url && (
                                        <div className="review-image" style={{ marginTop: '15px' }}>
                                            <img src={layUrlHinhAnh(dg.image_url)} alt="Review" style={{ maxWidth: '200px', borderRadius: '12px', boxShadow: '0 5px 15px rgba(0,0,0,0.1)' }} />
                                        </div>
                                    )}

                                    <span className="review-date">{new Date(dg.created_at).toLocaleDateString('vi-VN')}</span>
                                </div>
                            )) : (
                                <p style={{ textAlign: 'center', color: '#999' }}>Chưa có đánh giá nào cho sản phẩm này. Hãy là người đầu tiên!</p>
                            )}
                        </div>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default ChiTietSanPham;
