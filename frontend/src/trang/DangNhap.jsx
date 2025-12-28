import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import NutBam from '../thanh_phan/NutBam';
import { nguoiDungAPI } from '../api/nguoi_dung';
import { useToast } from '../thanh_phan/Toast';
import '../styles/auth.css';

const DangNhap = () => {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
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
            const res = await nguoiDungAPI.dangNhap(formData);
            if (res.data) {
                localStorage.setItem('ivie_token', res.data.access_token);
                localStorage.setItem('ivie_user', JSON.stringify(res.data.user));
                addToast({ message: `Chào mừng trở lại, ${res.data.user.full_name}!`, type: "success" });
                navigate('/');
                // Dispatch event to update Navbar
                window.dispatchEvent(new Event('authChange'));
            }
        } catch (error) {
            const msg = error.response?.data?.detail || "Tên đăng nhập hoặc mật khẩu không đúng";
            addToast({ message: msg, type: "error" });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <h2 className="auth-title">Đăng Nhập</h2>
                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label>Tên đăng nhập</label>
                        <input name="username" required value={formData.username} onChange={handleChange} placeholder="Username" />
                    </div>
                    <div className="form-group">
                        <label>Mật khẩu</label>
                        <input name="password" type="password" required value={formData.password} onChange={handleChange} placeholder="••••••••" />
                    </div>
                    <NutBam variant="primary" type="submit" className="btn-block" disabled={loading}>
                        {loading ? "ĐANG ĐĂNG NHẬP..." : "ĐĂNG NHẬP"}
                    </NutBam>
                </form>
                <p className="auth-footer">
                    Chưa có tài khoản? <Link to="/dang-ky">Đăng ký ngay</Link>
                </p>
            </div>
        </div>
    );
};

export default DangNhap;
