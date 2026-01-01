import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

// Component hiệu ứng gõ chữ
const TypewriterText = ({ text, isActive }) => {
    const [displayText, setDisplayText] = useState('');

    useEffect(() => {
        if (!isActive) {
            setDisplayText('');
            return;
        }

        let index = 0;
        const timer = setInterval(() => {
            if (index <= text.length) {
                setDisplayText(text.slice(0, index));
                index++;
            } else {
                clearInterval(timer);
            }
        }, 80);

        return () => clearInterval(timer);
    }, [text, isActive]);

    return (
        <span style={{ display: 'inline-flex', alignItems: 'center' }}>
            {displayText}
            {isActive && displayText.length < text.length && (
                <span
                    style={{
                        display: 'inline-block',
                        width: '2px',
                        height: '20px',
                        backgroundColor: '#b59410',
                        marginLeft: '4px',
                        animation: 'blink 0.5s infinite'
                    }}
                />
            )}
        </span>
    );
};

const CardCarousel = ({ items = [] }) => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [isMobile, setIsMobile] = useState(false);

    // Fallback data nếu không có items
    const fallbackItems = [
        {
            id: 1,
            title: "Gói Chụp Ảnh Cưới Premium",
            description: "Trọn gói chụp ảnh cưới cao cấp với 200+ ảnh đã chỉnh sửa",
            image: "https://picsum.photos/id/1011/800/600"
        },
        {
            id: 2,
            title: "Gói Chụp Ảnh Gia Đình",
            description: "Lưu giữ khoảnh khắc hạnh phúc bên gia đình thân yêu",
            image: "https://picsum.photos/id/1012/800/600"
        },
        {
            id: 3,
            title: "Gói Chụp Ảnh Kỷ Yếu",
            description: "Kỷ niệm tuổi học trò với bộ ảnh kỷ yếu độc đáo",
            image: "https://picsum.photos/id/1013/800/600"
        }
    ];

    // Sử dụng items nếu có đủ 3, không thì dùng fallback
    const displayItems = items.length >= 3 ? items : fallbackItems;

    // Check mobile
    useEffect(() => {
        const checkMobile = () => {
            setIsMobile(window.innerWidth < 768);
        };
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    const handleNext = () => {
        setActiveIndex((prev) => (prev + 1) % displayItems.length);
    };

    const handlePrev = () => {
        setActiveIndex((prev) => (prev - 1 + displayItems.length) % displayItems.length);
    };

    // Lấy 3 card hiển thị: prev, active, next
    const getVisibleItems = () => {
        const prev = (activeIndex - 1 + displayItems.length) % displayItems.length;
        const next = (activeIndex + 1) % displayItems.length;
        return [
            { ...displayItems[prev], position: 'left', index: prev },
            { ...displayItems[activeIndex], position: 'center', index: activeIndex },
            { ...displayItems[next], position: 'right', index: next }
        ];
    };

    const visibleItems = getVisibleItems();

    return (
        <div style={{
            position: 'relative',
            width: '100%',
            padding: isMobile ? '40px 0' : '60px 0',
            backgroundColor: '#f5f5f5',
            overflow: 'hidden'
        }}>
            {/* CSS cho animation */}
            <style>{`
                @keyframes blink {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0; }
                }
            `}</style>

            {/* Header */}
            <div style={{
                textAlign: 'center',
                marginBottom: isMobile ? '24px' : '40px',
                padding: '0 16px'
            }}>
                <h2 style={{
                    fontSize: isMobile ? '24px' : '32px',
                    fontWeight: 'bold',
                    color: '#1a1a1a',
                    marginBottom: '8px'
                }}>
                    Dịch Vụ Nổi Bật
                </h2>
                <p style={{
                    fontSize: isMobile ? '14px' : '16px',
                    color: '#666'
                }}>
                    Khám phá các gói dịch vụ chụp ảnh chuyên nghiệp
                </p>
            </div>

            {/* Carousel Container */}
            <div style={{
                maxWidth: '1200px',
                margin: '0 auto',
                padding: '0 16px'
            }}>
                {/* Cards - Mobile: chỉ hiện 1 card, Desktop: 3 cards */}
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: isMobile ? '0' : '20px',
                    minHeight: isMobile ? '280px' : '350px'
                }}>
                    {visibleItems.map((item) => {
                        const isCenter = item.position === 'center';
                        
                        // Mobile: chỉ hiện card center
                        if (isMobile && !isCenter) return null;
                        
                        return (
                            <motion.div
                                key={`${item.position}-${item.index}`}
                                initial={{ opacity: 0, scale: 0.8 }}
                                animate={{ 
                                    opacity: isCenter ? 1 : 0.6,
                                    scale: isCenter ? 1 : 0.9,
                                }}
                                transition={{ duration: 0.4, ease: 'easeOut' }}
                                onClick={() => {
                                    if (item.position === 'left') handlePrev();
                                    if (item.position === 'right') handleNext();
                                }}
                                style={{
                                    position: 'relative',
                                    overflow: 'hidden',
                                    borderRadius: '16px',
                                    cursor: isCenter ? 'default' : 'pointer',
                                    flexShrink: 0,
                                    width: isMobile 
                                        ? 'calc(100% - 32px)' 
                                        : (isCenter ? '500px' : '180px'),
                                    maxWidth: isMobile ? '350px' : 'none',
                                    height: isMobile ? '260px' : (isCenter ? '350px' : '280px'),
                                    opacity: isCenter ? 1 : 0.6,
                                    boxShadow: isCenter 
                                        ? '0 20px 40px rgba(0,0,0,0.2)' 
                                        : '0 10px 20px rgba(0,0,0,0.1)'
                                }}
                            >
                                {/* Image */}
                                <img
                                    src={item.image}
                                    alt={item.title}
                                    style={{
                                        width: '100%',
                                        height: '100%',
                                        objectFit: 'cover'
                                    }}
                                />
                                
                                {/* Overlay gradient - chỉ cho card giữa */}
                                {isCenter && (
                                    <div style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: 0,
                                        right: 0,
                                        bottom: 0,
                                        background: 'linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 50%, transparent 100%)'
                                    }} />
                                )}
                                
                                {/* Text overlay - chỉ cho card giữa */}
                                {isCenter && (
                                    <div style={{
                                        position: 'absolute',
                                        bottom: 0,
                                        left: 0,
                                        right: 0,
                                        padding: isMobile ? '16px' : '24px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'flex-start'
                                    }}>
                                        <h3 style={{
                                            fontSize: isMobile ? '18px' : '24px',
                                            fontWeight: 'bold',
                                            color: '#fff',
                                            textShadow: '0 2px 10px rgba(0,0,0,0.5)',
                                            marginBottom: '8px'
                                        }}>
                                            <TypewriterText 
                                                text={item.title} 
                                                isActive={isCenter} 
                                            />
                                        </h3>
                                    </div>
                                )}

                                {/* Play button - cho card giữa */}
                                {isCenter && (
                                    <div style={{
                                        position: 'absolute',
                                        top: '16px',
                                        right: '16px',
                                        width: '36px',
                                        height: '36px',
                                        backgroundColor: 'rgba(255,255,255,0.9)',
                                        borderRadius: '50%',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
                                    }}>
                                        <div style={{
                                            width: 0,
                                            height: 0,
                                            borderTop: '6px solid transparent',
                                            borderBottom: '6px solid transparent',
                                            borderLeft: '10px solid #333',
                                            marginLeft: '2px'
                                        }} />
                                    </div>
                                )}
                            </motion.div>
                        );
                    })}
                </div>

                {/* Dots indicator - Mobile */}
                {isMobile && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'center',
                        gap: '8px',
                        marginTop: '16px'
                    }}>
                        {displayItems.map((_, idx) => (
                            <button
                                key={idx}
                                onClick={() => setActiveIndex(idx)}
                                style={{
                                    width: activeIndex === idx ? '24px' : '8px',
                                    height: '8px',
                                    borderRadius: '4px',
                                    backgroundColor: activeIndex === idx ? '#b59410' : '#ccc',
                                    border: 'none',
                                    cursor: 'pointer',
                                    transition: 'all 0.3s ease'
                                }}
                            />
                        ))}
                    </div>
                )}

                {/* Description và Navigation */}
                <div style={{
                    marginTop: isMobile ? '20px' : '32px',
                    display: 'flex',
                    flexDirection: isMobile ? 'column' : 'row',
                    alignItems: isMobile ? 'center' : 'flex-start',
                    justifyContent: 'space-between',
                    gap: '16px',
                    padding: '0 16px',
                    textAlign: isMobile ? 'center' : 'left'
                }}>
                    {/* Text description */}
                    <div style={{ flex: 1 }}>
                        <h4 style={{
                            fontSize: isMobile ? '18px' : '20px',
                            fontWeight: 'bold',
                            color: '#1a1a1a',
                            marginBottom: '8px'
                        }}>
                            {displayItems[activeIndex]?.title || 'Dịch vụ'}
                        </h4>
                        <p style={{
                            fontSize: '14px',
                            color: '#666',
                            maxWidth: '400px',
                            marginBottom: '12px',
                            margin: isMobile ? '0 auto 12px' : '0 0 12px'
                        }}>
                            {displayItems[activeIndex]?.description || 'Dịch vụ chụp ảnh chuyên nghiệp'}
                        </p>
                        <a 
                            href="/lien-he" 
                            style={{
                                display: 'inline-flex',
                                alignItems: 'center',
                                gap: '4px',
                                color: '#b59410',
                                fontWeight: '500',
                                textDecoration: 'none',
                                fontSize: '14px'
                            }}
                        >
                            Xem chi tiết
                            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </a>
                    </div>

                    {/* Navigation buttons */}
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px'
                    }}>
                        <button
                            onClick={handlePrev}
                            style={{
                                width: '44px',
                                height: '44px',
                                borderRadius: '50%',
                                border: '1px solid #ccc',
                                backgroundColor: '#fff',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'pointer'
                            }}
                        >
                            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        
                        <button
                            onClick={handleNext}
                            style={{
                                width: '44px',
                                height: '44px',
                                borderRadius: '50%',
                                border: '1px solid #ccc',
                                backgroundColor: '#fff',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                cursor: 'pointer'
                            }}
                        >
                            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CardCarousel;
