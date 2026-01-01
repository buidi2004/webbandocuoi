import { Link } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import './Footer.css';

const ChanTrang = () => {
    const footerRef = useRef(null);
    const [isVisible, setIsVisible] = useState(false);
    
    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                }
            },
            { threshold: 0.2 }
        );
        
        if (footerRef.current) {
            observer.observe(footerRef.current);
        }
        
        return () => observer.disconnect();
    }, []);
    
    return (
        <footer ref={footerRef} className="footer-wrapper">
            {/* Cành mai trái - góc dưới trái */}
            <img 
                src="/images/canh-mai-trai.png" 
                alt="Cành mai trái"
                className={`canh-mai canh-mai-trai ${isVisible ? 'visible' : ''}`}
            />
            
            {/* Cành mai phải - góc dưới phải */}
            <img 
                src="/images/canh-mai-phai.png" 
                alt="Cành mai phải"
                className={`canh-mai canh-mai-phai ${isVisible ? 'visible' : ''}`}
            />
            
            {/* Nội dung chính - căn giữa bằng Flexbox */}
            <div className="footer-center">
                {/* Logo */}
                <h2 className="footer-logo">IVIE</h2>
                
                {/* Slogan */}
                <p className="footer-slogan">Lưu giữ khoảnh khắc hạnh phúc của bạn</p>
                
                {/* Menu Links */}
                <nav className="footer-nav">
                    <Link to="/chinh-sach">Chính sách bảo mật</Link>
                    <span className="nav-divider">|</span>
                    <Link to="/chinh-sach">Quy định đặt cọc</Link>
                    <span className="nav-divider">|</span>
                    <Link to="/lien-he">Liên hệ</Link>
                </nav>
                
                {/* Social Icons */}
                <div className="footer-social">
                    <a href="https://www.facebook.com/di.di.717541" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                        </svg>
                    </a>
                    <a href="https://zalo.me/0793919384" target="_blank" rel="noopener noreferrer" aria-label="Zalo">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2C6.48 2 2 5.58 2 10c0 2.29 1.12 4.33 2.88 5.64L2 22l6.36-2.88C9.67 20.88 11.71 22 14 22c5.42 0 10-3.58 10-8S17.42 2 12 2zm0 16c-1.38 0-2.68-.35-3.82-.97l-.24-.14-2.54.55.55-2.54-.14-.24C5.35 14.68 5 13.38 5 12c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7z" />
                        </svg>
                    </a>
                    <a href="tel:0793919384" aria-label="Phone">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" />
                        </svg>
                    </a>
                </div>
                
                {/* Copyright */}
                <p className="footer-copyright">&copy; 2024 IVIE Wedding Studio. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default ChanTrang;
