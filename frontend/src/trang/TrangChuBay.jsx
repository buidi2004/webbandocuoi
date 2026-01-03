import React from 'react';
import AntiGravityScene from '../thanh_phan/AntiGravityScene';
import GravityCards from '../thanh_phan/GravityCards';

export default function AntiGravityLanding() {
  return (
    <div>
      {/* Background 3D scene */}
      <div style={{ position: 'relative', height: '70vh' }}>
        <AntiGravityScene count={5} style={{ height: '70vh', width: '100%' }} />
        {/* place a translucent overlay for content */}
        <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', pointerEvents: 'none' }}>
          <h1 style={{ pointerEvents: 'none', color: '#111827', background: 'rgba(255,255,255,0.7)', padding: '12px 18px', borderRadius: 10 }}>Anti-Gravity Landing</h1>
        </div>
      </div>

      {/* Cards area (foreground) */}
      <div style={{ background: '#faf9f7' }}>
        <GravityCards />
      </div>
    </div>
  );
}
