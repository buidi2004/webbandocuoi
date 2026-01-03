import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api, { layUrlHinhAnh } from '../api/khach_hang';
import '../styles/blog.css';

const Blog = () => {
    const [baiViets, setBaiViets] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const [categoryFilter, setCategoryFilter] = useState('all');

    useEffect(() => {
        layBaiViet();
    }, [categoryFilter]);

    const layBaiViet = async () => {
        try {
            let url = '/api/blog/';
            if (categoryFilter !== 'all') {
                url += `?category=${categoryFilter}`;
            }
            const res = await api.get(url);
            setBaiViets(res.data);
        } catch (error) {
            console.error('Lỗi tải blog:', error);
        } finally {
            setDangTai(false);
        }
    };

    const categories = [
        { id: 'all', label: 'Tất cả' },
        { id: 'tips', label: '💡 Mẹo cưới' },
        { id: 'news', label: '📰 Tin tức' },
        { id: 'wedding-story', label: '💕 Câu chuyện cưới' }
    ];

    return (
        <div className="blog-page">
            <section className="blog-hero">
                <div className="container">
                    <h1 className="page-title" data-sal="slide-up" data-sal-delay="100">Blog & Tin Tức</h1>
                    <p className="page-subtitle" data-sal="slide-up" data-sal-delay="200">Mẹo hay, xu hướng cưới và câu chuyện đẹp</p>
                </div>
            </section>

            <section className="blog-content">
                <div className="container">
                    <div className="blog-filters" data-sal="fade" data-sal-delay="300">
                        {categories.map(cat => (
                            <button
                                key={cat.id}
                                className={`filter-btn ${categoryFilter === cat.id ? 'active' : ''}`}
                                onClick={() => setCategoryFilter(cat.id)}
                            >
                                {cat.label}
                            </button>
                        ))}
                    </div>

                    {dangTai ? (
                        <div className="loading">Đang tải bài viết...</div>
                    ) : baiViets.length === 0 ? (
                        <div className="no-posts">
                            <p>Chưa có bài viết nào.</p>
                        </div>
                    ) : (
                        <div className="blog-grid">
                            {baiViets.map(post => (
                                <article key={post.id} className="blog-card">
                                    <Link to={`/blog/${post.slug}`} className="blog-card-image">
                                        <img
                                            src={layUrlHinhAnh(post.image_url)}
                                            alt={post.title}
                                            onError={(e) => e.target.src = 'https://placehold.co/600x400/111/fff?text=Blog'}
                                        />
                                        <span className="blog-category">{post.category}</span>
                                    </Link>
                                    <div className="blog-card-content">
                                        <h2 className="blog-title">
                                            <Link to={`/blog/${post.slug}`}>{post.title}</Link>
                                        </h2>
                                        <p className="blog-excerpt">{post.excerpt}</p>
                                        <div className="blog-meta">
                                            <span className="blog-date">
                                                {new Date(post.created_at).toLocaleDateString('vi-VN')}
                                            </span>
                                            <span className="blog-views">👁️ {post.views} lượt xem</span>
                                        </div>
                                        <Link to={`/blog/${post.slug}`} className="read-more">
                                            Đọc tiếp →
                                        </Link>
                                    </div>
                                </article>
                            ))}
                        </div>
                    )}
                </div>
            </section>
        </div>
    );
};

export default Blog;
