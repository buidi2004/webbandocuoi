import { Link } from "react-router-dom";
import "./Footer.css";

// Component cành mai thật hơn với hiệu ứng gió
const CanhMaiThuc = ({ side }) => {
  const isLeft = side === "trai";

  return (
    <div className={`canh-mai-container canh-mai-${side}`}>
      <svg
        className="canh-mai-svg"
        viewBox="0 0 400 300"
        preserveAspectRatio="xMidYMid meet"
      >
        <defs>
          {/* Gradient cho cành */}
          <linearGradient
            id={`branchGradient-${side}`}
            x1="0%"
            y1="0%"
            x2="100%"
            y2="0%"
          >
            <stop offset="0%" stopColor="#3E2723" />
            <stop offset="50%" stopColor="#5D4037" />
            <stop offset="100%" stopColor="#4E342E" />
          </linearGradient>

          {/* Gradient cho hoa mai */}
          <radialGradient
            id={`flowerGradient-${side}`}
            cx="50%"
            cy="50%"
            r="50%"
          >
            <stop offset="0%" stopColor="#FFF9C4" />
            <stop offset="40%" stopColor="#FFD54F" />
            <stop offset="100%" stopColor="#FFB300" />
          </radialGradient>

          {/* Gradient cho nụ hoa */}
          <radialGradient id={`budGradient-${side}`} cx="50%" cy="30%" r="60%">
            <stop offset="0%" stopColor="#FFE082" />
            <stop offset="100%" stopColor="#FFA000" />
          </radialGradient>

          {/* Filter cho hiệu ứng mềm mại */}
          <filter
            id={`softGlow-${side}`}
            x="-20%"
            y="-20%"
            width="140%"
            height="140%"
          >
            <feGaussianBlur stdDeviation="1" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Nhóm chính với animation gió */}
        <g className="canh-mai-group">
          {/* Cành chính - uốn lượn tự nhiên */}
          <g className="canh-chinh">
            <path
              d="M 0,280
                               Q 30,260 60,240
                               Q 100,210 140,180
                               Q 180,150 220,130
                               Q 260,110 300,95
                               Q 340,80 380,70"
              stroke={`url(#branchGradient-${side})`}
              strokeWidth="8"
              fill="none"
              strokeLinecap="round"
              className="canh-goc"
            />

            {/* Vân gỗ trên cành */}
            <path
              d="M 40,255 Q 60,245 80,235"
              stroke="#3E2723"
              strokeWidth="1"
              fill="none"
              opacity="0.3"
            />
            <path
              d="M 120,195 Q 140,185 160,175"
              stroke="#3E2723"
              strokeWidth="1"
              fill="none"
              opacity="0.3"
            />
          </g>

          {/* Cành phụ 1 - đung đưa mạnh hơn */}
          <g className="canh-phu canh-phu-1">
            <path
              d="M 80,225 Q 100,200 130,185 Q 150,175 170,170"
              stroke={`url(#branchGradient-${side})`}
              strokeWidth="5"
              fill="none"
              strokeLinecap="round"
            />
            {/* Nhánh nhỏ */}
            <path
              d="M 110,195 Q 120,180 125,165"
              stroke="#5D4037"
              strokeWidth="2.5"
              fill="none"
              strokeLinecap="round"
            />
            <path
              d="M 140,180 Q 155,165 165,150"
              stroke="#5D4037"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
            />
          </g>

          {/* Cành phụ 2 */}
          <g className="canh-phu canh-phu-2">
            <path
              d="M 180,155 Q 200,130 235,115 Q 260,105 280,100"
              stroke={`url(#branchGradient-${side})`}
              strokeWidth="4"
              fill="none"
              strokeLinecap="round"
            />
            <path
              d="M 220,120 Q 235,100 250,85"
              stroke="#5D4037"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
            />
          </g>

          {/* Cành phụ 3 - phía trên */}
          <g className="canh-phu canh-phu-3">
            <path
              d="M 280,100 Q 310,80 340,65 Q 360,55 380,50"
              stroke="#5D4037"
              strokeWidth="3"
              fill="none"
              strokeLinecap="round"
            />
            <path
              d="M 320,75 Q 335,55 350,40"
              stroke="#5D4037"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
            />
          </g>

          {/* Cành nhỏ phía dưới */}
          <g className="canh-phu canh-phu-4">
            <path
              d="M 50,260 Q 70,280 95,285"
              stroke="#5D4037"
              strokeWidth="3"
              fill="none"
              strokeLinecap="round"
            />
          </g>

          {/* ===== HOA MAI ===== */}

          {/* Hoa 1 - Lớn, nở rộ */}
          <g
            className="hoa-mai hoa-1"
            transform="translate(95, 220)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-12"
                  rx="8"
                  ry="12"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="5" fill="#8B4513" />
            <circle cx="-2" cy="-2" r="1.5" fill="#FFD700" />
            <circle cx="2" cy="-1" r="1.5" fill="#FFD700" />
            <circle cx="0" cy="2" r="1.5" fill="#FFD700" />
            <circle cx="-2" cy="1" r="1" fill="#FFD700" />
            <circle cx="2" cy="2" r="1" fill="#FFD700" />
          </g>

          {/* Hoa 2 */}
          <g
            className="hoa-mai hoa-2"
            transform="translate(155, 175)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-10"
                  rx="7"
                  ry="10"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.15}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="4" fill="#8B4513" />
            <circle cx="-1.5" cy="-1.5" r="1.2" fill="#FFD700" />
            <circle cx="1.5" cy="-1" r="1.2" fill="#FFD700" />
            <circle cx="0" cy="1.5" r="1.2" fill="#FFD700" />
          </g>

          {/* Hoa 3 */}
          <g
            className="hoa-mai hoa-3"
            transform="translate(125, 160)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-9"
                  rx="6"
                  ry="9"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.12}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="3.5" fill="#8B4513" />
            <circle cx="0" cy="-1" r="1" fill="#FFD700" />
            <circle cx="1" cy="0.5" r="1" fill="#FFD700" />
            <circle cx="-1" cy="0.5" r="1" fill="#FFD700" />
          </g>

          {/* Hoa 4 */}
          <g
            className="hoa-mai hoa-4"
            transform="translate(240, 110)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-11"
                  rx="7"
                  ry="11"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.1}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="4.5" fill="#8B4513" />
            <circle cx="-1.5" cy="-1" r="1.3" fill="#FFD700" />
            <circle cx="1.5" cy="-1" r="1.3" fill="#FFD700" />
            <circle cx="0" cy="1.5" r="1.3" fill="#FFD700" />
          </g>

          {/* Hoa 5 */}
          <g
            className="hoa-mai hoa-5"
            transform="translate(255, 85)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-8"
                  rx="5.5"
                  ry="8"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.13}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="3" fill="#8B4513" />
            <circle cx="0" cy="0" r="1" fill="#FFD700" />
          </g>

          {/* Hoa 6 */}
          <g
            className="hoa-mai hoa-6"
            transform="translate(340, 60)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-9"
                  rx="6"
                  ry="9"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.11}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="3.5" fill="#8B4513" />
            <circle cx="0" cy="-0.5" r="1.2" fill="#FFD700" />
          </g>

          {/* Hoa 7 - nhỏ */}
          <g
            className="hoa-mai hoa-7"
            transform="translate(350, 40)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-7"
                  rx="5"
                  ry="7"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.14}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="3" fill="#8B4513" />
            <circle cx="0" cy="0" r="1" fill="#FFD700" />
          </g>

          {/* Hoa 8 - trên cành dưới */}
          <g
            className="hoa-mai hoa-8"
            transform="translate(85, 280)"
            filter={`url(#softGlow-${side})`}
          >
            <g className="canh-hoa-group">
              {[0, 72, 144, 216, 288].map((angle, i) => (
                <ellipse
                  key={i}
                  cx="0"
                  cy="-8"
                  rx="5.5"
                  ry="8"
                  fill={`url(#flowerGradient-${side})`}
                  transform={`rotate(${angle})`}
                  className="canh-hoa"
                  style={{ animationDelay: `${i * 0.12}s` }}
                />
              ))}
            </g>
            <circle cx="0" cy="0" r="3" fill="#8B4513" />
            <circle cx="0" cy="0" r="1" fill="#FFD700" />
          </g>

          {/* ===== NỤ HOA ===== */}

          {/* Nụ 1 - sắp nở */}
          <g className="nu-hoa nu-1" transform="translate(170, 165)">
            <ellipse
              cx="0"
              cy="0"
              rx="5"
              ry="8"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -3,-6 Q 0,-10 3,-6"
              stroke="#4E342E"
              strokeWidth="1.5"
              fill="none"
            />
          </g>

          {/* Nụ 2 */}
          <g className="nu-hoa nu-2" transform="translate(200, 125)">
            <ellipse
              cx="0"
              cy="0"
              rx="4"
              ry="6"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -2,-4 Q 0,-7 2,-4"
              stroke="#4E342E"
              strokeWidth="1"
              fill="none"
            />
          </g>

          {/* Nụ 3 */}
          <g className="nu-hoa nu-3" transform="translate(280, 95)">
            <ellipse
              cx="0"
              cy="0"
              rx="4.5"
              ry="7"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -2.5,-5 Q 0,-8 2.5,-5"
              stroke="#4E342E"
              strokeWidth="1"
              fill="none"
            />
          </g>

          {/* Nụ 4 */}
          <g className="nu-hoa nu-4" transform="translate(310, 70)">
            <ellipse
              cx="0"
              cy="0"
              rx="3.5"
              ry="5.5"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -2,-4 Q 0,-6 2,-4"
              stroke="#4E342E"
              strokeWidth="1"
              fill="none"
            />
          </g>

          {/* Nụ 5 - nhỏ */}
          <g className="nu-hoa nu-5" transform="translate(370, 55)">
            <ellipse
              cx="0"
              cy="0"
              rx="3"
              ry="5"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -1.5,-3 Q 0,-5 1.5,-3"
              stroke="#4E342E"
              strokeWidth="0.8"
              fill="none"
            />
          </g>

          {/* Nụ 6 */}
          <g className="nu-hoa nu-6" transform="translate(60, 250)">
            <ellipse
              cx="0"
              cy="0"
              rx="4"
              ry="6"
              fill={`url(#budGradient-${side})`}
            />
            <path
              d="M -2,-4 Q 0,-7 2,-4"
              stroke="#4E342E"
              strokeWidth="1"
              fill="none"
            />
          </g>
        </g>
      </svg>
    </div>
  );
};

// Hạt vàng lấp lánh
const HatVangLapLanh = ({ side }) => {
  const particles = [];
  for (let i = 0; i < 20; i++) {
    const style = {
      left: `${Math.random() * 100}%`,
      top: `${Math.random() * 100}%`,
      animationDelay: `${Math.random() * 3}s`,
      animationDuration: `${2 + Math.random() * 2}s`,
    };
    particles.push(<div key={i} className="hat-vang" style={style} />);
  }
  return (
    <div className={`hat-vang-container hat-vang-${side}`}>{particles}</div>
  );
};

// Cánh hoa rơi
const CanhHoaRoi = ({ side }) => {
  const petals = [];
  for (let i = 0; i < 6; i++) {
    const style = {
      left: `${10 + Math.random() * 80}%`,
      animationDelay: `${Math.random() * 8}s`,
      animationDuration: `${6 + Math.random() * 4}s`,
    };
    petals.push(
      <div key={i} className="canh-hoa-roi" style={style}>
        <svg viewBox="0 0 20 20" width="12" height="12">
          <ellipse cx="10" cy="10" rx="6" ry="9" fill="#FFD54F" opacity="0.8" />
        </svg>
      </div>,
    );
  }
  return (
    <div className={`canh-hoa-roi-container canh-hoa-roi-${side}`}>
      {petals}
    </div>
  );
};

const ChanTrang = () => {
  return (
    <footer className="footer-wrapper">
      {/* Cành mai bên trái */}
      <div className="trang-tri-trai">
        <HatVangLapLanh side="trai" />
        <CanhHoaRoi side="trai" />
        <CanhMaiThuc side="trai" />
      </div>

      {/* Cành mai bên phải */}
      <div className="trang-tri-phai">
        <HatVangLapLanh side="phai" />
        <CanhHoaRoi side="phai" />
        <CanhMaiThuc side="phai" />
      </div>

      {/* Nội dung chính */}
      <div className="footer-center">
        <h2 className="footer-logo">IVIE</h2>
        <p className="footer-slogan">Lưu giữ khoảnh khắc hạnh phúc của bạn</p>
        <nav className="footer-nav">
          <Link to="/chinh-sach">Chính sách bảo mật</Link>
          <span className="nav-divider">|</span>
          <Link to="/chinh-sach">Quy định đặt cọc</Link>
          <span className="nav-divider">|</span>
          <Link to="/lien-he">Liên hệ</Link>
        </nav>
        <div className="footer-social">
          <a
            href="https://www.facebook.com/di.di.717541"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Facebook"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
            </svg>
          </a>
          <a
            href="https://zalo.me/0793919384"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Zalo"
          >
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
        <p className="footer-copyright">
          © 2024 IVIE Wedding Studio. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default ChanTrang;
