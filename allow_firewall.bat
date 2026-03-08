@echo off
echo السماح لتطبيق نقل الملفات بالمرور عبر الجدار الناري
echo ================================================

REM التحقق من صلاحيات المدير
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo يتطلب صلاحيات المدير!
    echo انقر بزر اليمين على الملف واختر "Run as administrator"
    pause
    exit /b 1
)

REM السماح بالبورت 8888
netsh advfirewall firewall add rule name="File Transfer Port" dir=in action=allow protocol=TCP localport=8888
netsh advfirewall firewall add rule name="File Transfer Port OUT" dir=out action=allow protocol=TCP localport=8888

echo تم السماح للتطبيق بالمرور عبر الجدار الناري
echo - البورت 8888 مفتوح للدخول والخروج

pause