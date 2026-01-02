import { Link } from 'react-router-dom';
import './Footer.css';

const CanhMaiNgang = ({ side }) => (
    <svg 
        className={`canh-mai-ngang canh-mai-ngang-${side}`}
        viewBox="0 0 300 80" 
        preserveAspectRatio="xMidYMid meet"
    >
        <path d="M0 40 Q50 35 100 30 Q150 25 200 20 Q250 15 300 10" stroke="#5D4037" strokeWidth="4" fill="none" strokeLinecap="round"/>
        <path d="M50 35 Q80 50 120 55" stroke="#5D4037" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
        <path d="M150 22 Q180 35 220 40" stroke="#5D4037" strokeWidth="2" fill="none" strokeLinecap="round"/>
        <path d="M220 18 Q250 30 280 35" stroke="#5D4037" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
        <g transform="translate(80, 32)">
            <circle cx="0" cy="-6" r="5" fill="#FFD700"/>
            <circle cx="5" cy="-2" r="5" fill="#FFD700"/>
            <circle cx="4" cy="4" r="5" fill="#FFD700"/>
            <circle cx="-4" cy="4" r="5" fill="#FFD700"/>
            <circle cx="-5" cy="-2" r="5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="3" fill="#FFA000"/>
        </g>
        <g transform="translate(160, 24)">
            <circle cx="0" cy="-5" r="4.5" fill="#FFD700"/>
            <circle cx="4" cy="-1" r="4.5" fill="#FFD700"/>
            <circle cx="3" cy="4" r="4.5" fill="#FFD700"/>
            <circle cx="-3" cy="4" r="4.5" fill="#FFD700"/>
            <circle cx="-4" cy="-1" r="4.5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2.5" fill="#FFA000"/>
        </g>
        <g transform="translate(240, 16)">
            <circle cx="0" cy="-4" r="4" fill="#FFD700"/>
            <circle cx="4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="2" cy="3" r="4" fill="#FFD700"/>
            <circle cx="-2" cy="3" r="4" fill="#FFD700"/>
            <circle cx="-4" cy="-1" r="4" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2" fill="#FFA000"/>
        </g>
        <g transform="translate(110, 52)">
            <circle cx="0" cy="-4" r="3.5" fill="#FFD700"/>
            <circle cx="3" cy="-1" r="3.5" fill="#FFD700"/>
            <circle cx="2" cy="3" r="3.5" fill="#FFD700"/>
            <circle cx="-2" cy="3" r="3.5" fill="#FFD700"/>
            <circle cx="-3" cy="-1" r="3.5" fill="#FFD700"/>
            <circle cx="0" cy="0" r="2" fill="#FFA000"/>
        </g>
        <g transform="translate(200, 38)">
            <circle cx="0" cy="-3" r="3" fill="#FFD700"/>
            <circle cx="3" cy="-1" r="3" fill="#FFD700"/>
            <circle cx="2" cy="2" r="3" fill="#FFD700"/>
            <circle cx="-2" cy="2" r="3" fill="#FFD700"/>
            <circle cx="-3" cy="-1" r="3" fill="#FFD700"/>
            <circle cx="0" cy="0" r="1.5" fill="#FFA000"/>
        </g>
        <circle cx="40" cy="38" r="3" fill="#FFD700"/>
        <circle cx="130" cy="28" r="2.5" fill="#FFD700"/>
        <circle cx="270" cy="32" r="2.5" fill="#FFD700"/>
        <g transform="translate(60, 45)">
            <line x1="0" y1="-8" x2="0" y2="0" stroke="#8B0000" strokeWidth="1"/>
            <ellipse cx="0" cy="6" rx="5" ry="7" fill="#DC143C"/>
            <rect x="-5" y="-1" width="10" height="2" fill="#FFD700"/>
            <rect x="-5" y="12" width="10" height="2" fill="#FFD700"/>
            <line x1="0" y1="14" x2="0" y2="18" stroke="#DC143C" strokeWidth="1"/>
        </g>
    </svg>
);

const HatVangLapLanh = ({ side }) => {
    const particles = [];
    for (let i = 0; i < 25; i++) {
        const style = {
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
            animationDuration: `${2 + Math.random() * 2}s`
        };
        particles.push(<div key={i} className="hat-vang" style={style} />);
    }
    return <div className={`hat-vang-container hat-vang-${side}`}>{particles}</div>;
};

const ChanTrang = () => {
    return (
        <footer className="footer-wrapper">
            <div className="trang-tri-trai">
                <HatVangLapLanh side="trai" />
                <CanhMaiNgang side="trai" />
            </div>
            <div className="trang-tri-phai">
                <HatVangLapLanh side="phai" />
                <CanhMaiNgang side="phai" />
            </div>
            <div className="footer-center">
                <h2 className="footer-logo">IVIE</h2>
                <p className="footer-slogan">Luu giu khoanh khac hanh phuc cua ban</p>
                <nav className="footer-nav">
                    <Link to="/chinh-sach">Chinh sach bao mat</Link>
                    <span className="nav-divider">|</span>
                    <Link to="/chinh-sach">Quy dinh dat coc</Link>
                    <span className="nav-divider">|</span>
                    <Link to="/lien-he">Lien he</Link>
                </nav>
                <div className="footer-social">
                    <a href="https://www.facebook.com/di.di.717541" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    </a>
                    <a href="https://zalo.me/0793919384" target="_blank" rel="noopener noreferrer" aria-label="Zalo">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 5.58 2 10c0 2.29 1.12 4.33 2.88 5.64L2 22l6.36-2.88C9.67 20.88 11.71 22 14 22c5.42 0 10-3.58 10-8S17.42 2 12 2zm0 16c-1.38 0-2.68-.35-3.82-.97l-.24-.14-2.54.55.55-2.54-.14-.24C5.35 14.68 5 13.38 5 12c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7z"/></svg>
                    </a>
                    <a href="tel:0793919384" aria-label="Phone">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
                    </a>
                </div>
                <p className="footer-copyright">2024 IVIE Wedding Studio. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default ChanTrang;