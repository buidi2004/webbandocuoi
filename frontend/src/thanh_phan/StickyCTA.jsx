import { useState } from 'react';
import './StickyCTA.css';

/**
 * StickyCTA - Nút Zalo và Hotline cố định góc phải màn hình
 * Responsive: compact trên mobile, expanded on hover trên desktop
 */
const StickyCTA = ({ 
    zaloLink = 'https://zalo.me/0901234567', // Placeholder - thay bằng link Zalo OA thật
    phoneNumber = '0901234567', // Placeholder - thay bằng số hotline thật
    showOnMobile = true 
}) => {
    const [isExpanded, setIsExpanded] = useState(false);

    return (
        <div 
            className={`sticky-cta ${showOnMobile ? '' : 'hide-mobile'}`}
            onMouseEnter={() => setIsExpanded(true)}
            onMouseLeave={() => setIsExpanded(false)}
        >
            {/* Zalo Button */}
            <a 
                href={zaloLink}
                target="_blank"
                rel="noopener noreferrer"
                className="cta-btn zalo-btn"
                aria-label="Chat Zalo"
            >
                <span className="cta-icon">
                    <svg viewBox="0 0 48 48" fill="currentColor" width="24" height="24">
                        <path d="M24 4C12.954 4 4 12.954 4 24s8.954 20 20 20 20-8.954 20-20S35.046 4 24 4zm9.707 27.707l-1.414 1.414L24 24.828l-8.293 8.293-1.414-1.414L22.586 23l-8.293-8.293 1.414-1.414L24 21.586l8.293-8.293 1.414 1.414L25.414 23l8.293 8.293z"/>
                    </svg>
                </span>
                <span className={`cta-text ${isExpanded ? 'show' : ''}`}>
                    Chat Zalo
                </span>
            </a>

            {/* Phone Button */}
            <a 
                href={`tel:${phoneNumber}`}
                className="cta-btn phone-btn"
                aria-label="Gọi điện"
            >
                <span className="cta-icon">📞</span>
                <span className={`cta-text ${isExpanded ? 'show' : ''}`}>
                    Gọi ngay
                </span>
            </a>

            {/* Messenger/Facebook Button (optional) */}
            <a 
                href="https://m.me/ivie.wedding.studio"
                target="_blank"
                rel="noopener noreferrer"
                className="cta-btn messenger-btn"
                aria-label="Messenger"
            >
                <span className="cta-icon">💬</span>
                <span className={`cta-text ${isExpanded ? 'show' : ''}`}>
                    Messenger
                </span>
            </a>
        </div>
    );
};

export default StickyCTA;
