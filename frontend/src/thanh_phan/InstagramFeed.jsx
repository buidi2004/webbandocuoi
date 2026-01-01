import { useState } from 'react';
import '../styles/instagram-feed.css';

const InstagramFeed = () => {
    // Dữ liệu mẫu Instagram posts (thay bằng API thực tế nếu có)
    const instaPosts = [
        { id: 1, image: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=300', likes: 234, comments: 18 },
        { id: 2, image: 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=300', likes: 189, comments: 12 },
        { id: 3, image: 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=300', likes: 312, comments: 24 },
        { id: 4, image: 'https://images.unsplash.com/photo-1522673607200-164d1b6ce486?w=300', likes: 156, comments: 9 },
        { id: 5, image: 'https://images.unsplash.com/photo-1591604466107-ec97de577aff?w=300', likes: 278, comments: 21 },
        { id: 6, image: 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=300', likes: 198, comments: 15 },
    ];

    return (
        <section className="instagram-feed-section">
            <div className="container">
                <div className="insta-header">
                    <div className="insta-logo">
                        <span className="insta-icon">📸</span>
                        <div>
                            <h3>@ivie.wedding.studio</h3>
                            <p>Theo dõi chúng tôi trên Instagram</p>
                        </div>
                    </div>
                    <a 
                        href="https://instagram.com/ivie.wedding.studio" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="insta-follow-btn"
                    >
                        Theo Dõi
                    </a>
                </div>

                <div className="insta-grid">
                    {instaPosts.map(post => (
                        <a 
                            key={post.id} 
                            href="https://instagram.com/ivie.wedding.studio"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="insta-post"
                        >
                            <img src={post.image} alt={`Instagram post ${post.id}`} />
                            <div className="insta-overlay">
                                <span>❤️ {post.likes}</span>
                                <span>💬 {post.comments}</span>
                            </div>
                        </a>
                    ))}
                </div>

                <div className="insta-cta">
                    <p>Xem thêm hình ảnh và video tại Instagram của chúng tôi</p>
                    <a 
                        href="https://instagram.com/ivie.wedding.studio" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="insta-view-more"
                    >
                        Xem Tất Cả →
                    </a>
                </div>
            </div>
        </section>
    );
};

export default InstagramFeed;
