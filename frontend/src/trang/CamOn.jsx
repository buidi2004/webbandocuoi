import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { trackConversion } from '../utils/analytics';
import '../styles/thank-you.css';

/**
 * CamOn - Trang cảm ơn sau khi gửi form
 * URL: /cam-on
 * Dùng để tracking conversion trong GA4
 */
const CamOn = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const formType = location.state?.formType || 'contact';
    const productName = location.state?.productName || '';

    useEffect(() => {
        // Track conversion event in GA4
        trackConversion('form_submission', {
            form_type: formType,
            product_name: productName
        });
    }, [formType, productName]);

    return (
        <div className="thank-you-page">
            <div className="thank-you-container">
                {/* Success Icon */}
                <div className="success-icon">
                    <svg viewBox="0 0 52 52" className="checkmark">
                        <circle className="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                        <path className="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
                    </svg>
                </div>

                {/* Thank You Message */}
                <h1 className="thank-you-title">Cảm ơn bạn!</h1>
                <p className="thank-you-subtitle">
                    Yêu cầu của bạn đã được gửi thành công
                </p>

                {/* Response Time */}
                <div className="response-info">
                    <div className="response-icon">⏰</div>
                    <div className="response-text">
                        <h3>Thời gian phản hồi</h3>
                        <p>Chúng tôi sẽ liên hệ lại trong vòng <strong>24 giờ</strong></p>
                    </div>
                </div>

                {/* Contact Info */}
                <div className="quick-contact">
                    <p>Hoặc liên hệ ngay qua:</p>
                    <div className="contact-buttons">
                        <a href="tel:0901234567" className="contact-btn phone">
                            📞 090 123 4567
                        </a>
                        <a href="https://zalo.me/0901234567" target="_blank" rel="noopener noreferrer" className="contact-btn zalo">
                            💬 Chat Zalo
                        </a>
                    </div>
                </div>

                {/* Action Buttons */}
                <div className="action-buttons">
                    <button 
                        className="btn-primary"
                        onClick={() => navigate('/')}
                    >
                        Về Trang Chủ
                    </button>
                    <button 
                        className="btn-secondary"
                        onClick={() => navigate('/san-pham')}
                    >
                        Xem Sản Phẩm
                    </button>
                </div>

                {/* Social Proof */}
                <div className="social-proof">
                    <p>🎉 Hơn <strong>500+</strong> cặp đôi đã tin tưởng IVIE</p>
                </div>
            </div>
        </div>
    );
};

export default CamOn;
