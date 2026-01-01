import HieuUngHat from './HieuUngHat';

export default function HieuUngHatCuoiTrang() {
    return (
        <section style={{ 
            position: 'relative',
            width: '100%',
            height: '600px',
            background: '#fff',
            overflow: 'hidden'
        }}
        className="hieu-ung-cuoi-trang"
        >
            {/* Giảm số hạt - component sẽ tự giảm thêm trên mobile */}
            <HieuUngHat particleCount={200} nenTrang={true} />
            
            {/* Content overlay căn giữa */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                zIndex: 10,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '30px 20px',
                pointerEvents: 'none',
                textAlign: 'center'
            }}>
                <h2 style={{
                    color: '#1a1a1a',
                    fontSize: 'clamp(28px, 5vw, 42px)',
                    fontWeight: 700,
                    lineHeight: 1.2,
                    marginBottom: '16px',
                    fontFamily: 'Playfair Display, serif',
                    textShadow: '0 1px 2px rgba(255,255,255,0.8)'
                }}>
                    Khám Phá Thêm
                </h2>
                <p style={{
                    color: '#666',
                    fontSize: 'clamp(14px, 3vw, 18px)',
                    maxWidth: '500px',
                    marginBottom: '30px',
                    textShadow: '0 1px 2px rgba(255,255,255,0.8)'
                }}>
                    Trải nghiệm dịch vụ cưới trọn gói chuẩn quốc tế tại IVIE Studio
                </p>
                <div style={{ display: 'flex', gap: '12px', pointerEvents: 'auto', flexWrap: 'wrap', justifyContent: 'center' }}>
                    <a href="/lien-he" style={{
                        padding: '12px 24px',
                        background: '#c9a86c',
                        color: '#fff',
                        fontSize: '14px',
                        fontWeight: 600,
                        borderRadius: '8px',
                        border: 'none',
                        cursor: 'pointer',
                        textDecoration: 'none',
                        transition: 'transform 0.2s, box-shadow 0.2s'
                    }}
                    onMouseEnter={(e) => {
                        e.target.style.transform = 'translateY(-2px)';
                        e.target.style.boxShadow = '0 4px 12px rgba(201, 168, 108, 0.4)';
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.transform = 'translateY(0)';
                        e.target.style.boxShadow = 'none';
                    }}
                    >
                        Liên Hệ Ngay
                    </a>
                    <a href="/san-pham" style={{
                        padding: '12px 24px',
                        background: 'rgba(255,255,255,0.9)',
                        color: '#1a1a1a',
                        fontSize: '14px',
                        fontWeight: 600,
                        borderRadius: '8px',
                        border: '2px solid #1a1a1a',
                        cursor: 'pointer',
                        textDecoration: 'none',
                        transition: 'all 0.2s'
                    }}
                    onMouseEnter={(e) => {
                        e.target.style.background = '#1a1a1a';
                        e.target.style.color = '#fff';
                    }}
                    onMouseLeave={(e) => {
                        e.target.style.background = 'rgba(255,255,255,0.9)';
                        e.target.style.color = '#1a1a1a';
                    }}
                    >
                        Xem Sản Phẩm
                    </a>
                </div>
            </div>
            
            {/* CSS cho mobile */}
            <style>{`
                @media (max-width: 768px) {
                    .hieu-ung-cuoi-trang {
                        height: 450px !important;
                    }
                }
            `}</style>
        </section>
    );
}
