import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MoveHorizontal } from 'lucide-react';

const ThanhTruotTruocSau = ({ anhTruoc, anhSau, moTa = 'So sánh ảnh trước và sau' }) => {
  const [viTriThanhtruot, setViTriThanhTruot] = useState(50);
  const [dangKeo, setDangKeo] = useState(false);
  const containerRef = useRef(null);

  const xuLyDiChuyen = (toaDoX) => {
    if (!containerRef.current) return;

    const khung = containerRef.current.getBoundingClientRect();
    const x = toaDoX - khung.left;
    const phanTram = (x / khung.width) * 100;

    setViTriThanhTruot(Math.max(0, Math.min(100, phanTram)));
  };

  const xuLyBatDauKeo = () => setDangKeo(true);
  const xuLyKetThucKeo = () => setDangKeo(false);

  const xuLyDiChuyenChuot = (e) => {
    if (!dangKeo) return;
    xuLyDiChuyen(e.clientX);
  };

  const xuLyDiChuyenCham = (e) => {
    xuLyDiChuyen(e.touches[0].clientX);
  };

  useEffect(() => {
    const xuLyKetThucChuotToanCuc = () => setDangKeo(false);
    const xuLyDiChuyenChuotToanCuc = (e) => {
      if (dangKeo) xuLyDiChuyen(e.clientX);
    };

    document.addEventListener('mouseup', xuLyKetThucChuotToanCuc);
    document.addEventListener('mousemove', xuLyDiChuyenChuotToanCuc);

    return () => {
      document.removeEventListener('mouseup', xuLyKetThucChuotToanCuc);
      document.removeEventListener('mousemove', xuLyDiChuyenChuotToanCuc);
    };
  }, [dangKeo]);

  return (
    <div className="relative w-full max-w-4xl mx-auto">
      <div
        ref={containerRef}
        className="relative overflow-hidden rounded-lg shadow-2xl cursor-ew-resize select-none"
        onMouseDown={xuLyBatDauKeo}
        onMouseMove={xuLyDiChuyenChuot}
        onTouchMove={xuLyDiChuyenCham}
        onTouchEnd={xuLyKetThucKeo}
      >
        {/* Ảnh SAU (Nền) */}
        <div className="relative w-full">
          <img
            src={anhSau}
            alt={`${moTa} - Sau`}
            className="w-full h-auto block"
            draggable={false}
          />

          {/* Nhãn SAU */}
          <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: viTriThanhtruot < 85 ? 1 : 0 }}
            className="absolute top-4 right-4 px-3 py-1.5 bg-black/70 text-white text-xs font-bold rounded-full backdrop-blur-sm"
          >
            SAU
          </motion.div>
        </div>

        {/* Ảnh TRƯỚC (Lớp phủ với clip) */}
        <div
          className="absolute inset-0 overflow-hidden"
          style={{ clipPath: `inset(0 ${100 - viTriThanhtruot}% 0 0)` }}
        >
          <img
            src={anhTruoc}
            alt={`${moTa} - Trước`}
            className="w-full h-full object-cover"
            draggable={false}
          />

          {/* Nhãn TRƯỚC */}
          <motion.div
            initial={{ opacity: 1 }}
            animate={{ opacity: viTriThanhtruot > 15 ? 1 : 0 }}
            className="absolute top-4 left-4 px-3 py-1.5 bg-black/70 text-white text-xs font-bold rounded-full backdrop-blur-sm"
          >
            TRƯỚC
          </motion.div>
        </div>

        {/* Thanh chia */}
        <div
          className="absolute top-0 bottom-0 w-1 bg-white shadow-lg"
          style={{ left: `${viTriThanhtruot}%`, transform: 'translateX(-50%)' }}
        >
          {/* Tay cầm thanh trượt */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <motion.div
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="w-12 h-12 bg-white rounded-full shadow-xl flex items-center justify-center cursor-grab active:cursor-grabbing"
            >
              <MoveHorizontal size={20} className="text-gray-700" />
            </motion.div>
          </div>

          {/* Mũi tên trên */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-t-[8px] border-t-white" />

          {/* Mũi tên dưới */}
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[8px] border-b-white" />
        </div>
      </div>

      {/* Hướng dẫn */}
      <p className="text-center text-sm text-gray-500 mt-4">
        Kéo thanh trượt để so sánh ảnh trước và sau chỉnh sửa
      </p>
    </div>
  );
};

export default ThanhTruotTruocSau;
