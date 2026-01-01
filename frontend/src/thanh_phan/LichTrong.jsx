import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/availability-calendar.css';

const LichTrong = () => {
    const [thangHienTai, setThangHienTai] = useState(new Date());
    
    // Dữ liệu mẫu ngày đã kín lịch (thực tế sẽ lấy từ API)
    const ngayKinLich = [
        // Tháng hiện tại
        new Date(2026, 0, 5),
        new Date(2026, 0, 12),
        new Date(2026, 0, 18),
        new Date(2026, 0, 19),
        new Date(2026, 0, 25),
        new Date(2026, 0, 26),
        // Tháng sau
        new Date(2026, 1, 1),
        new Date(2026, 1, 8),
        new Date(2026, 1, 14),
        new Date(2026, 1, 15),
        new Date(2026, 1, 22),
    ];

    // Ngày gần kín (còn 1-2 slot)
    const ngayGanKin = [
        new Date(2026, 0, 11),
        new Date(2026, 0, 17),
        new Date(2026, 1, 7),
        new Date(2026, 1, 21),
    ];

    const tenThang = [
        'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6',
        'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
    ];

    const tenThu = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];

    const layNgayTrongThang = (date) => {
        const nam = date.getFullYear();
        const thang = date.getMonth();
        const ngayDauThang = new Date(nam, thang, 1);
        const ngayCuoiThang = new Date(nam, thang + 1, 0);
        
        const ngays = [];
        const thuDauThang = ngayDauThang.getDay();
        
        // Thêm ngày trống đầu tháng
        for (let i = 0; i < thuDauThang; i++) {
            ngays.push(null);
        }
        
        // Thêm các ngày trong tháng
        for (let ngay = 1; ngay <= ngayCuoiThang.getDate(); ngay++) {
            ngays.push(new Date(nam, thang, ngay));
        }
        
        return ngays;
    };

    const kiemTraKinLich = (ngay) => {
        if (!ngay) return false;
        return ngayKinLich.some(d => 
            d.getDate() === ngay.getDate() && 
            d.getMonth() === ngay.getMonth() && 
            d.getFullYear() === ngay.getFullYear()
        );
    };

    const kiemTraGanKin = (ngay) => {
        if (!ngay) return false;
        return ngayGanKin.some(d => 
            d.getDate() === ngay.getDate() && 
            d.getMonth() === ngay.getMonth() && 
            d.getFullYear() === ngay.getFullYear()
        );
    };

    const kiemTraQuaKhu = (ngay) => {
        if (!ngay) return false;
        const homNay = new Date();
        homNay.setHours(0, 0, 0, 0);
        return ngay < homNay;
    };

    const kiemTraCuoiTuan = (ngay) => {
        if (!ngay) return false;
        const thu = ngay.getDay();
        return thu === 0 || thu === 6;
    };

    const thangTruoc = () => {
        setThangHienTai(new Date(thangHienTai.getFullYear(), thangHienTai.getMonth() - 1, 1));
    };

    const thangSau = () => {
        setThangHienTai(new Date(thangHienTai.getFullYear(), thangHienTai.getMonth() + 1, 1));
    };

    const ngays = layNgayTrongThang(thangHienTai);
    const soNgayKin = ngayKinLich.filter(d => d.getMonth() === thangHienTai.getMonth()).length;
    const tongNgayCuoiTuan = ngays.filter(d => d && kiemTraCuoiTuan(d) && !kiemTraQuaKhu(d)).length;

    return (
        <section className="availability-section">
            <div className="container">
                <div className="avail-header">
                    <div>
                        <h2 className="section-title">Lịch Trống Tháng Này</h2>
                        <p className="section-subtitle">Đặt sớm để giữ ngày đẹp cho bạn</p>
                    </div>
                    <div className="avail-stats">
                        <div className="stat-badge hot">
                            <span className="stat-num">{soNgayKin}</span>
                            <span className="stat-text">ngày đã kín</span>
                        </div>
                        <div className="stat-badge warning">
                            <span className="stat-num">{tongNgayCuoiTuan - soNgayKin}</span>
                            <span className="stat-text">cuối tuần còn trống</span>
                        </div>
                    </div>
                </div>

                <div className="calendar-wrapper">
                    <div className="calendar-nav">
                        <button onClick={thangTruoc} className="nav-btn">←</button>
                        <h3>{tenThang[thangHienTai.getMonth()]} {thangHienTai.getFullYear()}</h3>
                        <button onClick={thangSau} className="nav-btn">→</button>
                    </div>

                    <div className="calendar-grid">
                        {tenThu.map(thu => (
                            <div key={thu} className="calendar-header">{thu}</div>
                        ))}
                        
                        {ngays.map((ngay, idx) => {
                            const kinLich = kiemTraKinLich(ngay);
                            const ganKin = kiemTraGanKin(ngay);
                            const quaKhu = kiemTraQuaKhu(ngay);
                            const cuoiTuan = kiemTraCuoiTuan(ngay);
                            
                            let className = 'calendar-day';
                            if (!ngay) className += ' empty';
                            else if (quaKhu) className += ' past';
                            else if (kinLich) className += ' booked';
                            else if (ganKin) className += ' almost';
                            else if (cuoiTuan) className += ' weekend';
                            else className += ' available';
                            
                            return (
                                <div key={idx} className={className}>
                                    {ngay && (
                                        <>
                                            <span className="day-num">{ngay.getDate()}</span>
                                            {kinLich && <span className="day-status">Kín</span>}
                                            {ganKin && !kinLich && <span className="day-status hot">Hot</span>}
                                        </>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    <div className="calendar-legend">
                        <div className="legend-item">
                            <span className="legend-dot available"></span>
                            <span>Còn trống</span>
                        </div>
                        <div className="legend-item">
                            <span className="legend-dot weekend"></span>
                            <span>Cuối tuần</span>
                        </div>
                        <div className="legend-item">
                            <span className="legend-dot almost"></span>
                            <span>Gần kín</span>
                        </div>
                        <div className="legend-item">
                            <span className="legend-dot booked"></span>
                            <span>Đã kín</span>
                        </div>
                    </div>
                </div>

                <div className="avail-cta">
                    <div className="cta-content">
                        <h3>🔥 Ngày cuối tuần đang được đặt rất nhanh!</h3>
                        <p>Liên hệ ngay để giữ chỗ cho ngày trọng đại của bạn</p>
                    </div>
                    <Link to="/lien-he" className="cta-btn">ĐẶT LỊCH NGAY</Link>
                </div>
            </div>
        </section>
    );
};

export default LichTrong;
