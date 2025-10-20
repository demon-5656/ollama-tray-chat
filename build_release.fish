#!/usr/bin/env fish
# Скрипт для создания релизных версий Ollama Tray Chat

set -l VERSION "1.0.0"
set -l APP_NAME "ollama-tray-chat"

echo "🚀 Создание релизных версий $APP_NAME v$VERSION"
echo ""

# Проверка PyInstaller
if not command -v pyinstaller &> /dev/null
    echo "❌ PyInstaller не установлен. Устанавливаю..."
    pip install pyinstaller
end

# Создаём директорию для релизов
mkdir -p releases

echo "📦 Сборка для Linux (Arch/Ubuntu/Debian)..."
pyinstaller --name=$APP_NAME \
    --onefile \
    --windowed \
    --icon=icons/ollama-chat.svg \
    --add-data="icons:icons" \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    ollama_tray_chat.py

# Создаём архив для Linux
if test -f "dist/$APP_NAME"
    echo "✅ Исполняемый файл создан: dist/$APP_NAME"
    
    # Создаём полный пакет для Linux
    mkdir -p "releases/$APP_NAME-$VERSION-linux"
    cp "dist/$APP_NAME" "releases/$APP_NAME-$VERSION-linux/"
    cp README.md QUICKSTART.md LICENSE "releases/$APP_NAME-$VERSION-linux/"
    cp -r icons "releases/$APP_NAME-$VERSION-linux/"
    cp ollama-tray-chat.desktop "releases/$APP_NAME-$VERSION-linux/"
    cp install.fish uninstall.fish run.fish "releases/$APP_NAME-$VERSION-linux/"
    
    # Создаём tar.gz архив
    cd releases
    tar -czf "$APP_NAME-$VERSION-linux-x86_64.tar.gz" "$APP_NAME-$VERSION-linux"
    cd ..
    
    echo "✅ Создан архив: releases/$APP_NAME-$VERSION-linux-x86_64.tar.gz"
else
    echo "❌ Ошибка сборки для Linux"
end

echo ""
echo "✨ Релизы готовы в папке releases/"
echo ""
echo "📋 Следующие шаги:"
echo "1. Для сборки Windows версии запустите этот скрипт на Windows с установленным Python и PyQt6"
echo "2. Загрузите архивы на GitHub Releases"
echo "3. Создайте .deb и .rpm пакеты (опционально)"
