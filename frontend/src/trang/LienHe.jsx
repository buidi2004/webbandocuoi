import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import NutBam from '../thanh_phan/NutBam';
import The from '../thanh_phan/The';
import '../styles/contact.css';
import { lienHeAPI, khieuNaiAPI } from '../api/khach_hang';
import { useToast } from '../thanh_phan/Toast';
import { trackGenerateLead } from '../utils/analytics';


const LienHe = () => {
    const [activeTab, setActiveTab] = useState('consult'); // consult, complaint, partner
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const { addToast } = useToast();

    useEffect(() => {
        const storedUser = localStorage.getItem('ivie_user');
        if (storedUser) setUser(JSON.parse(storedUser));
    }, []);

    // Form Tư vấn
    const [duLieuConsult, setDuLieuConsult] = useState({
        name: '', phone: '', email: '', service: 'wedding_photo', address: '', message: '', date: '',
        chi_nhanh: 'cao_lanh', ngan_sach: ''
    });
    const [loadingConsult, setLoadingConsult] = useState(false);

    // Form Khiếu nại
    const [duLieuComplaint, setDuLieuComplaint] = useState({
        title: '', content: '', customer_name: '', customer_phone: ''
    });
    const [loadingComplaint, setLoadingComplaint] = useState(false);

    const xuLyThayDoiConsult = (e) => setDuLieuConsult({ ...duLieuConsult, [e.target.name]: e.target.value });
    const xuLyThayDoiComplaint = (e) => setDuLieuComplaint({ ...duLieuComplaint, [e.target.name]: e.target.value });

    const guiConsult = async (e) => {
        e.preventDefault();
        setLoadingConsult(true);
        try {
            const tenChiNhanh = { cao_lanh: 'Cao Lãnh', sa_dec: 'Sa Đéc', can_tho: 'Cần Thơ' };
            const tenNganSach = { duoi_5tr: 'Dưới 5 triệu', '5_10tr': '5-10 triệu', '10_20tr': '10-20 triệu', '20_50tr': '20-50 triệu', tren_50tr: 'Trên 50 triệu' };
            const payload = {
                name: duLieuConsult.name,
                phone: duLieuConsult.phone,
                email: duLieuConsult.email,
                address: duLieuConsult.address,
                message: `[Dịch vụ: ${duLieuConsult.service}] [Chi nhánh: ${tenChiNhanh[duLieuConsult.chi_nhanh] || duLieuConsult.chi_nhanh}] [Ngân sách: ${tenNganSach[duLieuConsult.ngan_sach] || 'Chưa chọn'}] [Ngày: ${duLieuConsult.date}] ${duLieuConsult.message}`
            };
            await lienHeAPI.datLich(payload);
            
            // Track GA4 event
            trackGenerateLead('consult', { service: duLieuConsult.service });
            
            // Redirect to Thank You page
            navigate('/cam-on', { 
                state: { 
                    formType: 'consult',
                    productName: duLieuConsult.service 
                } 
            });
        } catch (loi) {
            addToast({ message: 'Không thể gửi yêu cầu.', type: 'error' });
        } finally {
            setLoadingConsult(false);
        }
    };

    const guiComplaint = async (e) => {
        e.preventDefault();
        setLoadingComplaint(true);
        try {
            await khieuNaiAPI.gui(duLieuComplaint, user?.id);
            
            // Track GA4 event
            trackGenerateLead('complaint');
            
            // Redirect to Thank You page
            navigate('/cam-on', { 
                state: { formType: 'complaint' } 
            });
        } catch (loi) {
            addToast({ message: 'Không thể gửi khiếu nại.', type: 'error' });
        } finally {
            setLoadingComplaint(false);
        }
    };

    return (
        <div className="contact-page">
            <section className="contact-hero">
                <div className="contact-hero-content">
                    <h1 className="page-title" data-sal="slide-up" data-sal-delay="100" data-sal-duration="600">Trung Tâm Hỗ Trợ IVIE</h1>
                    <p className="page-subtitle" data-sal="slide-up" data-sal-delay="200" data-sal-duration="600">Chúng tôi luôn sẵn sàng lắng nghe và đồng hành cùng bạn</p>
                </div>
            </section>

            <section className="contact-section">
                <div className="container">
                    <div className="contact-tabs" data-sal="fade" data-sal-delay="300">
                        <button className={`tab-btn ${activeTab === 'consult' ? 'active' : ''}`} onClick={() => setActiveTab('consult')}>Tư Vấn & Đặt Lịch</button>
                        <button className={`tab-btn ${activeTab === 'complaint' ? 'active' : ''}`} onClick={() => setActiveTab('complaint')}>Gửi Khiếu Nại</button>
                        <button className={`tab-btn ${activeTab === 'partner' ? 'active' : ''}`} onClick={() => setActiveTab('partner')}>Hợp Tác Đối Tác</button>
                    </div>

                    {activeTab === 'consult' && (
                        <div className="contact-grid" data-sal="slide-up" data-sal-delay="400">
                            <div className="contact-info">
                                <h2 className="section-title" style={{ textAlign: 'left' }}>Thông Tin Liên Hệ</h2>
                                <div className="info-item"><span>📍</span> <div><h3>Địa Chỉ</h3><p>753 PHẠM HỮU LẦU, PHƯỜNG CAO LÃNH, ĐỒNG THÁP</p></div></div>
                                <div className="info-item"><span>📞</span> <div><h3>Hotline</h3><p><a href="tel:0739193848" className="contact-link">0739 193 848</a></p></div></div>
                                <div className="info-item"><span>✉️</span> <div><h3>Email</h3><p><a href="mailto:contact@iviestudio.vn" className="contact-link">contact@iviestudio.vn</a></p></div></div>
                            </div>
                            <The className="booking-form-card">
                                <h2 className="form-title">Đăng Ký Tư Vấn</h2>
                                <form onSubmit={guiConsult} className="booking-form">
                                    <div className="form-row">
                                        <div className="form-group"><label>Họ Tên *</label><input name="name" value={duLieuConsult.name} onChange={xuLyThayDoiConsult} required placeholder="Nhập họ tên của bạn" /></div>
                                        <div className="form-group"><label>SĐT *</label><input name="phone" value={duLieuConsult.phone} onChange={xuLyThayDoiConsult} required placeholder="0xxx xxx xxx" /></div>
                                    </div>
                                    <div className="form-row">
                                        <div className="form-group"><label>Email</label><input name="email" type="email" value={duLieuConsult.email} onChange={xuLyThayDoiConsult} placeholder="email@example.com" /></div>
                                        <div className="form-group"><label>Địa Chỉ *</label><input name="address" value={duLieuConsult.address} onChange={xuLyThayDoiConsult} required placeholder="Địa chỉ của bạn" /></div>
                                    </div>
                                    <div className="form-row">
                                        <div className="form-group"><label>Dịch Vụ</label><select name="service" value={duLieuConsult.service} onChange={xuLyThayDoiConsult}><option value="wedding_photo">Chụp Ảnh</option><option value="makeup">Trang Điểm</option><option value="dress">Thuê Váy</option><option value="combo">Combo Trọn Gói</option></select></div>
                                        <div className="form-group"><label>Chi Nhánh</label><select name="chi_nhanh" value={duLieuConsult.chi_nhanh} onChange={xuLyThayDoiConsult}><option value="cao_lanh">Cao Lãnh - Đồng Tháp</option><option value="sa_dec">Sa Đéc - Đồng Tháp</option><option value="can_tho">Cần Thơ</option></select></div>
                                    </div>
                                    <div className="form-row">
                                        <div className="form-group">
                                            <label>Ngày Dự Kiến 📅</label>
                                            <div className="date-input-wrapper">
                                                <input type="date" name="date" value={duLieuConsult.date} onChange={xuLyThayDoiConsult} />
                                            </div>
                                        </div>
                                        <div className="form-group">
                                            <label>Ngân Sách Dự Kiến 💰</label>
                                            <select name="ngan_sach" value={duLieuConsult.ngan_sach} onChange={xuLyThayDoiConsult}>
                                                <option value="">-- Chọn ngân sách --</option>
                                                <option value="duoi_5tr">Dưới 5 triệu</option>
                                                <option value="5_10tr">5 - 10 triệu</option>
                                                <option value="10_20tr">10 - 20 triệu</option>
                                                <option value="20_50tr">20 - 50 triệu</option>
                                                <option value="tren_50tr">Trên 50 triệu</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div className="form-group"><label>Nội dung</label><textarea name="message" value={duLieuConsult.message} onChange={xuLyThayDoiConsult} rows="3" placeholder="Mô tả yêu cầu của bạn..." /></div>
                                    <NutBam type="submit" variant="primary" className="btn-submit-highlight" disabled={loadingConsult}>{loadingConsult ? 'Đang gửi...' : '✨ GỬI YÊU CẦU'}</NutBam>
                                </form>
                            </The>
                        </div>
                    )}

                    {activeTab === 'complaint' && (
                        <div className="complaint-container">
                            <The className="complaint-card">
                                <h2 className="form-title">Gửi Khiếu Nại</h2>
                                <p className="complaint-commitment">Chúng tôi chân thành xin lỗi về những trải nghiệm chưa hài lòng. <strong>IVIE cam kết sẽ xử lý khiếu nại của bạn trong vòng 24h.</strong></p>
                                <form onSubmit={guiComplaint} className="complaint-form">
                                    <div className="form-group"><label>Tiêu đề khiếu nại *</label><input name="title" value={duLieuComplaint.title} onChange={xuLyThayDoiComplaint} required placeholder="Ví dụ: Phản ánh về thái độ phục vụ..." /></div>
                                    <div className="form-row">
                                        <div className="form-group"><label>Họ Tên (Nếu không đăng nhập)</label><input name="customer_name" value={duLieuComplaint.customer_name} onChange={xuLyThayDoiComplaint} placeholder="Nhập họ tên" /></div>
                                        <div className="form-group"><label>Số Điện Thoại</label><input name="customer_phone" value={duLieuComplaint.customer_phone} onChange={xuLyThayDoiComplaint} placeholder="0xxx xxx xxx" /></div>
                                    </div>
                                    <div className="form-group"><label>Nội dung chi tiết *</label><textarea name="content" value={duLieuComplaint.content} onChange={xuLyThayDoiComplaint} rows="5" required placeholder="Mô tả chi tiết vấn đề bạn gặp phải..." /></div>
                                    <NutBam type="submit" variant="danger" disabled={loadingComplaint}>{loadingComplaint ? 'Đang gửi...' : 'GỬI KHIẾU NẠI'}</NutBam>
                                </form>
                            </The>
                        </div>
                    )}

                    {activeTab === 'partner' && (
                        <div className="partner-intro">
                            <h2>Trở Thành Đối Tác Của IVIE</h2>
                            <p>
                                IVIE Wedding Studio luôn tìm kiếm các đối tác chuyên nghiệp trong lĩnh vực <b>Makeup Artist</b>, <b>Nhiếp Ảnh Gia</b>, và <b>Quay Phim</b> để cùng kiến tạo những khoảnh khắc tuyệt vời nhất cho khách hàng.
                            </p>
                            <div className="partner-benefits">
                                <div className="benefit-box">
                                    <div className="benefit-icon">💄</div>
                                    <h3>Đối tác Trang điểm</h3>
                                    <p>Cơ hội làm việc với hàng trăm cô dâu mỗi tháng, môi trường studio hiện đại, thu nhập hấp dẫn theo show.</p>
                                </div>
                                <div className="benefit-box">
                                    <div className="benefit-icon">📸</div>
                                    <h3>Đối tác Quay chụp</h3>
                                    <p>Hợp tác trong các bộ phim ngắn, album cưới cinematic, trang thiết bị hỗ trợ tối đa.</p>
                                </div>
                            </div>
                            <div className="action-box">
                                <h3>Bắt đầu hành trình cùng IVIE ngay hôm nay!</h3>
                                <NutBam
                                    onClick={() => user ? navigate('/doi-tac-portal') : navigate('/dang-nhap?redirect=doi-tac-portal')}
                                    variant="dark"
                                    className="btn-large"
                                >
                                    ĐI ĐẾN TRANG ĐĂNG KÝ ĐỐI TÁC
                                </NutBam>
                                {!user && <p className="login-hint">* Bạn cần đăng nhập để nộp hồ sơ CV.</p>}
                            </div>
                        </div>
                    )}


                </div>
            </section>
        </div>
    );
};

export default LienHe;

