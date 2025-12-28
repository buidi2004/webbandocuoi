import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const BoSuuTapTiLeVang = ({ danhSachAnh }) => {
  const [anhDuocChon, setAnhDuocChon] = useState(null);

  return (
    <>
      {/* Lưới ảnh */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
        {danhSachAnh.map((anh, viTri) => {
          // Xác định hướng: ngang (3:2) hoặc dọc (2:3)
          const laAnhDoc = anh.huong === 'doc';

          return (
            <motion.div
              key={viTri}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: viTri * 0.1 }}
              className={`relative group cursor-pointer ${
                laAnhDoc ? 'md:row-span-2' : ''
              }`}
              onClick={() => setAnhDuocChon(anh)}
            >
              {/* Khung viền vàng */}
              <div className="relative p-1 bg-gradient-to-br from-[#d4af37]/30 via-[#f4e5c3]/20 to-[#d4af37]/30 rounded-lg shadow-lg hover:shadow-2xl transition-all duration-500">
                {/* Container ảnh với tỉ lệ vàng */}
                <div
                  className={`relative overflow-hidden rounded-md ${
                    laAnhDoc ? 'aspect-[2/3]' : 'aspect-[3/2]'
                  }`}
                >
                  <img
                    src={anh.url}
                    alt={anh.moTa || `Ảnh ${viTri + 1}`}
                    className="w-full h-full object-cover transition-all duration-700 group-hover:scale-110 group-hover:brightness-110"
                  />

                  {/* Lớp phủ gradient */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div className="absolute bottom-0 left-0 right-0 p-4">
                      <p className="text-white text-sm font-medium">
                        {anh.moTa}
                      </p>
                      <p className="text-white/70 text-xs mt-1">
                        {laAnhDoc ? 'Dọc 2:3' : 'Ngang 3:2'}
                      </p>
                    </div>
                  </div>

                  {/* Góc trang trí vàng */}
                  <div className="absolute top-2 right-2 w-8 h-8 border-t-2 border-r-2 border-[#d4af37] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="absolute bottom-2 left-2 w-8 h-8 border-b-2 border-l-2 border-[#d4af37] opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>

                {/* Viền vàng bên trong */}
                <div className="absolute inset-0 border border-[#d4af37]/20 rounded-lg pointer-events-none" />
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Hộp thoại xem ảnh */}
      <AnimatePresence>
        {anhDuocChon && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 backdrop-blur-md flex items-center justify-center p-4"
            onClick={() => setAnhDuocChon(null)}
          >
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              className="relative max-w-5xl"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Khung vàng cho hộp thoại */}
              <div className="p-2 bg-gradient-to-br from-[#d4af37]/40 via-[#f4e5c3]/30 to-[#d4af37]/40 rounded-lg">
                <img
                  src={anhDuocChon.url}
                  alt={anhDuocChon.moTa}
                  className="max-w-full max-h-[85vh] object-contain rounded-md"
                />
              </div>

              {/* Mô tả */}
              <div className="mt-4 text-center">
                <p className="text-white text-lg font-medium">
                  {anhDuocChon.moTa}
                </p>
                <p className="text-white/60 text-sm mt-1">
                  IVIE Studio - Bộ Sưu Tập Cao Cấp
                </p>
              </div>

              {/* Nút đóng */}
              <button
                onClick={() => setAnhDuocChon(null)}
                className="absolute -top-12 right-0 text-white hover:text-[#d4af37] transition-colors"
              >
                <svg
                  className="w-8 h-8"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default BoSuuTapTiLeVang;

// ===== DỮ LIỆU MẪU =====
export const duLieuAnhTiLeVangMau = [
  {
    url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800',
    moTa: 'Váy Cưới Công Chúa',
    huong: 'doc', // 2:3
  },
  {
    url: 'https://images.unsplash.com/photo-1594552072238-6d4f0a7c3c8e?w=800',
    moTa: 'Bộ Sưu Tập Xuân',
    huong: 'ngang', // 3:2
  },
  {
    url: 'https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800',
    moTa: 'Váy Cưới Tối Giản',
    huong: 'doc',
  },
  {
    url: 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=800',
    moTa: 'Phong Cách Vintage',
    huong: 'ngang',
  },
  {
    url: 'https://images.unsplash.com/photo-1591604466107-ec97de577aff?w=800',
    moTa: 'Váy Cưới Boho',
    huong: 'doc',
  },
  {
    url: 'https://images.unsplash.com/photo-1595777216528-071e0127ccf4?w=800',
    moTa: 'Váy Cưới Ren',
    huong: 'ngang',
  },
];
