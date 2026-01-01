import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

// Default sections data với ảnh placeholder
const defaultSections = [
    {
        id: 1,
        title: "Chụp Ảnh Cưới Chuyên Nghiệp",
        description: "Lưu giữ khoảnh khắc hạnh phúc nhất của bạn với đội ngũ nhiếp ảnh gia giàu kinh nghiệm. Mỗi bức ảnh là một câu chuyện tình yêu được kể bằng ánh sáng và cảm xúc.",
        image: "https://picsum.photos/800/600?random=10",
        highlight: "500+ cặp đôi tin tưởng"
    },
    {
        id: 2,
        title: "Studio Hiện Đại",
        description: "Không gian chụp ảnh sang trọng với ánh sáng tự nhiên và thiết bị cao cấp. Studio được thiết kế để tôn vinh vẻ đẹp tự nhiên của bạn trong từng khung hình.",
        image: "https://picsum.photos/800/600?random=20",
        highlight: "3 studio tại Hà Nội"
    },
    {
        id: 3,
        title: "Trang Điểm Cô Dâu",
        description: "Makeup artist chuyên nghiệp giúp bạn tỏa sáng trong ngày trọng đại. Phong cách trang điểm tinh tế, phù hợp với từng gương mặt và concept chụp ảnh.",
        image: "https://picsum.photos/800/600?random=30",
        highlight: "Top Artist được yêu thích"
    },
    {
        id: 4,
        title: "Album & In Ấn Cao Cấp",
        description: "Album cưới cao cấp với chất liệu nhập khẩu, bền đẹp theo thời gian. Thiết kế tinh xảo, in ấn sắc nét để lưu giữ kỷ niệm trọn đời.",
        image: "https://picsum.photos/800/600?random=40",
        highlight: "Bảo hành trọn đời"
    }
];

// Component cho từng section text - tách riêng để tuân thủ rules of hooks
const SectionTextItem = ({ section, scrollYProgress, index, totalSections }) => {
    const sectionStart = index / totalSections;
    const sectionEnd = (index + 1) / totalSections;
    
    // Section đầu tiên hiển thị ngay với opacity = 1
    const opacity = useTransform(
        scrollYProgress,
        index === 0 
            ? [0, sectionEnd - 0.05, sectionEnd]
            : [sectionStart, sectionStart + 0.05, sectionEnd - 0.05, sectionEnd],
        index === 0
            ? [1, 1, 0.3]
            : [0.3, 1, 1, 0.3]
    );
    const y = useTransform(
        scrollYProgress,
        index === 0
            ? [0, sectionEnd - 0.05, sectionEnd]
            : [sectionStart, sectionStart + 0.05, sectionEnd - 0.05, sectionEnd],
        index === 0
            ? [0, 0, -50]
            : [50, 0, 0, -50]
    );

    return (
        <motion.div
            style={{ opacity, y }}
            className="h-screen flex flex-col justify-center px-6 md:px-12 lg:px-16"
        >
            {section.highlight && (
                <span className="inline-block px-4 py-2 mb-4 text-sm font-medium rounded-full bg-[#b59410]/10 text-[#b59410] w-fit">
                    {section.highlight}
                </span>
            )}
            <h2 
                className="text-3xl md:text-4xl lg:text-5xl font-bold text-[#2c2c2c] mb-6 leading-tight"
                style={{ fontFamily: "'Be Vietnam Pro', system-ui, sans-serif" }}
            >
                {section.title}
            </h2>
            <p 
                className="text-lg md:text-xl text-gray-600 leading-relaxed max-w-lg"
                style={{ fontFamily: "'Be Vietnam Pro', system-ui, sans-serif" }}
            >
                {section.description}
            </p>
            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="mt-8 px-8 py-4 bg-[#2c2c2c] text-white rounded-full font-medium hover:bg-[#b59410] transition-colors w-fit"
            >
                Tìm hiểu thêm
            </motion.button>
        </motion.div>
    );
};

// Component cho từng image - tách riêng để tuân thủ rules of hooks
const ImageItem = ({ section, scrollYProgress, index, totalSections }) => {
    const start = index / totalSections;
    const end = (index + 1) / totalSections;
    const mid = (start + end) / 2;
    
    // Ảnh đầu tiên hiển thị ngay với opacity = 1
    const opacity = useTransform(
        scrollYProgress,
        index === 0
            ? [0, mid, end]
            : [start, mid, end],
        index === 0
            ? [1, 1, 0]
            : [0, 1, index === totalSections - 1 ? 1 : 0]
    );
    const y = useTransform(
        scrollYProgress, 
        [start, end], 
        index === 0 ? [0, -100] : [100, -100]
    );
    const scale = useTransform(
        scrollYProgress, 
        [start, mid, end], 
        index === 0 ? [1, 1, 1.05] : [0.9, 1, 1.05]
    );

    return (
        <motion.div
            style={{ opacity, y, scale, willChange: 'transform, opacity' }}
            className="absolute inset-0"
        >
            <img
                src={section.image}
                alt={section.title}
                loading="lazy"
                className="w-full h-full object-cover rounded-2xl shadow-2xl"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent rounded-2xl" />
        </motion.div>
    );
};


// Component indicator dot - tách riêng
const IndicatorDot = ({ scrollYProgress, index, totalSections }) => {
    const start = index / totalSections;
    const end = (index + 1) / totalSections;
    const mid = (start + end) / 2;
    
    const scale = useTransform(scrollYProgress, [start, mid, end], [1, 1.5, 1]);
    const bgColor = useTransform(
        scrollYProgress,
        [start, mid, end],
        ['#d1d5db', '#b59410', '#d1d5db']
    );

    return (
        <motion.div
            style={{ scale, backgroundColor: bgColor }}
            className="w-2 h-2 rounded-full"
        />
    );
};

// Component mobile section - tách riêng
const MobileSectionItem = ({ section, scrollYProgress, index, totalSections }) => {
    const sectionStart = index / totalSections;
    const sectionEnd = (index + 1) / totalSections;
    
    const opacity = useTransform(
        scrollYProgress,
        [sectionStart, sectionStart + 0.1, sectionEnd - 0.1, sectionEnd],
        [0, 1, 1, 0]
    );
    const y = useTransform(
        scrollYProgress,
        [sectionStart, sectionStart + 0.1, sectionEnd - 0.1, sectionEnd],
        [30, 0, 0, -30]
    );

    return (
        <motion.div className="h-screen flex flex-col justify-center px-6 py-12">
            <motion.div style={{ opacity, y }} className="relative mb-8">
                <img
                    src={section.image}
                    alt={section.title}
                    loading="lazy"
                    className="w-full h-[250px] object-cover rounded-2xl shadow-xl"
                />
            </motion.div>
            <motion.div style={{ opacity, y }}>
                {section.highlight && (
                    <span className="inline-block px-3 py-1.5 mb-3 text-xs font-medium rounded-full bg-[#b59410]/10 text-[#b59410]">
                        {section.highlight}
                    </span>
                )}
                <h2 
                    className="text-2xl font-bold text-[#2c2c2c] mb-4"
                    style={{ fontFamily: "'Be Vietnam Pro', system-ui, sans-serif" }}
                >
                    {section.title}
                </h2>
                <p className="text-base text-gray-600 leading-relaxed">
                    {section.description}
                </p>
            </motion.div>
        </motion.div>
    );
};

// Sticky Image Stack component
const StickyImageStack = ({ sections, scrollYProgress }) => {
    return (
        <div className="sticky top-0 h-screen flex items-center justify-center overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-[#f8f6f3] to-[#e8e4df]" />
            <div className="absolute top-20 right-20 w-64 h-64 bg-[#b59410]/10 rounded-full blur-3xl" />
            <div className="absolute bottom-20 left-20 w-96 h-96 bg-[#d4af37]/10 rounded-full blur-3xl" />
            
            <div className="relative w-[300px] md:w-[400px] lg:w-[500px] h-[400px] md:h-[500px] lg:h-[600px]">
                {sections.map((section, index) => (
                    <ImageItem
                        key={section.id}
                        section={section}
                        scrollYProgress={scrollYProgress}
                        index={index}
                        totalSections={sections.length}
                    />
                ))}
            </div>
            
            <div className="absolute right-8 top-1/2 -translate-y-1/2 flex flex-col gap-3">
                {sections.map((_, index) => (
                    <IndicatorDot
                        key={index}
                        scrollYProgress={scrollYProgress}
                        index={index}
                        totalSections={sections.length}
                    />
                ))}
            </div>
        </div>
    );
};

// Main component
const HieuUngCuonDinh = ({ sections: propSections, className = '' }) => {
    const containerRef = useRef(null);
    const sections = propSections || defaultSections;
    
    const { scrollYProgress } = useScroll({
        target: containerRef,
        offset: ["start start", "end end"]
    });

    return (
        <div 
            ref={containerRef} 
            className={`relative bg-[#f8f6f3] ${className}`}
            style={{ height: `${sections.length * 100}vh` }}
        >
            {/* Desktop layout */}
            <div className="hidden md:grid md:grid-cols-[40%_60%] h-full">
                <div className="relative z-10">
                    {sections.map((section, index) => (
                        <SectionTextItem
                            key={section.id}
                            section={section}
                            scrollYProgress={scrollYProgress}
                            index={index}
                            totalSections={sections.length}
                        />
                    ))}
                </div>
                <div className="relative">
                    <StickyImageStack sections={sections} scrollYProgress={scrollYProgress} />
                </div>
            </div>
            
            {/* Mobile layout */}
            <div className="md:hidden">
                {sections.map((section, index) => (
                    <MobileSectionItem
                        key={section.id}
                        section={section}
                        scrollYProgress={scrollYProgress}
                        index={index}
                        totalSections={sections.length}
                    />
                ))}
            </div>
            
            {/* Progress bar */}
            <motion.div
                className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#b59410] to-[#d4af37] origin-left z-50"
                style={{ scaleX: scrollYProgress }}
            />
        </div>
    );
};

export default HieuUngCuonDinh;
