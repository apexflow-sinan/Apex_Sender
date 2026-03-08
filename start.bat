@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ====================================
echo      Apex Sender - Launcher
echo ====================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: Python not installed!
    echo Please install Python from: https://python.org
    echo.
    pause
    exit /b 1
)

REM Check main file
if not exist "main.py" (
    echo Error: main.py not found!
    echo.
    pause
    exit /b 1
)

echo Starting Apex Sender...
echo.
echo Choose mode:
echo [1] With Console (Development)
echo [2] Without Console (Normal Use)
echo.
set /p choice="Choose (1 or 2): "

if "%choice%"=="2" (
    echo Starting without console...
    start pythonw main.pyw
    exit
) else (
    echo Starting with console...
    python main.py --skip-firewall
)

if %errorLevel% neq 0 (
    echo.
    echo Application error occurred!
    echo.
)

pause