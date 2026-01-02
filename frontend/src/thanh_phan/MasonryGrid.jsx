import { useCallback, useEffect, useRef } from 'react';
import GalleryImage from './GalleryImage';
import './MasonryGrid.css';

/**
 * MasonryGrid - Component layout masonry responsive
 * 
 * Props:
 * - images: Array<{ url: string, title?: string, id: string | number }>
 * - gap: Khoảng cách giữa items (default: 20)
 * - onImageClick: Callback khi click vào ảnh (index) => void
 */
const MasonryGrid = ({ 
    images = [], 
    gap = 20,
    onImageClick 
}) => {
    const gridRef = useRef(null);
    const resizeTimeoutRef = useRef(null);

    // Debounced resize handler
    useEffect(() => {
        const handleResize = () => {
            if (resizeTimeoutRef.current) {
                clearTimeout(resizeTimeoutRef.current);
            }
            resizeTimeoutRef.current = setTimeout(() => {
                // Force re-render on resize if needed
                if (gridRef.current) {
                    gridRef.current.style.opacity = '0.99';
                    requestAnimationFrame(() => {
                        if (gridRef.current) {
                            gridRef.current.style.opacity = '1';
                        }
                    });
                }
            }, 150);
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
            if (resizeTimeoutRef.current) {
                clearTimeout(resizeTimeoutRef.current);
            }
        };
    }, []);

    const handleImageClick = useCallback((index) => {
        if (onImageClick) {
            onImageClick(index);
        }
    }, [onImageClick]);

    if (!images || images.length === 0) {
        return (
            <div className="masonry-empty">
                <span>📷</span>
                <p>Chưa có ảnh trong thư viện</p>
            </div>
        );
    }

    return (
        <div 
            ref={gridRef}
            className="masonry-grid"
            style={{ '--masonry-gap': `${gap}px` }}
        >
            {images.map((image, index) => (
                <div key={image.id || index} className="masonry-item">
                    <GalleryImage
                        src={image.url}
                        alt={image.title || `Gallery ${index + 1}`}
                        title={image.title}
                        index={index}
                        onClick={handleImageClick}
                    />
                </div>
            ))}
        </div>
    );
};

export default MasonryGrid;
