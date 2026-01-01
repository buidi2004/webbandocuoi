import { useRef, useEffect, useState } from 'react';

// Dữ liệu test với ảnh placeholder
const sections = [
    {
        id: 1,
        title: "Chụp Ảnh Cưới Chuyên Nghiệp",
        description: "Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với đội ngũ nhiếp ảnh gia giàu kinh nghiệm.",
        image: "https://picsum.photos/id/1015/800/600",
        highlight: "500+ cặp đôi tin tưởng"
    },
    {
        id: 2,
        title: "Studio Hiện Đại",
        description: "Không gian chụp ảnh sang trọng với ánh sáng tự nhiên và thiết bị cao cấp.",
        image: "https://picsum.photos/id/1016/800/600",
        highlight: "3 studio tại Hà Nội"
    },
    {
        id: 3,
        title: "Trang Điểm Cô Dâu",
        description: "Makeup artist chuyên nghiệp giúp bạn tỏa sáng trong ngày trọng đại.",
        image: "https://picsum.photos/id/1018/800/600",
        highlight: "Top Artist được yêu thích"
    },
    {
        id: 4,
        title: "Album & In Ấn Cao Cấp",
        description: "Album cưới cao cấp với chất liệu nhập khẩu, bền đẹp theo thời gian.",
        image: "https://picsum.photos/id/1019/800/600",
        highlight: "Bảo hành trọn đời"
    }
];

const DemoCuonDinh = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [scrollProgress, setScrollProgress] = useState(0);
    const containerRef = useRef(null);

    useEffect(() => {
        const handleScroll = () => {
            if (!containerRef.current) return;
            
            const container = containerRef.current;
            const rect = container.getBoundingClientRect();
            const containerHeight = container.offsetHeight;
            const windowHeight = window.innerHeight;
            
            // Tính scroll progress dựa trên vị trí của container trong viewport
            const scrollableDistance = containerHeight - windowHeight;
            const scrolled = -rect.top;
            const progress = Math.max(0, Math.min(1, scrolled / scrollableDistance));
            
            setScrollProgress(progress);
            
            // Calculate active section (0 to 3)
            const sectionIndex = Math.min(3, Math.floor(progress * 4));
            setActiveIndex(sectionIndex);
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll(); // Initial call
        
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div 
            ref={containerRef}
            style={{ 
                minHeight: '400vh',
                background: 'linear-gradient(135deg, #f8f6f3 0%, #e8e4df 100%)',
                position: 'relative'
            }}
        >
            {/* Progress bar */}
            <div
                style={{ 
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    height: '4px',
                    background: 'linear-gradient(90deg, #b59410, #d4af37)',
                    width: `${scrollProgress * 100}%`,
                    zIndex: 9999,
                    transition: 'width 0.1s ease-out'
                }}
            />

            {/* Main content */}
            <div style={{ 
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                minHeight: '400vh',
                maxWidth: '1400px',
                margin: '0 auto'
            }}>
                {/* Left: Text sections */}
                <div style={{ position: 'relative' }}>
                    {sections.map((section, index) => (
                        <div
                            key={section.id}
                            style={{
                                height: '100vh',
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'center',
                                padding: '40px 60px',
                                opacity: activeIndex === index ? 1 : 0.3,
                                transform: `translateY(${activeIndex === index ? 0 : 20}px)`,
                                transition: 'all 0.5s ease-out'
                            }}
                        >
                            <span style={{
                                display: 'inline-block',
                                padding: '8px 16px',
                                marginBottom: '16px',
                                fontSize: '14px',
                                fontWeight: 500,
                                borderRadius: '20px',
                                background: 'rgba(181, 148, 16, 0.15)',
                                color: '#b59410',
                                width: 'fit-content'
                            }}>
                                {section.highlight}
                            </span>
                            
                            <h2 style={{
                                fontSize: '42px',
                                fontWeight: 700,
                                color: '#2c2c2c',
                                marginBottom: '20px',
                                lineHeight: 1.2,
                                fontFamily: "'Be Vietnam Pro', sans-serif"
                            }}>
                                {section.title}
                            </h2>
                            
                            <p style={{
                                fontSize: '18px',
                                color: '#666',
                                lineHeight: 1.7,
                                maxWidth: '450px',
                                fontFamily: "'Be Vietnam Pro', sans-serif"
                            }}>
                                {section.description}
                            </p>
                            
                            <button style={{
                                marginTop: '30px',
                                padding: '14px 32px',
                                background: '#2c2c2c',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '30px',
                                fontSize: '15px',
                                fontWeight: 500,
                                cursor: 'pointer',
                                width: 'fit-content',
                                transition: 'all 0.3s ease'
                            }}>
                                Tìm hiểu thêm
                            </button>
                        </div>
                    ))}
                </div>

                {/* Right: Sticky images */}
                <div style={{ position: 'relative' }}>
                    <div style={{
                        position: 'sticky',
                        top: '100px',
                        height: 'calc(100vh - 120px)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        padding: '40px'
                    }}>
                        {/* Image container */}
                        <div style={{
                            position: 'relative',
                            width: '100%',
                            maxWidth: '500px',
                            height: '600px'
                        }}>
                            {sections.map((section, index) => (
                                <img
                                    key={section.id}
                                    src={section.image}
                                    alt={section.title}
                                    style={{
                                        position: 'absolute',
                                        top: 0,
                                        left: 0,
                                        width: '100%',
                                        height: '100%',
                                        objectFit: 'cover',
                                        borderRadius: '20px',
                                        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
                                        opacity: activeIndex === index ? 1 : 0,
                                        transform: `scale(${activeIndex === index ? 1 : 0.95})`,
                                        transition: 'all 0.6s ease-out',
                                        zIndex: activeIndex === index ? 10 : 1
                                    }}
                                />
                            ))}
                        </div>

                        {/* Dots indicator */}
                        <div style={{
                            position: 'absolute',
                            right: '20px',
                            top: '50%',
                            transform: 'translateY(-50%)',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '12px'
                        }}>
                            {sections.map((_, index) => (
                                <div
                                    key={index}
                                    style={{
                                        width: activeIndex === index ? '12px' : '8px',
                                        height: activeIndex === index ? '12px' : '8px',
                                        borderRadius: '50%',
                                        background: activeIndex === index ? '#b59410' : '#ccc',
                                        transition: 'all 0.3s ease'
                                    }}
                                />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DemoCuonDinh;
