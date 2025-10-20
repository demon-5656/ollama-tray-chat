#!/usr/bin/env fish
# Скрипт установки Ollama Tray Chat для Arch Linux + KDE

set APP_DIR (dirname (realpath (status -f)))
set APP_NAME "ollama-tray-chat"
set DESKTOP_FILE "$APP_DIR/$APP_NAME.desktop"
set LOCAL_APPS "$HOME/.local/share/applications"
set ICON_DIR "$HOME/.local/share/icons/hicolor/scalable/apps"

echo "🚀 Установка Ollama Tray Chat..."
echo ""

# Проверка зависимостей
echo "📦 Проверка зависимостей..."

set MISSING_DEPS ""

if not command -v python3 &> /dev/null
    set MISSING_DEPS "$MISSING_DEPS python"
end

if not python3 -c "import PyQt6" 2>/dev/null
    set MISSING_DEPS "$MISSING_DEPS python-pyqt6"
end

if not python3 -c "import requests" 2>/dev/null
    set MISSING_DEPS "$MISSING_DEPS python-requests"
end

if test -n "$MISSING_DEPS"
    echo "❌ Отсутствуют зависимости:$MISSING_DEPS"
    echo ""
    echo "Установите их командой:"
    echo "  sudo pacman -S$MISSING_DEPS"
    exit 1
end

echo "✅ Все зависимости установлены"
echo ""

# Делаем скрипт исполняемым
echo "🔧 Настройка прав доступа..."
chmod +x "$APP_DIR/ollama_tray_chat.py"
echo "✅ Права установлены"
echo ""

# Создаём директории
echo "📁 Создание директорий..."
mkdir -p "$LOCAL_APPS"
mkdir -p "$ICON_DIR"
echo "✅ Директории созданы"
echo ""

# Копируем .desktop файл
echo "📋 Установка ярлыка приложения..."
cp "$DESKTOP_FILE" "$LOCAL_APPS/"
echo "✅ Ярлык установлен в $LOCAL_APPS"
echo ""

# Копируем иконку
echo "🎨 Установка иконки..."
cp "$APP_DIR/icons/ollama-chat.svg" "$ICON_DIR/"
echo "✅ Иконка установлена"
echo ""

# Обновляем базу приложений
echo "🔄 Обновление базы приложений..."
update-desktop-database "$LOCAL_APPS" 2>/dev/null
echo "✅ База обновлена"
echo ""

# Обновляем кэш иконок
echo "🎨 Обновление кэша иконок..."
if command -v gtk-update-icon-cache &> /dev/null
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null
end
echo "✅ Кэш обновлён"
echo ""

# Проверка Ollama
echo "🤖 Проверка Ollama..."
if systemctl --user is-active ollama &> /dev/null
    echo "✅ Ollama запущен"
else
    echo "⚠️  Ollama не запущен"
    echo ""
    echo "Для установки и запуска Ollama:"
    echo "  yay -S ollama-bin"
    echo "  systemctl --user enable --now ollama"
    echo "  ollama pull phi3.5:3.8b-mini-instruct"
end
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Установка завершена успешно!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 Теперь вы можете:"
echo "  1. Найти приложение в меню KDE (Ollama Tray Chat)"
echo "  2. Запустить из терминала: $APP_DIR/ollama_tray_chat.py"
echo "  3. Запустить свёрнутым в трей: $APP_DIR/ollama_tray_chat.py --minimize"
echo ""
echo "📂 Конфигурация: ~/.config/ollama-tray-chat/"
echo "📜 История чатов: ~/.local/share/ollama-tray-chat/"
echo ""
echo "Приятного использования! 🚀"
