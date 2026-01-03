import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import './MasonryGrid.css';

const MasonryGrid = ({ images = [], onImageClick }) => {
    const [columns, setColumns] = useState(3);
    const containerRef = useRef(null);

    useEffect(() => {
        const updateColumns = () => {
            const width = window.innerWidth;
            if (width < 600) setColumns(2);
            else if (width < 900) setColumns(3);
            else setColumns(4);
        };

        updateColumns();
        window.addEventListener('resize', updateColumns);
        return () => window.removeEventListener('resize', updateColumns);
    }, []);

    // Distribute images into columns
    const getColumns = () => {
        const cols = Array.from({ length: columns }, () => []);
        images.forEach((img, idx) => {
            cols[idx % columns].push({ ...img, originalIndex: idx });
        });
        return cols;
    };

    const columnData = getColumns();

    return (
        <div className="masonry-grid" ref={containerRef}>
            {columnData.map((column, colIdx) => (
                <div key={colIdx} className="masonry-column">
                    {column.map((img, imgIdx) => (
                        <motion.div
                            key={img.id || imgIdx}
                            className="masonry-item"
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: imgIdx * 0.1 }}
                            onClick={() => onImageClick?.(img.originalIndex)}
                        >
                            <img
                                src={img.image_url || img.url}
                                alt={img.title || `Ảnh ${img.originalIndex + 1}`}
                                loading="lazy"
                            />
                            {img.title && (
                                <div className="masonry-overlay">
                                    <span>{img.title}</span>
                                </div>
                            )}
                        </motion.div>
                    ))}
                </div>
            ))}
        </div>
    );
};

export default MasonryGrid;
