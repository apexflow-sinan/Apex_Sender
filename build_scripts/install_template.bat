@echo off
chcp 65001 >nul
echo ====================================
echo   Apex Sender - Installation
echo ====================================
echo.

set "INSTALL_DIR=%LOCALAPPDATA%\ApexSender"
set "DESKTOP=%USERPROFILE%\Desktop"

echo [1/3] Checking requirements...
if not exist "ApexSender\ApexSender.exe" (
    echo Error: ApexSender.exe not found in current directory.
    echo Please run this script from the installer folder.
    pause
    exit /b 1
)

echo [2/3] Installing application...
if exist "%INSTALL_DIR%" (
    echo Removing old installation...
    rmdir /s /q "%INSTALL_DIR%" 2>nul
)

echo Copying files...
xcopy /E /I /Y "ApexSender" "%INSTALL_DIR%" >nul
if %errorlevel% neq 0 (
    echo Error: Failed to copy application files.
    echo Please check permissions and try running as Administrator.
    pause
    exit /b 1
)
echo Application files copied successfully.

echo [3/3] Creating desktop shortcut...
if exist "%INSTALL_DIR%\ApexSender.exe" (
    powershell -ExecutionPolicy Bypass -Command "try { $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Apex Sender.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\ApexSender.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; if (Test-Path '%INSTALL_DIR%\_internal\assets\app_icon.ico') { $Shortcut.IconLocation = '%INSTALL_DIR%\_internal\assets\app_icon.ico' } else { $Shortcut.IconLocation = '%INSTALL_DIR%\ApexSender.exe' }; $Shortcut.Save(); exit 0 } catch { Write-Host 'Error: Could not create desktop shortcut.'; exit 1 }"
    if %errorlevel% equ 0 (
        echo Desktop shortcut created successfully.
    ) else (
        echo Warning: Could not create desktop shortcut. Try running as Administrator.
    )
) else (
    echo Warning: ApexSender.exe not found after installation.
)

echo.
echo ====================================
echo   Installation Completed!
echo ====================================
echo.
echo Location: %INSTALL_DIR%
if exist "%DESKTOP%\Apex Sender.lnk" (
    echo Shortcut: %DESKTOP%\Apex Sender.lnk
) else (
    echo Shortcut: Not created (check permissions)
)
echo.
echo You can now run Apex Sender from:
echo - Desktop shortcut (if created)
echo - Start Menu (search for "Apex Sender")
echo - Direct path: %INSTALL_DIR%\ApexSender.exe
echo.
pause