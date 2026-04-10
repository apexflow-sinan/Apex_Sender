@echo off
echo Uninstalling Apex Sender Service...
echo.
echo This requires Administrator privileges.
echo.

python main.py --uninstall-service

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Service uninstalled successfully!
) else (
    echo.
    echo Failed to uninstall service. Make sure you run this as Administrator.
)

pause
