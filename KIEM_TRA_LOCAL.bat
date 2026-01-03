@echo off
chcp 65001 >nul
color 0B
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     KIỂM TRA HỆ THỐNG LOCAL                                ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set "errors=0"

REM Kiểm tra Python
echo [1/8] Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python CHƯA cài đặt
    set /a errors+=1
) else (
    python --version
    echo ✅ Python OK
)
echo.

REM Kiểm tra Node.js
echo [2/8] Kiểm tra Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js CHƯA cài đặt
    set /a errors+=1
) else (
    node --version
    echo ✅ Node.js OK
)
echo.

REM Kiểm tra npm
echo [3/8] Kiểm tra npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm CHƯA cài đặt
    set /a errors+=1
) else (
    npm --version
    echo ✅ npm OK
)
echo.

REM Kiểm tra Database
echo [4/8] Kiểm tra Database...
if exist "backend\ivie.db" (
    echo ✅ Database tồn tại: backend\ivie.db
    for %%A in ("backend\ivie.db") do echo    Kích thước: %%~zA bytes
) else (
    echo ⚠️  Database CHƯA có (sẽ tạo khi chạy backend)
)
echo.

REM Kiểm tra .env files
echo [5/8] Kiểm tra Environment Files...
if exist "backend\.env" (
    echo ✅ backend\.env
) else (
    echo ❌ backend\.env KHÔNG tồn tại
    set /a errors+=1
)
if exist "frontend\.env" (
    echo ✅ frontend\.env
) else (
    echo ❌ frontend\.env KHÔNG tồn tại
    set /a errors+=1
)
if exist "admin-python\.env" (
    echo ✅ admin-python\.env
) else (
    echo ❌ admin-python\.env KHÔNG tồn tại
    set /a errors+=1
)
echo.

REM Kiểm tra Backend dependencies
echo [6/8] Kiểm tra Backend Dependencies...
if exist "backend\requirements.txt" (
    echo ✅ backend\requirements.txt tồn tại
) else (
    echo ❌ backend\requirements.txt KHÔNG tồn tại
    set /a errors+=1
)
echo.

REM Kiểm tra Frontend dependencies
echo [7/8] Kiểm tra Frontend Dependencies...
if exist "frontend\package.json" (
    echo ✅ frontend\package.json tồn tại
    if exist "frontend\node_modules" (
        echo ✅ frontend\node_modules đã cài
    ) else (
        echo ⚠️  frontend\node_modules CHƯA cài (chạy: cd frontend && npm install)
    )
) else (
    echo ❌ frontend\package.json KHÔNG tồn tại
    set /a errors+=1
)
echo.

REM Kiểm tra Ports
echo [8/8] Kiểm tra Ports đang sử dụng...
netstat -ano | findstr :8000 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 8000 (Backend) - Trống
) else (
    echo ⚠️  Port 8000 (Backend) - Đang được sử dụng
)
netstat -ano | findstr :5173 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 5173 (Frontend) - Trống
) else (
    echo ⚠️  Port 5173 (Frontend) - Đang được sử dụng
)
netstat -ano | findstr :8501 >nul 2>&1
if errorlevel 1 (
    echo ✅ Port 8501 (Admin) - Trống
) else (
    echo ⚠️  Port 8501 (Admin) - Đang được sử dụng
)
echo.

REM Tổng kết
echo ╔════════════════════════════════════════════════════════════╗
if %errors% EQU 0 (
    echo ║     ✅ HỆ THỐNG SẴN SÀNG - CÓ THỂ CHẠY LOCAL              ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo 🚀 Chạy lệnh sau để khởi động:
    echo    CHAY_LOCAL.bat
) else (
    echo ║     ❌ CÓ %errors% LỖI - CẦN KHẮC PHỤC                              ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo 📋 Xem hướng dẫn chi tiết:
    echo    HUONG_DAN_CHAY_LOCAL.md
)
echo.
pause
