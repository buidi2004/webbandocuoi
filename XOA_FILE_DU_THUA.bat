@echo off
chcp 65001 >nul
echo ========================================
echo XÓA TẤT CẢ FILE DƯ THỪA
echo ========================================
echo.

REM Xóa các file documentation dư thừa
echo [1/5] Xóa file documentation dư thừa...
del /F /Q "ADMIN_FEATURE_CHECK.md" 2>nul
del /F /Q "ADMIN_QUICK_START.md" 2>nul
del /F /Q "ADMIN_UPDATE_LOG.md" 2>nul
del /F /Q "BAT_DAU_NGAY.md" 2>nul
del /F /Q "DANG_NHAP_ADMIN.md" 2>nul
del /F /Q "DEBUG_BUTTONS.md" 2>nul
del /F /Q "DEPLOY_ADMIN_RENDER.md" 2>nul
del /F /Q "DEPLOY_RENDER_MANUAL.md" 2>nul
del /F /Q "DEPLOY_RENDER.md" 2>nul
del /F /Q "DEPLOY_VERCEL.md" 2>nul
del /F /Q "DEPLOYMENT_CHECKLIST.md" 2>nul
del /F /Q "FIX_ADMIN_ISSUES.md" 2>nul
del /F /Q "FIX_CORS_AND_DEPLOYMENT.md" 2>nul
del /F /Q "FIX_FRONTEND_BACKEND_CONNECTION.md" 2>nul
del /F /Q "FIX_UPLOAD_422.md" 2>nul
del /F /Q "FIXES_APPLIED.md" 2>nul
del /F /Q "HUONG_DAN_CHAY_LOCAL.md" 2>nul
del /F /Q "INDEX_TAI_LIEU.md" 2>nul
del /F /Q "KIEM_TRA_KET_NOI.md" 2>nul
del /F /Q "QUICK_FIX_BACKEND.md" 2>nul
del /F /Q "QUICK_FIX_REFERENCE.md" 2>nul
del /F /Q "README_LOCAL.md" 2>nul
del /F /Q "RENDER_FREE_ALTERNATIVES.md" 2>nul
del /F /Q "SO_SANH_2_FILE_ADMIN.md" 2>nul
del /F /Q "SUMMARY.md" 2>nul
del /F /Q "TEST_BUTTONS_FIX.md" 2>nul
del /F /Q "TOM_TAT_SETUP.md" 2>nul
del /F /Q "TRANG_THAI_ADMIN.md" 2>nul
del /F /Q "TRANG_THAI_CUOI_CUNG.md" 2>nul
del /F /Q "TRANG_THAI_SERVER.md" 2>nul

REM Xóa các file test
echo [2/5] Xóa file test...
del /F /Q "test_admin_api.py" 2>nul
del /F /Q "test_upload_direct.py" 2>nul
del /F /Q "test-connection.html" 2>nul
del /F /Q "test-cors-locally.html" 2>nul

REM Xóa các file script dư thừa
echo [3/5] Xóa script dư thừa...
del /F /Q "chay_server_optimized.bat" 2>nul
del /F /Q "chay_server.bat" 2>nul
del /F /Q "run_servers.py" 2>nul
del /F /Q "package-lock.json" 2>nul

REM Xóa file config không dùng
echo [4/5] Xóa config không dùng...
del /F /Q "docker-compose.yml" 2>nul
del /F /Q "vercel.json" 2>nul

REM Xóa thư mục docs_cu
echo [5/5] Xóa thư mục docs_cu...
if exist "docs_cu" (
    rmdir /S /Q "docs_cu" 2>nul
)

REM Xóa thư mục tep_tin
if exist "tep_tin" (
    rmdir /S /Q "tep_tin" 2>nul
)

REM Xóa admin optimized version
echo [6/7] Xóa admin optimized version...
del /F /Q "admin-python\quan_tri_optimized_v2.py" 2>nul
del /F /Q "admin-python\test_auth.py" 2>nul
del /F /Q "admin-python\modules\api_client.py" 2>nul

REM Xóa backend migration files
echo [7/7] Xóa migration files...
del /F /Q "backend\migrate_combo.py" 2>nul
del /F /Q "backend\tao_du_lieu_mau.py" 2>nul

echo.
echo ========================================
echo ✅ HOÀN TẤT!
echo ========================================
echo.
echo Đã xóa tất cả file dư thừa.
echo.
pause
