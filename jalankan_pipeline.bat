@echo off
setlocal
title XARA PROJECT V2 - AUTOMATED PIPELINE LAUNCHER
color 0A

cd /d "C:\Users\Lenovo\xara_copilot"

echo =========================================================================
echo       XARA PROJECT V2: AUTOMATED SINGLE-RUNNER PIPELINE ENGINE
echo =========================================================================
echo.

set "EXCEL_PATH=%~1"

if not defined EXCEL_PATH (
    echo [PETUNJUK] Anda bisa drag-and-drop file Excel ATAU FOLDER langsung ke icon file .bat ini,
    echo            atau ketik/paste path file Template / folder kerja di bawah ini:
    echo.
    set /p "EXCEL_PATH=Masukkan Path File Excel atau Folder: "
)

if not defined EXCEL_PATH (
    echo [ERROR] Tidak ada path file yang dimasukkan.
    pause
    exit /b 1
)

:: Bersihkan tanda petik
set "EXCEL_PATH=%EXCEL_PATH:"=%"

if not exist "%EXCEL_PATH%" (
    color 0C
    echo.
    echo [ERROR] File atau Folder tidak ditemukan:
    echo "%EXCEL_PATH%"
    echo Silakan periksa kembali path Anda.
    echo.
    pause
    exit /b 1
)

echo.
echo [*] Memulai eksekusi LIVE REALTIME...
echo [*] Target : "%EXCEL_PATH%"
echo.

python -u run_project_v2_pipeline.py --excel "%EXCEL_PATH%"

if %ERRORLEVEL% equ 0 (
    color 0A
    echo.
    echo =========================================================================
    echo [SELESAI] Eksekusi berhasil 100%% tanpa error!
    echo =========================================================================
) else (
    color 0C
    echo.
    echo =========================================================================
    echo [GAGAL] Terjadi kesalahan saat eksekusi. Periksa log di atas.
    echo =========================================================================
)

echo.
pause
