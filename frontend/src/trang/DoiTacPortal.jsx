import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import NutBam from '../thanh_phan/NutBam';
import The from '../thanh_phan/The';
import { doiTacAPI, API_BASE_URL } from '../api/khach_hang';
import { useToast } from '../thanh_phan/Toast';
import axios from 'axios';


const DoiTacPortal = () => {
    const [user, setUser] = useState(null);
    const [hoso, setHoso] = useState([]);
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const fileInputRef = useRef(null);
    const navigate = useNavigate();
    const { addToast } = useToast();

    const [form, setForm] = useState({
        partner_type: 'makeup',
        full_name: '',
        phone: '',
        email: '',
        experience: '',
        portfolio_url: '',
        cv_url: ''
    });

    useEffect(() => {
        const storedUser = localStorage.getItem('ivie_user');
        if (!storedUser) {
            navigate('/dang-nhap?redirect=doi-tac-portal');
            return;
        }
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
        fetchHoSo(parsedUser.id);
    }, [navigate]);

    const fetchHoSo = async (userId) => {
        try {
            const res = await doiTacAPI.layHoSo(userId);
            setHoso(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (e) => {
        const file = e.target.files?.[0] || e;
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Reusing upload endpoint
            const res = await axios.post(`${API_BASE_URL}/api/tap_tin/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            setForm({ ...form, cv_url: res.data.url });
            addToast({ message: 'Đã tải lên CV!', type: 'success' });
        } catch (err) {

            addToast({ message: 'Lỗi khi tải lên hình ảnh.', type: 'error' });
        } finally {
            setUploading(false);
        }
    };

    // Drag and drop handlers
    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleUpload(e.dataTransfer.files[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!form.cv_url && !form.portfolio_url) {
            addToast({ message: 'Vui lòng cung cấp CV hoặc Portfolio.', type: 'warning' });
            return;
        }

        try {
            await doiTacAPI.dangKy(form, user.id);
            addToast({ message: 'Đã gửi hồ sơ thành công!', type: 'success' });
            fetchHoSo(user.id);
            setActiveView('status');
        } catch (err) {
            addToast({ message: err.response?.data?.detail || 'Lỗi khi gửi hồ sơ.', type: 'error' });
        }
    };

    const [activeView, setActiveView] = useState('apply'); // apply, status
    const [scrollY, setScrollY] = useState(0);

    // Theo dõi scroll để tạo hiệu ứng parallax
    useEffect(() => {
        const handleScroll = () => {
            setScrollY(window.scrollY);
        };
        window.addEventListener('scroll', handleScroll, { passive: true });
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    // Component cành mai với hiệu ứng parallax
    const CanhMai = ({ side }) => {
        // Tính toán hiệu ứng dựa trên scroll
        const parallaxY = scrollY * 0.15; // Di chuyển theo chiều dọc
        const rotation = Math.sin(scrollY * 0.005) * 3; // Lắc nhẹ
        const scale = 1 + Math.sin(scrollY * 0.003) * 0.05; // Co giãn nhẹ
        
        return (
        <div style={{
            position: 'fixed',
            [side]: 0,
            top: `calc(50% + ${parallaxY}px)`,
            transform: `translateY(-50%) ${side === 'right' ? 'scaleX(-1)' : ''} rotate(${side === 'left' ? rotation : -rotation}deg) scale(${scale})`,
            zIndex: 10,
            pointerEvents: 'none',
            opacity: 0.9,
            transition: 'transform 0.1s ease-out'
        }}>
            <svg width="120" height="400" viewBox="0 0 120 400">
                {/* Thân cành chính */}
                <path 
                    d="M10 400 Q30 300 25 200 Q20 100 40 20" 
                    stroke="#5D4037" 
                    strokeWidth="6" 
                    fill="none"
                />
                {/* Cành phụ 1 */}
                <path 
                    d="M25 280 Q50 260 70 240" 
                    stroke="#5D4037" 
                    strokeWidth="3" 
                    fill="none"
                />
                {/* Cành phụ 2 */}
                <path 
                    d="M22 180 Q55 170 80 150" 
                    stroke="#5D4037" 
                    strokeWidth="3" 
                    fill="none"
                />
                {/* Cành phụ 3 */}
                <path 
                    d="M30 100 Q60 90 90 70" 
                    stroke="#5D4037" 
                    strokeWidth="2.5" 
                    fill="none"
                />
                {/* Cành phụ 4 */}
                <path 
                    d="M35 50 Q55 40 75 25" 
                    stroke="#5D4037" 
                    strokeWidth="2" 
                    fill="none"
                />
                
                {/* Hoa mai - vàng rực */}
                {/* Hoa 1 */}
                <g transform="translate(65, 235)">
                    <circle cx="0" cy="-8" r="6" fill="#FFD700"/>
                    <circle cx="7" cy="-2" r="6" fill="#FFD700"/>
                    <circle cx="5" cy="6" r="6" fill="#FFD700"/>
                    <circle cx="-5" cy="6" r="6" fill="#FFD700"/>
                    <circle cx="-7" cy="-2" r="6" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="4" fill="#FFA000"/>
                </g>
                
                {/* Hoa 2 */}
                <g transform="translate(75, 145)">
                    <circle cx="0" cy="-7" r="5" fill="#FFD700"/>
                    <circle cx="6" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="4" cy="5" r="5" fill="#FFD700"/>
                    <circle cx="-4" cy="5" r="5" fill="#FFD700"/>
                    <circle cx="-6" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="3" fill="#FFA000"/>
                </g>
                
                {/* Hoa 3 */}
                <g transform="translate(85, 65)">
                    <circle cx="0" cy="-6" r="5" fill="#FFD700"/>
                    <circle cx="5" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="3" cy="4" r="5" fill="#FFD700"/>
                    <circle cx="-3" cy="4" r="5" fill="#FFD700"/>
                    <circle cx="-5" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="3" fill="#FFA000"/>
                </g>
                
                {/* Hoa 4 */}
                <g transform="translate(70, 20)">
                    <circle cx="0" cy="-5" r="4" fill="#FFD700"/>
                    <circle cx="4" cy="-1" r="4" fill="#FFD700"/>
                    <circle cx="3" cy="4" r="4" fill="#FFD700"/>
                    <circle cx="-3" cy="4" r="4" fill="#FFD700"/>
                    <circle cx="-4" cy="-1" r="4" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="2.5" fill="#FFA000"/>
                </g>
                
                {/* Hoa 5 - trên cành chính */}
                <g transform="translate(28, 250)">
                    <circle cx="0" cy="-6" r="5" fill="#FFD700"/>
                    <circle cx="5" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="3" cy="4" r="5" fill="#FFD700"/>
                    <circle cx="-3" cy="4" r="5" fill="#FFD700"/>
                    <circle cx="-5" cy="-2" r="5" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="3" fill="#FFA000"/>
                </g>
                
                {/* Hoa 6 */}
                <g transform="translate(25, 160)">
                    <circle cx="0" cy="-5" r="4" fill="#FFD700"/>
                    <circle cx="4" cy="-1" r="4" fill="#FFD700"/>
                    <circle cx="3" cy="4" r="4" fill="#FFD700"/>
                    <circle cx="-3" cy="4" r="4" fill="#FFD700"/>
                    <circle cx="-4" cy="-1" r="4" fill="#FFD700"/>
                    <circle cx="0" cy="0" r="2.5" fill="#FFA000"/>
                </g>
                
                {/* Nụ mai */}
                <circle cx="40" cy="30" r="4" fill="#FFD700"/>
                <circle cx="55" cy="110" r="3" fill="#FFD700"/>
                <circle cx="45" cy="200" r="3.5" fill="#FFD700"/>
                <circle cx="60" cy="270" r="3" fill="#FFD700"/>
            </svg>
        </div>
        );
    };

    if (loading) return <div style={{ padding: '100px', textAlign: 'center' }}>Đang tải...</div>;

    return (
        <div className="partner-portal" style={{ padding: '100px 0', minHeight: '80vh', background: '#0a0a0a', color: 'white', position: 'relative', overflow: 'hidden' }}>
            {/* Cành mai 2 bên */}
            <CanhMai side="left" />
            <CanhMai side="right" />
            
            <div className="container">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px' }}>
                    <h1 style={{ color: '#c09a6a' }}>Cổng Thông Tin Đối Tác</h1>
                    <div style={{ display: 'flex', gap: '10px' }}>
                        <NutBam variant={activeView === 'apply' ? 'primary' : 'outline'} onClick={() => setActiveView('apply')}>Nộp Hồ Sơ</NutBam>
                        <NutBam variant={activeView === 'status' ? 'primary' : 'outline'} onClick={() => setActiveView('status')} title="Số lượng hồ sơ đã nộp">
                            Trạng Thái ({hoso.length})
                        </NutBam>
                    </div>
                </div>

                {activeView === 'apply' ? (
                    <The style={{ maxWidth: '800px', margin: '0 auto', background: '#111' }}>
                        <h2 style={{ marginBottom: '20px' }}>Hồ Sơ Ứng Tuyển</h2>
                        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '20px' }}>
                            <div className="form-group">
                                <label>Lĩnh vực hợp tác</label>
                                <select
                                    style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                    value={form.partner_type}
                                    onChange={e => setForm({ ...form, partner_type: e.target.value })}
                                >
                                    <option value="makeup">Trang điểm (Makeup Artist)</option>
                                    <option value="media">Quay phim / Chụp ảnh</option>
                                </select>
                            </div>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                                <div className="form-group">
                                    <label>Họ và Tên</label>
                                    <input style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                        type="text" required value={form.full_name} onChange={e => setForm({ ...form, full_name: e.target.value })} />
                                </div>
                                <div className="form-group">
                                    <label>Số Điện Thoại</label>
                                    <input style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                        type="tel" required value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} />
                                </div>
                            </div>
                            <div className="form-group">
                                <label>Email liên hệ</label>
                                <input style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                    type="email" required value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} />
                            </div>
                            <div className="form-group">
                                <label>Kinh nghiệm / Giới thiệu bản thân</label>
                                <textarea style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                    rows="4" value={form.experience} onChange={e => setForm({ ...form, experience: e.target.value })} />
                            </div>
                            <div className="form-group">
                                <label>Link Portfolio (nếu có)</label>
                                <input style={{ width: '100%', padding: '12px', background: '#222', border: '1px solid #333', color: 'white' }}
                                    placeholder="Behance, Facebook, Website..." value={form.portfolio_url} onChange={e => setForm({ ...form, portfolio_url: e.target.value })} />
                            </div>
                            <div className="form-group">
                                <label>Ảnh CV / Portfolio của bạn *</label>
                                <div 
                                    onDragEnter={handleDrag}
                                    onDragLeave={handleDrag}
                                    onDragOver={handleDrag}
                                    onDrop={handleDrop}
                                    onClick={() => fileInputRef.current?.click()}
                                    style={{
                                        border: `2px dashed ${dragActive ? '#c09a6a' : '#444'}`,
                                        borderRadius: '12px',
                                        padding: '30px',
                                        textAlign: 'center',
                                        cursor: 'pointer',
                                        background: dragActive ? 'rgba(192, 154, 106, 0.1)' : '#1a1a1a',
                                        transition: 'all 0.3s ease'
                                    }}
                                >
                                    <input 
                                        type="file" 
                                        ref={fileInputRef}
                                        onChange={handleUpload} 
                                        style={{ display: 'none' }} 
                                        accept="image/*,.pdf"
                                    />
                                    {uploading ? (
                                        <p style={{ color: '#c09a6a' }}>⏳ Đang tải ảnh lên...</p>
                                    ) : form.cv_url ? (
                                        <div style={{ color: '#2ecc71' }}>
                                            <span style={{ fontSize: '2rem' }}>✅</span>
                                            <p>Đã đính kèm file</p>
                                            <p style={{ fontSize: '0.8rem', color: '#888' }}>Nhấn để thay đổi</p>
                                        </div>
                                    ) : (
                                        <div>
                                            <span style={{ fontSize: '2.5rem', display: 'block', marginBottom: '10px' }}>📁</span>
                                            <p style={{ color: '#888' }}>Kéo thả file vào đây hoặc nhấn để chọn</p>
                                            <p style={{ fontSize: '0.8rem', color: '#666', marginTop: '5px' }}>Hỗ trợ: JPG, PNG, PDF</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                            <NutBam type="submit" variant="primary" style={{ marginTop: '20px' }}>GỬI HỒ SƠ ỨNG TUYỂN</NutBam>
                        </form>
                    </The>
                ) : (
                    <div style={{ display: 'grid', gap: '20px' }}>
                        {hoso.length === 0 ? (
                            <p style={{ textAlign: 'center', padding: '50px' }}>Bạn chưa có hồ sơ nào.</p>
                        ) : (
                            hoso.map(item => (
                                <The key={item.id} style={{ background: '#111', borderLeft: `5px solid ${item.status === 'accepted' ? '#2ecc71' : item.status === 'rejected' ? '#e74c3c' : '#f1c40f'}` }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                        <div>
                                            <h3 style={{ marginBottom: '5px' }}>{item.partner_type === 'makeup' ? 'Trang điểm' : 'Quay chụp'} - {item.full_name}</h3>
                                            <p style={{ color: '#888', fontSize: '0.9rem' }}>Ngày gửi: {new Date(item.created_at).toLocaleDateString('vi-VN')}</p>
                                        </div>
                                        <div style={{ textAlign: 'right' }}>
                                            <span style={{
                                                padding: '5px 15px',
                                                borderRadius: '20px',
                                                background: item.status === 'accepted' ? '#2ecc71' : item.status === 'rejected' ? '#e74c3c' : '#f1c40f',
                                                color: 'black', fontWeight: 'bold'
                                            }}>
                                                {item.status === 'pending' ? 'Chờ duyệt' :
                                                    item.status === 'interviewing' ? 'Hẹn phỏng vấn' :
                                                        item.status === 'accepted' ? 'Đã trúng tuyển' : 'Từ chối'}
                                            </span>
                                        </div>
                                    </div>

                                    {item.admin_reply && (
                                        <div style={{ marginTop: '20px', padding: '15px', background: '#222', borderRadius: '5px' }}>
                                            <p style={{ fontWeight: 'bold', color: '#c09a6a', marginBottom: '5px' }}>Phản hồi từ IVIE Admin:</p>
                                            <p style={{ whiteSpace: 'pre-wrap' }}>{item.admin_reply}</p>
                                        </div>
                                    )}

                                    {item.contract_content && item.status === 'accepted' && (
                                        <div style={{ marginTop: '20px', padding: '15px', background: '#c09a6a', borderRadius: '5px', color: 'black' }}>
                                            <p style={{ fontWeight: 'bold', marginBottom: '10px' }}>Hợp Đồng & Điều Khoản Hợp Tác:</p>
                                            <p style={{ whiteSpace: 'pre-wrap' }}>{item.contract_content}</p>
                                            <p style={{ marginTop: '10px', fontSize: '0.8rem', fontStyle: 'italic' }}>* Vui lòng liên hệ hotline để hoàn tất thủ tục ký kết.</p>
                                        </div>
                                    )}
                                </The>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default DoiTacPortal;
