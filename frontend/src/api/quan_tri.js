import api from './khach_hang';

export const quanTriAPI = {
    // Lấy danh sách sản phẩm (tái sử dụng API khách hàng)
    layTatCa: (params) => api.get('/api/san_pham', { params }),

    // Tạo sản phẩm mới
    tao: (duLieu) => api.post('/api/san_pham', duLieu),

    // Cập nhật sản phẩm
    capNhat: (id, duLieu) => api.put(`/api/san_pham/${id}`, duLieu),

    // Xóa sản phẩm
    xoa: (id) => api.delete(`/api/san_pham/${id}`),

    // --- Chuyên Gia ---
    layTatCaChuyenGia: () => api.get('/api/dich_vu/chuyen_gia'),
    taoChuyenGia: (duLieu) => api.post('/api/dich_vu/chuyen_gia', duLieu),
    capNhatChuyenGia: (id, duLieu) => api.put(`/api/dich_vu/chuyen_gia/${id}`, duLieu),
    xoaChuyenGia: (id) => api.delete(`/api/dich_vu/chuyen_gia/${id}`),

    // --- Dịch Vụ ---
    layTatCaDichVu: () => api.get('/api/dich_vu/'),
    taoDichVu: (duLieu) => api.post('/api/dich_vu/', duLieu),
    capNhatDichVu: (id, duLieu) => api.put(`/api/dich_vu/${id}`, duLieu),
    xoaDichVu: (id) => api.delete(`/api/dich_vu/${id}`),

    // --- Banner ---
    layTatCaBanner: () => api.get('/api/banner/tat_ca'),
    taoBanner: (duLieu) => api.post('/api/banner/', duLieu),
    capNhatBanner: (id, duLieu) => api.put(`/api/banner/${id}`, duLieu),
    xoaBanner: (id) => api.delete(`/api/banner/${id}`),

    // --- Nội Dung Trang Chủ ---
    layGioiThieu: () => api.get('/api/noi_dung/gioi_thieu'),
    capNhatGioiThieu: (duLieu) => api.put('/api/noi_dung/gioi_thieu', duLieu),

    layTatCaDiemNhan: () => api.get('/api/noi_dung/diem_nhan'),
    taoDiemNhan: (duLieu) => api.post('/api/noi_dung/diem_nhan', duLieu),
    capNhatDiemNhan: (id, duLieu) => api.put(`/api/noi_dung/diem_nhan/${id}`, duLieu),
    xoaDiemNhan: (id) => api.delete(`/api/noi_dung/diem_nhan/${id}`),

    // Tải lên hình ảnh
    uploadHinhAnh: (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/api/tap_tin/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    }
};
