@echo off
chcp 65001 >nul
title IVIE Wedding Studio - Server Manager

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║          IVIE WEDDING STUDIO - SERVER MANAGER             ║
echo ║                  Optimized Edition                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Set working directory
cd /d "%~dp0"

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python khong duoc cai dat hoac khong co trong PATH
    pause
    exit /b 1
)

echo [INFO] Dang khoi dong servers...
echo.

:: Start Backend Server in new window
echo [1/2] Khoi dong Backend API Server (port 8000)...
start "IVIE Backend API" cmd /k "cd /d %~dp0backend && python -m uvicorn ung_dung.chinh:ung_dung --host 0.0.0.0 --port 8000 --reload"

:: Wait for backend to start
echo [INFO] Doi backend khoi dong...
timeout /t 3 /nobreak >nul

:: Start Admin Panel in new window
echo [2/2] Khoi dong Admin Panel (port 8501)...
start "IVIE Admin Panel" cmd /k "cd /d %~dp0admin-python && streamlit run quan_tri.py --server.port 8501 --server.address 0.0.0.0"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                    SERVERS STARTED!                       ║
echo ╠═══════════════════════════════════════════════════════════╣
echo ║  Backend API:    http://localhost:8000                    ║
echo ║  API Docs:       http://localhost:8000/docs               ║
echo ║  Admin Panel:    http://localhost:8501                    ║
echo ╠═══════════════════════════════════════════════════════════╣
echo ║  Nhan phim bat ky de mo Admin Panel trong trinh duyet...  ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

pause >nul

:: Open Admin Panel in browser
start http://localhost:8501

echo.
echo [INFO] Da mo Admin Panel trong trinh duyet
echo [INFO] Dong cua so nay se KHONG dung servers
echo [INFO] De dung servers, dong cac cua so "IVIE Backend API" va "IVIE Admin Panel"
echo.
pause
