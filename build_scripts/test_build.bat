@echo off
chcp 65001 >nul
echo ====================================
echo Testing Built Application
echo ====================================
echo.

if not exist "dist\ApexSender\ApexSender.exe" (
    echo Error: ApexSender.exe not found!
    echo Please build the application first using build_portable.bat
    pause
    exit /b 1
)

echo Testing executable...
echo.
cd dist\ApexSender
ApexSender.exe --help 2>nul
if %errorlevel% neq 0 (
    echo Warning: Application may have issues
)

echo.
echo Checking required folders...
if exist "_internal\src" (
    echo [OK] src folder found
) else (
    echo [ERROR] src folder missing!
)

if exist "_internal\assets" (
    echo [OK] assets folder found
) else (
    echo [ERROR] assets folder missing!
)

if exist "_internal\web" (
    echo [OK] web folder found
) else (
    echo [ERROR] web folder missing!
)

if exist "_internal\ApexGames" (
    echo [OK] ApexGames folder found
) else (
    echo [ERROR] ApexGames folder missing!
)

echo.
echo Test completed!
echo.
pause
