@echo off
cd /d "%~dp0.."
echo ====================================
echo Building Apex Sender (Portable + Game Server)
echo ====================================
echo.

REM Install requirements
echo [1/3] Installing requirements...
pip install -q pyinstaller
if exist requirements.txt pip install -q -r requirements.txt

REM Clean old ghost files
if exist "build_scripts\build" rmdir /s /q "build_scripts\build"
if exist "build_scripts\dist" rmdir /s /q "build_scripts\dist"
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec"
if exist "ApexSender.spec" del /q "ApexSender.spec"

echo [2/3] Building application...
echo Current directory: %CD%
echo.
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

REM Create service and install scripts
echo @echo off > "%OUTPUT_DIR%\install.bat"
echo echo Installing Apex Sender... >> "%OUTPUT_DIR%\install.bat"
echo xcopy /E /I /Y "ApexSender" "%%LOCALAPPDATA%%\ApexSender" ^>nul >> "%OUTPUT_DIR%\install.bat"
echo echo Installation completed. >> "%OUTPUT_DIR%\install.bat"
echo pause >> "%OUTPUT_DIR%\install.bat"

echo.
echo ====================================
echo Installer package created successfully!
echo ====================================
echo.
echo Location: %CD%\%OUTPUT_DIR%
echo.
echo Cleaning temporary files...
if exist "build_scripts\build" rmdir /s /q "build_scripts\build" 2>nul
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec" 2>nul
echo.
pause