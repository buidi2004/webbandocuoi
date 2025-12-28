# Hướng dẫn chạy Server

## ⚠️ Lưu ý quan trọng

**Backend yêu cầu Python 3.12 hoặc 3.13** (không tương thích với Python 3.14 RC)

## Cách chạy nhanh

Chạy file `chay_server.bat` để khởi động tất cả các server cùng lúc.

## Cách chạy thủ công

### 1. Backend API (Port 8000)

```bash
cd backend
python -m uvicorn ung_dung.chinh:ung_dung --reload --host 127.0.0.1 --port 8000
```

**Truy cập:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### 2. Frontend (Port 5173)

```bash
cd frontend
npm install  # Chỉ cần chạy lần đầu
npm run dev
```

**Truy cập:** http://localhost:5173

### 3. Admin Panel (Port 8501)

```bash
cd admin-python
streamlit run quan_tri.py --server.port 8501 --server.address 127.0.0.1
```

**Truy cập:** http://localhost:8501

## Kiểm tra Python version

```bash
python --version
```

Nếu là Python 3.14, bạn cần:
1. Cài đặt Python 3.12 hoặc 3.13
2. Hoặc sử dụng virtual environment với Python 3.12/3.13

## Cài đặt dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

### Admin Panel
```bash
cd admin-python
pip install -r requirements.txt
```

