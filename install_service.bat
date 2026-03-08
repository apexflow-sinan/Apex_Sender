@echo off
echo Installing Apex Sender Service...
echo.
echo This requires Administrator privileges.
echo.

python main.py --install-service

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Service installed successfully!
    echo You can now start it from Services or use: sc start ApexSenderService
) else (
    echo.
    echo Failed to install service. Make sure you run this as Administrator.
)

pause
