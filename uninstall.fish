#!/usr/bin/env fish
# Скрипт удаления Ollama Tray Chat

set APP_NAME "ollama-tray-chat"
set LOCAL_APPS "$HOME/.local/share/applications"
set ICON_DIR "$HOME/.local/share/icons/hicolor/scalable/apps"
set CONFIG_DIR "$HOME/.config/$APP_NAME"
set DATA_DIR "$HOME/.local/share/$APP_NAME"

echo "🗑️  Удаление Ollama Tray Chat..."
echo ""

# Удаляем .desktop файл
if test -f "$LOCAL_APPS/$APP_NAME.desktop"
    rm "$LOCAL_APPS/$APP_NAME.desktop"
    echo "✅ Ярлык удалён"
else
    echo "ℹ️  Ярлык не найден"
end

# Удаляем иконку
if test -f "$ICON_DIR/ollama-chat.svg"
    rm "$ICON_DIR/ollama-chat.svg"
    echo "✅ Иконка удалена"
else
    echo "ℹ️  Иконка не найдена"
end

# Обновляем базы
update-desktop-database "$LOCAL_APPS" 2>/dev/null
if command -v gtk-update-icon-cache &> /dev/null
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null
end

echo ""
echo "❓ Удалить настройки и историю чатов?"
echo "   Конфигурация: $CONFIG_DIR"
echo "   История: $DATA_DIR"
echo ""
read -P "Удалить? (y/N): " -n 1 answer

if test "$answer" = "y" -o "$answer" = "Y"
    if test -d "$CONFIG_DIR"
        rm -rf "$CONFIG_DIR"
        echo "✅ Конфигурация удалена"
    end
    if test -d "$DATA_DIR"
        rm -rf "$DATA_DIR"
        echo "✅ История удалена"
    end
else
    echo "ℹ️  Настройки и история сохранены"
end

echo ""
echo "✨ Удаление завершено!"
