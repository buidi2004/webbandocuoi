import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { laySanPhamLienQuan, layUrlHinhAnh } from '../api/khach_hang';
import './RelatedProducts.css';

const RelatedProducts = ({ productId }) => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchRelated = async () => {
            if (!productId) return;
            
            setLoading(true);
            setError(null);
            
            try {
                const data = await laySanPhamLienQuan(productId);
                setProducts(data || []);
            } catch (err) {
                console.error('Error fetching related products:', err);
                setError('Không thể tải sản phẩm liên quan');
            } finally {
                setLoading(false);
            }
        };

        fetchRelated();
    }, [productId]);

    const handleProductClick = (id) => {
        navigate(`/san-pham/${id}`);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    const formatPrice = (price) => {
        if (!price) return '0đ';
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ';
    };

    // Không hiển thị nếu không có sản phẩm
    if (!loading && products.length === 0) return null;

    return (
        <section className="related-products">
            <h3 className="related-title">Sản phẩm liên quan</h3>
            
            {loading ? (
                <div className="related-loading">
                    <div className="loading-spinner"></div>
                    <span>Đang tải...</span>
                </div>
            ) : error ? (
                <div className="related-error">{error}</div>
            ) : (
                <div className="related-grid">
                    {products.map((product) => (
                        <div 
                            key={product.id}
                            className="related-card"
                            onClick={() => handleProductClick(product.id)}
                        >
                            <div className="related-image">
                                <img 
                                    src={layUrlHinhAnh(product.hinh_anh || product.image_url)}
                                    alt={product.ten || product.name}
                                    loading="lazy"
                                    onError={(e) => {
                                        e.target.src = 'https://placehold.co/300x400/f5f5f5/333?text=IVIE';
                                    }}
                                />
                                {product.la_hot && (
                                    <span className="related-badge hot">Hot</span>
                                )}
                                {product.la_moi && (
                                    <span className="related-badge new">Mới</span>
                                )}
                            </div>
                            <div className="related-info">
                                <h4 className="related-name">{product.ten || product.name}</h4>
                                <p className="related-price">
                                    {formatPrice(product.gia_thue_ngay || product.rental_price_day)}
                                    <span>/ngày</span>
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </section>
    );
};

export default RelatedProducts;
