import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api, { layUrlHinhAnh } from '../api/khach_hang';
import '../styles/blog.css';

const ChiTietBlog = () => {
    const { slug } = useParams();
    const [baiViet, setBaiViet] = useState(null);
    const [dangTai, setDangTai] = useState(true);

    useEffect(() => {
        layChiTiet();
    }, [slug]);

    const layChiTiet = async () => {
        try {
            const res = await api.get(`/api/blog/${slug}`);
            setBaiViet(res.data);
        } catch (error) {
            console.error('Lỗi tải bài viết:', error);
        } finally {
            setDangTai(false);
        }
    };

    if (dangTai) {
        return <div className="loading" style={{ padding: '100px', textAlign: 'center' }}>Đang tải bài viết...</div>;
    }

    if (!baiViet) {
        return (
            <div className="not-found" style={{ padding: '100px', textAlign: 'center' }}>
                <h2>Không tìm thấy bài viết</h2>
                <Link to="/blog">← Quay lại Blog</Link>
            </div>
        );
    }

    return (
        <div className="blog-detail-page">
            <article className="blog-article">
                <header className="article-header">
                    <div className="container">
                        <Link to="/blog" className="back-link">← Quay lại Blog</Link>
                        <span className="article-category">{baiViet.category}</span>
                        <h1 className="article-title">{baiViet.title}</h1>
                        <div className="article-meta">
                            <span>{new Date(baiViet.created_at).toLocaleDateString('vi-VN')}</span>
                            <span>•</span>
                            <span>👁️ {baiViet.views} lượt xem</span>
                        </div>
                    </div>
                </header>

                {baiViet.image_url && (
                    <div className="article-featured-image">
                        <img src={layUrlHinhAnh(baiViet.image_url)} alt={baiViet.title} />
                    </div>
                )}

                <div className="container">
                    <div className="article-content" dangerouslySetInnerHTML={{ __html: baiViet.content }} />
                </div>

                <footer className="article-footer">
                    <div className="container">
                        <div className="share-buttons">
                            <span>Chia sẻ:</span>
                            <button onClick={() => navigator.clipboard.writeText(window.location.href)}>
                                📋 Copy link
                            </button>
                        </div>
                    </div>
                </footer>
            </article>
        </div>
    );
};

export default ChiTietBlog;
