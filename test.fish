#!/usr/bin/env fish
# Тестовый запуск приложения с проверкой Ollama

set APP_DIR (dirname (realpath (status -f)))

echo "🧪 ТЕСТОВЫЙ ЗАПУСК OLLAMA TRAY CHAT"
echo ""

# Проверка зависимостей
echo "1. Проверка Python зависимостей..."
if python3 -c "import PyQt6, requests" 2>/dev/null
    echo "   ✅ PyQt6 и requests установлены"
else
    echo "   ❌ Отсутствуют зависимости!"
    echo "   Установите: sudo pacman -S python-pyqt6 python-requests"
    exit 1
end

# Проверка Ollama
echo ""
echo "2. Проверка Ollama..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1
    set models (curl -s http://127.0.0.1:11434/api/tags | python3 -c "import sys, json; print(len(json.load(sys.stdin)['models']))")
    echo "   ✅ Ollama запущен, доступно моделей: $models"
else
    echo "   ⚠️  Ollama не отвечает на http://127.0.0.1:11434"
    echo "   Запустите: systemctl --user start ollama"
    echo ""
    read -P "Продолжить запуск приложения? (y/N): " -n 1 answer
    if test "$answer" != "y" -a "$answer" != "Y"
        exit 1
    end
end

# Запуск приложения
echo ""
echo "3. Запуск приложения..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$APP_DIR"
python3 ollama_tray_chat.py $argv
