import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ChevronLeft, ChevronRight } from 'lucide-react';

const AlbumThongMinh = ({ danhSachAnh }) => {
  const [viTriDuocChon, setViTriDuocChon] = useState(null);
  const [diemBatDauCham, setDiemBatDauCham] = useState(0);
  const [diemKetThucCham, setDiemKetThucCham] = useState(0);

  const moHopThoai = (viTri) => setViTriDuocChon(viTri);
  const dongHopThoai = () => setViTriDuocChon(null);

  const diChuyenTruoc = () => {
    setViTriDuocChon((truoc) => (truoc > 0 ? truoc - 1 : danhSachAnh.length - 1));
  };

  const diChuyenSau = () => {
    setViTriDuocChon((truoc) => (truoc < danhSachAnh.length - 1 ? truoc + 1 : 0));
  };

  // Xử lý vuốt trên mobile
  const xuLyBatDauCham = (e) => {
    setDiemBatDauCham(e.targetTouches[0].clientX);
  };

  const xuLyDiChuyenCham = (e) => {
    setDiemKetThucCham(e.targetTouches[0].clientX);
  };

  const xuLyKetThucCham = () => {
    if (diemBatDauCham - diemKetThucCham > 75) {
      diChuyenSau();
    }
    if (diemBatDauCham - diemKetThucCham < -75) {
      diChuyenTruoc();
    }
  };

  // Điều hướng bằng bàn phím
  const xuLyPhimBam = (e) => {
    if (viTriDuocChon === null) return;
    if (e.key === 'ArrowLeft') diChuyenTruoc();
    if (e.key === 'ArrowRight') diChuyenSau();
    if (e.key === 'Escape') dongHopThoai();
  };

  return (
    <>
      {/* Lưới ảnh */}
      <div className="grid grid-cols-5 md:grid-cols-7 lg:grid-cols-9 xl:grid-cols-12 gap-1.5 p-2">
        {danhSachAnh.map((anh, viTri) => (
          <motion.div
            key={viTri}
            className="relative aspect-square overflow-hidden rounded cursor-pointer group"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => moHopThoai(viTri)}
          >
            <img
              src={anh.url}
              alt={anh.moTa || `Ảnh ${viTri + 1}`}
              className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300" />
          </motion.div>
        ))}
      </div>

      {/* Hộp thoại xem ảnh */}
      <AnimatePresence>
        {viTriDuocChon !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center"
            onClick={dongHopThoai}
            onKeyDown={xuLyPhimBam}
            tabIndex={0}
          >
            {/* Nền mờ */}
            <div className="absolute inset-0 bg-black/80 backdrop-blur-md" />

            {/* Nút đóng */}
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="absolute top-4 right-4 z-50 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
              onClick={dongHopThoai}
            >
              <X size={24} />
            </motion.button>

            {/* Nút điều hướng */}
            {danhSachAnh.length > 1 && (
              <>
                <motion.button
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="absolute left-4 z-50 p-3 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    diChuyenTruoc();
                  }}
                >
                  <ChevronLeft size={28} />
                </motion.button>

                <motion.button
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="absolute right-4 z-50 p-3 rounded-full bg-white/10 hover:bg-white/20 text-white transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    diChuyenSau();
                  }}
                >
                  <ChevronRight size={28} />
                </motion.button>
              </>
            )}

            {/* Container ảnh */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
              className="relative max-w-7xl max-h-[90vh] mx-4"
              onClick={(e) => e.stopPropagation()}
              onTouchStart={xuLyBatDauCham}
              onTouchMove={xuLyDiChuyenCham}
              onTouchEnd={xuLyKetThucCham}
            >
              <img
                src={danhSachAnh[viTriDuocChon].url}
                alt={danhSachAnh[viTriDuocChon].moTa}
                className="max-w-full max-h-[80vh] object-contain rounded-lg shadow-2xl"
              />

              {/* Mô tả */}
              {danhSachAnh[viTriDuocChon].moTa && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent rounded-b-lg"
                >
                  <p className="text-white text-center text-sm md:text-base">
                    {danhSachAnh[viTriDuocChon].moTa}
                  </p>
                  <p className="text-white/60 text-center text-xs mt-1">
                    {viTriDuocChon + 1} / {danhSachAnh.length}
                  </p>
                </motion.div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default AlbumThongMinh;
