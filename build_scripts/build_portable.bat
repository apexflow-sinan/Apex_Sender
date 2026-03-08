@echo off
cd /d "%~dp0.."
echo ====================================
echo Building Apex Sender (Portable)
echo ====================================
echo.

REM Install requirements
echo [1/3] Installing requirements...
pip install -q pyinstaller
if exist requirements.txt pip install -q -r requirements.txt

REM Clean old files
if exist "build_scripts\build" rmdir /s /q "build_scripts\build"
if exist "build_scripts\dist" rmdir /s /q "build_scripts\dist"
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec"

echo [2/3] Building application...
echo Current directory: %CD%
echo.
echo Excluding large unnecessary files (android-sdk, gradle, ApexGamesAPK)...
python -m PyInstaller --noconfirm --onedir --windowed --name="ApexSender" --icon="%CD%\assets\icons\app_icon_multi.ico" --add-data="%CD%\src;src" --add-data="%CD%\assets;assets" --add-data="%CD%\web;web" --add-data="%CD%\ApexGames\assets;ApexGames/assets" --add-data="%CD%\ApexGames\Games;ApexGames/Games" --add-data="%CD%\ApexGames\res;ApexGames/res" --add-data="%CD%\ApexGames\data;ApexGames/data" --add-data="%CD%\ApexGames\*.html;ApexGames" --add-data="%CD%\ApexGames\*.js;ApexGames" --add-data="%CD%\ApexGames\*.json;ApexGames" --add-data="%CD%\ApexGames\server.py;ApexGames" --add-data="%CD%\ApexGames\README.md;ApexGames" --hidden-import="win32timezone" --hidden-import="flask" --hidden-import="werkzeug" --hidden-import="jinja2" --collect-submodules="src" --distpath="%CD%\build_scripts\dist" --workpath="%CD%\build_scripts\build" --specpath="%CD%\build_scripts" "%CD%\main.py"

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo [3/3] Creating installer package...
set "OUTPUT_DIR=build_scripts\ApexSender_Installer"
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

REM Copy application
xcopy /E /I /Y "build_scripts\dist\ApexSender" "%OUTPUT_DIR%\ApexSender" >nul

REM Create install script from template
if exist "build_scripts\install_template.bat" (
    copy "build_scripts\install_template.bat" "%OUTPUT_DIR%\install.bat" >nul
) else (
    echo Warning: install_template.bat not found, creating basic installer...
    echo @echo off > "%OUTPUT_DIR%\install.bat"
    echo echo Installing Apex Sender... >> "%OUTPUT_DIR%\install.bat"
    echo xcopy /E /I /Y "ApexSender" "%%LOCALAPPDATA%%\ApexSender" ^>nul >> "%OUTPUT_DIR%\install.bat"
    echo echo Installation completed. >> "%OUTPUT_DIR%\install.bat"
    echo pause >> "%OUTPUT_DIR%\install.bat"
)

REM Create service install script
echo @echo off > "%OUTPUT_DIR%\install_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\install_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\install_service.bat"
echo echo   Installing Apex Sender Service >> "%OUTPUT_DIR%\install_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\install_service.bat"
echo echo. >> "%OUTPUT_DIR%\install_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\install_service.bat"
echo ApexSender.exe --install-service >> "%OUTPUT_DIR%\install_service.bat"
echo if %%errorlevel%% equ 0 ^( >> "%OUTPUT_DIR%\install_service.bat"
echo     echo. >> "%OUTPUT_DIR%\install_service.bat"
echo     echo Service installed successfully! >> "%OUTPUT_DIR%\install_service.bat"
echo     echo. >> "%OUTPUT_DIR%\install_service.bat"
echo     echo Starting service... >> "%OUTPUT_DIR%\install_service.bat"
echo     sc start ApexSenderService ^>nul 2^>^&1 >> "%OUTPUT_DIR%\install_service.bat"
echo     if %%errorlevel%% equ 0 ^( >> "%OUTPUT_DIR%\install_service.bat"
echo         echo Service started successfully! >> "%OUTPUT_DIR%\install_service.bat"
echo     ^) else ^( >> "%OUTPUT_DIR%\install_service.bat"
echo         echo Note: Service installed but needs manual start. >> "%OUTPUT_DIR%\install_service.bat"
echo         echo Run as Administrator: sc start ApexSenderService >> "%OUTPUT_DIR%\install_service.bat"
echo     ^) >> "%OUTPUT_DIR%\install_service.bat"
echo ^) else ^( >> "%OUTPUT_DIR%\install_service.bat"
echo     echo Failed to install service. >> "%OUTPUT_DIR%\install_service.bat"
echo ^) >> "%OUTPUT_DIR%\install_service.bat"
echo echo. >> "%OUTPUT_DIR%\install_service.bat"
echo pause >> "%OUTPUT_DIR%\install_service.bat"

REM Create service uninstall script
echo @echo off > "%OUTPUT_DIR%\uninstall_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\uninstall_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\uninstall_service.bat"
echo echo   Uninstalling Apex Sender Service >> "%OUTPUT_DIR%\uninstall_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\uninstall_service.bat"
echo echo. >> "%OUTPUT_DIR%\uninstall_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\uninstall_service.bat"
echo ApexSender.exe --uninstall-service >> "%OUTPUT_DIR%\uninstall_service.bat"
echo if %%errorlevel%% equ 0 ^( >> "%OUTPUT_DIR%\uninstall_service.bat"
echo     echo Service uninstalled successfully! >> "%OUTPUT_DIR%\uninstall_service.bat"
echo ^) else ^( >> "%OUTPUT_DIR%\uninstall_service.bat"
echo     echo Failed to uninstall service. >> "%OUTPUT_DIR%\uninstall_service.bat"
echo ^) >> "%OUTPUT_DIR%\uninstall_service.bat"
echo echo. >> "%OUTPUT_DIR%\uninstall_service.bat"
echo pause >> "%OUTPUT_DIR%\uninstall_service.bat"

REM Create service run script
echo @echo off > "%OUTPUT_DIR%\run_service.bat"
echo chcp 65001 ^>nul >> "%OUTPUT_DIR%\run_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\run_service.bat"
echo echo   Running Apex Sender in Service Mode >> "%OUTPUT_DIR%\run_service.bat"
echo echo ===================================== >> "%OUTPUT_DIR%\run_service.bat"
echo echo. >> "%OUTPUT_DIR%\run_service.bat"
echo echo Press Ctrl+C to stop... >> "%OUTPUT_DIR%\run_service.bat"
echo echo. >> "%OUTPUT_DIR%\run_service.bat"
echo cd /d "%%~dp0ApexSender" >> "%OUTPUT_DIR%\run_service.bat"
echo ApexSender.exe --service >> "%OUTPUT_DIR%\run_service.bat"

REM Create README file
echo ===================================== > "%OUTPUT_DIR%\README.txt"
echo   Apex Sender - Installation Guide >> "%OUTPUT_DIR%\README.txt"
echo ===================================== >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Installation Steps: >> "%OUTPUT_DIR%\README.txt"
echo 1. Run install.bat as Administrator >> "%OUTPUT_DIR%\README.txt"
echo 2. The application will be installed automatically >> "%OUTPUT_DIR%\README.txt"
echo 3. A desktop shortcut will be created >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Service Mode (Background): >> "%OUTPUT_DIR%\README.txt"
echo - install_service.bat: Install as Windows service >> "%OUTPUT_DIR%\README.txt"
echo - uninstall_service.bat: Remove Windows service >> "%OUTPUT_DIR%\README.txt"
echo - run_service.bat: Run in service mode (console) >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Alternatively, you can run directly from: >> "%OUTPUT_DIR%\README.txt"
echo ApexSender\ApexSender.exe >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Command Line Options: >> "%OUTPUT_DIR%\README.txt"
echo --service: Run in service mode (no GUI) >> "%OUTPUT_DIR%\README.txt"
echo --install-service: Install Windows service >> "%OUTPUT_DIR%\README.txt"
echo --uninstall-service: Remove Windows service >> "%OUTPUT_DIR%\README.txt"
echo --setup: Show setup dialog only >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo Features: >> "%OUTPUT_DIR%\README.txt"
echo - Fast file transfer over local network >> "%OUTPUT_DIR%\README.txt"
echo - Send files and folders >> "%OUTPUT_DIR%\README.txt"
echo - Automatic folder compression >> "%OUTPUT_DIR%\README.txt"
echo - Simple and modern interface >> "%OUTPUT_DIR%\README.txt"
echo - Background service support >> "%OUTPUT_DIR%\README.txt"
echo. >> "%OUTPUT_DIR%\README.txt"
echo ===================================== >> "%OUTPUT_DIR%\README.txt"

echo.
echo ====================================
echo Installer package created successfully!
echo ====================================
echo.
echo Location: %CD%\%OUTPUT_DIR%
echo.
echo You can now:
echo 1. Copy "%OUTPUT_DIR%" folder to any device
echo 2. Run install.bat to install GUI version
echo 3. Run install_service.bat to install as Windows service
echo 4. Run run_service.bat for console service mode
echo 5. Or run ApexSender.exe directly
echo.
echo Cleaning temporary files...
if exist "build_scripts\build" rmdir /s /q "build_scripts\build" 2>nul
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec" 2>nul
echo.
pause
