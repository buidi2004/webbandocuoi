import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Eye } from 'lucide-react';

const GanTheSanPham = ({ duongDanAnh, danhSachThe }) => {
  const [theDangHoatDong, setTheDangHoatDong] = useState(null);
  const dieuHuong = useNavigate();

  const xuLyClickThe = (the) => {
    setTheDangHoatDong(theDangHoatDong === the.id ? null : the.id);
  };

  const xuLyXemChiTiet = (maSanPham) => {
    dieuHuong(`/san-pham/${maSanPham}`);
  };

  return (
    <div className="relative w-full max-w-5xl mx-auto">
      {/* Ảnh chính */}
      <div className="relative overflow-hidden rounded-lg shadow-2xl">
        <img
          src={duongDanAnh}
          alt="Bộ Sưu Tập IVIE Studio"
          className="w-full h-auto"
        />

        {/* Các điểm đánh dấu sản phẩm */}
        {danhSachThe.map((the) => (
          <div
            key={the.id}
            className="absolute"
            style={{ top: `${the.viTriTren}%`, left: `${the.viTriTrai}%` }}
          >
            {/* Điểm đánh dấu với hiệu ứng nhấp nháy */}
            <motion.div
              className="relative cursor-pointer"
              onClick={() => xuLyClickThe(the)}
              whileHover={{ scale: 1.2 }}
              whileTap={{ scale: 0.9 }}
            >
              {/* Vòng nhấp nháy */}
              <motion.div
                className="absolute inset-0 rounded-full bg-white/40"
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.6, 0, 0.6],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: 'easeInOut',
                }}
                style={{ width: '40px', height: '40px', marginLeft: '-20px', marginTop: '-20px' }}
              />

              {/* Điểm trung tâm */}
              <div className="relative w-5 h-5 -ml-2.5 -mt-2.5 rounded-full bg-white border-2 border-[#b59410] shadow-lg flex items-center justify-center">
                <div className="w-2 h-2 rounded-full bg-[#b59410]" />
              </div>
            </motion.div>

            {/* Thẻ thông tin sản phẩm */}
            <AnimatePresence>
              {theDangHoatDong === the.id && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.8, y: 10 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.8, y: 10 }}
                  transition={{ type: 'spring', damping: 20, stiffness: 300 }}
                  className="absolute z-10 mt-2 -translate-x-1/2 left-1/2"
                  style={{ minWidth: '200px' }}
                >
                  {/* Mũi tên */}
                  <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 bg-white rotate-45 shadow-lg" />

                  {/* Nội dung thẻ */}
                  <div className="relative bg-white rounded-lg shadow-2xl overflow-hidden">
                    {/* Ảnh sản phẩm */}
                    <div className="relative h-32 overflow-hidden">
                      <img
                        src={the.anhSanPham}
                        alt={the.tenSanPham}
                        className="w-full h-full object-cover"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                    </div>

                    {/* Thông tin sản phẩm */}
                    <div className="p-3">
                      <h4 className="font-semibold text-gray-900 text-sm mb-1">
                        {the.tenSanPham}
                      </h4>
                      <p className="text-xs text-gray-600 mb-3">
                        Mã: {the.maSanPham}
                      </p>

                      {/* Nút xem chi tiết */}
                      <button
                        onClick={() => xuLyXemChiTiet(the.idSanPham)}
                        className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-[#b59410] hover:bg-[#9a7d0d] text-white text-sm font-medium rounded-lg transition-colors"
                      >
                        <Eye size={16} />
                        Xem chi tiết
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>

      {/* Hướng dẫn */}
      <p className="text-center text-sm text-gray-500 mt-4">
        Click vào các điểm sáng để xem thông tin sản phẩm
      </p>
    </div>
  );
};

export default GanTheSanPham;

// ===== DỮ LIỆU MẪU =====
export const duLieuTheMau = [
  {
    id: 1,
    viTriTren: 35,
    viTriTrai: 25,
    idSanPham: 1,
    tenSanPham: 'Váy Cưới Công Chúa Ren Pháp',
    maSanPham: 'WD-001',
    anhSanPham: 'https://placehold.co/400x300/f7f1ea/333?text=Váy+Mẫu+1',
  },
  {
    id: 2,
    viTriTren: 45,
    viTriTrai: 60,
    idSanPham: 2,
    tenSanPham: 'Váy Cưới Đuôi Cá Sang Trọng',
    maSanPham: 'WD-002',
    anhSanPham: 'https://placehold.co/400x300/fff0f0/333?text=Váy+Mẫu+2',
  },
  {
    id: 3,
    viTriTren: 55,
    viTriTrai: 80,
    idSanPham: 3,
    tenSanPham: 'Váy Cưới Tối Giản Hiện Đại',
    maSanPham: 'WD-003',
    anhSanPham: 'https://placehold.co/400x300/e6f7f0/333?text=Váy+Mẫu+3',
  },
];
