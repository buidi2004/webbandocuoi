import { Link } from 'react-router-dom';
import './Footer.css';

// Component cành mai nằm ngang SVG - v6.0 nhiều nhánh hình chữ Y
const CanhMaiNgang = ({ side }) => (
    <svg 
        className={`canh-mai-ngang canh-mai-ngang-${side}`}
        viewBox="0 0 400 280" 
        preserveAspectRatio="xMinYMin meet"
        style={{ overflow: 'visible' }}
    >
        <defs>
            <radialGradient id={`hoaMaiGlow-${side}`} cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#FFE066"/>
                <stop offset="60%" stopColor="#FFD700"/>
                <stop offset="100%" stopColor="#FFA500"/>
            </radialGradient>
            <radialGradient id={`nhuyHoa-${side}`} cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#FF8C00"/>
                <stop offset="100%" stopColor="#CC6600"/>
            </radialGradient>
            <filter id={`glow-${side}`} x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
        </defs>
        
        {/* Cành chính */}
        <path d="M0 70 Q60 65 120 55 Q180 45 240 38 Q300 32 360 28 Q380 25 400 22" 
              stroke="#4A2C2A" strokeWidth="7" fill="none" strokeLinecap="round"/>
        
        {/* ===== NHÁNH CHỮ Y 1 - Gần gốc ===== */}
        <path d="M40 68 Q55 85 70 100" stroke="#5D3A38" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <path d="M70 100 Q60 120 50 140 Q45 155 42 170" stroke="#5D3A38" strokeWidth="3.5" fill="none" strokeLinecap="round"/>
        <path d="M70 100 Q90 115 105 135 Q115 150 120 165" stroke="#5D3A38" strokeWidth="3.5" fill="none" strokeLinecap="round"/>
        <path d="M55 130 Q45 140 38 155" stroke="#6B4442" strokeWidth="2" fill="none" strokeLinecap="round"/>
        <path d="M95 125 Q105 135 115 145" stroke="#6B4442" strokeWidth="2" fill="none" strokeLinecap="round"/>
        
        {/* ===== NHÁNH CHỮ Y 2 - Giữa ===== */}
        <path d="M140 50 Q160 70 175 90" stroke="#5D3A38" strokeWidth="4.5" fill="none" strokeLinecap="round"/>
        <path d="M175 90 Q165 110 155 130 Q148 145 145 160" stroke="#5D3A38" strokeWidth="3" fill="none" strokeLinecap="round"/>
        <path d="M175 90 Q195 105 210 125 Q220 140 225 155" stroke="#5D3A38" strokeWidth="3" fill="none" strokeLinecap="round"/>
        <path d="M160 115 Q150 125 145 140" stroke="#6B4442" strokeWidth="2" fill="none" strokeLinecap="round"/>
        <path d="M200 115 Q210 125 218 138" stroke="#6B4442" strokeWidth="2" fill="none" strokeLinecap="round"/>

        {/* ===== NHÁNH CHỮ Y 3 - Xa hơn ===== */}
        <path d="M240 40 Q260 55 275 75" stroke="#5D3A38" strokeWidth="4" fill="none" strokeLinecap="round"/>
        <path d="M275 75 Q265 95 258 115 Q252 130 250 145" stroke="#5D3A38" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
        <path d="M275 75 Q295 90 310 108 Q320 122 325 138" stroke="#5D3A38" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
        <path d="M262 100 Q255 110 250 125" stroke="#6B4442" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
        <path d="M300 98 Q310 108 318 120" stroke="#6B4442" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
        
        {/* ===== NHÁNH CHỮ Y 4 - Cuối ===== */}
        <path d="M330 32 Q345 45 355 60" stroke="#5D3A38" strokeWidth="3.5" fill="none" strokeLinecap="round"/>
        <path d="M355 60 Q348 78 342 95 Q338 108 336 120" stroke="#5D3A38" strokeWidth="2" fill="none" strokeLinecap="round"/>
        <path d="M355 60 Q372 72 385 88 Q392 100 395 112" stroke="#5D3A38" strokeWidth="2" fill="none" strokeLinecap="round"/>
        
        {/* Cành phụ hướng lên */}
        <path d="M80 58 Q110 40 150 28" stroke="#5D3A38" strokeWidth="3" fill="none" strokeLinecap="round"/>
        <path d="M200 42 Q230 28 270 20" stroke="#5D3A38" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
        <path d="M300 30 Q330 18 370 12" stroke="#5D3A38" strokeWidth="2" fill="none" strokeLinecap="round"/>

        {/* ===== HOA MAI ===== */}
        <g transform="translate(60, 68)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-10" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="9" cy="-3" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="8" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="8" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-9" cy="-3" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="4" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(160, 52)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-10" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="9" cy="-3" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="8" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="8" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-9" cy="-3" r="9" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="4" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(260, 40)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-9" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="8" cy="-3" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="7" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="7" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-8" cy="-3" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="3.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(360, 28)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-8" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="7" cy="-2" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="6" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="6" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-7" cy="-2" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="3" fill={`url(#nhuyHoa-${side})`}/>
        </g>

        {/* Hoa trên nhánh Y */}
        <g transform="translate(70, 100)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-9" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="8" cy="-3" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="7" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="7" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-8" cy="-3" r="8" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="3.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(45, 165)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-7" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(118, 160)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-7" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>

        <g transform="translate(175, 90)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-8" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="7" cy="-2" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="6" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="6" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-7" cy="-2" r="7" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="3" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(148, 155)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-6" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(222, 150)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-6" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>

        <g transform="translate(275, 75)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-7" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="5" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-6" cy="-2" r="6" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(252, 140)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(322, 135)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>

        <g transform="translate(355, 60)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-6" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-2" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(338, 118)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="-1" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="2" cy="3" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-2" cy="3" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="-1" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="1.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(392, 110)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="4" cy="-1" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="2" cy="3" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-2" cy="3" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-4" cy="-1" r="4" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="1.5" fill={`url(#nhuyHoa-${side})`}/>
        </g>

        {/* Hoa nhỏ trên cành lên */}
        <g transform="translate(130, 32)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        <g transform="translate(250, 22)" filter={`url(#glow-${side})`}>
            <circle cx="0" cy="-5" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-3" cy="4" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="-5" cy="-1" r="5" fill={`url(#hoaMaiGlow-${side})`}/>
            <circle cx="0" cy="0" r="2" fill={`url(#nhuyHoa-${side})`}/>
        </g>
        
        {/* Nụ mai */}
        <circle cx="90" cy="60" r="4" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="200" cy="48" r="3.5" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="310" cy="35" r="3" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="55" cy="125" r="3" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="100" cy="130" r="3" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="160" cy="120" r="2.5" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="205" cy="118" r="2.5" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="265" cy="105" r="2.5" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="305" cy="100" r="2" fill="#FFD700" filter={`url(#glow-${side})`}/>
        <circle cx="350" cy="85" r="2" fill="#FFD700" filter={`url(#glow-${side})`}/>

        {/* Pháo đỏ trên nhánh Y */}
        <g className="phao-do">
            <rect x="42" y="175" width="6" height="18" rx="2" fill="#DC143C"/>
            <rect x="40" y="172" width="10" height="4" rx="1" fill="#FFD700"/>
            <line x1="45" y1="172" x2="45" y2="165" stroke="#FFD700" strokeWidth="1"/>
            
            <rect x="115" y="168" width="6" height="16" rx="2" fill="#DC143C"/>
            <rect x="113" y="165" width="10" height="4" rx="1" fill="#FFD700"/>
            <line x1="118" y1="165" x2="118" y2="158" stroke="#FFD700" strokeWidth="1"/>
            
            <rect x="145" y="162" width="5" height="14" rx="2" fill="#DC143C"/>
            <rect x="143" y="159" width="9" height="3" rx="1" fill="#FFD700"/>
            <line x1="147.5" y1="159" x2="147.5" y2="153" stroke="#FFD700" strokeWidth="1"/>
            
            <rect x="220" y="158" width="5" height="14" rx="2" fill="#DC143C"/>
            <rect x="218" y="155" width="9" height="3" rx="1" fill="#FFD700"/>
            <line x1="222.5" y1="155" x2="222.5" y2="149" stroke="#FFD700" strokeWidth="1"/>
            
            <rect x="250" y="148" width="4" height="12" rx="1.5" fill="#DC143C"/>
            <rect x="248" y="145" width="8" height="3" rx="1" fill="#FFD700"/>
            <line x1="252" y1="145" x2="252" y2="140" stroke="#FFD700" strokeWidth="1"/>
            
            <rect x="320" y="142" width="4" height="12" rx="1.5" fill="#DC143C"/>
            <rect x="318" y="139" width="8" height="3" rx="1" fill="#FFD700"/>
            <line x1="322" y1="139" x2="322" y2="134" stroke="#FFD700" strokeWidth="1"/>
        </g>
    </svg>
);


// Component hạt vàng lấp lánh
const HatVangLapLanh = () => (
    <div className="hat-vang-container">
        {[...Array(20)].map((_, i) => (
            <div 
                key={i} 
                className="hat-vang"
                style={{
                    left: `${Math.random() * 100}%`,
                    top: `${Math.random() * 100}%`,
                    animationDelay: `${Math.random() * 3}s`,
                    animationDuration: `${2 + Math.random() * 2}s`
                }}
            />
        ))}
    </div>
);

// Component Footer chính
const ChanTrang = () => {
    return (
        <footer className="chan-trang">
            <HatVangLapLanh />
            
            <div className="canh-mai-trang-tri canh-mai-trai">
                <CanhMaiNgang side="left" />
            </div>
            <div className="canh-mai-trang-tri canh-mai-phai">
                <CanhMaiNgang side="right" />
            </div>
            
            <div className="chan-trang-noi-dung">
                <div className="chan-trang-cot">
                    <h3>IVIE Bridal</h3>
                    <p>Cho thuê váy cưới cao cấp</p>
                    <p>Địa chỉ: TP. Hồ Chí Minh</p>
                </div>
                
                <div className="chan-trang-cot">
                    <h4>Liên kết</h4>
                    <ul>
                        <li><Link to="/">Trang chủ</Link></li>
                        <li><Link to="/san-pham">Sản phẩm</Link></li>
                        <li><Link to="/thu-vien">Thư viện</Link></li>
                        <li><Link to="/lien-he">Liên hệ</Link></li>
                    </ul>
                </div>
                
                <div className="chan-trang-cot">
                    <h4>Liên hệ</h4>
                    <p>📞 Hotline: 0909 XXX XXX</p>
                    <p>📧 Email: contact@iviebridal.com</p>
                    <div className="mang-xa-hoi">
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
                        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">Instagram</a>
                    </div>
                </div>
            </div>
            
            <div className="chan-trang-ban-quyen">
                <p>© 2025 IVIE Bridal. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default ChanTrang;
