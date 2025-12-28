import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

const CuonPhongTo = () => {
  const containerRef = useRef(null);
  
  // Theo dõi tiến trình cuộn
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  // Các giá trị biến đổi theo cuộn
  const tiLe = useTransform(scrollYProgress, [0, 0.5, 1], [1, 1.5, 2]);
  const doMo = useTransform(scrollYProgress, [0, 0.3, 0.6, 1], [0.3, 1, 1, 0.8]);
  const doMoChu = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6], [0, 1, 1, 0]);
  const viTriChuY = useTransform(scrollYProgress, [0, 0.3], [100, 0]);

  return (
    <div ref={containerRef} className="relative bg-gradient-to-br from-[#f8f6f3] to-[#e8e4df]">
      {/* Container cuộn - Chiều cao 300vh */}
      <div className="h-[300vh] relative">
        
        {/* Container cố định */}
        <div className="sticky top-0 h-screen flex items-center justify-center overflow-hidden">
          
          {/* Các phần tử trang trí nền */}
          <motion.div 
            className="absolute inset-0 opacity-10"
            style={{ opacity: useTransform(scrollYProgress, [0, 0.5], [0.1, 0.3]) }}
          >
            <div className="absolute top-20 left-20 w-64 h-64 bg-[#b59410] rounded-full blur-3xl" />
            <div className="absolute bottom-20 right-20 w-96 h-96 bg-[#d4af37] rounded-full blur-3xl" />
          </motion.div>

          {/* Ảnh chính với hiệu ứng phóng to */}
          <motion.div
            style={{ scale: tiLe, opacity: doMo }}
            className="relative z-10"
          >
            <img
              src="https://images.unsplash.com/photo-1519741497674-611481863552?w=1200&q=80"
              alt="Áo cưới IVIE Studio"
              className="w-[600px] h-[800px] object-cover rounded-lg shadow-2xl"
            />
            
            {/* Lớp phủ gradient tạo chiều sâu */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent rounded-lg" />
          </motion.div>

          {/* Chữ - Xuất hiện và biến mất */}
          <motion.div
            style={{ opacity: doMoChu, y: viTriChuY }}
            className="absolute top-1/4 left-1/2 transform -translate-x-1/2 text-center z-20"
          >
            <h1 className="text-6xl md:text-8xl font-serif text-[#2c2c2c] mb-4 tracking-wider">
              IVIE STUDIO
            </h1>
            <p className="text-xl md:text-2xl text-[#6b6b6b] font-light tracking-widest">
              Khoảnh khắc hạnh phúc của bạn
            </p>
          </motion.div>

          {/* Chữ phía dưới */}
          <motion.div
            style={{ 
              opacity: useTransform(scrollYProgress, [0.4, 0.6, 0.8], [0, 1, 0]),
              y: useTransform(scrollYProgress, [0.4, 0.6], [50, 0])
            }}
            className="absolute bottom-20 left-1/2 transform -translate-x-1/2 text-center z-20"
          >
            <p className="text-3xl md:text-4xl font-serif text-[#2c2c2c] italic">
              Sang trọng • Tinh tế • Đẳng cấp
            </p>
          </motion.div>

          {/* Chỉ báo cuộn */}
          <motion.div
            style={{ 
              opacity: useTransform(scrollYProgress, [0, 0.1], [1, 0])
            }}
            className="absolute bottom-10 left-1/2 transform -translate-x-1/2 z-20"
          >
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 1.5, repeat: Infinity }}
              className="flex flex-col items-center"
            >
              <span className="text-[#6b6b6b] text-sm mb-2 tracking-widest">CUỘN XUỐNG</span>
              <svg 
                className="w-6 h-6 text-[#b59410]" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path 
                  strokeLinecap="round" 
                  strokeLinejoin="round" 
                  strokeWidth={2} 
                  d="M19 14l-7 7m0 0l-7-7m7 7V3" 
                />
              </svg>
            </motion.div>
          </motion.div>

          {/* Thanh tiến trình */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#b59410] to-[#d4af37] origin-left z-30"
            style={{ scaleX: scrollYProgress }}
          />
        </div>
      </div>

      {/* Phần kết thúc */}
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="text-center px-4">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-5xl md:text-6xl font-serif text-[#2c2c2c] mb-6">
              Bộ Sưu Tập Áo Cưới
            </h2>
            <p className="text-xl text-[#6b6b6b] max-w-2xl mx-auto mb-8">
              Khám phá những thiết kế áo cưới độc đáo, được chế tác tỉ mỉ 
              để tôn vinh vẻ đẹp của bạn trong ngày trọng đại
            </p>
            <button className="px-8 py-4 bg-[#b59410] text-white rounded-full hover:bg-[#d4af37] transition-all duration-300 text-lg font-medium">
              Xem Bộ Sưu Tập
            </button>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default CuonPhongTo;
