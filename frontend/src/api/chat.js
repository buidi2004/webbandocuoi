import api from './khach_hang';

export const chatAPI = {
    guiTinNhan: (duLieu, token) => api.post(`/api/chat/gui?token=${token}`, duLieu),
    layLichSu: (token) => api.get(`/api/chat/lich_su?token=${token}`)
};
