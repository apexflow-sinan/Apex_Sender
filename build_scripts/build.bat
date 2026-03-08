@echo off
cd /d "%~dp0.."
echo ====================================
echo Building Apex Sender (Single File)
echo ====================================
echo.

echo [1/3] Installing dependencies...
pip install -q pyinstaller
if exist requirements.txt pip install -q -r requirements.txt

REM Clean old files
if exist "build_scripts\build" rmdir /s /q "build_scripts\build"
if exist "build_scripts\dist" rmdir /s /q "build_scripts\dist"
if exist "build_scripts\ApexSender.spec" del /q "build_scripts\ApexSender.spec"

echo [2/3] Building application...
echo.
echo Excluding large unnecessary files (android-sdk, gradle, ApexGamesAPK)...
python -m PyInstaller --noconfirm --onefile --windowed --name="ApexSender" --icon="%CD%\assets\icons\app_icon_multi.ico" --add-data="%CD%\src;src" --add-data="%CD%\assets;assets" --add-data="%CD%\web;web" --add-data="%CD%\ApexGames\assets;ApexGames/assets" --add-data="%CD%\ApexGames\Games;ApexGames/Games" --add-data="%CD%\ApexGames\res;ApexGames/res" --add-data="%CD%\ApexGames\data;ApexGames/data" --add-data="%CD%\ApexGames\*.html;ApexGames" --add-data="%CD%\ApexGames\*.js;ApexGames" --add-data="%CD%\ApexGames\*.json;ApexGames" --add-data="%CD%\ApexGames\server.py;ApexGames" --add-data="%CD%\ApexGames\README.md;ApexGames" --hidden-import="win32timezone" --hidden-import="flask" --hidden-import="werkzeug" --hidden-import="jinja2" --collect-submodules="src" --distpath="%CD%\build_scripts\dist" --workpath="%CD%\build_scripts\build" --specpath="%CD%\build_scripts" "%CD%\main.py"

if %errorlevel% neq 0 (
    echo Build failed!
    pause
    exit /b 1
)

echo [3/3] Build completed successfully!
echo.
echo ====================================
echo Build Complete!
echo ====================================
echo.
echo Location: build_scripts\dist\ApexSender.exe
echo.
echo You can now run the executable directly!
echo.
pause
