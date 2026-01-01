import { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/policy.css';

const ChinhSach = () => {
    const [activeTab, setActiveTab] = useState('privacy');

    return (
        <div className="policy-page">
            <section className="policy-hero">
                <div className="container">
                    <h1>Chính Sách & Quy Định</h1>
                    <p>Thông tin quan trọng về quyền lợi và trách nhiệm của khách hàng</p>
                </div>
            </section>

            <section className="policy-content">
                <div className="container">
                    <div className="policy-tabs">
                        <button 
                            className={`policy-tab ${activeTab === 'privacy' ? 'active' : ''}`}
                            onClick={() => setActiveTab('privacy')}
                        >
                            🔒 Chính Sách Bảo Mật
                        </button>
                        <button 
                            className={`policy-tab ${activeTab === 'deposit' ? 'active' : ''}`}
                            onClick={() => setActiveTab('deposit')}
                        >
                            💰 Quy Định Đặt Cọc
                        </button>
                        <button 
                            className={`policy-tab ${activeTab === 'refund' ? 'active' : ''}`}
                            onClick={() => setActiveTab('refund')}
                        >
                            ↩️ Chính Sách Hoàn Tiền
                        </button>
                    </div>

                    {activeTab === 'privacy' && (
                        <div className="policy-section">
                            <h2>Chính Sách Bảo Mật Thông Tin</h2>
                            <p className="policy-update">Cập nhật lần cuối: 01/01/2026</p>
                            
                            <div className="policy-block">
                                <h3>1. Thu Thập Thông Tin</h3>
                                <p>IVIE Wedding Studio thu thập các thông tin cá nhân khi bạn:</p>
                                <ul>
                                    <li>Đăng ký tài khoản trên website</li>
                                    <li>Đặt lịch tư vấn hoặc sử dụng dịch vụ</li>
                                    <li>Liên hệ với chúng tôi qua form hoặc hotline</li>
                                    <li>Tham gia các chương trình khuyến mãi</li>
                                </ul>
                                <p>Thông tin thu thập bao gồm: Họ tên, số điện thoại, email, địa chỉ, ngày cưới dự kiến.</p>
                            </div>

                            <div className="policy-block">
                                <h3>2. Mục Đích Sử Dụng</h3>
                                <p>Chúng tôi sử dụng thông tin của bạn để:</p>
                                <ul>
                                    <li>Cung cấp dịch vụ và hỗ trợ khách hàng</li>
                                    <li>Gửi thông báo về đơn hàng, lịch hẹn</li>
                                    <li>Gửi thông tin khuyến mãi (nếu bạn đồng ý)</li>
                                    <li>Cải thiện chất lượng dịch vụ</li>
                                </ul>
                            </div>

                            <div className="policy-block">
                                <h3>3. Bảo Vệ Thông Tin</h3>
                                <p>IVIE cam kết:</p>
                                <ul>
                                    <li>Không bán, trao đổi thông tin khách hàng cho bên thứ ba</li>
                                    <li>Áp dụng các biện pháp bảo mật tiên tiến</li>
                                    <li>Chỉ nhân viên được ủy quyền mới truy cập được dữ liệu</li>
                                    <li>Tuân thủ quy định pháp luật về bảo vệ dữ liệu cá nhân</li>
                                </ul>
                            </div>

                            <div className="policy-block">
                                <h3>4. Quyền Của Khách Hàng</h3>
                                <p>Bạn có quyền:</p>
                                <ul>
                                    <li>Yêu cầu xem, chỉnh sửa thông tin cá nhân</li>
                                    <li>Yêu cầu xóa tài khoản và dữ liệu</li>
                                    <li>Từ chối nhận email marketing</li>
                                    <li>Khiếu nại về việc xử lý dữ liệu</li>
                                </ul>
                            </div>

                            <div className="policy-contact">
                                <p>📧 Liên hệ về bảo mật: <strong>privacy@iviestudio.vn</strong></p>
                                <p>📞 Hotline: <strong>090 123 4567</strong></p>
                            </div>
                        </div>
                    )}

                    {activeTab === 'deposit' && (
                        <div className="policy-section">
                            <h2>Quy Định Đặt Cọc</h2>
                            <p className="policy-update">Áp dụng từ: 01/01/2026</p>

                            <div className="policy-block highlight">
                                <h3>💡 Tại Sao Cần Đặt Cọc?</h3>
                                <p>Đặt cọc giúp IVIE giữ chỗ cho ngày cưới của bạn và chuẩn bị tốt nhất các dịch vụ. Đây cũng là cam kết từ cả hai phía để đảm bảo quyền lợi.</p>
                            </div>

                            <div className="policy-block">
                                <h3>1. Mức Đặt Cọc</h3>
                                <table className="policy-table">
                                    <thead>
                                        <tr>
                                            <th>Dịch Vụ</th>
                                            <th>Mức Cọc</th>
                                            <th>Ghi Chú</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Thuê váy cưới</td>
                                            <td>30% giá trị</td>
                                            <td>Tối thiểu 500.000đ</td>
                                        </tr>
                                        <tr>
                                            <td>Chụp ảnh cưới</td>
                                            <td>50% giá trị</td>
                                            <td>Thanh toán khi ký hợp đồng</td>
                                        </tr>
                                        <tr>
                                            <td>Makeup cô dâu</td>
                                            <td>30% giá trị</td>
                                            <td>Tối thiểu 300.000đ</td>
                                        </tr>
                                        <tr>
                                            <td>Combo trọn gói</td>
                                            <td>40% giá trị</td>
                                            <td>Ưu đãi giảm 5% khi cọc sớm</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <div className="policy-block">
                                <h3>2. Hình Thức Thanh Toán</h3>
                                <ul>
                                    <li><strong>Tiền mặt:</strong> Tại studio IVIE</li>
                                    <li><strong>Chuyển khoản:</strong> Ngân hàng Vietcombank - STK: 1234567890 - IVIE STUDIO</li>
                                    <li><strong>Ví điện tử:</strong> Momo, ZaloPay, VNPay</li>
                                </ul>
                            </div>

                            <div className="policy-block">
                                <h3>3. Thời Hạn Giữ Chỗ</h3>
                                <ul>
                                    <li>Sau khi đặt cọc, lịch của bạn được giữ trong <strong>6 tháng</strong></li>
                                    <li>Có thể đổi ngày 1 lần miễn phí (báo trước 30 ngày)</li>
                                    <li>Đổi ngày lần 2 trở đi: phí 200.000đ/lần</li>
                                </ul>
                            </div>
                        </div>
                    )}

                    {activeTab === 'refund' && (
                        <div className="policy-section">
                            <h2>Chính Sách Hoàn Tiền</h2>
                            <p className="policy-update">Áp dụng từ: 01/01/2026</p>

                            <div className="policy-block warning">
                                <h3>⚠️ Lưu Ý Quan Trọng</h3>
                                <p>Vui lòng đọc kỹ chính sách hoàn tiền trước khi đặt cọc. IVIE luôn cố gắng hỗ trợ khách hàng trong mọi trường hợp.</p>
                            </div>

                            <div className="policy-block">
                                <h3>1. Trường Hợp Hoàn Tiền 100%</h3>
                                <ul>
                                    <li>IVIE không thể cung cấp dịch vụ như cam kết</li>
                                    <li>Sự cố bất khả kháng từ phía IVIE</li>
                                    <li>Hủy trong vòng 24h sau khi đặt cọc (chưa ký hợp đồng)</li>
                                </ul>
                            </div>

                            <div className="policy-block">
                                <h3>2. Hoàn Tiền Theo Thời Gian Hủy</h3>
                                <table className="policy-table">
                                    <thead>
                                        <tr>
                                            <th>Thời Gian Hủy</th>
                                            <th>Mức Hoàn</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Trước 60 ngày</td>
                                            <td className="green">Hoàn 80% tiền cọc</td>
                                        </tr>
                                        <tr>
                                            <td>Trước 30-60 ngày</td>
                                            <td className="yellow">Hoàn 50% tiền cọc</td>
                                        </tr>
                                        <tr>
                                            <td>Trước 15-30 ngày</td>
                                            <td className="orange">Hoàn 30% tiền cọc</td>
                                        </tr>
                                        <tr>
                                            <td>Dưới 15 ngày</td>
                                            <td className="red">Không hoàn tiền</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <div className="policy-block">
                                <h3>3. Trường Hợp Đặc Biệt</h3>
                                <p>IVIE sẽ xem xét hoàn tiền đặc biệt trong các trường hợp:</p>
                                <ul>
                                    <li>Thiên tai, dịch bệnh (có xác nhận chính quyền)</li>
                                    <li>Tai nạn, bệnh nặng (có giấy tờ y tế)</li>
                                    <li>Các trường hợp bất khả kháng khác</li>
                                </ul>
                            </div>

                            <div className="policy-block">
                                <h3>4. Quy Trình Hoàn Tiền</h3>
                                <ol>
                                    <li>Gửi yêu cầu hủy qua email hoặc đến trực tiếp studio</li>
                                    <li>IVIE xác nhận và tính toán mức hoàn trong 3 ngày làm việc</li>
                                    <li>Hoàn tiền trong 7-14 ngày làm việc qua hình thức ban đầu</li>
                                </ol>
                            </div>

                            <div className="policy-contact">
                                <p>📧 Email hỗ trợ: <strong>support@iviestudio.vn</strong></p>
                                <p>📞 Hotline: <strong>090 123 4567</strong></p>
                            </div>
                        </div>
                    )}

                    <div className="policy-footer">
                        <p>Bằng việc sử dụng dịch vụ của IVIE, bạn đồng ý với các chính sách trên.</p>
                        <Link to="/lien-he" className="policy-cta">Liên Hệ Tư Vấn</Link>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default ChinhSach;
