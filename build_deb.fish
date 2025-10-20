#!/usr/bin/env fish
# Создание .deb пакета для Ubuntu/Debian

set -l VERSION "1.0.0"
set -l APP_NAME "ollama-tray-chat"
set -l MAINTAINER "demon-5656 <your-email@example.com>"

echo "📦 Создание .deb пакета для Ubuntu/Debian..."

# Создаём структуру пакета
set -l DEB_DIR "releases/$APP_NAME-$VERSION-deb"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/icons/hicolor/scalable/apps"
mkdir -p "$DEB_DIR/usr/share/doc/$APP_NAME"

# Control файл
echo "Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: amd64
Depends: python3 (>= 3.10), python3-pyqt6, python3-requests
Maintainer: $MAINTAINER
Description: GUI chat client for Ollama with system tray support
 Ollama Tray Chat is a desktop application that provides a graphical
 interface for interacting with Ollama AI models. Features include:
 - System tray integration
 - Command execution with AI suggestions
 - Chat history persistence
 - Streaming responses
Homepage: https://github.com/demon-5656/ollama-tray-chat" > "$DEB_DIR/DEBIAN/control"

# Postinst скрипт
echo "#!/bin/bash
set -e
update-desktop-database || true
gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
exit 0" > "$DEB_DIR/DEBIAN/postinst"
chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Копируем файлы
cp ollama_tray_chat.py "$DEB_DIR/usr/bin/$APP_NAME"
chmod 755 "$DEB_DIR/usr/bin/$APP_NAME"
cp ollama-tray-chat.desktop "$DEB_DIR/usr/share/applications/"
cp icons/ollama-chat.svg "$DEB_DIR/usr/share/icons/hicolor/scalable/apps/"
cp README.md LICENSE "$DEB_DIR/usr/share/doc/$APP_NAME/"

# Создаём copyright файл
echo "Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: $APP_NAME
Source: https://github.com/demon-5656/ollama-tray-chat

Files: *
Copyright: 2025 demon-5656
License: MIT
 (Full license text from LICENSE file)" > "$DEB_DIR/usr/share/doc/$APP_NAME/copyright"

# Собираем пакет
dpkg-deb --build "$DEB_DIR" "releases/$APP_NAME-$VERSION-amd64.deb"

if test -f "releases/$APP_NAME-$VERSION-amd64.deb"
    echo "✅ .deb пакет создан: releases/$APP_NAME-$VERSION-amd64.deb"
    echo ""
    echo "Установка: sudo dpkg -i releases/$APP_NAME-$VERSION-amd64.deb"
    echo "           sudo apt-get install -f  # если есть зависимости"
else
    echo "❌ Ошибка создания .deb пакета"
end
