#!/usr/bin/env fish
# Скрипт для автоматического создания GitHub Release

set -l VERSION "1.0.0"
set -l REPO "demon-5656/ollama-tray-chat"
set -l TAG "v$VERSION"

echo "🚀 Создание GitHub Release $TAG..."

# Проверка gh CLI
if not command -v gh &> /dev/null
    echo "❌ GitHub CLI (gh) не установлен"
    echo "Установите: sudo pacman -S github-cli"
    echo "Или используйте веб-интерфейс: https://github.com/$REPO/releases/new?tag=$TAG"
    exit 1
end

# Проверка авторизации
if not gh auth status &> /dev/null
    echo "❌ Необходима авторизация в GitHub"
    echo "Выполните: gh auth login"
    exit 1
end

# Создание релиза
gh release create "$TAG" \
    --repo "$REPO" \
    --title "Ollama Tray Chat v$VERSION - Initial Release" \
    --notes-file RELEASE_NOTES.md \
    releases/ollama-tray-chat-$VERSION-linux-x86_64.tar.gz

if test $status -eq 0
    echo "✅ Release $TAG успешно создан!"
    echo "🔗 https://github.com/$REPO/releases/tag/$TAG"
else
    echo "❌ Ошибка создания релиза"
    echo "Попробуйте через веб-интерфейс: https://github.com/$REPO/releases/new?tag=$TAG"
end
