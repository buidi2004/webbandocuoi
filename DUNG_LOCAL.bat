@echo off
chcp 65001 >nul
color 0C
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     DỪNG TẤT CẢ SERVICE LOCAL                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Dừng Backend API (Python/Uvicorn)...
taskkill /F /FI "WINDOWTITLE eq 🔧 Backend API*" >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Backend*" >nul 2>&1
echo ✅ Backend đã dừng

echo [2/4] Dừng Frontend (Node/Vite)...
taskkill /F /FI "WINDOWTITLE eq 🎨 Frontend*" >nul 2>&1
taskkill /F /IM node.exe /FI "WINDOWTITLE eq *Frontend*" >nul 2>&1
echo ✅ Frontend đã dừng

echo [3/4] Dừng Admin Panel (Streamlit)...
taskkill /F /FI "WINDOWTITLE eq 👨‍💼 Admin Panel*" >nul 2>&1
taskkill /F /IM streamlit.exe >nul 2>&1
echo ✅ Admin Panel đã dừng

echo [4/4] Dọn dẹp các process còn sót...
taskkill /F /IM python.exe /FI "MEMUSAGE gt 50000" >nul 2>&1
echo ✅ Hoàn tất

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║     ✅ ĐÃ DỪNG TẤT CẢ SERVICE                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
pause
