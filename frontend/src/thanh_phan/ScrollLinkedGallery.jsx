import { useRef, useEffect, useState } from 'react';

const ScrollLinkedGallery = ({ sections, showProgressBar = true }) => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [scrollProgress, setScrollProgress] = useState(0);
    const [isInView, setIsInView] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    const containerRef = useRef(null);

    // Check mobile
    useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth < 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    useEffect(() => {
        const handleScroll = () => {
            if (!containerRef.current) return;
            
            const container = containerRef.current;
            const rect = container.getBoundingClientRect();
            const containerHeight = container.offsetHeight;
            const windowHeight = window.innerHeight;
            
            const isVisible = rect.top < windowHeight && rect.bottom > 0;
            setIsInView(isVisible);
            
            const scrollableDistance = containerHeight - windowHeight;
            const scrolled = -rect.top;
            const progress = Math.max(0, Math.min(1, scrolled / scrollableDistance));
            
            setScrollProgress(progress);
            
            const sectionIndex = Math.min(sections.length - 1, Math.floor(progress * sections.length));
            setActiveIndex(sectionIndex);
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll();
        
        return () => window.removeEventListener('scroll', handleScroll);
    }, [sections.length]);

    // Mobile: Render đơn giản hơn - không dùng sticky
    if (isMobile) {
        return (
            <div style={{ 
                background: 'linear-gradient(135deg, #f8f6f3 0%, #e8e4df 100%)',
                padding: '40px 0'
            }}>
                {sections.map((section, index) => (
                    <div
                        key={section.id}
                        style={{
                            padding: '30px 20px',
                            marginBottom: '20px'
                        }}
                    >
                        {/* Image */}
                        <div style={{
                            width: '100%',
                            height: '250px',
                            marginBottom: '24px',
                            borderRadius: '16px',
                            overflow: 'hidden',
                            boxShadow: '0 10px 30px rgba(0,0,0,0.15)'
                        }}>
                            <img
                                src={section.image}
                                alt={section.title}
                                style={{
                                    width: '100%',
                                    height: '100%',
                                    objectFit: 'cover'
                                }}
                            />
                        </div>

                        {/* Text content */}
                        <span style={{
                            display: 'inline-block',
                            padding: '6px 14px',
                            marginBottom: '12px',
                            fontSize: '12px',
                            fontWeight: 500,
                            borderRadius: '20px',
                            background: 'rgba(181, 148, 16, 0.15)',
                            color: '#b59410'
                        }}>
                            {section.highlight}
                        </span>
                        
                        <h2 style={{
                            fontSize: '24px',
                            fontWeight: 700,
                            color: '#2c2c2c',
                            marginBottom: '12px',
                            lineHeight: 1.3
                        }}>
                            {section.title}
                        </h2>
                        
                        <p style={{
                            fontSize: '14px',
                            color: '#666',
                            lineHeight: 1.6,
                            marginBottom: '20px'
                        }}>
                            {section.description}
                        </p>
                        
                        <a 
                            href="/lien-he"
                            style={{
                                display: 'inline-block',
                                padding: '12px 24px',
                                background: '#2c2c2c',
                                color: '#fff',
                                borderRadius: '25px',
                                fontSize: '14px',
                                fontWeight: 500,
                                textDecoration: 'none'
                            }}
                        >
                            Tìm hiểu thêm
                        </a>
                    </div>
                ))}
            </div>
        );
    }

    // Desktop: Giữ nguyên scroll-linked animation
    return (
        <div 
            ref={containerRef}
            style={{ 
                minHeight: `${sections.length * 100}vh`,
                background: 'linear-gradient(135deg, #f8f6f3 0%, #e8e4df 100%)',
                position: 'relative'
            }}
        >
            {/* Progress bar */}
            {showProgressBar && isInView && (
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
            )}

            {/* Main content */}
            <div style={{ 
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                minHeight: `${sections.length * 100}vh`,
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
                                lineHeight: 1.2
                            }}>
                                {section.title}
                            </h2>
                            
                            <p style={{
                                fontSize: '18px',
                                color: '#666',
                                lineHeight: 1.7,
                                maxWidth: '450px'
                            }}>
                                {section.description}
                            </p>
                            
                            <a 
                                href="/lien-he"
                                style={{
                                    marginTop: '30px',
                                    padding: '14px 32px',
                                    background: '#2c2c2c',
                                    color: '#fff',
                                    borderRadius: '30px',
                                    fontSize: '15px',
                                    fontWeight: 500,
                                    width: 'fit-content',
                                    textDecoration: 'none',
                                    display: 'inline-block'
                                }}
                            >
                                Tìm hiểu thêm
                            </a>
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

export default ScrollLinkedGallery;
