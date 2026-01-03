import { useNavigate } from 'react-router-dom';
import './NutDatLich.css';

const BookingButton = ({ productId, productName, className = '' }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        // Navigate to contact page with product info
        navigate('/lien-he', { 
            state: { 
                productId, 
                productName,
                subject: `Đặt lịch thử váy: ${productName}`
            } 
        });
    };

    return (
        <button 
            className={`booking-button ${className}`}
            onClick={handleClick}
            aria-label={`Đặt lịch thử ${productName}`}
        >
            <span className="booking-icon">📅</span>
            <span className="booking-text">Đặt lịch thử váy</span>
        </button>
    );
};

export default BookingButton;
