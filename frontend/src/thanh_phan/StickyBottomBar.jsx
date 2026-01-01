import { useState, useEffect } from 'react';
import './StickyBottomBar.css';

const StickyBottomBar = () => {
    const [hienThi, setHienThi] = useState(false);
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const kiemTraMobile = () => {
            setIsMobile(window.innerWidth <= 768);
        };
        
        kiemTraMobile();
        window.addEventListener('resize', kiemTraMobile);
        
        const handleScroll = () => {
            // Hiển thị sau khi scroll qua hero section
            setHienThi(window.scrollY > 300);
        };
        
        window.addEventListener('scroll', handleScroll);
        
        return () => {
            window.removeEventListener('resize', kiemTraMobile);
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    if (!isMobile || !hienThi) return null;

    return (
        <div className="sticky-bottom-bar">
            <a href="tel:0793919384" className="sticky-btn call-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                </svg>
                <span>Gọi ngay</span>
            </a>
            
            <a href="https://zalo.me/0793919384" target="_blank" rel="noopener noreferrer" className="sticky-btn zalo-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12.49 10.272v-.45h1.347v6.322h-.77a.576.576 0 01-.577-.573v-.049a2.627 2.627 0 11.001-5.25zm1.347 2.625a1.46 1.46 0 10-2.92 0 1.46 1.46 0 002.92 0zM9.24 16.144h1.347V9.822H9.24v6.322zM6.594 16.144h1.347v-4.063h1.04v-1.17H7.94v-.107c0-.5.168-.7.77-.7h.27V8.87h-.452c-1.224 0-1.934.677-1.934 1.912v.3H5.5v1.17h1.094v4.063-.17zm10.334-4.063h-1.04v4.063h-1.347v-4.063h-.693v-1.17h.693v-.107c0-1.235.71-1.912 1.934-1.912h.453v1.234h-.27c-.602 0-.77.2-.77.7v.107h1.04v1.148zM12 0C5.373 0 0 4.925 0 11s5.373 11 12 11 12-4.925 12-11S18.627 0 12 0z"/>
                </svg>
                <span>Zalo</span>
            </a>
            
            <a href="https://maps.google.com/?q=IVIE+Wedding+Studio" target="_blank" rel="noopener noreferrer" className="sticky-btn map-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                <span>Chỉ đường</span>
            </a>
            
            <a href="/lien-he" className="sticky-btn book-btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM9 10H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2zm-8 4H7v2h2v-2zm4 0h-2v2h2v-2zm4 0h-2v2h2v-2z"/>
                </svg>
                <span>Đặt lịch</span>
            </a>
        </div>
    );
};

export default StickyBottomBar;
