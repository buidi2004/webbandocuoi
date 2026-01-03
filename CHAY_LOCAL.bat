@echo off
chcp 65001 >nul
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     IVIE WEDDING STUDIO - CHẠY LOCAL                       ║
echo ║     Frontend + Backend + Database + Admin                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Kiểm tra Python
echo [Bước 1/5] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được cài đặt!
    echo    Vui lòng cài Python 3.12 hoặc 3.13
    pause
    exit /b 1
)
python --version
echo ✅ Python OK
echo.

REM Kiểm tra Node.js
echo [Bước 2/5] Kiểm tra Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js không được cài đặt!
    echo    Vui lòng cài Node.js từ https://nodejs.org
    pause
    exit /b 1
)
node --version
npm --version
echo ✅ Node.js OK
echo.

REM Kiểm tra Database
echo [Bước 3/5] Kiểm tra Database...
if exist "backend\ivie.db" (
    echo ✅ Database đã tồn tại: backend\ivie.db
) else (
    echo ⚠️  Database chưa có, sẽ tạo mới khi khởi động backend
)
echo.

REM Kiểm tra .env files
echo [Bước 4/5] Kiểm tra Environment Files...
if exist "backend\.env" (
    echo ✅ backend\.env
) else (
    echo ⚠️  backend\.env không tồn tại
)
if exist "frontend\.env" (
    echo ✅ frontend\.env
) else (
    echo ⚠️  frontend\.env không tồn tại
)
if exist "admin-python\.env" (
    echo ✅ admin-python\.env
) else (
    echo ⚠️  admin-python\.env không tồn tại
)
echo.

REM Khởi động các service
echo [Bước 5/5] Khởi động các service...
echo.
echo ┌─────────────────────────────────────────────────────────┐
echo │ 🚀 Đang khởi động Backend API (Port 8000)...            │
echo └─────────────────────────────────────────────────────────┘
start "🔧 Backend API - Port 8000" cmd /k "cd backend && python -m uvicorn ung_dung.chinh:ung_dung --reload --host 127.0.0.1 --port 8000"
timeout /t 3 /nobreak >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ 🎨 Đang khởi động Frontend (Port 5173)...               │
echo └─────────────────────────────────────────────────────────┘
start "🎨 Frontend - Port 5173" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo ┌─────────────────────────────────────────────────────────┐
echo │ 👨‍💼 Đang khởi động Admin Panel (Port 8501)...            │
echo └─────────────────────────────────────────────────────────┘
start "👨‍💼 Admin Panel - Port 8501" cmd /k "cd admin-python && streamlit run quan_tri.py --server.port 8501 --server.address 127.0.0.1"
timeout /t 2 /nobreak >nul

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  ✅ TẤT CẢ SERVICE ĐÃ KHỞI ĐỘNG           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📍 CÁC ĐƯỜNG DẪN:
echo ─────────────────────────────────────────────────────────────
echo.
echo   🔧 Backend API:       http://localhost:8000
echo   📚 API Docs:          http://localhost:8000/docs
echo   🧪 Health Check:      http://localhost:8000/api/health
echo   🗄️  Database Test:     http://localhost:8000/api/db-test
echo.
echo   🎨 Frontend:          http://localhost:5173
echo.
echo   👨‍💼 Admin Panel:       http://localhost:8501
echo.
echo ─────────────────────────────────────────────────────────────
echo.
echo 💡 MẸO:
echo   - Mở test-cors-locally.html để kiểm tra kết nối
echo   - Xem logs trong các cửa sổ terminal đã mở
echo   - Nhấn Ctrl+C trong terminal để dừng service
echo.
echo 🔄 Để dừng tất cả service:
echo   - Đóng tất cả cửa sổ terminal
echo   - Hoặc chạy: DUNG_LOCAL.bat
echo.
pause
