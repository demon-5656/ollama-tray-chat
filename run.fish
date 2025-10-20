#!/usr/bin/env fish
# Быстрый запуск Ollama Tray Chat

set APP_DIR (dirname (realpath (status -f)))

# Проверка Ollama
if not systemctl --user is-active ollama &> /dev/null
    echo "⚠️  Ollama не запущен. Запускаю..."
    systemctl --user start ollama
    sleep 2
end

# Запуск приложения
python3 "$APP_DIR/ollama_tray_chat.py" $argv
