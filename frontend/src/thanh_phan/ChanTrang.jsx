import { Link } from 'react-router-dom';
import './Footer.css';

// Component hạt vàng lấp lánh
const HatVangLapLanh = () => (
    <div className="hat-vang-container">
        {[...Array(20)].map((_, i) => (
            <div 
                key={i} 
                className="hat-vang"
                style={{
                    left: `${Math.random() * 100}%`,
                    top: `${Math.random() * 100}%`,
                    animationDelay: `${Math.random() * 3}s`,
                    animationDuration: `${2 + Math.random() * 2}s`
                }}
            />
        ))}
    </div>
);

// Component Footer chính
const ChanTrang = () => {
    return (
        <footer className="chan-trang">
            <HatVangLapLanh />
            
            <div className="chan-trang-noi-dung">
                <div className="chan-trang-cot">
                    <h3>IVIE Bridal</h3>
                    <p>Cho thuê váy cưới cao cấp</p>
                    <p>Địa chỉ: TP. Hồ Chí Minh</p>
                </div>
                
                <div className="chan-trang-cot">
                    <h4>Liên kết</h4>
                    <ul>
                        <li><Link to="/">Trang chủ</Link></li>
                        <li><Link to="/san-pham">Sản phẩm</Link></li>
                        <li><Link to="/thu-vien">Thư viện</Link></li>
                        <li><Link to="/lien-he">Liên hệ</Link></li>
                    </ul>
                </div>
                
                <div className="chan-trang-cot">
                    <h4>Liên hệ</h4>
                    <p>📞 Hotline: 0909 XXX XXX</p>
                    <p>📧 Email: contact@iviebridal.com</p>
                    <div className="mang-xa-hoi">
                        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
                        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">Instagram</a>
                    </div>
                </div>
            </div>
            
            <div className="chan-trang-ban-quyen">
                <p>© 2025 IVIE Bridal. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default ChanTrang;
