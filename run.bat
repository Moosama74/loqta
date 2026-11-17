@echo off
chcp 65001 >nul
title منصة لقطة للسيارات - تشغيل تلقائي
echo ========================================================
echo        مرحباً بك في منصة لُقطـة للسيارات (Loqta Cars)
echo ========================================================
echo.
echo * ملاحظة هامة: المنصة لا تحتاج XAMPP ولا MySQL نهائياً!
echo * قاعدة البيانات تعمل بتقنية SQLite المدمجة تلقائياً.
echo.

cd /d "%~dp0"

:: Set Python Path
set "PYTHON_EXE=python"
if exist "C:\Users\SHOEIB TEK\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=C:\Users\SHOEIB TEK\AppData\Local\Programs\Python\Python312\python.exe"
)

echo [1/3] فحص قاعدة البيانات وتجهيز البيانات الافتراضية...
"%PYTHON_EXE%" init_db.py

echo.
echo [2/3] فتح الموقع تلقائياً في المتصفح...
start http://localhost:8000

echo.
echo [3/3] تشغيل سيرفر المنصة على الرابط: http://localhost:8000
echo.
echo ========================================================
echo السيرفر يعمل الآن بنجاح! لا تغلق هذه النافذة أثناء التصفح.
echo لوحة الأرباح والعمولات متاحة على: http://localhost:8000/admin
echo ========================================================
echo.

"%PYTHON_EXE%" -m uvicorn main:app --host 127.0.0.1 --port 8000
if %errorlevel% neq 0 (
    echo.
    echo حدث خطأ أثناء التشغيل. تفاصيل الخطأ في الأعلى.
    pause
)
