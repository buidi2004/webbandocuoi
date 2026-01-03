@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================
REM IVIE Wedding Studio - Deploy Script (Windows)
REM ============================================
REM Quick script to commit and push changes to GitHub
REM Render will automatically deploy when changes are pushed

echo ============================================
echo    IVIE Wedding Studio - Deploy Script
echo ============================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo [WARNING] Git not initialized. Initializing...
    git init
    echo [OK] Git initialized
)

REM Check for uncommitted changes
git status --porcelain > temp_status.txt
set /p STATUS=<temp_status.txt
del temp_status.txt

if "!STATUS!"=="" (
    echo [WARNING] No changes to commit
    goto :end
)

REM Show status
echo [INFO] Current changes:
git status --short
echo.

REM Get commit message
if "%~1"=="" (
    set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
    if "!COMMIT_MSG!"=="" (
        for /f "tokens=1-5 delims=/ " %%a in ('date /t') do set DATE=%%c-%%a-%%b
        for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIME=%%a:%%b
        set COMMIT_MSG=Update: !DATE! !TIME!
    )
) else (
    set COMMIT_MSG=%~1
)

echo.
echo [INFO] Commit message: !COMMIT_MSG!
echo.

REM Add all changes
echo [INFO] Adding all changes...
git add .

REM Commit
echo [INFO] Committing...
git commit -m "!COMMIT_MSG!"

REM Push to origin
echo [INFO] Pushing to GitHub...

REM Try pushing to main branch first, then master
git push origin main 2>nul
if errorlevel 1 (
    git push origin master 2>nul
    if errorlevel 1 (
        echo [WARNING] Push failed. Trying to set upstream...
        git push -u origin main 2>nul
        if errorlevel 1 (
            git push -u origin master 2>nul
            if errorlevel 1 (
                echo [ERROR] No remote 'origin' configured.
                echo Please run:
                echo   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
                goto :end
            )
        )
    )
)

echo.
echo ============================================
echo [SUCCESS] Successfully pushed to GitHub!
echo ============================================
echo.
echo [INFO] Render will automatically deploy in 2-5 minutes.
echo.
echo Check deployment status at:
echo   https://dashboard.render.com
echo.

:end
endlocal
pause
