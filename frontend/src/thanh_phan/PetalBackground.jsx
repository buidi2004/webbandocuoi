import { useEffect, useRef, useCallback } from 'react';
import './PetalBackground.css';

/**
 * PetalBackground - Canvas-based floating petal animation
 * 
 * Props:
 * - petalCount: Số lượng cánh hoa (15-25, default: 20)
 * - enabled: Bật/tắt animation (default: true)
 */
const PetalBackground = ({ 
    petalCount = 20, 
    enabled = true 
}) => {
    const canvasRef = useRef(null);
    const animationRef = useRef(null);
    const petalsRef = useRef([]);

    // Clamp petal count to 15-25
    const actualPetalCount = Math.max(15, Math.min(25, petalCount));

    // Create a single petal
    const createPetal = useCallback((width, height, existingPetal = null) => {
        return {
            x: existingPetal?.x ?? Math.random() * width,
            y: existingPetal?.y ?? Math.random() * height - height,
            size: 10 + Math.random() * 15, // 10-25px
            rotation: Math.random() * Math.PI * 2,
            rotationSpeed: (Math.random() - 0.5) * 0.02,
            fallSpeed: 0.3 + Math.random() * 0.5,
            swayAmplitude: 20 + Math.random() * 30,
            swaySpeed: 0.01 + Math.random() * 0.02,
            swayOffset: Math.random() * Math.PI * 2,
            opacity: 0.3 + Math.random() * 0.4, // 0.3-0.7
            color: `hsl(${350 + Math.random() * 20}, 70%, ${85 + Math.random() * 10}%)` // Pink tones
        };
    }, []);

    // Initialize petals
    const initPetals = useCallback((width, height) => {
        petalsRef.current = [];
        for (let i = 0; i < actualPetalCount; i++) {
            const petal = createPetal(width, height);
            // Distribute initial Y positions
            petal.y = Math.random() * height;
            petalsRef.current.push(petal);
        }
    }, [actualPetalCount, createPetal]);

    // Draw a petal shape
    const drawPetal = useCallback((ctx, petal, time) => {
        ctx.save();
        
        // Calculate sway
        const swayX = Math.sin(time * petal.swaySpeed + petal.swayOffset) * petal.swayAmplitude;
        
        ctx.translate(petal.x + swayX, petal.y);
        ctx.rotate(petal.rotation);
        ctx.globalAlpha = petal.opacity;
        
        // Draw petal shape (ellipse with pointed ends)
        ctx.beginPath();
        ctx.fillStyle = petal.color;
        
        const w = petal.size;
        const h = petal.size * 0.6;
        
        ctx.moveTo(0, -h);
        ctx.bezierCurveTo(w * 0.5, -h * 0.5, w * 0.5, h * 0.5, 0, h);
        ctx.bezierCurveTo(-w * 0.5, h * 0.5, -w * 0.5, -h * 0.5, 0, -h);
        
        ctx.fill();
        ctx.restore();
    }, []);

    useEffect(() => {
        if (!enabled) return;

        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width, height;
        let isVisible = true;
        let startTime = performance.now();

        // Resize handler
        const resize = () => {
            const parent = canvas.parentElement;
            if (!parent) return;

            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            width = parent.offsetWidth;
            height = parent.offsetHeight;

            canvas.width = width * dpr;
            canvas.height = height * dpr;
            canvas.style.width = `${width}px`;
            canvas.style.height = `${height}px`;
            ctx.scale(dpr, dpr);

            if (petalsRef.current.length === 0) {
                initPetals(width, height);
            }
        };

        // Visibility change handler
        const handleVisibilityChange = () => {
            isVisible = !document.hidden;
            if (isVisible && !animationRef.current) {
                animate();
            }
        };

        // Animation loop
        const animate = () => {
            if (!isVisible || !enabled) {
                animationRef.current = null;
                return;
            }

            const time = (performance.now() - startTime) / 1000;

            // Clear canvas
            ctx.clearRect(0, 0, width, height);

            // Update and draw petals
            petalsRef.current.forEach((petal, index) => {
                // Update position
                petal.y += petal.fallSpeed;
                petal.rotation += petal.rotationSpeed;

                // Reset petal when it goes off screen (object pooling)
                if (petal.y > height + petal.size) {
                    const newPetal = createPetal(width, height);
                    newPetal.y = -newPetal.size;
                    petalsRef.current[index] = newPetal;
                } else {
                    drawPetal(ctx, petal, time);
                }
            });

            animationRef.current = requestAnimationFrame(animate);
        };

        // Initialize
        resize();
        animate();

        // Event listeners
        window.addEventListener('resize', resize);
        document.addEventListener('visibilitychange', handleVisibilityChange);

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
            window.removeEventListener('resize', resize);
            document.removeEventListener('visibilitychange', handleVisibilityChange);
        };
    }, [enabled, initPetals, createPetal, drawPetal]);

    if (!enabled) return null;

    return (
        <canvas 
            ref={canvasRef} 
            className="petal-background"
            aria-hidden="true"
        />
    );
};

export default PetalBackground;
