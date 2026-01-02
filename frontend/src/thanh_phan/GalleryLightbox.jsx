import { useEffect, useCallback } from 'react';
import { createPortal } from 'react-dom';
import './GalleryLightbox.css';

/**
 * GalleryLightbox - Full-screen image viewer với navigation
 * 
 * Props:
 * - images: Array<{ url: string, title?: string }>
 * - currentIndex: Index của ảnh đang hiển thị
 * - isOpen: Boolean điều khiển hiển thị
 * - onClose: Callback đóng lightbox
 * - onNavigate: Callback navigate ('prev' | 'next')
 */
const GalleryLightbox = ({ 
    images = [], 
    currentIndex = 0, 
    isOpen = false, 
    onClose, 
    onNavigate 
}) => {
    // Keyboard navigation
    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (e) => {
            switch (e.key) {
                case 'Escape':
                    onClose?.();
                    break;
                case 'ArrowLeft':
                    onNavigate?.('prev');
                    break;
                case 'ArrowRight':
                    onNavigate?.('next');
                    break;
                default:
                    break;
            }
        };

        document.addEventListener('keydown', handleKeyDown);
        // Prevent body scroll when lightbox is open
        document.body.style.overflow = 'hidden';

        return () => {
            document.removeEventListener('keydown', handleKeyDown);
            document.body.style.overflow = '';
        };
    }, [isOpen, onClose, onNavigate]);

    const handleOverlayClick = useCallback((e) => {
        if (e.target === e.currentTarget) {
            onClose?.();
        }
    }, [onClose]);

    const handlePrev = useCallback((e) => {
        e.stopPropagation();
        onNavigate?.('prev');
    }, [onNavigate]);

    const handleNext = useCallback((e) => {
        e.stopPropagation();
        onNavigate?.('next');
    }, [onNavigate]);

    const handleClose = useCallback((e) => {
        e.stopPropagation();
        onClose?.();
    }, [onClose]);

    if (!isOpen || !images.length) return null;

    const currentImage = images[currentIndex];
    const total = images.length;
    const displayIndex = currentIndex + 1;

    const lightboxContent = (
        <div className="lightbox-overlay" onClick={handleOverlayClick}>
            {/* Close button */}
            <button 
                className="lightbox-close" 
                onClick={handleClose}
                aria-label="Đóng"
            >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
            </button>

            {/* Navigation - Previous */}
            {total > 1 && (
                <button 
                    className="lightbox-nav lightbox-prev" 
                    onClick={handlePrev}
                    aria-label="Ảnh trước"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M15 18l-6-6 6-6"/>
                    </svg>
                </button>
            )}

            {/* Main image */}
            <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
                <img 
                    src={currentImage?.url} 
                    alt={currentImage?.title || `Ảnh ${displayIndex}`}
                    className="lightbox-image"
                />
                
                {/* Image info */}
                <div className="lightbox-info">
                    {currentImage?.title && (
                        <p className="lightbox-title">{currentImage.title}</p>
                    )}
                    <p className="lightbox-index">{displayIndex} / {total}</p>
                </div>
            </div>

            {/* Navigation - Next */}
            {total > 1 && (
                <button 
                    className="lightbox-nav lightbox-next" 
                    onClick={handleNext}
                    aria-label="Ảnh tiếp"
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M9 18l6-6-6-6"/>
                    </svg>
                </button>
            )}
        </div>
    );

    // Render via Portal
    return createPortal(lightboxContent, document.body);
};

export default GalleryLightbox;
