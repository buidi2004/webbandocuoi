import { useState, useEffect } from 'react';
import { quanTriAPI } from '../api/quan_tri';
import NutBam from '../thanh_phan/NutBam';
import '../styles/products.css';

const QuanTri = () => {
    const [tabHienTai, setTabHienTai] = useState('san_pham');
    const [subTabHome, setSubTabHome] = useState('gioi_thieu'); // 'gioi_thieu' or 'diem_nhan'
    const [danhSach, setDanhSach] = useState([]);
    const [dangTai, setDangTai] = useState(true);
    const [hienForm, setHienForm] = useState(false);
    const [dangChinhSua, setDangChinhSua] = useState(null);
    const [duLieuForm, setDuLieuForm] = useState({});

    // Cấu hình mặc định cho từng loại dữ liệu
    const cauHinhTabs = {
        san_pham: {
            ten: 'Sản Phẩm',
            apiLay: quanTriAPI.layTatCa,
            apiTao: quanTriAPI.tao,
            apiSua: quanTriAPI.capNhat,
            apiXoa: quanTriAPI.xoa,
            macDinh: { name: '', code: '', category: 'wedding_modern', gender: 'female', description: '', rental_price_day: 0, rental_price_week: 0, purchase_price: 0, image_url: '', is_new: false, is_hot: false }
        },
        chuyen_gia: {
            ten: 'Chuyên Gia',
            apiLay: quanTriAPI.layTatCaChuyenGia,
            apiTao: quanTriAPI.taoChuyenGia,
            apiSua: quanTriAPI.capNhatChuyenGia,
            apiXoa: quanTriAPI.xoaChuyenGia,
            macDinh: { name: '', title: '', bio: '', years_experience: 0, brides_count: 0, specialties: [], image_url: '', social_facebook: '', social_instagram: '' }
        },
        dich_vu: {
            ten: 'Dịch Vụ',
            apiLay: quanTriAPI.layTatCaDichVu,
            apiTao: quanTriAPI.taoDichVu,
            apiSua: quanTriAPI.capNhatDichVu,
            apiXoa: quanTriAPI.xoaDichVu,
            macDinh: { name: '', description: '', features: [], price_from: 0, is_featured: false, icon: '' }
        },
        banner: {
            ten: 'Banner',
            apiLay: quanTriAPI.layTatCaBanner,
            apiTao: quanTriAPI.taoBanner,
            apiSua: quanTriAPI.capNhatBanner,
            apiXoa: quanTriAPI.xoaBanner,
            macDinh: { image_url: '', title: '', subtitle: '', link: '', is_active: true, order: 0 }
        },
        trang_chu: {
            ten: 'Trang Chủ',
            apiLay: async () => {
                if (subTabHome === 'gioi_thieu') {
                    const res = await quanTriAPI.layGioiThieu();
                    return { data: [res.data] };
                } else {
                    return await quanTriAPI.layTatCaDiemNhan();
                }
            },
            apiTao: quanTriAPI.taoDiemNhan,
            apiSua: async (id, data) => {
                if (subTabHome === 'gioi_thieu') return await quanTriAPI.capNhatGioiThieu(data);
                return await quanTriAPI.capNhatDiemNhan(id, data);
            },
            apiXoa: quanTriAPI.xoaDiemNhan
        }
    };

    useEffect(() => {
        taiDuLieu();
    }, [tabHienTai, subTabHome]);

    const taiDuLieu = async () => {
        setDangTai(true);
        try {
            const res = await cauHinhTabs[tabHienTai].apiLay();
            setDanhSach(Array.isArray(res.data) ? res.data : []);
        } catch (err) {
            console.error(err);
            alert("Lỗi tải dữ liệu");
        } finally {
            setDangTai(false);
        }
    };

    const xuLyXoa = async (id) => {
        if (tabHienTai === 'trang_chu' && subTabHome === 'gioi_thieu') return;
        if (!window.confirm("Bạn có chắc muốn xóa mục này?")) return;
        try {
            await cauHinhTabs[tabHienTai].apiXoa(id);
            taiDuLieu();
        } catch (err) {
            alert("Lỗi khi xóa");
        }
    };

    const moForm = (item = null) => {
        setDangChinhSua(item);
        if (item) {
            setDuLieuForm({ ...item });
        } else {
            const macDinh = subTabHome === 'diem_nhan' && tabHienTai === 'trang_chu'
                ? { title: '', description: '', image_url: '', order: 0 }
                : cauHinhTabs[tabHienTai].macDinh;
            setDuLieuForm({ ...macDinh });
        }
        setHienForm(true);
    };

    const xuLyLuu = async (e) => {
        e.preventDefault();
        try {
            const config = cauHinhTabs[tabHienTai];
            if (dangChinhSua || (tabHienTai === 'trang_chu' && subTabHome === 'gioi_thieu')) {
                const id = dangChinhSua?.id || 0;
                await config.apiSua(id, duLieuForm);
            } else {
                await config.apiTao(duLieuForm);
            }
            setHienForm(false);
            taiDuLieu();
        } catch (err) {
            alert("Lỗi khi lưu dữ liệu");
        }
    };

    const xuLyFile = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
            const res = await quanTriAPI.uploadHinhAnh(file);
            setDuLieuForm({ ...duLieuForm, image_url: res.data.url });
        } catch (err) {
            alert("Lỗi upload ảnh");
        }
    };

    return (
        <div className="container section admin-page">
            <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
                <h1 className="section-title">Quản Trị Nội Dung</h1>
                {(tabHienTai !== 'trang_chu' || subTabHome === 'diem_nhan') && (
                    <NutBam variant="primary" onClick={() => moForm()}>
                        + Thêm {tabHienTai === 'trang_chu' ? 'Điểm Nhấn' : cauHinhTabs[tabHienTai].ten} Mới
                    </NutBam>
                )}
            </div>

            {/* Tabs Navigation */}
            <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #ddd', paddingBottom: '10px', overflowX: 'auto' }}>
                {Object.keys(cauHinhTabs).map(key => (
                    <button
                        key={key}
                        onClick={() => { setTabHienTai(key); setSubTabHome('gioi_thieu'); }}
                        style={{
                            padding: '10px 20px',
                            cursor: 'pointer',
                            border: 'none',
                            background: tabHienTai === key ? 'var(--primary)' : 'transparent',
                            color: tabHienTai === key ? 'white' : 'black',
                            borderRadius: '4px',
                            fontWeight: 'bold',
                            whiteSpace: 'nowrap'
                        }}
                    >
                        {cauHinhTabs[key].ten}
                    </button>
                ))}
            </div>

            {/* Sub-tabs for Trang Chu */}
            {tabHienTai === 'trang_chu' && (
                <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
                    <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', fontWeight: subTabHome === 'gioi_thieu' ? 'bold' : 'normal', color: subTabHome === 'gioi_thieu' ? 'var(--primary)' : 'inherit' }}>
                        <input type="radio" name="subHome" checked={subTabHome === 'gioi_thieu'} onChange={() => setSubTabHome('gioi_thieu')} style={{ marginRight: '8px' }} />
                        Câu chuyện IVIE
                    </label>
                    <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', fontWeight: subTabHome === 'diem_nhan' ? 'bold' : 'normal', color: subTabHome === 'diem_nhan' ? 'var(--primary)' : 'inherit' }}>
                        <input type="radio" name="subHome" checked={subTabHome === 'diem_nhan'} onChange={() => setSubTabHome('diem_nhan')} style={{ marginRight: '8px' }} />
                        Dịch vụ nổi bật (3 ô)
                    </label>
                </div>
            )}

            {dangTai ? <div>Đang tải...</div> : (
                <div style={{ overflowX: 'auto', background: 'white', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ background: '#f8f9fa', textAlign: 'left', borderBottom: '2px solid #dee2e6' }}>
                                <th style={{ padding: '15px' }}>ID</th>
                                <th style={{ padding: '15px' }}>Thông Tin</th>
                                <th style={{ padding: '15px' }}>Hình Ảnh</th>
                                <th style={{ padding: '15px' }}>Hành Động</th>
                            </tr>
                        </thead>
                        <tbody>
                            {danhSach.map(item => (
                                <tr key={item.id} style={{ borderBottom: '1px solid #eee' }}>
                                    <td style={{ padding: '15px' }}>{item.id}</td>
                                    <td style={{ padding: '15px' }}>
                                        <div style={{ fontWeight: 'bold' }}>{item.name || item.title || 'Không có tên'}</div>
                                        {item.code && <div style={{ fontSize: '12px', color: '#666' }}>Mã: {item.code}</div>}
                                        {item.subtitle && <div style={{ fontSize: '12px', color: '#666' }}>{item.subtitle}</div>}
                                    </td>
                                    <td style={{ padding: '15px' }}>
                                        {item.image_url && <img src={item.image_url} alt="Preview" style={{ width: '50px', height: '50px', objectFit: 'cover', borderRadius: '4px' }} />}
                                    </td>
                                    <td style={{ padding: '15px' }}>
                                        <button onClick={() => moForm(item)} style={{ marginRight: '10px', color: '#1a73e8', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>Sửa</button>
                                        {(tabHienTai !== 'trang_chu' || subTabHome === 'diem_nhan') && (
                                            <button onClick={() => xuLyXoa(item.id)} style={{ color: '#d93025', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>Xóa</button>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Modal Form */}
            {hienForm && (
                <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
                    <div style={{ background: 'white', padding: '30px', borderRadius: '12px', width: '90%', maxWidth: '700px', maxHeight: '90vh', overflowY: 'auto', boxShadow: '0 10px 25px rgba(0,0,0,0.2)' }}>
                        <h2 style={{ marginBottom: '20px', borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
                            {dangChinhSua ? 'Chỉnh Sửa' : 'Thêm Mới'} {tabHienTai === 'trang_chu' ? (subTabHome === 'gioi_thieu' ? 'Giới Thiệu' : 'Điểm Nhấn') : cauHinhTabs[tabHienTai].ten}
                        </h2>

                        <form onSubmit={xuLyLuu} style={{ display: 'grid', gap: '15px' }}>
                            {/* Các trường chung */}
                            <input
                                placeholder="Tiêu đề / Tên"
                                value={duLieuForm.name || duLieuForm.title || ''}
                                onChange={e => setDuLieuForm({ ...duLieuForm, [duLieuForm.name !== undefined ? 'name' : 'title']: e.target.value })}
                                required
                                style={inputStyle}
                            />

                            {(tabHienTai === 'banner' || (tabHienTai === 'trang_chu' && subTabHome === 'gioi_thieu')) && (
                                <input placeholder="Tiêu đề phụ" value={duLieuForm.subtitle || ''} onChange={e => setDuLieuForm({ ...duLieuForm, subtitle: e.target.value })} style={inputStyle} />
                            )}

                            {tabHienTai === 'san_pham' && (
                                <>
                                    <input placeholder="Mã sản phẩm" value={duLieuForm.code || ''} onChange={e => setDuLieuForm({ ...duLieuForm, code: e.target.value })} required style={inputStyle} />
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                                        <select value={duLieuForm.category} onChange={e => setDuLieuForm({ ...duLieuForm, category: e.target.value })} style={inputStyle}>
                                            <option value="wedding_modern">Váy Cưới Hiện Đại</option>
                                            <option value="traditional">Áo Dài Truyền Thống</option>
                                        </select>
                                        <select value={duLieuForm.gender} onChange={e => setDuLieuForm({ ...duLieuForm, gender: e.target.value })} style={inputStyle}>
                                            <option value="female">Nữ</option>
                                            <option value="male">Nam</option>
                                        </select>
                                    </div>
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                                        <input type="number" placeholder="Giá thuê" value={duLieuForm.rental_price_day} onChange={e => setDuLieuForm({ ...duLieuForm, rental_price_day: Number(e.target.value) })} style={inputStyle} />
                                        <input type="number" placeholder="Giá mua" value={duLieuForm.purchase_price} onChange={e => setDuLieuForm({ ...duLieuForm, purchase_price: Number(e.target.value) })} style={inputStyle} />
                                    </div>
                                </>
                            )}

                            {tabHienTai === 'chuyen_gia' && (
                                <>
                                    <input placeholder="Chức danh" value={duLieuForm.title || ''} onChange={e => setDuLieuForm({ ...duLieuForm, title: e.target.value })} required style={inputStyle} />
                                    <input placeholder="Kinh nghiệm (năm)" type="number" value={duLieuForm.years_experience || 0} onChange={e => setDuLieuForm({ ...duLieuForm, years_experience: Number(e.target.value) })} style={inputStyle} />
                                    <input placeholder="Kỹ năng (phân cách bằng dấu phẩy)" value={Array.isArray(duLieuForm.specialties) ? duLieuForm.specialties.join(', ') : ''} onChange={e => setDuLieuForm({ ...duLieuForm, specialties: e.target.value.split(',').map(s => s.trim()) })} style={inputStyle} />
                                </>
                            )}

                            {tabHienTai === 'dich_vu' && (
                                <>
                                    <input type="number" placeholder="Giá từ" value={duLieuForm.price_from || 0} onChange={e => setDuLieuForm({ ...duLieuForm, price_from: Number(e.target.value) })} style={inputStyle} />
                                    <input placeholder="Đặc điểm (phân cách bằng dấu phẩy)" value={Array.isArray(duLieuForm.features) ? duLieuForm.features.join(', ') : ''} onChange={e => setDuLieuForm({ ...duLieuForm, features: e.target.value.split(',').map(s => s.trim()) })} style={inputStyle} />
                                </>
                            )}

                            {tabHienTai === 'trang_chu' && subTabHome === 'gioi_thieu' && (
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
                                    <div>
                                        <label style={{ fontSize: '12px' }}>Thống kê 1</label>
                                        <input placeholder="Ví dụ: 500+" value={duLieuForm.stat1_number} onChange={e => setDuLieuForm({ ...duLieuForm, stat1_number: e.target.value })} style={inputStyle} />
                                        <input placeholder="Ví dụ: Cặp Đôi" value={duLieuForm.stat1_label} onChange={e => setDuLieuForm({ ...duLieuForm, stat1_label: e.target.value })} style={{ ...inputStyle, marginTop: '5px' }} />
                                    </div>
                                    <div>
                                        <label style={{ fontSize: '12px' }}>Thống kê 2</label>
                                        <input placeholder="Ví dụ: 10+" value={duLieuForm.stat2_number} onChange={e => setDuLieuForm({ ...duLieuForm, stat2_number: e.target.value })} style={inputStyle} />
                                        <input placeholder="Ví dụ: Năm KN" value={duLieuForm.stat2_label} onChange={e => setDuLieuForm({ ...duLieuForm, stat2_label: e.target.value })} style={{ ...inputStyle, marginTop: '5px' }} />
                                    </div>
                                    <div>
                                        <label style={{ fontSize: '12px' }}>Thống kê 3</label>
                                        <input placeholder="Ví dụ: 100%" value={duLieuForm.stat3_number} onChange={e => setDuLieuForm({ ...duLieuForm, stat3_number: e.target.value })} style={inputStyle} />
                                        <input placeholder="Ví dụ: Hài Lòng" value={duLieuForm.stat3_label} onChange={e => setDuLieuForm({ ...duLieuForm, stat3_label: e.target.value })} style={{ ...inputStyle, marginTop: '5px' }} />
                                    </div>
                                </div>
                            )}

                            {tabHienTai === 'banner' && (
                                <>
                                    <input placeholder="Tiêu đề chính" value={duLieuForm.title || ''} onChange={e => setDuLieuForm({ ...duLieuForm, title: e.target.value })} style={inputStyle} />
                                    <input placeholder="Tiêu đề phụ" value={duLieuForm.subtitle || ''} onChange={e => setDuLieuForm({ ...duLieuForm, subtitle: e.target.value })} style={inputStyle} />
                                    <input placeholder="Đường dẫn (Link)" value={duLieuForm.link || ''} onChange={e => setDuLieuForm({ ...duLieuForm, link: e.target.value })} style={inputStyle} />
                                </>
                            )}

                            <textarea placeholder="Mô tả" value={duLieuForm.description || duLieuForm.bio || ''} onChange={e => setDuLieuForm({ ...duLieuForm, [tabHienTai === 'chuyen_gia' ? 'bio' : 'description']: e.target.value })} style={{ ...inputStyle, minHeight: '80px' }} />

                            {/* Image Upload section */}
                            <div style={{ border: '1px dashed #ccc', padding: '15px', borderRadius: '8px', background: '#f9f9f9' }}>
                                <label style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>Hình Ảnh:</label>
                                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                                    <input type="file" accept="image/*" onChange={xuLyFile} />
                                    {duLieuForm.image_url && (
                                        <div style={{ position: 'relative' }}>
                                            <img src={duLieuForm.image_url} alt="Preview" style={{ width: '80px', height: '80px', objectFit: 'cover', borderRadius: '4px', border: '1px solid #ddd' }} />
                                            <button type="button" onClick={() => setDuLieuForm({ ...duLieuForm, image_url: '' })} style={{ position: 'absolute', top: '-5px', right: '-5px', background: 'red', color: 'white', border: 'none', borderRadius: '50%', width: '20px', height: '20px', cursor: 'pointer', fontSize: '12px' }}>×</button>
                                        </div>
                                    )}
                                </div>
                                <input placeholder="Hoặc nhập URL ảnh" value={duLieuForm.image_url || ''} onChange={e => setDuLieuForm({ ...duLieuForm, image_url: e.target.value })} style={{ ...inputStyle, marginTop: '10px' }} />
                            </div>

                            <div style={{ display: 'flex', gap: '15px', marginTop: '10px' }}>
                                <NutBam type="submit" variant="primary">Lưu Thay Đổi</NutBam>
                                <NutBam type="button" variant="outline" onClick={() => setHienForm(false)}>Hủy</NutBam>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

const inputStyle = {
    padding: '12px',
    border: '1px solid #dee2e6',
    borderRadius: '6px',
    width: '100%',
    fontSize: '14px'
};

export default QuanTri;
