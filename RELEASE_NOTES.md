# Release Notes v1.0.0

**Release Date**: 20 октября 2025

## 🎉 Initial Release

Первая стабильная версия Ollama Tray Chat - графического клиента для работы с Ollama AI моделями.

---

## ✨ Основные возможности

### 💬 Чат с AI
- Потоковая передача ответов от Ollama API
- Поддержка различных моделей (настраивается)
- Системные промпты для кастомизации поведения
- История сообщений с persistence в JSONL

### 🖥️ Интерфейс
- Нативный GUI на PyQt6 для Linux
- Интеграция с системным треем KDE Plasma
- Темная тема с высоким контрастом
- Адаптивный дизайн окна

### ⚙️ Выполнение команд
- **AI-предложенные команды**: ассистент предлагает готовые команды
- **Ручное одобрение**: пользователь контролирует выполнение
- **Allowlist безопасности**: разрешены только безопасные утилиты
  - `ls`, `cat`, `echo`, `grep`, `systemctl`, `git`, `ps`, `df`, `pacman` и др.
- **Deny-паттерны**: автоматическая блокировка опасных команд
  - `rm -rf`, форкбомбы, редиректы в `/dev/null`
- **Live вывод**: стриминг stdout/stderr во время выполнения

### 📦 Установка
- **Arch Linux**: Fish-скрипты для автоматической установки
- **.desktop файл**: интеграция в меню приложений KDE
- **Иконка SVG**: масштабируемая иконка для трея
- **Автозапуск**: опциональный старт при загрузке системы

---

## 📥 Доступные пакеты

### Linux (универсальный бинарник)
- **Файл**: `ollama-tray-chat-1.0.0-linux-x86_64.tar.gz` (104 MB)
- **Архитектура**: x86_64
- **Дистрибутивы**: Arch, Ubuntu 22.04+, Debian 12+, Fedora 38+
- **Установка**:
  ```bash
  tar -xzf ollama-tray-chat-1.0.0-linux-x86_64.tar.gz
  cd ollama-tray-chat-1.0.0-linux
  ./install.fish
  ```

### Arch Linux (PKGBUILD)
- **Файл**: `PKGBUILD`
- **Установка через AUR** (скоро):
  ```bash
  yay -S ollama-tray-chat
  ```
- **Установка вручную**:
  ```bash
  makepkg -si
  ```

### Windows (скоро)
- **Файл**: `ollama-tray-chat-1.0.0-windows-x86_64.zip`
- **Требования**: Windows 10/11, Ollama установлен
- Для сборки используйте `build_windows.bat` на Windows машине

### Debian/Ubuntu (в разработке)
- **Файл**: `ollama-tray-chat-1.0.0-amd64.deb`
- Требует `dpkg-deb` для сборки

---

## 🔧 Требования

### Обязательные
- Python 3.10+
- PyQt6
- requests
- **Ollama** запущен на `http://127.0.0.1:11434`

### Рекомендуемые
- KDE Plasma 6 (для лучшей интеграции трея)
- Fish shell (для установочных скриптов)
- 2GB RAM минимум

---

## 🚀 Быстрый старт

1. **Убедитесь, что Ollama запущен:**
   ```bash
   ollama serve
   ```

2. **Установите приложение:**
   ```bash
   # Через скрипт установки (Arch Linux)
   ./install.fish
   
   # Или запустите напрямую
   python3 ollama_tray_chat.py
   ```

3. **Настройте модель** в Settings → Model

4. **Начните чат** и попросите AI предложить команды:
   ```
   Предложи команду для просмотра использования диска
   ```

5. **Одобрьте команды** из списка справа кнопкой "Одобрить"

---

## 📝 Известные ограничения

### v1.0.0
- ❌ Windows версия не собрана (требуется Windows для сборки)
- ❌ .deb пакет не создан (требуется `dpkg-deb`)
- ❌ Нет поддержки интерактивных команд (PTY)
- ❌ Allowlist команд жестко закодирован (нельзя редактировать в UI)
- ⚠️ Протестировано только на Arch Linux + KDE Plasma

### Планируется в v1.1.0
- ✅ Windows binary
- ✅ .deb и .rpm пакеты
- ✅ Настраиваемый allowlist команд
- ✅ Dry-run mode для команд
- ✅ Отдельный лог для выполненных команд
- ✅ Экспорт истории чата

---

## 🛡️ Безопасность

### Allowlist команд
Разрешены только:
```python
"ls", "cat", "echo", "grep", "sed", "awk", "head", "tail",
"systemctl", "journalctl", "docker", "git", "curl", "wget",
"ping", "whoami", "id", "ps", "df", "du", "uptime", "free",
"pacman", "apt", "snap", "uname"
```

### Deny-паттерны
Блокируются:
- `rm -rf` - удаление с рекурсией
- `:(){ :|:& };:` - форкбомбы
- `> /dev/null 2>&1 &` - фоновые процессы с редиректами

**⚠️ ВАЖНО**: Всегда проверяйте команды перед одобрением! AI может ошибаться.

---

## 📚 Документация

- [README.md](README.md) - основная документация
- [QUICKSTART.md](QUICKSTART.md) - быстрый старт за 5 минут
- [BUILD_GUIDE.md](BUILD_GUIDE.md) - инструкции по сборке релизов
- [COLOR_SCHEMES.md](COLOR_SCHEMES.md) - альтернативные цветовые схемы
- [CONTRIBUTING.md](CONTRIBUTING.md) - гайд для контрибьюторов

---

## 🤝 Благодарности

- [Ollama](https://ollama.ai/) - за локальный AI runtime
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - за GUI фреймворк
- Сообществу Arch Linux за отличные пакеты

---

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE)

---

## 🔗 Ссылки

- **GitHub**: https://github.com/demon-5656/ollama-tray-chat
- **Issues**: https://github.com/demon-5656/ollama-tray-chat/issues
- **Wiki**: https://github.com/demon-5656/ollama-tray-chat/wiki (скоро)

---

**Спасибо за использование Ollama Tray Chat!** 🎉

Если вы нашли баг или хотите предложить фичу - создайте issue на GitHub.
