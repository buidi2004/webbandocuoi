# ⚡ DEPLOY NHANH LÊN RENDER

## 🎯 3 BƯỚC CHÍNH

### 1️⃣ BACKEND API
```
Dashboard → New + → Web Service
Repository: webbandocuoi
Root Directory: backend
Build: pip install -r requirements.txt
Start: uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port $PORT

Environment Variables:
- PYTHON_VERSION = 3.12.0
- SECRET_KEY = ivie-secret-key-2024-production
- CORS_ORIGINS = (sẽ cập nhật sau)
```

### 2️⃣ FRONTEND
```
Dashboard → New + → Static Site
Repository: webbandocuoi
Root Directory: frontend
Build: npm install && npm run build
Publish: dist

Environment Variables:
- NODE_VERSION = 20.11.0
- VITE_API_URL = https://ivie-backend-api.onrender.com
```

### 3️⃣ ADMIN PANEL
```
Dashboard → New + → Web Service
Repository: webbandocuoi
Root Directory: admin-python
Build: pip install -r requirements.txt
Start: streamlit run quan_tri.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

Environment Variables:
- PYTHON_VERSION = 3.12.0
- API_BASE_URL = https://ivie-backend-api.onrender.com
- ADMIN_USERNAME = admin
- ADMIN_PASSWORD = admin123
```

---

## 🔧 SAU KHI DEPLOY

### Cập nhật CORS
Vào Backend → Environment → Sửa `CORS_ORIGINS`:
```
https://ivie-frontend.onrender.com,https://ivie-admin-panel.onrender.com
```

### Kiểm tra
- ✅ Backend: https://ivie-backend-api.onrender.com/docs
- ✅ Frontend: https://ivie-frontend.onrender.com
- ✅ Admin: https://ivie-admin-panel.onrender.com

---

## ⚠️ LƯU Ý QUAN TRỌNG

1. **Free Plan**: Service sleep sau 15 phút → Lần đầu truy cập chậm 30-60s
2. **Auto Deploy**: Push code lên GitHub → Render tự động deploy
3. **Logs**: Vào service → Tab "Logs" để xem lỗi
4. **Database**: Mỗi service có database riêng (SQLite)

---

## 🚨 XỬ LÝ LỖI NHANH

### CORS Error
→ Kiểm tra `CORS_ORIGINS` trong Backend

### Build Failed
→ Xem Logs → Kiểm tra requirements.txt/package.json

### 502 Bad Gateway
→ Service đang khởi động, đợi 1-2 phút

### Không có dữ liệu
→ Vào Admin → Thêm sản phẩm mẫu

---

**📖 Xem hướng dẫn chi tiết: `HUONG_DAN_DEPLOY_RENDER.md`**
