import { useState, useRef, useEffect } from 'react';
import { layUrlHinhAnh } from '../api/khach_hang';
import './ProductGallery.css';

const ProductGallery = ({ images = [], videoUrl = null, productName = 'Sản phẩm' }) => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isZoomOpen, setIsZoomOpen] = useState(false);
    const [zoomLevel, setZoomLevel] = useState(1);
    const [panPosition, setPanPosition] = useState({ x: 0, y: 0 });
    const [isDragging, setIsDragging] = useState(false);
    const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
    const [isVideoPlaying, setIsVideoPlaying] = useState(false);
    
    const videoRef = useRef(null);
    const zoomImageRef = useRef(null);

    // Tạo danh sách media (images + video nếu có)
    const mediaList = videoUrl 
        ? [...images, { type: 'video', url: videoUrl }]
        : images.map(url => ({ type: 'image', url }));

    const currentMedia = mediaList[currentIndex];
    const isCurrentVideo = currentMedia?.type === 'video';

    // Pause video khi switch media
    useEffect(() => {
        if (videoRef.current && !isCurrentVideo) {
            videoRef.current.pause();
            setIsVideoPlaying(false);
        }
    }, [currentIndex, isCurrentVideo]);

    // Reset zoom khi đóng modal
    useEffect(() => {
        if (!isZoomOpen) {
            setZoomLevel(1);
            setPanPosition({ x: 0, y: 0 });
        }
    }, [isZoomOpen]);

    // Handle keyboard events
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (isZoomOpen && e.key === 'Escape') {
                setIsZoomOpen(false);
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [isZoomOpen]);

    // Zoom handlers
    const handleWheel = (e) => {
        if (!isZoomOpen) return;
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.2 : 0.2;
        setZoomLevel(prev => Math.min(3, Math.max(1, prev + delta)));
    };

    // Pan handlers
    const handleMouseDown = (e) => {
        if (zoomLevel > 1) {
            setIsDragging(true);
            setDragStart({ x: e.clientX - panPosition.x, y: e.clientY - panPosition.y });
        }
    };

    const handleMouseMove = (e) => {
        if (!isDragging || zoomLevel <= 1) return;
        const newX = e.clientX - dragStart.x;
        const newY = e.clientY - dragStart.y;
        
        // Constrain pan position
        const maxPan = (zoomLevel - 1) * 200;
        setPanPosition({
            x: Math.min(maxPan, Math.max(-maxPan, newX)),
            y: Math.min(maxPan, Math.max(-maxPan, newY))
        });
    };

    const handleMouseUp = () => {
        setIsDragging(false);
    };

    // Touch handlers for mobile
    const handleTouchStart = (e) => {
        if (zoomLevel > 1 && e.touches.length === 1) {
            setIsDragging(true);
            setDragStart({ 
                x: e.touches[0].clientX - panPosition.x, 
                y: e.touches[0].clientY - panPosition.y 
            });
        }
    };

    const handleTouchMove = (e) => {
        if (!isDragging || zoomLevel <= 1) return;
        const newX = e.touches[0].clientX - dragStart.x;
        const newY = e.touches[0].clientY - dragStart.y;
        
        const maxPan = (zoomLevel - 1) * 200;
        setPanPosition({
            x: Math.min(maxPan, Math.max(-maxPan, newX)),
            y: Math.min(maxPan, Math.max(-maxPan, newY))
        });
    };

    const handleTouchEnd = () => {
        setIsDragging(false);
    };

    // Navigation
    const goNext = () => {
        setCurrentIndex(prev => (prev + 1) % mediaList.length);
    };

    const goPrev = () => {
        setCurrentIndex(prev => (prev - 1 + mediaList.length) % mediaList.length);
    };

    // Video controls
    const toggleVideo = () => {
        if (videoRef.current) {
            if (isVideoPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsVideoPlaying(!isVideoPlaying);
        }
    };

    if (mediaList.length === 0) {
        return (
            <div className="product-gallery">
                <div className="gallery-main-display">
                    <img 
                        src="https://placehold.co/800x1100/f5f5f5/333?text=No+Image" 
                        alt="No image available"
                    />
                </div>
            </div>
        );
    }

    return (
        <div className="product-gallery">
            {/* Main Display */}
            <div className="gallery-main-display">
                {isCurrentVideo ? (
                    <div className="video-container">
                        <video
                            ref={videoRef}
                            src={currentMedia.url}
                            controls
                            playsInline
                            onPlay={() => setIsVideoPlaying(true)}
                            onPause={() => setIsVideoPlaying(false)}
                            onError={(e) => console.error('Video error:', e)}
                        />
                    </div>
                ) : (
                    <img
                        src={layUrlHinhAnh(currentMedia.url)}
                        alt={`${productName} - ${currentIndex + 1}`}
                        onClick={() => setIsZoomOpen(true)}
                        onError={(e) => e.target.src = 'https://placehold.co/800x1100/f5f5f5/333?text=IVIE'}
                    />
                )}

                {/* Navigation Arrows */}
                {mediaList.length > 1 && (
                    <>
                        <button className="gallery-nav prev" onClick={goPrev} aria-label="Previous">
                            ‹
                        </button>
                        <button className="gallery-nav next" onClick={goNext} aria-label="Next">
                            ›
                        </button>
                    </>
                )}

                {/* Zoom Button (only for images) */}
                {!isCurrentVideo && (
                    <button 
                        className="zoom-btn" 
                        onClick={() => setIsZoomOpen(true)}
                        aria-label="Zoom image"
                    >
                        🔍
                    </button>
                )}
            </div>

            {/* Thumbnails */}
            <div className="gallery-thumbnails">
                {mediaList.map((media, idx) => (
                    <div
                        key={idx}
                        className={`thumbnail ${idx === currentIndex ? 'active' : ''}`}
                        onClick={() => setCurrentIndex(idx)}
                    >
                        {media.type === 'video' ? (
                            <div className="video-thumb">
                                <div className="play-icon">▶</div>
                                <span>Video</span>
                            </div>
                        ) : (
                            <img
                                src={layUrlHinhAnh(media.url)}
                                alt={`Thumbnail ${idx + 1}`}
                                onError={(e) => e.target.src = 'https://placehold.co/100x130/f5f5f5/333?text=Thumb'}
                            />
                        )}
                    </div>
                ))}
            </div>

            {/* Zoom Modal */}
            {isZoomOpen && !isCurrentVideo && (
                <div 
                    className="zoom-modal-overlay"
                    onClick={() => setIsZoomOpen(false)}
                >
                    <div 
                        className="zoom-modal-content"
                        onClick={(e) => e.stopPropagation()}
                        onWheel={handleWheel}
                        onMouseDown={handleMouseDown}
                        onMouseMove={handleMouseMove}
                        onMouseUp={handleMouseUp}
                        onMouseLeave={handleMouseUp}
                        onTouchStart={handleTouchStart}
                        onTouchMove={handleTouchMove}
                        onTouchEnd={handleTouchEnd}
                    >
                        <button 
                            className="zoom-close" 
                            onClick={() => setIsZoomOpen(false)}
                            aria-label="Close zoom"
                        >
                            ×
                        </button>
                        
                        <div className="zoom-controls">
                            <button onClick={() => setZoomLevel(prev => Math.min(3, prev + 0.5))}>+</button>
                            <span>{Math.round(zoomLevel * 100)}%</span>
                            <button onClick={() => setZoomLevel(prev => Math.max(1, prev - 0.5))}>−</button>
                            <button onClick={() => { setZoomLevel(1); setPanPosition({ x: 0, y: 0 }); }}>Reset</button>
                        </div>

                        <div 
                            className="zoom-image-container"
                            style={{ cursor: zoomLevel > 1 ? 'grab' : 'zoom-in' }}
                        >
                            <img
                                ref={zoomImageRef}
                                src={layUrlHinhAnh(currentMedia.url)}
                                alt={`${productName} - Zoomed`}
                                style={{
                                    transform: `scale(${zoomLevel}) translate(${panPosition.x / zoomLevel}px, ${panPosition.y / zoomLevel}px)`,
                                    transition: isDragging ? 'none' : 'transform 0.2s ease'
                                }}
                                draggable={false}
                            />
                        </div>

                        <p className="zoom-hint">
                            {zoomLevel > 1 ? 'Kéo để di chuyển • Scroll để zoom' : 'Scroll hoặc nhấn + để phóng to'}
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ProductGallery;
