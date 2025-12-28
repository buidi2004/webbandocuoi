import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import NutBam from '../thanh_phan/NutBam';
import { nguoiDungAPI } from '../api/nguoi_dung';
import { useToast } from '../thanh_phan/Toast';
import '../styles/auth.css';

const DangKy = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        full_name: '',
        phone: '',
        address: '',
        email: ''
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const { addToast } = useToast();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // Làm sạch dữ liệu: Nếu field trống thì gửi null thay vì chuỗi rỗng
            const cleanedData = { ...formData };
            Object.keys(cleanedData).forEach(key => {
                if (cleanedData[key] === '') {
                    cleanedData[key] = null;
                }
            });

            await nguoiDungAPI.dangKy(cleanedData);
            addToast({ message: "Đăng ký thành công! Vui lòng đăng nhập.", type: "success" });
            navigate('/dang-nhap');
        } catch (error) {
            console.error("Registration error:", error);
            let msg = "Lỗi đăng ký";

            if (error.response?.data?.detail) {
                if (Array.isArray(error.response.data.detail)) {
                    // Xử lý lỗi validation từ FastAPI (Pydantic)
                    msg = error.response.data.detail.map(d => d.msg).join(", ");
                } else {
                    msg = error.response.data.detail;
                }
            }

            addToast({ message: msg, type: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <h2 className="auth-title">Đăng Ký Thành Viên</h2>
                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label>Tên đăng nhập *</label>
                        <input name="username" required value={formData.username} onChange={handleChange} placeholder="user123..." />
                    </div>
                    <div className="form-group">
                        <label>Mật khẩu *</label>
                        <input name="password" type="password" required value={formData.password} onChange={handleChange} placeholder="••••••••" />
                    </div>
                    <div className="form-group">
                        <label>Họ và Tên *</label>
                        <input name="full_name" required value={formData.full_name} onChange={handleChange} placeholder="Nguyễn Văn A" />
                    </div>
                    <div className="form-group">
                        <label>Số điện thoại *</label>
                        <input name="phone" required value={formData.phone} onChange={handleChange} placeholder="090..." />
                    </div>
                    <div className="form-group">
                        <label>Địa chỉ *</label>
                        <input name="address" required value={formData.address} onChange={handleChange} placeholder="Số nhà, đường, phường..." />
                    </div>
                    <div className="form-group">
                        <label>Email (Không bắt buộc)</label>
                        <input name="email" type="email" value={formData.email} onChange={handleChange} placeholder="example@gmail.com" />
                    </div>
                    <NutBam variant="primary" type="submit" className="btn-block" disabled={loading}>
                        {loading ? "ĐANG XỬ LÝ..." : "ĐĂNG KÝ NGAY"}
                    </NutBam>
                </form>
                <p className="auth-footer">
                    Đã có tài khoản? <Link to="/dang-nhap">Đăng nhập</Link>
                </p>
            </div>
        </div>
    );
};

export default DangKy;
