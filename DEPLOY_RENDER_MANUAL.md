# 🚀 Deploy Database & Backend Thủ Công Trên Render

Hướng dẫn chi tiết từng bước để deploy PostgreSQL Database và Backend (Python) lên Render miễn phí.

---

## 📋 Tổng Quan

**Thứ tự deploy:**
1. Database (PostgreSQL) - Tạo trước
2. Backend (Web Service Python) - Kết nối với Database

**Thời gian:** ~15-20 phút

---

## 🗄️ BƯỚC 1: Deploy PostgreSQL Database

### 1.1. Tạo Database

1. **Vào Render Dashboard:** https://dashboard.render.com
2. **Đăng nhập** bằng GitHub
3. Click **"New +"** → Chọn **"PostgreSQL"**

### 1.2. Cấu Hình Database

Điền thông tin:

| Field | Giá Trị |
|-------|---------|
| **Name** | `ivie-db-final` (hoặc tên bạn muốn) |
| **Database** | `ivie_wedding` |
| **User** | `ivie_user` |
| **Region** | `Singapore` (gần Việt Nam nhất) |
| **PostgreSQL Version** | `16` (mới nhất) |
| **Plan** | **Free** ⭐ |

### 1.3. Tạo Database

- Click **"Create Database"**
- Chờ 2-3 phút để Render provision database
- Trạng thái sẽ chuyển từ "Creating" → "Available"

### 1.4. Lấy Connection String

Sau khi database sẵn sàng:

1. Vào tab **"Info"**
2. Tìm **"Internal Database URL"** hoặc **"External Database URL"**
3. Copy URL này (dạng: `postgresql://user:password@host:port/database`)
4. **LƯU LẠI** - sẽ dùng cho Backend

**Ví dụ:**
```
postgresql://ivie_user:abc123xyz@dpg-xxxxx-a.singapore-postgres.render.com/ivie_wedding
```

### 1.5. Kiểm Tra Database

Trong tab **"Info"**, bạn sẽ thấy:
- ✅ Status: Available
- ✅ Connection Info
- ✅ PSQL Command (để connect từ terminal nếu cần)

---

## 🐍 BƯỚC 2: Deploy Backend (Python Web Service)

### 2.1. Tạo Web Service

1. Vào Render Dashboard
2. Click **"New +"** → Chọn **"Web Service"**
3. Chọn **"Build and deploy from a Git repository"**
4. Click **"Next"**

### 2.2. Kết Nối GitHub Repository

1. **Connect Repository:**
   - Nếu chưa connect GitHub: Click "Connect GitHub"
   - Authorize Render truy cập repos
   
2. **Chọn Repository:**
   - Tìm repo `webbandocuoi`
   - Click **"Connect"**

### 2.3. Cấu Hình Backend Service

Điền thông tin:

| Field | Giá Trị |
|-------|---------|
| **Name** | `ivie-be-final` |
| **Region** | `Singapore` |
| **Branch** | `main` |
| **Root Directory** | `backend` ⚠️ QUAN TRỌNG! |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn ung_dung.chinh:ung_dung --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 60` |
| **Plan** | **Free** ⭐ |

### 2.4. Thêm Environment Variables

Scroll xuống phần **"Environment Variables"**, click **"Add Environment Variable"**:

#### Biến 1: DATABASE_URL
- **Key:** `DATABASE_URL`
- **Value:** `<paste Internal Database URL từ bước 1.4>`

#### Biến 2: PORT
- **Key:** `PORT`
- **Value:** `8000`

#### Biến 3: PYTHON_VERSION
- **Key:** `PYTHON_VERSION`
- **Value:** `3.12.0`

#### Biến 4: TELEGRAM_BOT_TOKEN (nếu có)
- **Key:** `TELEGRAM_BOT_TOKEN`
- **Value:** `<your_telegram_bot_token>`

#### Biến 5: TELEGRAM_CHAT_ID (nếu có)
- **Key:** `TELEGRAM_CHAT_ID`
- **Value:** `<your_telegram_chat_id>`

### 2.5. Auto-Deploy Settings

Trong phần **"Auto-Deploy"**:
- ✅ Bật **"Auto-Deploy"** (Yes)
- Render sẽ tự động deploy khi bạn push code mới

### 2.6. Tạo Service

- Click **"Create Web Service"**
- Render sẽ bắt đầu build và deploy
- Chờ 5-10 phút

### 2.7. Theo Dõi Build Process

Trong tab **"Logs"**, bạn sẽ thấy:
```
==> Cloning from https://github.com/buidi2004/webbandocuoi...
==> Installing dependencies...
==> pip install -r requirements.txt
==> Starting service...
==> Your service is live 🎉
```

### 2.8. Kiểm Tra Backend

Sau khi deploy thành công:

1. **Lấy URL:**
   - Ở đầu trang, copy URL (dạng: `https://ivie-be-final.onrender.com`)

2. **Test API:**
   - Mở browser, vào: `https://ivie-be-final.onrender.com/docs`
   - Bạn sẽ thấy Swagger UI (FastAPI docs)
   - Test một vài endpoints

3. **Kiểm tra Health:**
   - Vào: `https://ivie-be-final.onrender.com/api/health`
   - Nếu thấy response OK → Backend hoạt động!

---

## 🔗 BƯỚC 3: Kết Nối Frontend Với Backend

### 3.1. Cập Nhật Frontend Config

Nếu Frontend đang trên Vercel, thêm Environment Variable:

1. Vào Vercel Dashboard
2. Chọn project Frontend
3. Settings → Environment Variables
4. Thêm:
   ```
   VITE_API_URL=https://ivie-be-final.onrender.com
   ```
5. Redeploy Frontend

### 3.2. Cập Nhật CORS Trong Backend

Nếu Frontend gặp lỗi CORS, cập nhật file `backend/ung_dung/chinh.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push code lên GitHub, Render sẽ tự động redeploy.

---

## 🎯 BƯỚC 4: Tạo Dữ Liệu Mẫu (Tùy Chọn)

### 4.1. Kết Nối Database Từ Local

Dùng PSQL command từ Render Dashboard:

```bash
psql postgresql://ivie_user:password@host:port/ivie_wedding
```

### 4.2. Chạy Migration Script

Hoặc tạo endpoint trong Backend để init data:

```python
@app.post("/api/init-data")
async def init_data():
    # Chạy script tạo dữ liệu mẫu
    # ...
    return {"message": "Data initialized"}
```

Sau đó call endpoint này một lần:
```bash
curl -X POST https://ivie-be-final.onrender.com/api/init-data
```

---

## 🐛 Troubleshooting

### Lỗi: Build Failed

**Nguyên nhân:** Thiếu dependencies hoặc lỗi code

**Giải pháp:**
1. Check logs trong Render Dashboard
2. Kiểm tra `requirements.txt` có đầy đủ không
3. Test build local:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m ung_dung.chinh
   ```

### Lỗi: Application Failed to Start

**Nguyên nhân:** Start command sai hoặc port không đúng

**Giải pháp:**
1. Kiểm tra Start Command:
   ```bash
   gunicorn ung_dung.chinh:ung_dung --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker
   ```
2. Đảm bảo `gunicorn` và `uvicorn` có trong `requirements.txt`

### Lỗi: Database Connection Failed

**Nguyên nhân:** DATABASE_URL sai hoặc database chưa sẵn sàng

**Giải pháp:**
1. Kiểm tra DATABASE_URL trong Environment Variables
2. Đảm bảo database status = "Available"
3. Dùng **Internal Database URL** (nhanh hơn External)

### Lỗi: Service Sleeps After 15 Minutes

**Nguyên nhân:** Free tier tự động sleep khi không có traffic

**Giải pháp:**
1. Dùng UptimeRobot để ping mỗi 5 phút:
   - URL: `https://ivie-be-final.onrender.com/api/health`
   - Interval: 5 minutes
2. Hoặc chấp nhận cold start (15-30 giây) khi có request đầu tiên

### Lỗi: CORS Policy

**Nguyên nhân:** Backend chưa cho phép domain Frontend

**Giải pháp:**
Thêm domain Vercel vào CORS config (xem Bước 3.2)

---

## 📊 Monitoring & Logs

### Xem Logs

1. Vào Render Dashboard
2. Chọn service Backend
3. Tab **"Logs"** → Xem real-time logs
4. Tab **"Metrics"** → Xem CPU, Memory usage

### Restart Service

Nếu service bị lỗi:
1. Tab **"Settings"**
2. Scroll xuống
3. Click **"Manual Deploy"** → **"Clear build cache & deploy"**

---

## 💡 Tips Tối Ưu

### 1. Giảm Cold Start Time

Thêm vào `backend/ung_dung/chinh.py`:
```python
@app.on_event("startup")
async def startup():
    # Warm up database connection
    pass
```

### 2. Cache Dependencies

Render tự động cache pip packages giữa các builds.

### 3. Optimize Workers

Free tier chỉ có 512MB RAM, dùng 1 worker:
```bash
--workers 1
```

### 4. Health Check Endpoint

Tạo endpoint để monitoring:
```python
@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now()}
```

---

## 📝 Checklist Deploy

### Database
- [ ] Tạo PostgreSQL database
- [ ] Chọn region Singapore
- [ ] Chọn plan Free
- [ ] Copy Internal Database URL
- [ ] Kiểm tra status = Available

### Backend
- [ ] Tạo Web Service
- [ ] Connect GitHub repo
- [ ] Set Root Directory = `backend`
- [ ] Set Runtime = Python 3
- [ ] Set Build Command
- [ ] Set Start Command
- [ ] Thêm DATABASE_URL environment variable
- [ ] Thêm PORT environment variable
- [ ] Bật Auto-Deploy
- [ ] Kiểm tra build logs
- [ ] Test API endpoints
- [ ] Test /docs endpoint

### Frontend Connection
- [ ] Cập nhật VITE_API_URL trong Vercel
- [ ] Cập nhật CORS trong Backend
- [ ] Test API calls từ Frontend

---

## 🎉 Kết Luận

Bạn đã deploy thành công:
- ✅ PostgreSQL Database (FREE)
- ✅ Backend API (FREE)
- ✅ Auto-deploy khi push code

**URLs:**
- Database: `postgresql://...` (internal)
- Backend: `https://ivie-be-final.onrender.com`
- API Docs: `https://ivie-be-final.onrender.com/docs`

**Tổng chi phí:** $0/tháng 🎉

---

## 📚 Tài Liệu Tham Khảo

- [Render PostgreSQL Docs](https://render.com/docs/databases)
- [Render Web Services Docs](https://render.com/docs/web-services)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Gunicorn with Uvicorn Workers](https://www.uvicorn.org/deployment/#gunicorn)
