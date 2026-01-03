import { useState, useRef, useEffect } from 'react';
import './AnhTaiCham.css';

/**
 * LazyImage - Component tải ảnh lazy với Intersection Observer
 * Chỉ tải ảnh khi gần viewport (200px threshold)
 * 
 * Props:
 * - src: URL ảnh
 * - alt: Alt text (SEO)
 * - width/height: Kích thước để tránh CLS
 * - aspectRatio: Tỷ lệ khung hình (default: 4/3)
 * - priority: true nếu là ảnh quan trọng (LCP)
 * - threshold: Khoảng cách trước viewport để bắt đầu load (px)
 */
const LazyImage = ({ 
    src, 
    alt = '', 
    className = '', 
    placeholderColor = '#f0f0f0',
    threshold = 200,
    onClick,
    style = {},
    width,
    height,
    aspectRatio = '4/3',
    priority = false, // Ảnh quan trọng (LCP) - load ngay
    ...props 
}) => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [isInView, setIsInView] = useState(priority); // Priority images load immediately
    const [hasError, setHasError] = useState(false);
    const imgRef = useRef(null);

    useEffect(() => {
        // Skip observer for priority images
        if (priority) return;
        
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        setIsInView(true);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { rootMargin: `${threshold}px` }
        );

        if (imgRef.current) {
            observer.observe(imgRef.current);
        }

        return () => {
            if (imgRef.current) {
                observer.unobserve(imgRef.current);
            }
        };
    }, [threshold, priority]);

    const handleLoad = () => {
        setIsLoaded(true);
    };

    const handleError = () => {
        setHasError(true);
        setIsLoaded(true);
    };

    return (
        <div 
            ref={imgRef}
            className={`lazy-image-container ${className}`}
            style={{ 
                backgroundColor: placeholderColor,
                aspectRatio: aspectRatio,
                ...style 
            }}
            onClick={onClick}
        >
            {/* Placeholder skeleton */}
            {!isLoaded && (
                <div className="lazy-image-placeholder">
                    <div className="lazy-image-skeleton"></div>
                </div>
            )}

            {/* Actual image - only load when in view */}
            {isInView && !hasError && (
                <img
                    src={src}
                    alt={alt}
                    width={width}
                    height={height}
                    className={`lazy-image ${isLoaded ? 'loaded' : ''}`}
                    onLoad={handleLoad}
                    onError={handleError}
                    loading={priority ? "eager" : "lazy"}
                    decoding="async"
                    fetchPriority={priority ? "high" : "auto"}
                    {...props}
                />
            )}

            {/* Error state */}
            {hasError && (
                <div className="lazy-image-error">
                    <span>📷</span>
                    <p>Không tải được ảnh</p>
                </div>
            )}
        </div>
    );
};

export default LazyImage;
