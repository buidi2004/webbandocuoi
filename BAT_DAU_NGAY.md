# 🌅 Bắt Đầu Ngày Làm Việc - IVIE Wedding Studio

## ⚡ Quick Start (30 giây)

```bash
# 1. Kiểm tra hệ thống
KIEM_TRA_LOCAL.bat

# 2. Khởi động tất cả
CHAY_LOCAL.bat

# 3. Mở browser
# - Frontend: http://localhost:5173
# - Backend Docs: http://localhost:8000/docs
# - Admin: http://localhost:8501
```

## 📊 Trạng Thái Hiện Tại

### ✅ Đã Cấu Hình
- [x] Backend `.env` → SQLite local
- [x] Frontend `.env` → API localhost:8000
- [x] Admin `.env` → API localhost:8000
- [x] Database `ivie.db` → Đã tồn tại
- [x] CORS → Đã cấu hình cho localhost

### 🎯 Service Ports
| Service | Port | Status |
|---------|------|--------|
| Backend | 8000 | ✅ Ready |
| Frontend | 5173 | ✅ Ready |
| Admin | 8501 | ✅ Ready |

## 🔄 Workflow Hàng Ngày

### 1. Sáng - Bắt Đầu
```bash
git pull origin main          # Lấy code mới nhất
CHAY_LOCAL.bat               # Khởi động services
```

### 2. Trong Ngày - Phát Triển
- Sửa code → Service tự động reload
- Test trong browser
- Commit thường xuyên

### 3. Tối - Kết Thúc
```bash
DUNG_LOCAL.bat               # Dừng services
git add .
git commit -m "feat: ..."
git push origin main
```

## 🧪 Test Nhanh

### Test Backend
```bash
# Mở browser
http://localhost:8000/api/health
# Kết quả: {"status": "healthy"}
```

### Test Frontend
```bash
# Mở browser
http://localhost:5173
# Kiểm tra: Trang chủ hiển thị, không có CORS error
```

### Test Admin
```bash
# Mở browser
http://localhost:8501
# Kiểm tra: Dashboard hiển thị
```

### Test Kết Nối
```bash
# Mở file
test-cors-locally.html
# Chạy tất cả 4 tests → Tất cả phải pass ✅
```

## 🐛 Lỗi Thường Gặp

### "Port already in use"
```bash
DUNG_LOCAL.bat
# Đợi 5 giây
CHAY_LOCAL.bat
```

### "Module not found"
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### "CORS Error"
```bash
# Kiểm tra backend/.env có:
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Restart backend
```

## 📁 Files Bạn Cần Biết

### Scripts
- `KIEM_TRA_LOCAL.bat` - Kiểm tra hệ thống
- `CHAY_LOCAL.bat` - Chạy tất cả
- `DUNG_LOCAL.bat` - Dừng tất cả

### Docs
- `README_LOCAL.md` - Tổng quan
- `HUONG_DAN_CHAY_LOCAL.md` - Chi tiết
- `FIXES_APPLIED.md` - Các fix đã áp dụng

### Test
- `test-cors-locally.html` - Test kết nối

## 💡 Tips Hữu Ích

### 1. Xem Logs
Mỗi service chạy trong terminal riêng → Xem logs trực tiếp

### 2. Hot Reload
- Backend: Tự động reload khi sửa Python
- Frontend: Tự động reload khi sửa React
- Admin: Tự động reload khi sửa Streamlit

### 3. Debug
```bash
# Backend với debug logs
cd backend
python -m uvicorn ung_dung.chinh:ung_dung --reload --log-level debug
```

### 4. Clear Cache
```bash
# Frontend
cd frontend
rmdir /s /q node_modules\.vite
npm run dev
```

### 5. Reset Database
```bash
cd backend
del ivie.db
python tao_du_lieu_mau.py
```

## 🎯 Checklist Hàng Ngày

### Trước Khi Code
- [ ] `git pull origin main`
- [ ] `CHAY_LOCAL.bat`
- [ ] Tất cả 3 service đang chạy
- [ ] Test với `test-cors-locally.html` pass
- [ ] Frontend hiển thị đúng

### Trong Khi Code
- [ ] Commit thường xuyên
- [ ] Test sau mỗi thay đổi
- [ ] Xem logs nếu có lỗi

### Trước Khi Kết Thúc
- [ ] Tất cả tests pass
- [ ] Code đã commit
- [ ] `DUNG_LOCAL.bat`
- [ ] `git push origin main`

## 🚀 Deploy Lên Production

Khi code xong và test OK:

```bash
# 1. Commit và push
git add .
git commit -m "feat: your feature"
git push origin main

# 2. Render sẽ tự động deploy
# Đợi 5-10 phút

# 3. Verify production
# Backend: https://ivie-be-final.onrender.com/api/health
# Frontend: https://ivie-fe-final.onrender.com
# Admin: https://ivie-ad-final.onrender.com
```

Xem `DEPLOYMENT_CHECKLIST.md` để biết chi tiết.

## 📞 Cần Trợ Giúp?

### Tài Liệu
1. `README_LOCAL.md` - Tổng quan
2. `HUONG_DAN_CHAY_LOCAL.md` - Chi tiết
3. `FIXES_APPLIED.md` - Các fix
4. `FIX_CORS_AND_DEPLOYMENT.md` - CORS issues

### Kiểm Tra
1. Chạy `KIEM_TRA_LOCAL.bat`
2. Xem logs trong terminal
3. Test với `test-cors-locally.html`

---

## ✅ Sẵn Sàng!

Nếu tất cả checklist ✅ → Bắt đầu code thôi! 🎉

**Happy Coding! 💻**
