@echo off
echo ========================================
echo   IVIE Wedding Studio - Start Servers
echo ========================================
echo.

echo [1/3] Starting Backend API (Port 8000)...
REM Khởi tạo dữ liệu nếu database chưa có
if not exist "backend\ivie.db" (
    echo Database not found. Initializing...
    backend\.venv312\Scripts\python.exe backend\khoi_tao_du_lieu.py
)
start "Backend API" cmd /k "cd backend && .\.venv312\Scripts\python.exe -m uvicorn ung_dung.chinh:ung_dung --reload --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend (Port 5173)...
start "Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo [3/3] Starting Admin Panel (Port 8501)...
start "Admin Panel" cmd /k "cd admin-python && streamlit run quan_tri.py --server.port 8501 --server.address 127.0.0.1"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   Servers đang khởi động...
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo Backend Docs: http://localhost:8000/docs
echo Frontend:     http://localhost:5173
echo Admin Panel:  http://localhost:8501
echo.
echo LƯU Ý: Backend có thể gặp lỗi nếu dùng Python 3.14 RC
echo        Nên sử dụng Python 3.12 hoặc 3.13
echo.
pause

