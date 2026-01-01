import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function HieuUngChuyenTrang() {
    const location = useLocation();
    const [dangChuyenTrang, setDangChuyenTrang] = useState(false);
    const [hienThi, setHienThi] = useState(false);

    useEffect(() => {
        // Bắt đầu hiệu ứng khi route thay đổi
        setHienThi(true);
        setDangChuyenTrang(true);

        // Fade out sau 600ms (tăng thời gian để người dùng thấy loading)
        const timer1 = setTimeout(() => {
            setDangChuyenTrang(false);
        }, 600);

        // Ẩn hoàn toàn sau 1000ms
        const timer2 = setTimeout(() => {
            setHienThi(false);
        }, 1000);

        return () => {
            clearTimeout(timer1);
            clearTimeout(timer2);
        };
    }, [location.pathname]);

    if (!hienThi) return null;

    return (
        <div
            style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                zIndex: 9999,
                pointerEvents: 'none',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: dangChuyenTrang 
                    ? 'linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(250,248,245,0.98) 100%)' 
                    : 'rgba(255, 255, 255, 0)',
                transition: 'background 0.4s ease-out'
            }}
        >
            {/* Logo IVIE với hiệu ứng xoay */}
            <div
                style={{
                    opacity: dangChuyenTrang ? 1 : 0,
                    transform: dangChuyenTrang ? 'scale(1)' : 'scale(0.8)',
                    transition: 'all 0.3s ease-out',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '20px'
                }}
            >
                {/* Logo xoay */}
                <div
                    style={{
                        width: '80px',
                        height: '80px',
                        borderRadius: '50%',
                        border: '3px solid transparent',
                        borderTopColor: '#c9a86c',
                        borderRightColor: '#d4b896',
                        animation: 'spin 1s linear infinite',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    <div
                        style={{
                            width: '60px',
                            height: '60px',
                            borderRadius: '50%',
                            background: 'linear-gradient(135deg, #c9a86c 0%, #d4b896 100%)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 4px 15px rgba(201, 168, 108, 0.3)'
                        }}
                    >
                        <span
                            style={{
                                fontSize: '20px',
                                fontWeight: 700,
                                color: '#fff',
                                fontFamily: 'Playfair Display, serif',
                                letterSpacing: '2px'
                            }}
                        >
                            IV
                        </span>
                    </div>
                </div>

                {/* Tên thương hiệu */}
                <span
                    style={{
                        fontSize: '32px',
                        fontWeight: 700,
                        color: '#c9a86c',
                        fontFamily: 'Playfair Display, serif',
                        letterSpacing: '6px'
                    }}
                >
                    IVIE
                </span>
                
                {/* Loading text */}
                <span
                    style={{
                        fontSize: '12px',
                        color: '#999',
                        letterSpacing: '3px',
                        textTransform: 'uppercase'
                    }}
                >
                    Đang tải...
                </span>

                {/* Loading bar */}
                <div
                    style={{
                        width: '120px',
                        height: '3px',
                        background: '#eee',
                        borderRadius: '3px',
                        overflow: 'hidden'
                    }}
                >
                    <div
                        style={{
                            width: '40%',
                            height: '100%',
                            background: 'linear-gradient(90deg, #c9a86c, #d4b896)',
                            borderRadius: '3px',
                            animation: 'loadingBar 1s ease-in-out infinite'
                        }}
                    />
                </div>
            </div>

            <style>{`
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                @keyframes loadingBar {
                    0% { transform: translateX(-100%); }
                    50% { transform: translateX(150%); }
                    100% { transform: translateX(300%); }
                }
            `}</style>
        </div>
    );
}
