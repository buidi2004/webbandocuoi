import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api, { layUrlHinhAnh } from '../api/khach_hang';
import '../styles/wishlist.css';

const YeuThich = () => {
    const [items, setItems] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            setUser(JSON.parse(userData));
        }
    }, []);

    useEffect(() => {
        if (user) {
            layDanhSach();
        } else {
            setDangTai(false);
        }
    }, [user]);

    const layDanhSach = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await api.get(`/api/yeu_thich/?token=${token}`);
            setItems(res.data);
        } catch (error) {
            console.error('Lỗi tải danh sách yêu thích:', error);
        } finally {
            setDangTai(false);
        }
    };

    const xoaKhoiYeuThich = async (productId) => {
        try {
            const token = localStorage.getItem('token');
            await api.delete(`/api/yeu_thich/xoa/${productId}?token=${token}`);
            setItems(items.filter(item => item.product_id !== productId));
        } catch (error) {
            console.error('Lỗi xóa:', error);
        }
    };

    const dinhDangGia = (gia) => {
        return new Intl.NumberFormat('vi-VN').format(gia) + 'đ';
    };

    if (!user) {
        return (
            <div className="wishlist-page">
                <section className="wishlist-hero">
                    <div className="container">
                        <h1 className="page-title" data-sal="slide-up">Sản Phẩm Yêu Thích</h1>
                    </div>
                </section>
                <div className="container">
                    <div className="empty-wishlist">
                        <span className="heart-icon">❤️</span>
                        <h2>Vui lòng đăng nhập</h2>
                        <p>Đăng nhập để xem và quản lý sản phẩm yêu thích của bạn</p>
                        <Link to="/dang-nhap" className="btn-primary">Đăng nhập ngay</Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="wishlist-page">
            <section className="wishlist-hero">
                <div className="container">
                    <h1 className="page-title" data-sal="slide-up">Sản Phẩm Yêu Thích</h1>
                    <p className="page-subtitle" data-sal="slide-up" data-sal-delay="100">
                        {items.length} sản phẩm trong danh sách
                    </p>
                </div>
            </section>

            <section className="wishlist-content">
                <div className="container">
                    {dangTai ? (
                        <div className="loading">Đang tải...</div>
                    ) : items.length === 0 ? (
                        <div className="empty-wishlist" data-sal="fade">
                            <span className="heart-icon">💔</span>
                            <h2>Danh sách trống</h2>
                            <p>Hãy khám phá và thêm sản phẩm yêu thích của bạn</p>
                            <Link to="/san-pham" className="btn-primary">Khám phá ngay</Link>
                        </div>
                    ) : (
                        <div className="wishlist-grid" data-sal="fade" data-sal-delay="200">
                            {items.map((item, index) => (
                                <div
                                    key={item.id}
                                    className="wishlist-card"
                                    data-sal="slide-up"
                                    data-sal-delay={index * 100}
                                >
                                    <Link to={`/san-pham/${item.product_id}`} className="card-image">
                                        <img
                                            src={layUrlHinhAnh(item.product_image)}
                                            alt={item.product_name}
                                            onError={(e) => e.target.src = 'https://placehold.co/300x400/111/fff?text=IVIE'}
                                        />
                                    </Link>
                                    <div className="card-info">
                                        <h3 className="card-name">
                                            <Link to={`/san-pham/${item.product_id}`}>{item.product_name}</Link>
                                        </h3>
                                        <p className="card-price">{item.product_price ? dinhDangGia(item.product_price) : ''}</p>
                                        <div className="card-actions">
                                            <Link to={`/san-pham/${item.product_id}`} className="btn-view">Xem chi tiết</Link>
                                            <button
                                                className="btn-remove"
                                                onClick={() => xoaKhoiYeuThich(item.product_id)}
                                            >
                                                🗑️
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default YeuThich;
