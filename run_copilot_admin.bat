@echo off
setlocal
cd /d "C:\Users\Lenovo\xara_copilot"

net session >nul 2>&1
if %errorlevel% neq 0 goto :NOT_ADMIN

:IS_ADMIN
title Xara Antigravity Co-Pilot Engine - Mode Administrator
cls
echo =========================================================
echo   XARA ANTIGRAVITY CO-PILOT - MODE ADMINISTRATOR
echo =========================================================
echo.
echo Menjalankan pengujian otomatis...
echo.

python test_engine.py

echo.
echo =========================================================
echo Selesai! Log tersimpan di: admin_test_log.txt
echo =========================================================
echo.
pause
exit /b

:NOT_ADMIN
echo =========================================================
echo   Meminta Hak Akses Administrator via UAC Prompt
echo =========================================================
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process cmd.exe -ArgumentList '/k cd /d C:\Users\Lenovo\xara_copilot && python test_engine.py' -Verb RunAs"
exit /b
