import { Link } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import './Footer.css';

// Component hạt vàng lấp lánh - 25 hạt như ban đầu
const HatVangLapLanh = ({ side }) => {
    const [particles, setParticles] = useState([]);
    
    useEffect(() => {
        const newParticles = [];
        for (let i = 0; i < 25; i++) {
            newParticles.push({
                id: i,
                x: Math.random() * 220,
                y: Math.random() * 120,
                size: Math.random() * 2 + 1,
                delay: Math.random() * 3,
                duration: Math.random() * 2 + 2
            });
        }
        setParticles(newParticles);
    }, []);
    
    return (
        <div 
            className="hat-vang-container"
            style={{
                position: 'absolute',
                [side]: 0,
                top: '50%',
                transform: `translateY(-50%) ${side === 'right' ? 'scaleX(-1)' : ''}`,
                width: '220px',
                height: '120px',
                pointerEvents: 'none',
                zIndex: 0
            }}
        >
            {particles.map(p => (
                <div
                    key={p.id}
                    className="hat-vang-lap-lanh"
                    style={{
                        position: 'absolute',
                        left: `${p.x}px`,
                        top: `${p.y}px`,
                        width: `${p.size}px`,
                        height: `${p.size}px`,
                        background: '#FFD700',
                        borderRadius: '50%',
                        animation: `twinkle ${p.duration}s ease-in-out ${p.delay}s infinite`
                    }}
                />
            ))}
        </div>
    );
};

// Component cành mai nằm ngang cho footer - slide từ 2 bên
const CanhMaiNgang = ({ side, isVisible }) => (
    <svg 
        width="220" 
        height="120" 
        viewBox="0 0 220 120"
        className={`canh-mai-footer ${side} ${isVisible ? 'visible' : ''}`}
        style={{
            position: 'absolute',
            [side]: 0,
            top: '50%',
            pointerEvents: 'none',
            zIndex: 1
        }}
    >
        {/* Cành chính nằm ngang */}
        <path 
            d="M0 70 Q50 65 100 55 Q150 45 200 30" 
            stroke="#4A3728" 
            strokeWidth="4" 
            fill="none"
        />
        {/* Cành phụ 1 */}
        <path 
            d="M60 62 Q80 45 100 35" 
            stroke="#4A3728" 
            strokeWidth="2.5" 
            fill="none"
        />
        {/* Cành phụ 2 */}
        <path 
            d="M120 50 Q140 35 165 25" 
            stroke="#4A3728" 
            strokeWidth="2" 
            fill="none"
        />
        {/* Cành phụ 3 - hướng xuống */}
        <path 
            d="M40 68 Q55 85 75 95" 
            stroke="#4A3728" 
            strokeWidth="2" 
            fill="none"
        />
        {/* Cành phụ 4 */}
        <path 
            d="M170 38 Q185 25 205 15" 
            stroke="#4A3728" 
            strokeWidth="1.5" 
            fill="none"
        />
        
        {/* Hoa mai 1 - lớn */}
        <g transform="translate(95, 32)">
            <circle cx="0" cy="-7" r="5" fill="#FFD700"/>
            <circle cx="6" cy="-2" r="5" fill="#FFD700"/>
            <circle cx="4" cy="5" r="5" fill="#FFD700"/>
            <circle cx="-4" cy="5" r="5" fill="#FFD700"/>
            <circle cx="-6" cy="-2" r="5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="3" fill="#FFA000"/>
        </g>
        
        {/* Hoa mai 2 */}
        <g transform="translate(160, 22)">
            <circle cx="0" cy="-6" r="4.5" fill="#FFD700"/>
            <circle cx="5" cy="-2" r="4.5" fill="#FFD700"/>
            <circle cx="3" cy="4" r="4.5" fill="#FFD700"/>
            <circle cx="-3" cy="4" r="4.5" fill="#FFD700"/>
            <circle cx="-5" cy="-2" r="4.5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2.5" fill="#FFA000"/>
        </g>
        
        {/* Hoa mai 3 */}
        <g transform="translate(200, 12)">
            <circle cx="0" cy="-5" r="4" fill="#FFD700"/>
            <circle cx="4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="3" cy="4" r="4" fill="#FFD700"/>
            <circle cx="-3" cy="4" r="4" fill="#FFD700"/>
            <circle cx="-4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2" fill="#FFA000"/>
        </g>
        
        {/* Hoa mai 4 - trên cành phụ xuống */}
        <g transform="translate(70, 92)">
            <circle cx="0" cy="-5" r="4" fill="#FFD700"/>
            <circle cx="4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="3" cy="4" r="4" fill="#FFD700"/>
            <circle cx="-3" cy="4" r="4" fill="#FFD700"/>
            <circle cx="-4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2" fill="#FFA000"/>
        </g>
        
        {/* Hoa mai 5 - nhỏ */}
        <g transform="translate(45, 60)">
            <circle cx="0" cy="-4" r="3.5" fill="#FFD700"/>
            <circle cx="3" cy="-1" r="3.5" fill="#FFD700"/>
            <circle cx="2" cy="3" r="3.5" fill="#FFD700"/>
            <circle cx="-2" cy="3" r="3.5" fill="#FFD700"/>
            <circle cx="-3" cy="-1" r="3.5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2" fill="#FFA000"/>
        </g>
        
        {/* Nụ mai */}
        <circle cx="130" cy="42" r="3" fill="#FFD700"/>
        <circle cx="180" cy="30" r="2.5" fill="#FFD700"/>
        <circle cx="55" cy="78" r="2.5" fill="#FFD700"/>
        <circle cx="25" cy="72" r="3" fill="#FFD700"/>
        
        {/* Đèn lồng đỏ */}
        <g transform="translate(115, 55)">
            {/* Dây treo */}
            <line x1="0" y1="-15" x2="0" y2="0" stroke="#8B0000" strokeWidth="1"/>
            {/* Thân đèn */}
            <ellipse cx="0" cy="8" rx="6" ry="10" fill="#DC143C"/>
            <ellipse cx="0" cy="8" rx="4" ry="8" fill="#FF4500" opacity="0.5"/>
            {/* Viền trên dưới */}
            <rect x="-5" y="-2" width="10" height="3" fill="#FFD700" rx="1"/>
            <rect x="-5" y="16" width="10" height="3" fill="#FFD700" rx="1"/>
            {/* Tua */}
            <line x1="-2" y1="19" x2="-2" y2="25" stroke="#DC143C" strokeWidth="1"/>
            <line x1="0" y1="19" x2="0" y2="27" stroke="#DC143C" strokeWidth="1"/>
            <line x1="2" y1="19" x2="2" y2="25" stroke="#DC143C" strokeWidth="1"/>
        </g>
    </svg>
);

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
        <footer ref={footerRef} className="footer" style={{ position: 'relative', overflow: 'hidden' }}>
            {/* Hiệu ứng hạt vàng lấp lánh */}
            <HatVangLapLanh side="left" />
            <HatVangLapLanh side="right" />
            
            {/* Cành mai 2 bên - slide từ từ */}
            <CanhMaiNgang side="left" isVisible={isVisible} />
            <CanhMaiNgang side="right" isVisible={isVisible} />
            
            <div className="container" style={{ position: 'relative', zIndex: 1 }}>
                <div className="footer-content">
                    <div className="footer-brand">
                        <h3 className="logo-text">IVIE</h3>
                        <p>Lưu giữ khoảnh khắc hạnh phúc của bạn</p>
                    </div>

                    <div className="footer-links">
                        <Link to="/chinh-sach">Chính sách bảo mật</Link>
                        <Link to="/chinh-sach">Quy định đặt cọc</Link>
                        <Link to="/lien-he">Liên hệ</Link>
                    </div>

                    <div className="footer-social">
                        <a href="https://www.facebook.com/di.di.717541" target="_blank" rel="noopener noreferrer" className="social-link" aria-label="Facebook">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                            </svg>
                        </a>
                        <a href="https://zalo.me/0793919384" target="_blank" rel="noopener noreferrer" className="social-link" aria-label="Zalo">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12 2C6.48 2 2 5.58 2 10c0 2.29 1.12 4.33 2.88 5.64L2 22l6.36-2.88C9.67 20.88 11.71 22 14 22c5.42 0 10-3.58 10-8S17.42 2 12 2zm0 16c-1.38 0-2.68-.35-3.82-.97l-.24-.14-2.54.55.55-2.54-.14-.24C5.35 14.68 5 13.38 5 12c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7z" />
                            </svg>
                        </a>
                        <a href="tel:0793919384" className="social-link" aria-label="Phone">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z" />
                            </svg>
                        </a>
                    </div>

                </div>

                <div className="footer-bottom">
                    <p>&copy; 2024 IVIE Wedding Studio. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default ChanTrang;
