import './ThanhLienHeCoDinh.css';

/**
 * StickyContactBar - Thanh liên hệ cố định dưới màn hình mobile
 * 3 nút: Gọi điện, Zalo, Google Maps
 * Màu vàng đồng sang trọng (#c9a86c)
 */
const StickyContactBar = ({
    phoneNumber = '0739193848',
    zaloLink = 'https://zalo.me/0739193848',
    mapsLink = 'https://maps.app.goo.gl/ivie-wedding-studio',
}) => {
    return (
        <div className="sticky-contact-bar">
            {/* Gọi điện */}
            <a
                href={`tel:${phoneNumber}`}
                className="contact-bar-btn"
                aria-label="Gọi điện tư vấn"
            >
                <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
                    <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                </svg>
                <span>Gọi ngay</span>
            </a>

            {/* Zalo */}
            <a
                href={zaloLink}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-bar-btn zalo"
                aria-label="Chat Zalo"
            >
                <svg viewBox="0 0 48 48" fill="currentColor" width="22" height="22">
                    <path d="M24 4C12.95 4 4 12.95 4 24s8.95 20 20 20 20-8.95 20-20S35.05 4 24 4zm7.17 26.83c-.39.39-1.02.39-1.41 0L24 25.41l-5.76 5.42c-.39.39-1.02.39-1.41 0-.39-.39-.39-1.02 0-1.41L22.59 24l-5.76-5.42c-.39-.39-.39-1.02 0-1.41.39-.39 1.02-.39 1.41 0L24 22.59l5.76-5.42c.39-.39 1.02-.39 1.41 0 .39.39.39 1.02 0 1.41L25.41 24l5.76 5.42c.39.39.39 1.02 0 1.41z"/>
                </svg>
                <span>Zalo</span>
            </a>

            {/* Google Maps */}
            <a
                href={mapsLink}
                target="_blank"
                rel="noopener noreferrer"
                className="contact-bar-btn maps"
                aria-label="Xem bản đồ"
            >
                <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                <span>Bản đồ</span>
            </a>
        </div>
    );
};

export default StickyContactBar;
