import { motion } from 'framer-motion';

const BoSuuTapDanXen = ({ danhSachAnh }) => {
  // Nhóm ảnh thành từng cặp
  const nhomAnh = [];
  for (let i = 0; i < danhSachAnh.length; i += 2) {
    nhomAnh.push({
      anhChinh: danhSachAnh[i],
      anhPhu: danhSachAnh[i + 1] || null,
    });
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12 space-y-12">
      {nhomAnh.map((nhom, viTri) => {
        const laChan = viTri % 2 === 0;

        return (
          <motion.div
            key={viTri}
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className={`grid grid-cols-1 lg:grid-cols-2 gap-6 ${
              laChan ? '' : 'lg:grid-flow-dense'
            }`}
          >
            {/* Ảnh lớn */}
            <div
              className={`relative group overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 ${
                laChan ? 'lg:col-start-1' : 'lg:col-start-2'
              }`}
            >
              <div className="aspect-[4/3] overflow-hidden">
                <img
                  src={nhom.anhChinh.url}
                  alt={nhom.anhChinh.moTa}
                  className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 group-hover:brightness-110"
                />
              </div>
              
              {/* Lớp phủ mô tả */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute bottom-0 left-0 right-0 p-6">
                  <h3 className="text-white text-xl font-semibold mb-2">
                    {nhom.anhChinh.moTa}
                  </h3>
                  <p className="text-white/80 text-sm">
                    Bộ Sưu Tập IVIE Studio
                  </p>
                </div>
              </div>
            </div>

            {/* Ảnh nhỏ hoặc nội dung */}
            {nhom.anhPhu && (
              <div
                className={`relative group overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 ${
                  laChan ? 'lg:col-start-2' : 'lg:col-start-1'
                }`}
              >
                <div className="aspect-[4/3] overflow-hidden">
                  <img
                    src={nhom.anhPhu.url}
                    alt={nhom.anhPhu.moTa}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110 group-hover:brightness-110"
                  />
                </div>

                {/* Lớp phủ mô tả */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="absolute bottom-0 left-0 right-0 p-6">
                    <h3 className="text-white text-xl font-semibold mb-2">
                      {nhom.anhPhu.moTa}
                    </h3>
                    <p className="text-white/80 text-sm">
                      Bộ Sưu Tập IVIE Studio
                    </p>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        );
      })}
    </div>
  );
};

export default BoSuuTapDanXen;
