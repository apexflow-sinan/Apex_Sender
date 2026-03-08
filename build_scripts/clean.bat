@echo off
cd /d "%~dp0.."
echo ====================================
echo Cleaning Build Files - Apex Sender
echo ====================================
echo.

REM Delete build folders
if exist "build_scripts\build" (
    echo Deleting build folder...
    rmdir /s /q "build_scripts\build"
    echo Build folder deleted
)

if exist "build_scripts\dist" (
    echo Deleting dist folder...
    rmdir /s /q "build_scripts\dist"
    echo Dist folder deleted
)

if exist "build_scripts\ApexSender_Installer" (
    echo Deleting installer folder...
    rmdir /s /q "build_scripts\ApexSender_Installer"
    echo Installer folder deleted
)

REM Delete .spec files
if exist "build_scripts\*.spec" (
    echo Deleting .spec files...
    del /q "build_scripts\*.spec"
    echo .spec files deleted
)

REM Delete __pycache__ folders
echo Deleting __pycache__ folders...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo __pycache__ folders deleted

REM Delete .pyc files
echo Deleting .pyc files...
del /s /q "*.pyc" 2>nul
echo .pyc files deleted

echo.
echo ====================================
echo Cleanup completed successfully!
echo ====================================
pause
