# 🚀 Hướng Dẫn Chạy Local - IVIE Wedding Studio

## 📋 Yêu Cầu Hệ Thống

### Phần Mềm Cần Cài
- ✅ **Python 3.12 hoặc 3.13** (KHÔNG dùng 3.14 RC)
- ✅ **Node.js 18+** và npm
- ✅ **Git** (để clone/pull code)

### Kiểm Tra Đã Cài Chưa
```bash
python --version    # Phải >= 3.12
node --version      # Phải >= 18
npm --version       # Đi kèm với Node.js
```

## 🎯 Cách Chạy Nhanh (Recommended)

### Bước 1: Chạy Script Tự Động
```bash
CHAY_LOCAL.bat
```

Script này sẽ:
1. ✅ Kiểm tra Python và Node.js
2. ✅ Kiểm tra Database
3. ✅ Kiểm tra các file .env
4. ✅ Khởi động Backend (Port 8000)
5. ✅ Khởi động Frontend (Port 5173)
6. ✅ Khởi động Admin Panel (Port 8501)

### Bước 2: Truy Cập Các Service

| Service | URL | Mô Tả |
|---------|-----|-------|
| 🎨 **Frontend** | http://localhost:5173 | Website chính |
| 🔧 **Backend API** | http://localhost:8000 | API Server |
| 📚 **API Docs** | http://localhost:8000/docs | Swagger UI |
| 🧪 **Health Check** | http://localhost:8000/api/health | Kiểm tra backend |
| 🗄️ **DB Test** | http://localhost:8000/api/db-test | Kiểm tra database |
| 👨‍💼 **Admin Panel** | http://localhost:8501 | Quản trị |

### Bước 3: Kiểm Tra Kết Nối
Mở file `test-cors-locally.html` trong browser và chạy tất cả các test.

### Bước 4: Dừng Tất Cả Service
```bash
DUNG_LOCAL.bat
```

## 🔧 Cách Chạy Thủ Công (Manual)

### 1. Backend API

```bash
# Terminal 1
cd backend
python -m uvicorn ung_dung.chinh:ung_dung --reload --host 127.0.0.1 --port 8000
```

Kiểm tra: http://localhost:8000/docs

### 2. Frontend

```bash
# Terminal 2
cd frontend
npm run dev
```

Kiểm tra: http://localhost:5173

### 3. Admin Panel

```bash
# Terminal 3
cd admin-python
streamlit run quan_tri_optimized_v2.py --server.port 8501
```

Kiểm tra: http://localhost:8501

## 📁 Cấu Trúc File Quan Trọng

```
webdichvumedia/
├── backend/
│   ├── .env                    # ✅ Đã tạo
│   ├── ivie.db                 # ✅ Database SQLite
│   └── ung_dung/chinh.py       # Entry point
│
├── frontend/
│   ├── .env                    # ✅ Đã có
│   ├── .env.production         # ✅ Đã tạo (cho production)
│   └── src/
│
├── admin-python/
│   ├── .env                    # ✅ Đã tạo
│   └── quan_tri_optimized_v2.py
│
├── CHAY_LOCAL.bat              # ✅ Script chạy tất cả
├── DUNG_LOCAL.bat              # ✅ Script dừng tất cả
└── test-cors-locally.html      # ✅ Tool test kết nối
```

## 🔍 Kiểm Tra Cấu Hình

### Backend (.env)
```env
DATABASE_URL=sqlite:///./ivie.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
PORT=8000
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_IMGBB_API_KEY=c525fc0204b449b541b0f0a5a4f5d9c4
```

### Admin (.env)
```env
API_BASE_URL=http://localhost:8000
STREAMLIT_SERVER_PORT=8501
```

## 🐛 Xử Lý Lỗi Thường Gặp

### Lỗi 1: Port đã được sử dụng

**Triệu chứng:**
```
Error: Address already in use
```

**Giải pháp:**
```bash
# Dừng tất cả service
DUNG_LOCAL.bat

# Hoặc kill port cụ thể
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Lỗi 2: Module không tìm thấy

**Triệu chứng:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Giải pháp:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Lỗi 3: Database không tồn tại

**Triệu chứng:**
```
OperationalError: no such table
```

**Giải pháp:**
```bash
cd backend
python tao_du_lieu_mau.py
```

### Lỗi 4: CORS Error

**Triệu chứng:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Giải pháp:**
1. Kiểm tra `backend/.env` có `CORS_ORIGINS` đúng không
2. Restart backend
3. Hard refresh browser (Ctrl+Shift+R)

### Lỗi 5: Frontend không kết nối được Backend

**Triệu chứng:**
- Frontend hiển thị "Cannot connect to server"
- Console có lỗi network

**Giải pháp:**
1. Kiểm tra backend đang chạy: http://localhost:8000/api/health
2. Kiểm tra `frontend/.env` có `VITE_API_BASE_URL=http://localhost:8000`
3. Restart frontend

## 🧪 Test Checklist

Sau khi chạy tất cả service, kiểm tra:

### Backend
- [ ] http://localhost:8000 → Trả về JSON
- [ ] http://localhost:8000/docs → Swagger UI hiển thị
- [ ] http://localhost:8000/api/health → `{"status": "healthy"}`
- [ ] http://localhost:8000/api/db-test → Thông tin database

### Frontend
- [ ] http://localhost:5173 → Trang chủ hiển thị
- [ ] Console không có CORS errors
- [ ] Sản phẩm/dịch vụ load được
- [ ] Hình ảnh hiển thị đúng

### Admin Panel
- [ ] http://localhost:8501 → Dashboard hiển thị
- [ ] Login thành công
- [ ] CRUD operations hoạt động

### Kết Nối
- [ ] Mở `test-cors-locally.html`
- [ ] Chạy tất cả 4 tests
- [ ] Tất cả đều pass ✅

## 💡 Tips & Tricks

### 1. Xem Logs
Mỗi service chạy trong terminal riêng, xem logs trực tiếp ở đó.

### 2. Hot Reload
- Backend: Tự động reload khi sửa code Python
- Frontend: Tự động reload khi sửa code React
- Admin: Tự động reload khi sửa code Streamlit

### 3. Debug Mode
```bash
# Backend với debug
cd backend
python -m uvicorn ung_dung.chinh:ung_dung --reload --log-level debug

# Frontend với debug
cd frontend
npm run dev -- --debug
```

### 4. Clear Cache
```bash
# Backend
cd backend
del /f /q __pycache__\*
del /f /q ung_dung\__pycache__\*

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

## 🔄 Workflow Phát Triển

### 1. Bắt Đầu Ngày Làm Việc
```bash
git pull origin main
CHAY_LOCAL.bat
```

### 2. Phát Triển Feature
- Sửa code trong editor
- Service tự động reload
- Test trong browser

### 3. Kết Thúc Ngày
```bash
DUNG_LOCAL.bat
git add .
git commit -m "feat: your feature"
git push origin main
```

## 📞 Hỗ Trợ

### Nếu Vẫn Gặp Vấn Đề:

1. **Kiểm tra logs** trong các terminal window
2. **Chạy test** với `test-cors-locally.html`
3. **Xem file** `FIXES_APPLIED.md` để biết các fix đã áp dụng
4. **Reset lại** bằng cách:
   ```bash
   DUNG_LOCAL.bat
   # Đợi 5 giây
   CHAY_LOCAL.bat
   ```

### Files Tham Khảo:
- `FIXES_APPLIED.md` - Các fix đã áp dụng
- `FIX_CORS_AND_DEPLOYMENT.md` - Fix CORS chi tiết
- `DEPLOYMENT_CHECKLIST.md` - Checklist deploy
- `QUICK_FIX_REFERENCE.md` - Tham khảo nhanh

## ✅ Checklist Hoàn Chỉnh

Trước khi bắt đầu code:
- [ ] Python 3.12/3.13 đã cài
- [ ] Node.js 18+ đã cài
- [ ] Đã chạy `CHAY_LOCAL.bat`
- [ ] Tất cả 3 service đang chạy
- [ ] Test với `test-cors-locally.html` pass
- [ ] Frontend hiển thị đúng
- [ ] Backend API hoạt động
- [ ] Admin Panel login được

Nếu tất cả ✅ → Bạn đã sẵn sàng code! 🎉
