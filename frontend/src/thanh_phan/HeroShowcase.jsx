import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Màu vàng gold chủ đạo
const GOLD_COLOR = '#b59410';

// Component hiệu ứng gõ chữ Typewriter
const TypewriterText = ({ text, isActive, className = '' }) => {
    const [displayText, setDisplayText] = useState('');
    const [isComplete, setIsComplete] = useState(false);

    useEffect(() => {
        if (!isActive) {
            setDisplayText('');
            setIsComplete(false);
            return;
        }

        let index = 0;
        setIsComplete(false);
        const timer = setInterval(() => {
            if (index <= text.length) {
                setDisplayText(text.slice(0, index));
                index++;
            } else {
                setIsComplete(true);
                clearInterval(timer);
            }
        }, 60);

        return () => clearInterval(timer);
    }, [text, isActive]);

    return (
        <span className={`inline-flex items-center ${className}`}>
            {displayText}
            {isActive && !isComplete && (
                <motion.span
                    animate={{ opacity: [1, 0, 1] }}
                    transition={{ duration: 0.5, repeat: Infinity }}
                    className="inline-block w-0.5 h-6 ml-1"
                    style={{ backgroundColor: GOLD_COLOR }}
                />
            )}
        </span>
    );
};

// Dữ liệu mặc định cho các dịch vụ
const defaultServices = [
    {
        id: 1,
        title: "Trang điểm cô dâu",
        subtitle: "Dịch vụ trang điểm chuyên nghiệp",
        description: "Tỏa sáng trong ngày trọng đại với makeup artist hàng đầu",
        image: "https://picsum.photos/id/64/800/600",
        link: "/dich-vu-trang-diem"
    },
    {
        id: 2,
        title: "Trang điểm sự kiện",
        subtitle: "Makeup cho mọi dịp đặc biệt",
        description: "Phong cách trang điểm đa dạng cho tiệc, sự kiện, chụp ảnh",
        image: "https://picsum.photos/id/65/800/600",
        link: "/dich-vu-trang-diem"
    },
    {
        id: 3,
        title: "Chụp ảnh cưới",
        subtitle: "Lưu giữ khoảnh khắc hạnh phúc",
        description: "Đội ngũ nhiếp ảnh gia chuyên nghiệp với studio hiện đại",
        image: "https://picsum.photos/id/1011/800/600",
        link: "/san-pham"
    },
    {
        id: 4,
        title: "Gói dịch vụ combo",
        subtitle: "Trọn gói tiết kiệm",
        description: "Kết hợp nhiều dịch vụ với giá ưu đãi đặc biệt",
        image: "https://picsum.photos/id/1012/800/600",
        link: "/chon-combo"
    },
    {
        id: 5,
        title: "Album cao cấp",
        subtitle: "In ấn chất lượng cao",
        description: "Album cưới sang trọng với chất liệu nhập khẩu",
        image: "https://picsum.photos/id/1013/800/600",
        link: "/san-pham"
    }
];

const HeroShowcase = ({ services = defaultServices }) => {
    const [activeIndex, setActiveIndex] = useState(Math.floor(services.length / 2));
    const [isMobile, setIsMobile] = useState(false);
    const [isAutoPlay, setIsAutoPlay] = useState(true);

    // Check mobile
    useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    // Auto play
    useEffect(() => {
        if (!isAutoPlay) return;
        const timer = setInterval(() => {
            setActiveIndex(prev => (prev + 1) % services.length);
        }, 5000);
        return () => clearInterval(timer);
    }, [isAutoPlay, services.length]);

    const handlePrev = useCallback(() => {
        setIsAutoPlay(false);
        setActiveIndex(prev => (prev - 1 + services.length) % services.length);
    }, [services.length]);

    const handleNext = useCallback(() => {
        setIsAutoPlay(false);
        setActiveIndex(prev => (prev + 1) % services.length);
    }, [services.length]);

    // Lấy các card hiển thị (5 cards: 2 trái, 1 giữa, 2 phải)
    const getVisibleCards = () => {
        const cards = [];
        for (let i = -2; i <= 2; i++) {
            const index = (activeIndex + i + services.length) % services.length;
            cards.push({
                ...services[index],
                position: i,
                isCenter: i === 0
            });
        }
        return cards;
    };

    const visibleCards = getVisibleCards();

    return (
        <section className="relative w-full overflow-hidden bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900"
            style={{ minHeight: isMobile ? '500px' : '600px' }}
        >
            {/* Background overlay */}
            <div className="absolute inset-0 bg-black/30" />
            
            {/* Header */}
            <div className="relative z-10 text-center pt-8 md:pt-12 px-4">
                <motion.h2 
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-2xl md:text-4xl font-bold text-white mb-2"
                >
                    Dịch Vụ Nổi Bật
                </motion.h2>
                <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="text-gray-300 text-sm md:text-base"
                >
                    Khám phá các dịch vụ chuyên nghiệp của IVIE Studio
                </motion.p>
            </div>

            {/* Carousel Container */}
            <div className="relative z-10 flex items-center justify-center px-4 py-8 md:py-12"
                style={{ minHeight: isMobile ? '350px' : '420px' }}
            >
                {/* Navigation Button - Left */}
                <button
                    onClick={handlePrev}
                    className="absolute left-2 md:left-8 z-20 w-10 h-10 md:w-12 md:h-12 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-110"
                    style={{ 
                        backgroundColor: 'rgba(255,255,255,0.1)',
                        border: `2px solid ${GOLD_COLOR}`,
                        color: GOLD_COLOR
                    }}
                >
                    <svg className="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                    </svg>
                </button>

                {/* Cards */}
                <div className="relative flex items-center justify-center w-full max-w-6xl">
                    <AnimatePresence mode="popLayout">
                        {visibleCards.map((card) => {
                            const isCenter = card.isCenter;
                            const pos = card.position;
                            
                            // Mobile: chỉ hiện 3 cards
                            if (isMobile && Math.abs(pos) > 1) return null;

                            // Tính toán style dựa trên vị trí
                            const scale = isCenter ? 1 : (Math.abs(pos) === 1 ? 0.75 : 0.55);
                            const opacity = isCenter ? 1 : (Math.abs(pos) === 1 ? 0.6 : 0.3);
                            const zIndex = isCenter ? 10 : (Math.abs(pos) === 1 ? 5 : 1);
                            const translateX = isMobile 
                                ? pos * 120 
                                : pos * 200;
                            const blur = isCenter ? 0 : Math.abs(pos) * 2;

                            return (
                                <motion.div
                                    key={`${card.id}-${pos}`}
                                    initial={{ opacity: 0, scale: 0.5 }}
                                    animate={{
                                        opacity,
                                        scale,
                                        x: translateX,
                                        zIndex,
                                        filter: `blur(${blur}px)`
                                    }}
                                    exit={{ opacity: 0, scale: 0.5 }}
                                    transition={{ duration: 0.5, ease: 'easeOut' }}
                                    onClick={() => {
                                        if (!isCenter) {
                                            setIsAutoPlay(false);
                                            setActiveIndex((activeIndex + pos + services.length) % services.length);
                                        }
                                    }}
                                    className="absolute cursor-pointer"
                                    style={{
                                        width: isMobile ? '240px' : '380px',
                                        height: isMobile ? '300px' : '380px',
                                    }}
                                >
                                    {/* Card */}
                                    <div className="relative w-full h-full rounded-2xl overflow-hidden shadow-2xl">
                                        {/* Image */}
                                        <img
                                            src={card.image}
                                            alt={card.title}
                                            className="w-full h-full object-cover"
                                        />
                                        
                                        {/* Gradient Overlay */}
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
                                        
                                        {/* Content - chỉ hiện cho card giữa */}
                                        {isCenter && (
                                            <div className="absolute bottom-0 left-0 right-0 p-4 md:p-6">
                                                {/* Subtitle với typewriter */}
                                                <div className="mb-2">
                                                    <span 
                                                        className="inline-block px-3 py-1 rounded-full text-xs md:text-sm font-medium"
                                                        style={{ 
                                                            backgroundColor: `${GOLD_COLOR}20`,
                                                            color: GOLD_COLOR
                                                        }}
                                                    >
                                                        <TypewriterText 
                                                            text={card.subtitle} 
                                                            isActive={isCenter}
                                                        />
                                                    </span>
                                                </div>
                                                
                                                {/* Title */}
                                                <h3 className="text-xl md:text-2xl font-bold text-white mb-2">
                                                    {card.title}
                                                </h3>
                                                
                                                {/* Description */}
                                                <p className="text-gray-300 text-sm md:text-base mb-4 line-clamp-2">
                                                    {card.description}
                                                </p>
                                                
                                                {/* CTA Button */}
                                                <a
                                                    href={card.link}
                                                    className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:scale-105"
                                                    style={{
                                                        backgroundColor: GOLD_COLOR,
                                                        color: '#fff'
                                                    }}
                                                >
                                                    Xem chi tiết
                                                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                                    </svg>
                                                </a>
                                            </div>
                                        )}

                                        {/* Play indicator cho card giữa */}
                                        {isCenter && (
                                            <div 
                                                className="absolute top-4 right-4 w-10 h-10 rounded-full flex items-center justify-center"
                                                style={{ backgroundColor: 'rgba(255,255,255,0.9)' }}
                                            >
                                                <div 
                                                    className="w-0 h-0 ml-1"
                                                    style={{
                                                        borderTop: '6px solid transparent',
                                                        borderBottom: '6px solid transparent',
                                                        borderLeft: `10px solid ${GOLD_COLOR}`
                                                    }}
                                                />
                                            </div>
                                        )}
                                    </div>
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>
                </div>

                {/* Navigation Button - Right */}
                <button
                    onClick={handleNext}
                    className="absolute right-2 md:right-8 z-20 w-10 h-10 md:w-12 md:h-12 rounded-full flex items-center justify-center transition-all duration-300 hover:scale-110"
                    style={{ 
                        backgroundColor: 'rgba(255,255,255,0.1)',
                        border: `2px solid ${GOLD_COLOR}`,
                        color: GOLD_COLOR
                    }}
                >
                    <svg className="w-5 h-5 md:w-6 md:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </button>
            </div>

            {/* Dots Indicator */}
            <div className="relative z-10 flex justify-center gap-2 pb-8">
                {services.map((_, idx) => (
                    <button
                        key={idx}
                        onClick={() => {
                            setIsAutoPlay(false);
                            setActiveIndex(idx);
                        }}
                        className="transition-all duration-300"
                        style={{
                            width: activeIndex === idx ? '24px' : '8px',
                            height: '8px',
                            borderRadius: '4px',
                            backgroundColor: activeIndex === idx ? GOLD_COLOR : 'rgba(255,255,255,0.3)'
                        }}
                    />
                ))}
            </div>

            {/* Service Info Bar */}
            <div className="relative z-10 bg-black/50 backdrop-blur-sm py-4 px-4">
                <div className="max-w-4xl mx-auto flex flex-wrap items-center justify-center gap-4 md:gap-8 text-center">
                    <div className="flex items-center gap-2">
                        <span style={{ color: GOLD_COLOR }}>✨</span>
                        <span className="text-white text-sm">500+ khách hàng</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span style={{ color: GOLD_COLOR }}>⭐</span>
                        <span className="text-white text-sm">Đánh giá 5 sao</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span style={{ color: GOLD_COLOR }}>🎯</span>
                        <span className="text-white text-sm">Chuyên nghiệp</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <span style={{ color: GOLD_COLOR }}>💝</span>
                        <span className="text-white text-sm">Tận tâm</span>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default HeroShowcase;
