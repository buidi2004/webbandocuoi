import React, { useRef, useState } from 'react';
import { motion, useViewportScroll, useTransform } from 'framer-motion';

const sampleCards = [
  { id: 1, title: 'Elegant Gown', subtitle: 'Luxury Bridal', price: '2.500.000đ' },
  { id: 2, title: 'Classic Suit', subtitle: 'Tailored Fit', price: '1.800.000đ' },
  { id: 3, title: 'Velvet Robe', subtitle: 'Evening Wear', price: '2.200.000đ' },
  { id: 4, title: 'Silk Tuxedo', subtitle: 'Premium', price: '3.100.000đ' }
];

// single card
function GravityCard({ item, index }) {
  const ref = useRef(null);
  const [hoverOffset, setHoverOffset] = useState({ x: 0, y: 0 });

  // floating (up/down) with different duration per card for randomness
  const floatDuration = 6 + index * 1.3 + Math.random() * 1.2; // seconds

  // parallax on scroll: deeper cards move less
  const { scrollYProgress } = useViewportScroll();
  const depth = 0.25 + (index * 0.12); // smaller => more back
  const yParallax = useTransform(scrollYProgress, [0, 1], [0, -depth * 120]);

  function handleMove(e) {
    const rect = ref.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    // small relative offset to feel "drift"
    setHoverOffset({ x: (e.clientX - cx) / 25, y: (e.clientY - cy) / 35 });
  }

  function handleLeave() {
    setHoverOffset({ x: 0, y: 0 });
  }

  return (
    <motion.div
      ref={ref}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      style={{
        originX: 0.5,
        originY: 0.5,
        y: yParallax,
      }}
      animate={{
        y: [0, -8, 0, 6, 0], // floating keyframes
      }}
      transition={{
        duration: floatDuration,
        repeat: Infinity,
        ease: 'easeInOut'
      }}
      whileHover={{
        scale: 1.04,
        x: hoverOffset.x,
        y: hoverOffset.y - 6,
        boxShadow: '0 18px 40px rgba(0,0,0,0.18)'
      }}
      className="gravity-card"
      >
      <div style={{ padding: '18px' }}>
        <div style={{ fontSize: '14px', color: '#b08968', fontWeight: 700 }}>{item.subtitle}</div>
        <h3 style={{ margin: '6px 0 12px', fontSize: '20px' }}>{item.title}</h3>
        <div style={{ fontWeight: 700, color: '#d4a373', fontSize: '18px' }}>{item.price}</div>
      </div>
    </motion.div>
  );
}

export default function GravityCards({ items = sampleCards }) {
  return (
    <div style={{ padding: '60px 16px' }}>
      <h2 style={{ marginBottom: 18 }}>Featured (Anti-Gravity)</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 20 }}>
        {items.map((it, idx) => (
          <GravityCard key={it.id} item={it} index={idx} />
        ))}
      </div>

      {/* Small CSS-in-JS for cards (kept local for demo) */}
      <style>{`
        .gravity-card {
          background: linear-gradient(180deg, #ffffff, #fffaf6);
          border-radius: 14px;
          border: 1px solid rgba(0,0,0,0.06);
          box-shadow: 0 8px 20px rgba(0,0,0,0.06);
          cursor: pointer;
          transform-origin: center;
          will-change: transform;
          min-height: 130px;
          display: flex;
          align-items: center;
        }
      `}</style>
    </div>
  );
}

/*
Notes / key props:
 - floatDuration: different per card to create 'randomness' in float loops.
 - useViewportScroll + useTransform: provides simple parallax (cards move less with depth factor).
 - whileHover + onMouseMove: creates the "lose gravity" drift toward pointer.
 - You can tweak depth, floatDuration & hover offset multipliers for stronger/weaker effects.
*/