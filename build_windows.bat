@echo off
REM Скрипт для создания Windows релиза Ollama Tray Chat
REM Запускать на Windows с установленным Python 3.10+, PyQt6 и PyInstaller

set VERSION=1.0.0
set APP_NAME=ollama-tray-chat

echo 🚀 Создание Windows релиза %APP_NAME% v%VERSION%
echo.

REM Проверка PyInstaller
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ❌ PyInstaller не установлен. Устанавливаю...
    python -m pip install pyinstaller
)

echo 📦 Сборка для Windows...
pyinstaller --name=%APP_NAME% ^
    --onefile ^
    --windowed ^
    --icon=icons\ollama-chat.svg ^
    --add-data="icons;icons" ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    ollama_tray_chat.py

if exist "dist\%APP_NAME%.exe" (
    echo ✅ Исполняемый файл создан: dist\%APP_NAME%.exe
    
    REM Создаём папку релиза
    if not exist "releases" mkdir releases
    if exist "releases\%APP_NAME%-%VERSION%-windows" rmdir /s /q "releases\%APP_NAME%-%VERSION%-windows"
    mkdir "releases\%APP_NAME%-%VERSION%-windows"
    
    copy "dist\%APP_NAME%.exe" "releases\%APP_NAME%-%VERSION%-windows\"
    copy README.md "releases\%APP_NAME%-%VERSION%-windows\"
    copy QUICKSTART.md "releases\%APP_NAME%-%VERSION%-windows\"
    copy LICENSE "releases\%APP_NAME%-%VERSION%-windows\"
    xcopy /E /I icons "releases\%APP_NAME%-%VERSION%-windows\icons"
    
    REM Создаём ZIP архив
    powershell Compress-Archive -Path "releases\%APP_NAME%-%VERSION%-windows" -DestinationPath "releases\%APP_NAME%-%VERSION%-windows-x86_64.zip" -Force
    
    echo ✅ Создан архив: releases\%APP_NAME%-%VERSION%-windows-x86_64.zip
) else (
    echo ❌ Ошибка сборки для Windows
)

echo.
echo ✨ Windows релиз готов!
pause
