# 🎯 IVIE Wedding Studio - Chạy Local

## 🚀 Khởi Động Nhanh (3 Bước)

### Bước 1: Kiểm Tra Hệ Thống
```bash
KIEM_TRA_LOCAL.bat
```

### Bước 2: Chạy Tất Cả Service
```bash
CHAY_LOCAL.bat
```

### Bước 3: Truy Cập
- 🎨 Frontend: http://localhost:5173
- 🔧 Backend: http://localhost:8000/docs
- 👨‍💼 Admin: http://localhost:8501

## 📋 Files Quan Trọng

| File | Mục Đích |
|------|----------|
| `KIEM_TRA_LOCAL.bat` | Kiểm tra hệ thống trước khi chạy |
| `CHAY_LOCAL.bat` | Khởi động tất cả service |
| `DUNG_LOCAL.bat` | Dừng tất cả service |
| `test-cors-locally.html` | Test kết nối API |
| `HUONG_DAN_CHAY_LOCAL.md` | Hướng dẫn chi tiết |

## 🔧 Cấu Hình Đã Tạo

### ✅ Backend (.env)
```env
DATABASE_URL=sqlite:///./ivie.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```

### ✅ Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```

### ✅ Admin (.env)
```env
API_BASE_URL=http://localhost:8000
STREAMLIT_SERVER_PORT=8501
```

## 🎯 Ports Sử Dụng

| Service | Port | URL |
|---------|------|-----|
| Backend API | 8000 | http://localhost:8000 |
| Frontend | 5173 | http://localhost:5173 |
| Admin Panel | 8501 | http://localhost:8501 |

## 🐛 Xử Lý Lỗi Nhanh

### Port đã được sử dụng?
```bash
DUNG_LOCAL.bat
```

### Module không tìm thấy?
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### CORS Error?
1. Kiểm tra backend đang chạy
2. Hard refresh: Ctrl+Shift+R
3. Xem `backend/.env` có đúng CORS_ORIGINS

## 📚 Tài Liệu Đầy Đủ

Xem `HUONG_DAN_CHAY_LOCAL.md` để biết:
- Yêu cầu hệ thống chi tiết
- Cách chạy thủ công từng service
- Xử lý lỗi chi tiết
- Tips & tricks
- Workflow phát triển

## ✅ Checklist

Trước khi bắt đầu:
- [ ] Chạy `KIEM_TRA_LOCAL.bat` → Tất cả ✅
- [ ] Chạy `CHAY_LOCAL.bat` → 3 service khởi động
- [ ] Mở `test-cors-locally.html` → Tất cả test pass
- [ ] Frontend hiển thị đúng
- [ ] Backend API hoạt động
- [ ] Admin Panel login được

## 🎉 Sẵn Sàng Code!

Nếu tất cả checklist ✅ → Bạn có thể bắt đầu phát triển!

---

**Cần trợ giúp?** Xem `HUONG_DAN_CHAY_LOCAL.md`
