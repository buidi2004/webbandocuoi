import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const BoSuuTapGach = ({ danhSachAnh }) => {
  const [anhDuocChon, setAnhDuocChon] = useState(null);

  // Hiệu ứng container
  const hieuUngContainer = {
    anDi: { opacity: 0 },
    hienThi: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  // Hiệu ứng từng item
  const hieuUngItem = {
    anDi: { opacity: 0, y: 30 },
    hienThi: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: [0.25, 0.46, 0.45, 0.94],
      },
    },
  };

  return (
    <>
      {/* Lưới Masonry với hiệu ứng xuất hiện lần lượt */}
      <motion.div
        className="columns-3 sm:columns-4 md:columns-6 lg:columns-8 xl:columns-10 gap-2 space-y-2"
        variants={hieuUngContainer}
        initial="anDi"
        whileInView="hienThi"
        viewport={{ once: true, margin: '-100px' }}
      >
        {danhSachAnh.map((anh, viTri) => (
          <motion.div
            key={viTri}
            variants={hieuUngItem}
            className="break-inside-avoid"
          >
            <div
              className="relative group cursor-pointer overflow-hidden rounded-lg shadow-md hover:shadow-2xl transition-all duration-500"
              onClick={() => setAnhDuocChon(anh)}
              data-cursor="view"
            >
              {/* Ảnh với hiệu ứng phóng to */}
              <motion.img
                src={anh.url}
                alt={anh.moTa || `Ảnh ${viTri + 1}`}
                className="w-full h-auto object-cover"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.4, ease: 'easeOut' }}
              />

              {/* Lớp phủ khi hover */}
              <motion.div
                className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent flex flex-col items-center justify-center"
                initial={{ opacity: 0 }}
                whileHover={{ opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {/* Icon */}
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  whileHover={{ scale: 1, rotate: 0 }}
                  transition={{ duration: 0.4, ease: 'backOut' }}
                  className="mb-3"
                >
                  <svg
                    className="w-12 h-12 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"
                    />
                  </svg>
                </motion.div>

                {/* Mô tả */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  whileHover={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.3, delay: 0.1 }}
                  className="absolute bottom-0 left-0 right-0 p-4"
                >
                  <p className="text-white text-sm font-medium text-center">
                    {anh.moTa}
                  </p>
                  <p className="text-white/70 text-xs text-center mt-1">
                    Click để xem chi tiết
                  </p>
                </motion.div>
              </motion.div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Hộp thoại xem ảnh lớn */}
      <AnimatePresence>
        {anhDuocChon && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/95 backdrop-blur-lg flex items-center justify-center p-4"
            onClick={() => setAnhDuocChon(null)}
          >
            {/* Container ảnh */}
            <motion.div
              initial={{ scale: 0.8, opacity: 0, rotateY: -15 }}
              animate={{ scale: 1, opacity: 1, rotateY: 0 }}
              exit={{ scale: 0.8, opacity: 0, rotateY: 15 }}
              transition={{
                duration: 0.5,
                ease: [0.25, 0.46, 0.45, 0.94],
              }}
              className="relative max-w-5xl"
              onClick={(e) => e.stopPropagation()}
            >
              <img
                src={anhDuocChon.url}
                alt={anhDuocChon.moTa}
                className="max-w-full max-h-[85vh] object-contain rounded-lg shadow-2xl"
              />

              {/* Mô tả với nền gradient */}
              <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="mt-6 text-center"
              >
                <div className="inline-block bg-gradient-to-r from-[#b59410]/20 via-[#d4af37]/30 to-[#b59410]/20 px-8 py-3 rounded-full backdrop-blur-sm">
                  <p className="text-white text-lg font-medium">
                    {anhDuocChon.moTa}
                  </p>
                  <p className="text-white/60 text-sm mt-1">
                    Bộ Sưu Tập IVIE Studio
                  </p>
                </div>
              </motion.div>
            </motion.div>

            {/* Nút đóng */}
            <motion.button
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0 }}
              transition={{ delay: 0.2 }}
              onClick={() => setAnhDuocChon(null)}
              className="absolute top-8 right-8 w-12 h-12 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-sm transition-all"
              whileHover={{ scale: 1.1, rotate: 90 }}
              whileTap={{ scale: 0.9 }}
            >
              <svg
                className="w-6 h-6"
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
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default BoSuuTapGach;
