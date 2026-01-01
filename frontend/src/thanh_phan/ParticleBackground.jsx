import { useEffect, useRef, useState } from 'react';

const ParticleBackground = ({ particleCount = 3000 }) => {
    const canvasRef = useRef(null);
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const checkMobile = () => setIsMobile(window.innerWidth <= 768);
        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        let animationId;
        let particles = [];
        let mouse = { x: -9999, y: -9999 };

        // Giảm mạnh số hạt trên mobile
        const actualCount = isMobile ? Math.min(particleCount * 0.15, 300) : particleCount;

        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            initParticles();
        };

        const initParticles = () => {
            particles = [];
            // Kích thước hạt nhỏ hơn trên mobile
            const maxSize = isMobile ? 1.5 : 2;
            const minSize = isMobile ? 0.5 : 1;
            
            for (let i = 0; i < actualCount; i++) {
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                particles.push({
                    x, y,
                    homeX: x,
                    homeY: y,
                    vx: 0,
                    vy: 0,
                    size: Math.random() * maxSize + minSize,
                    color: isMobile 
                        ? `hsla(${220 + Math.random() * 40}, 80%, ${60 + Math.random() * 20}%, 0.6)`
                        : `hsl(${220 + Math.random() * 40}, 80%, ${60 + Math.random() * 20}%)`
                });
            }
        };

        const animate = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            const repulsionRadius = isMobile ? 80 : 150;

            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];

                // Mouse repulsion
                const dx = p.x - mouse.x;
                const dy = p.y - mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < repulsionRadius && dist > 0) {
                    const force = (repulsionRadius - dist) / repulsionRadius;
                    const angle = Math.atan2(dy, dx);
                    p.vx += Math.cos(angle) * force * 3;
                    p.vy += Math.sin(angle) * force * 3;
                }

                // Spring back to home
                p.vx += (p.homeX - p.x) * 0.02;
                p.vy += (p.homeY - p.y) * 0.02;

                // Friction
                p.vx *= 0.92;
                p.vy *= 0.92;

                // Update position
                p.x += p.vx;
                p.y += p.vy;

                // Draw
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
            }

            animationId = requestAnimationFrame(animate);
        };

        const handleMouseMove = (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        };

        const handleTouchMove = (e) => {
            if (e.touches.length > 0) {
                mouse.x = e.touches[0].clientX;
                mouse.y = e.touches[0].clientY;
            }
        };

        const handleMouseLeave = () => {
            mouse.x = -9999;
            mouse.y = -9999;
        };

        resize();
        animate();

        window.addEventListener('resize', resize);
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseleave', handleMouseLeave);
        window.addEventListener('touchmove', handleTouchMove, { passive: true });
        window.addEventListener('touchend', handleMouseLeave);

        return () => {
            cancelAnimationFrame(animationId);
            window.removeEventListener('resize', resize);
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseleave', handleMouseLeave);
            window.removeEventListener('touchmove', handleTouchMove);
            window.removeEventListener('touchend', handleMouseLeave);
        };
    }, [particleCount, isMobile]);

    return (
        <canvas
            ref={canvasRef}
            style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                background: '#000',
                opacity: isMobile ? 0.7 : 1
            }}
        />
    );
};

export default ParticleBackground;
