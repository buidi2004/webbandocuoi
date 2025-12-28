import React from 'react';

export default function ImageModal({ src, alt, open, onClose }) {
  if (!open) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      onClick={onClose}
      style={{
        position: 'fixed', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.6)', zIndex: 2000
      }}
    >
      <div onClick={(e) => e.stopPropagation()} style={{ maxWidth: '90%', maxHeight: '90%' }}>
        <img src={src} alt={alt} style={{ width: '100%', height: 'auto', borderRadius: 8, boxShadow: '0 30px 60px rgba(0,0,0,0.5)' }} />
        <button onClick={onClose} aria-label="Đóng" style={{ marginTop: 10, display: 'block', marginLeft: 'auto', padding: '8px 10px', borderRadius: 8, border: 'none', cursor: 'pointer' }}>Đóng</button>
      </div>
    </div>
  );
}
