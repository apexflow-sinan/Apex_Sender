@echo off
chcp 65001 >nul
cd /d "%~dp0.."
echo ====================================
echo Building Apex Sender (Fast Build)
echo ====================================
echo.

REM Install requirements
echo [1/4] Installing requirements...
pip install -q pyinstaller
if exist requirements.txt pip install -q -r requirements.txt

REM Clean old files
if exist "build_scripts\build" rmdir /s /q "build_scripts\build"
if exist "build_scripts\dist" rmdir /s /q "build_scripts\dist"
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec"

REM Create temporary ApexGames folder without heavy files
echo [2/4] Preparing ApexGames (excluding android-sdk, gradle, APK)...
set "TEMP_GAMES=%CD%\build_scripts\temp_games"
if exist "%TEMP_GAMES%" rmdir /s /q "%TEMP_GAMES%"
mkdir "%TEMP_GAMES%"

xcopy /E /I /Y "%CD%\ApexGames\assets" "%TEMP_GAMES%\assets" >nul
xcopy /E /I /Y "%CD%\ApexGames\Games" "%TEMP_GAMES%\Games" >nul
xcopy /E /I /Y "%CD%\ApexGames\res" "%TEMP_GAMES%\res" >nul
xcopy /E /I /Y "%CD%\ApexGames\data" "%TEMP_GAMES%\data" >nul
copy /Y "%CD%\ApexGames\*.html" "%TEMP_GAMES%\" >nul 2>&1
copy /Y "%CD%\ApexGames\*.js" "%TEMP_GAMES%\" >nul 2>&1
copy /Y "%CD%\ApexGames\*.json" "%TEMP_GAMES%\" >nul 2>&1
copy /Y "%CD%\ApexGames\server.py" "%TEMP_GAMES%\" >nul 2>&1
copy /Y "%CD%\ApexGames\README.md" "%TEMP_GAMES%\" >nul 2>&1

echo [3/4] Building application (this will be much faster)...
echo.
python -m PyInstaller --noconfirm --onedir --windowed ^
    --name="ApexSender" ^
    --icon="%CD%\assets\icons\app_icon_multi.ico" ^
    --add-data="%CD%\src;src" ^
    --add-data="%CD%\assets;assets" ^
    --add-data="%CD%\web;web" ^
    --add-data="%TEMP_GAMES%;ApexGames" ^
    --hidden-import="win32timezone" ^
    --hidden-import="flask" ^
    --hidden-import="werkzeug" ^
    --hidden-import="jinja2" ^
    --collect-submodules="src" ^
    --exclude-module="PIL.SpiderImagePlugin" ^
    --exclude-module="PIL.WebPImagePlugin" ^
    --exclude-module="PIL.SgiImagePlugin" ^
    --distpath="%CD%\build_scripts\dist" ^
    --workpath="%CD%\build_scripts\build" ^
    --specpath="%CD%\build_scripts" ^
    "%CD%\main.py"

if %errorlevel% neq 0 (
    echo Build failed!
    rmdir /s /q "%TEMP_GAMES%" 2>nul
    pause
    exit /b 1
)

REM Clean temp folder
rmdir /s /q "%TEMP_GAMES%" 2>nul

echo [4/4] Creating installer package...
set "OUTPUT_DIR=build_scripts\ApexSender_Installer"
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

REM Copy application
xcopy /E /I /Y "build_scripts\dist\ApexSender" "%OUTPUT_DIR%\ApexSender" >nul

REM Create install script
if exist "build_scripts\install_template.bat" (
    copy "build_scripts\install_template.bat" "%OUTPUT_DIR%\install.bat" >nul
) else (
    echo @echo off > "%OUTPUT_DIR%\install.bat"
    echo echo Installing Apex Sender... >> "%OUTPUT_DIR%\install.bat"
    echo xcopy /E /I /Y "ApexSender" "%%LOCALAPPDATA%%\ApexSender" ^>nul >> "%OUTPUT_DIR%\install.bat"
    echo echo Installation completed. >> "%OUTPUT_DIR%\install.bat"
    echo pause >> "%OUTPUT_DIR%\install.bat"
)

REM Create service scripts
echo @echo off > "%OUTPUT_DIR%\install_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\install_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\install_service.bat"
echo ApexSender.exe --install-service >> "%OUTPUT_DIR%\install_service.bat"
echo pause >> "%OUTPUT_DIR%\install_service.bat"

echo @echo off > "%OUTPUT_DIR%\uninstall_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\uninstall_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\uninstall_service.bat"
echo ApexSender.exe --uninstall-service >> "%OUTPUT_DIR%\uninstall_service.bat"
echo pause >> "%OUTPUT_DIR%\uninstall_service.bat"

echo @echo off > "%OUTPUT_DIR%\run_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\run_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\run_service.bat"
echo ApexSender.exe --service >> "%OUTPUT_DIR%\run_service.bat"

REM Create README
echo ===================================== > "%OUTPUT_DIR%\README.txt"
echo   Apex Sender - Fast File Transfer >> "%OUTPUT_DIR%\README.txt"
echo ===================================== >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Run ApexSender\ApexSender.exe to start >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"

echo.
echo ====================================
echo Build Complete! (Fast Build)
echo ====================================
echo.
echo Location: %CD%\%OUTPUT_DIR%
echo.
echo Cleaning temporary files...
if exist "build_scripts\build" rmdir /s /q "build_scripts\build" 2>nul
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec" 2>nul
echo.
pause
