import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { layUrlHinhAnh, donHangAPI, sanPhamAPI } from '../api/khach_hang';
import '../styles/cart.css';

// Component hiển thị item trong giỏ hàng
const CartItem = ({ item, onRemove, onUpdateQuantity, formatPrice }) => {
    const [showComboDetails, setShowComboDetails] = useState(false);
    const [comboImages, setComboImages] = useState({ vay: [], vest: [] });
    const [loadingImages, setLoadingImages] = useState(false);

    // Load hình ảnh cho các item trong combo
    useEffect(() => {
        if (item.is_combo && showComboDetails && item.selected_items) {
            loadComboImages();
        }
    }, [showComboDetails, item.is_combo]);

    const loadComboImages = async () => {
        setLoadingImages(true);
        try {
            const vayIds = item.selected_items.vay?.map(v => v.id) || [];
            const vestIds = item.selected_items.vest?.map(v => v.id) || [];
            
            const vayPromises = vayIds.map(id => sanPhamAPI.layTheoId(id).catch(() => null));
            const vestPromises = vestIds.map(id => sanPhamAPI.layTheoId(id).catch(() => null));
            
            const [vayResults, vestResults] = await Promise.all([
                Promise.all(vayPromises),
                Promise.all(vestPromises)
            ]);
            
            setComboImages({
                vay: vayResults.filter(r => r).map(r => r.data),
                vest: vestResults.filter(r => r).map(r => r.data)
            });
        } catch (error) {
            console.error('Lỗi tải hình combo:', error);
        } finally {
            setLoadingImages(false);
        }
    };

    // Nếu là combo
    if (item.is_combo) {
        return (
            <div className="cart-item-tgdd combo-item">
                <div 
                    className="combo-image-wrapper"
                    onClick={() => setShowComboDetails(!showComboDetails)}
                    style={{ cursor: 'pointer' }}
                >
                    <img 
                        src={layUrlHinhAnh(item.image_url)} 
                        alt={item.name} 
                        onError={(e) => e.target.src = 'https://placehold.co/80x100/f5f5f5/333?text=IVIE'} 
                    />
                    <div className="combo-badge">GÓI COMBO</div>
                </div>
                <div className="item-info">
                    <h3>{item.name}</h3>
                    <p className="item-variant combo-summary">
                        📦 Trọn gói: {item.selected_items?.vay?.length || 0} váy + {item.selected_items?.vest?.length || 0} vest
                    </p>
                    <p className="combo-included-note">✓ Tất cả sản phẩm đã bao gồm trong giá combo</p>
                    <button 
                        className="btn-view-combo-details"
                        onClick={() => setShowComboDetails(!showComboDetails)}
                    >
                        {showComboDetails ? '▲ Thu gọn' : '▼ Xem chi tiết sản phẩm đã chọn'}
                    </button>
                    
                    {/* Chi tiết combo */}
                    {showComboDetails && (
                        <div className="combo-details">
                            {loadingImages ? (
                                <p style={{ fontSize: '13px', color: '#999' }}>Đang tải...</p>
                            ) : (
                                <>
                                    {item.selected_items?.vay?.length > 0 && (
                                        <div className="combo-section">
                                            <h4>👗 Váy cưới đã chọn ({item.selected_items.vay.length}):</h4>
                                            <div className="combo-items-grid">
                                                {(comboImages.vay.length > 0 ? comboImages.vay : item.selected_items.vay).map((vay, idx) => (
                                                    <div key={vay.id || idx} className="combo-mini-item">
                                                        <img 
                                                            src={layUrlHinhAnh(vay.image_url)} 
                                                            alt={vay.name}
                                                            onError={(e) => e.target.src = 'https://placehold.co/60x80/f5f5f5/333?text=IVIE'}
                                                        />
                                                        <span>{vay.name}</span>
                                                        <span className="included-tag">Đã bao gồm</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                    
                                    {item.selected_items?.vest?.length > 0 && (
                                        <div className="combo-section">
                                            <h4>🤵 Vest nam đã chọn ({item.selected_items.vest.length}):</h4>
                                            <div className="combo-items-grid">
                                                {(comboImages.vest.length > 0 ? comboImages.vest : item.selected_items.vest).map((vest, idx) => (
                                                    <div key={vest.id || idx} className="combo-mini-item">
                                                        <img 
                                                            src={layUrlHinhAnh(vest.image_url)} 
                                                            alt={vest.name}
                                                            onError={(e) => e.target.src = 'https://placehold.co/60x80/f5f5f5/333?text=IVIE'}
                                                        />
                                                        <span>{vest.name}</span>
                                                        <span className="included-tag">Đã bao gồm</span>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </>
                            )}
                        </div>
                    )}
                </div>
                <div className="item-price combo-price">
                    <span className="price-label">Giá trọn gói</span>
                    {formatPrice(item.price_to_use || item.purchase_price || item.rental_price_day)}
                </div>
                <div className="item-actions">
                    <button className="btn-remove" onClick={() => onRemove(item.id, item.loai)}>Xoá</button>
                </div>
            </div>
        );
    }

    // Nếu là sản phẩm thường
    return (
        <div className="cart-item-tgdd">
            <Link to={`/san-pham/${item.id}`} className="item-image-link">
                <img 
                    src={layUrlHinhAnh(item.image_url)} 
                    alt={item.name} 
                    onError={(e) => e.target.src = 'https://placehold.co/80x100/f5f5f5/333?text=IVIE'} 
                />
            </Link>
            <div className="item-info">
                <h3>{item.name}</h3>
                <p className="item-variant">
                    {item.loai === 'thue' ? `Thuê ${item.rental_days} ngày` : 'Mua'}
                </p>
                {item.so_luong && item.so_luong <= 3 && (
                    <p className="item-stock-warning">⚠️ Chỉ còn {item.so_luong} sản phẩm</p>
                )}
            </div>
            <div className="item-price">
                {formatPrice(item.price_to_use || item.purchase_price || item.rental_price_day)}
            </div>
            <div className="item-actions">
                <button className="btn-remove" onClick={() => onRemove(item.id, item.loai)}>Xoá</button>
                <div className="qty-control">
                    <button onClick={() => onUpdateQuantity(item.id, -1, item.loai)}>−</button>
                    <span>{item.quantity || 1}</span>
                    <button onClick={() => onUpdateQuantity(item.id, 1, item.loai)} disabled={(item.quantity || 1) >= (item.so_luong || 10)}>+</button>
                </div>
            </div>
        </div>
    );
};

const GioHang = () => {
    const [cartItems, setCartItems] = useState([]);
    const [deliveryType, setDeliveryType] = useState('delivery'); // delivery, pickup
    const [paymentMethod, setPaymentMethod] = useState('cod'); // cod, bank
    const [couponCode, setCouponCode] = useState('');
    const [showCoupon, setShowCoupon] = useState(false);
    const [agreedPolicy, setAgreedPolicy] = useState(false);
    const [customerInfo, setCustomerInfo] = useState({
        name: '',
        phone: '',
        email: '',
        address: '',
        weddingDate: ''
    });
    const [isSubmitted, setIsSubmitted] = useState(false);

    useEffect(() => {
        const savedCart = JSON.parse(localStorage.getItem('ivie_cart') || '[]');
        setCartItems(savedCart);
        // Load user info if logged in
        const user = JSON.parse(localStorage.getItem('ivie_user') || 'null');
        if (user) {
            setCustomerInfo({
                name: user.full_name || '',
                phone: user.phone || '',
                email: user.email || '',
                address: user.address || '',
                weddingDate: user.wedding_date || ''
            });
        }
    }, []);

    const updateQuantity = (id, delta, loai) => {
        const newCart = cartItems.map(item => {
            if (item.id === id && (item.loai || 'mua') === (loai || 'mua')) {
                const newQty = Math.max(1, (item.quantity || 1) + delta);
                const maxQty = item.so_luong || 10;
                return { ...item, quantity: Math.min(newQty, maxQty) };
            }
            return item;
        });
        setCartItems(newCart);
        localStorage.setItem('ivie_cart', JSON.stringify(newCart));
    };

    const removeItem = (id, loai) => {
        const newCart = cartItems.filter(item => !(item.id === id && (item.loai || 'mua') === (loai || 'mua')));
        setCartItems(newCart);
        localStorage.setItem('ivie_cart', JSON.stringify(newCart));
    };

    const formatPrice = (price) => new Intl.NumberFormat('vi-VN').format(price) + 'đ';

    const getTotal = () => {
        return cartItems.reduce((total, item) => {
            const price = item.price_to_use || item.rental_price_day || item.purchase_price;
            return total + (price * (item.quantity || 1));
        }, 0);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!agreedPolicy) {
            alert('Vui lòng đồng ý với chính sách xử lý dữ liệu');
            return;
        }
        if (!customerInfo.name || !customerInfo.phone || !customerInfo.address) {
            alert('Vui lòng điền đầy đủ thông tin nhận hàng');
            return;
        }
        
        try {
            // Lấy user_id nếu đã đăng nhập
            const user = JSON.parse(localStorage.getItem('ivie_user') || 'null');
            
            // Gửi đơn hàng lên API
            const orderData = {
                customer_name: customerInfo.name,
                customer_email: customerInfo.email || `${customerInfo.phone}@ivie.vn`,
                customer_phone: customerInfo.phone,
                shipping_address: customerInfo.address,
                total_amount: getTotal(),
                items: cartItems.map(item => ({
                    product_id: item.id,
                    quantity: item.quantity || 1,
                    price: item.price_to_use || item.purchase_price || item.rental_price_day,
                    loai: item.loai || 'mua',
                    rental_days: item.rental_days || 0
                })),
                payment_method: paymentMethod,
                delivery_type: deliveryType,
                note: `Hình thức: ${deliveryType === 'delivery' ? 'Giao tận nơi' : 'Nhận tại studio'} | Thanh toán: ${paymentMethod === 'cod' ? 'COD' : 'Chuyển khoản'}${customerInfo.weddingDate ? ` | Ngày cưới: ${customerInfo.weddingDate}` : ''}`,
                user_id: user?.id || null
            };
            
            await donHangAPI.tao(orderData);
            setIsSubmitted(true);
            localStorage.removeItem('ivie_cart');
            setCartItems([]);
        } catch (error) {
            console.error('Lỗi đặt hàng:', error);
            alert('Có lỗi xảy ra khi đặt hàng. Vui lòng thử lại!');
        }
    };

    if (isSubmitted) {
        return (
            <div className="cart-success">
                <div className="success-icon">🎉</div>
                <h2>Đặt Hàng Thành Công!</h2>
                <p>Cảm ơn bạn đã lựa chọn IVIE Studio.<br/>Chúng tôi sẽ liên hệ xác nhận trong 30 phút.</p>
                <Link to="/san-pham" className="btn-continue">Tiếp tục mua sắm</Link>
            </div>
        );
    }

    if (cartItems.length === 0) {
        return (
            <div className="cart-empty">
                <div className="empty-icon">🛒</div>
                <h2>Giỏ hàng trống</h2>
                <p>Bạn chưa có sản phẩm nào trong giỏ hàng</p>
                <Link to="/san-pham" className="btn-shop">Khám phá sản phẩm</Link>
            </div>
        );
    }

    return (
        <div className="cart-page-tgdd">
            <div className="cart-container">
                {/* Header */}
                <div className="cart-header">
                    <h1>Giỏ hàng <span>({cartItems.length} sản phẩm)</span></h1>
                </div>

                {/* Delivery Options */}
                <div className="delivery-options">
                    <label className={`delivery-option ${deliveryType === 'delivery' ? 'active' : ''}`}>
                        <input type="radio" name="delivery" checked={deliveryType === 'delivery'} onChange={() => setDeliveryType('delivery')} />
                        <span className="radio-custom"></span>
                        <span>Giao tận nơi</span>
                    </label>
                    <label className={`delivery-option ${deliveryType === 'pickup' ? 'active' : ''}`}>
                        <input type="radio" name="delivery" checked={deliveryType === 'pickup'} onChange={() => setDeliveryType('pickup')} />
                        <span className="radio-custom"></span>
                        <span>Nhận tại studio</span>
                    </label>
                </div>

                {/* Address Box */}
                {deliveryType === 'delivery' && (
                    <div className="address-box">
                        <div className="address-header">
                            <span className="address-icon">📍</span>
                            <span>Vui lòng cung cấp thông tin nhận hàng</span>
                        </div>
                        <div className="address-form">
                            <div className="form-row">
                                <input type="text" placeholder="Họ và tên *" value={customerInfo.name} onChange={e => setCustomerInfo({...customerInfo, name: e.target.value})} required />
                                <input type="tel" placeholder="Số điện thoại *" value={customerInfo.phone} onChange={e => setCustomerInfo({...customerInfo, phone: e.target.value})} required />
                            </div>
                            <input type="text" placeholder="Địa chỉ nhận hàng *" value={customerInfo.address} onChange={e => setCustomerInfo({...customerInfo, address: e.target.value})} required />
                            <input type="date" placeholder="Ngày cưới dự kiến" value={customerInfo.weddingDate || ''} onChange={e => setCustomerInfo({...customerInfo, weddingDate: e.target.value})} style={{marginTop: '10px'}} />
                        </div>
                    </div>
                )}

                {/* Cart Items */}
                <div className="cart-items-list">
                    {cartItems.map(item => (
                        <CartItem 
                            key={`${item.id}-${item.loai || 'mua'}`}
                            item={item}
                            onRemove={removeItem}
                            onUpdateQuantity={updateQuantity}
                            formatPrice={formatPrice}
                        />
                    ))}
                </div>

                {/* Subtotal */}
                <div className="cart-subtotal">
                    <span>Tạm tính ({cartItems.length} sản phẩm):</span>
                    <span className="subtotal-price">{formatPrice(getTotal())}</span>
                </div>

                {/* Shipping Info */}
                <div className="shipping-info-box">
                    <h4>Thông tin nhận hàng:</h4>
                    <div className="shipping-product">
                        <img src={layUrlHinhAnh(cartItems[0]?.image_url)} alt="" />
                        <div>
                            <p className="product-name">{cartItems[0]?.name}</p>
                            <p className="product-variant">{cartItems[0]?.loai === 'thue' ? `Thuê ${cartItems[0]?.rental_days} ngày` : 'Mua'} - SL: {cartItems.reduce((sum, i) => sum + (i.quantity || 1), 0)}</p>
                        </div>
                    </div>
                    <div className="shipping-time">
                        <span className="time-badge">Giao trước 12h, hôm nay ({new Date().getDate()}/{new Date().getMonth() + 1})</span>
                        <span className="fast-badge">⚡ Giao siêu nhanh</span>
                    </div>
                    <div className="shipping-fee">
                        <span>Phí giao hàng</span>
                        <span className="fee-free">Miễn phí</span>
                    </div>
                </div>

                {/* Coupon */}
                <div className="coupon-section">
                    <div className="coupon-toggle" onClick={() => setShowCoupon(!showCoupon)}>
                        <span>🏷️ Sử dụng mã giảm giá</span>
                        <span>{showCoupon ? '▲' : '▼'}</span>
                    </div>
                    {showCoupon && (
                        <div className="coupon-input">
                            <input type="text" placeholder="Nhập mã giảm giá" value={couponCode} onChange={e => setCouponCode(e.target.value)} />
                            <button>Áp dụng</button>
                        </div>
                    )}
                </div>

                {/* Total */}
                <div className="cart-total-box">
                    <div className="total-row">
                        <span>Tổng tiền</span>
                        <span className="total-price">{formatPrice(getTotal())}</span>
                    </div>
                </div>

                {/* Payment Methods */}
                <div className="payment-section">
                    <h4>Hình thức thanh toán</h4>
                    <label className={`payment-option ${paymentMethod === 'bank' ? 'active' : ''}`}>
                        <input type="radio" name="payment" checked={paymentMethod === 'bank'} onChange={() => setPaymentMethod('bank')} />
                        <span className="radio-custom"></span>
                        <span>💳 Chuyển khoản ngân hàng</span>
                    </label>
                    <label className={`payment-option ${paymentMethod === 'cod' ? 'active' : ''}`}>
                        <input type="radio" name="payment" checked={paymentMethod === 'cod'} onChange={() => setPaymentMethod('cod')} />
                        <span className="radio-custom"></span>
                        <span>💵 Thanh toán tiền mặt khi nhận hàng</span>
                    </label>
                </div>

                {/* Policy Agreement */}
                <div className="policy-section">
                    <label className="policy-checkbox">
                        <input type="checkbox" checked={agreedPolicy} onChange={e => setAgreedPolicy(e.target.checked)} />
                        <span className="checkbox-custom"></span>
                        <span>Tôi đồng ý với <a href="#">Chính sách xử lý dữ liệu cá nhân</a> của IVIE Studio</span>
                    </label>
                </div>

                {/* Submit Button */}
                <button className="btn-order" onClick={handleSubmit} disabled={!agreedPolicy}>
                    Đặt hàng
                </button>
            </div>
        </div>
    );
};

export default GioHang;
