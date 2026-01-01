import { useState } from 'react';
import { lienHeAPI } from '../api/khach_hang';
import { trackGenerateLead } from '../utils/analytics';
import './FormLienHeNhanh.css';

/**
 * FormLienHeNhanh - Form liên hệ tối giản với loading effect
 * SEO: Số điện thoại trong thẻ <a href="tel:">
 */
const FormLienHeNhanh = ({ 
    onSuccess,
    compact = false,
    title = "Đăng ký tư vấn miễn phí"
}) => {
    const [formData, setFormData] = useState({
        name: '',
        phone: '',
        message: ''
    });
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError('');
    };

    const validatePhone = (phone) => {
        const phoneRegex = /^(0|\+84)[0-9]{9,10}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validate
        if (!formData.name.trim()) {
            setError('Vui lòng nhập họ tên');
            return;
        }
        if (!validatePhone(formData.phone)) {
            setError('Số điện thoại không hợp lệ');
            return;
        }

        setLoading(true);
        setError('');

        try {
            await lienHeAPI.gui({
                name: formData.name,
                phone: formData.phone,
                email: '',
                address: '',
                message: formData.message || 'Yêu cầu tư vấn nhanh'
            });

            // Track GA4
            trackGenerateLead('quick_form');

            setSuccess(true);
            setFormData({ name: '', phone: '', message: '' });
            
            if (onSuccess) onSuccess();
        } catch (err) {
            setError('Không thể gửi. Vui lòng thử lại hoặc gọi trực tiếp.');
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className={`form-lien-he-nhanh ${compact ? 'compact' : ''}`}>
                <div className="success-message">
                    <span className="success-icon">✓</span>
                    <h3>Đã gửi thành công!</h3>
                    <p>Chúng tôi sẽ liên hệ bạn trong 15 phút.</p>
                    <p className="hotline-text">
                        Hoặc gọi ngay: <a href="tel:0739193848" itemProp="telephone">0739 193 848</a>
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className={`form-lien-he-nhanh ${compact ? 'compact' : ''}`}>
            {title && <h3 className="form-title">{title}</h3>}
            
            <form onSubmit={handleSubmit} className="quick-form">
                <div className="form-field">
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Họ tên của bạn *"
                        disabled={loading}
                        autoComplete="name"
                    />
                </div>

                <div className="form-field">
                    <input
                        type="tel"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        placeholder="Số điện thoại *"
                        disabled={loading}
                        autoComplete="tel"
                        itemProp="telephone"
                    />
                </div>

                {!compact && (
                    <div className="form-field">
                        <textarea
                            name="message"
                            value={formData.message}
                            onChange={handleChange}
                            placeholder="Bạn quan tâm dịch vụ gì? (tùy chọn)"
                            rows="2"
                            disabled={loading}
                        />
                    </div>
                )}

                {error && <p className="error-text">{error}</p>}

                <button 
                    type="submit" 
                    className={`submit-btn ${loading ? 'loading' : ''}`}
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <span className="spinner"></span>
                            Đang gửi...
                        </>
                    ) : (
                        'GỬI YÊU CẦU TƯ VẤN'
                    )}
                </button>
            </form>

            <p className="privacy-note">
                Thông tin của bạn được bảo mật. Hotline: {' '}
                <a href="tel:0739193848" itemProp="telephone">0739 193 848</a>
            </p>
        </div>
    );
};

export default FormLienHeNhanh;
