import { useState, useRef, useEffect, useCallback } from 'react';
import './GalleryImage.css';

/**
 * GalleryImage - Component ảnh gallery với lazy loading và hover effects
 * 
 * Props:
 * - src: URL ảnh
 * - alt: Alt text
 * - index: Vị trí trong gallery
 * - onClick: Callback khi click
 * - title: Tiêu đề ảnh (optional)
 */
const GalleryImage = ({ 
    src, 
    alt = '', 
    index,
    onClick,
    title = ''
}) => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [isInView, setIsInView] = useState(false);
    const [hasError, setHasError] = useState(false);
    const containerRef = useRef(null);
    const [isTouchDevice, setIsTouchDevice] = useState(false);

    // Detect touch device
    useEffect(() => {
        setIsTouchDevice('ontouchstart' in window || navigator.maxTouchPoints > 0);
    }, []);

    // Intersection Observer for lazy loading
    useEffect(() => {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setIsInView(true);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { 
                threshold: 0.1,
                rootMargin: '100px'
            }
        );

        if (containerRef.current) {
            observer.observe(containerRef.current);
        }

        return () => {
            if (containerRef.current) {
                observer.unobserve(containerRef.current);
            }
        };
    }, []);

    const handleLoad = useCallback(() => {
        setIsLoaded(true);
    }, []);

    const handleError = useCallback(() => {
        setHasError(true);
        setIsLoaded(true);
    }, []);

    const handleClick = useCallback(() => {
        if (onClick) {
            onClick(index);
        }
    }, [onClick, index]);

    return (
        <div 
            ref={containerRef}
            className={`gallery-image-container ${isTouchDevice ? 'touch-device' : ''}`}
            onClick={handleClick}
        >
            {/* Skeleton placeholder */}
            {!isLoaded && (
                <div className="gallery-image-skeleton">
                    <div className="skeleton-animation"></div>
                </div>
            )}

            {/* Actual image */}
            {isInView && !hasError && (
                <img
                    src={src}
                    alt={alt || title || `Gallery image ${index + 1}`}
                    className={`gallery-image ${isLoaded ? 'loaded' : ''}`}
                    onLoad={handleLoad}
                    onError={handleError}
                    loading="lazy"
                    decoding="async"
                />
            )}

            {/* Error state */}
            {hasError && (
                <div className="gallery-image-error">
                    <span>📷</span>
                    <p>Không tải được ảnh</p>
                </div>
            )}

            {/* Hover overlay - only on non-touch devices */}
            {isLoaded && !hasError && !isTouchDevice && (
                <div className="gallery-image-overlay">
                    <div className="overlay-icon">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                            <circle cx="11" cy="11" r="8"/>
                            <path d="M21 21l-4.35-4.35"/>
                            <path d="M11 8v6M8 11h6"/>
                        </svg>
                    </div>
                    {title && <p className="overlay-title">{title}</p>}
                </div>
            )}
        </div>
    );
};

export default GalleryImage;
