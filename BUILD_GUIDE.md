# 🔨 Build Guide - Ollama Tray Chat

Инструкции по созданию релизных версий для различных платформ.

---

## 📋 Содержание

- [Linux (универсальный бинарник)](#linux-универсальный-бинарник)
- [Arch Linux (PKGBUILD)](#arch-linux-pkgbuild)
- [Ubuntu/Debian (.deb)](#ubuntudebian-deb)
- [Windows (.exe)](#windows-exe)

---

## Linux (универсальный бинарник)

### Требования
- Python 3.10+
- PyQt6
- PyInstaller

### Сборка

```bash
# Установка зависимостей
pip install pyinstaller

# Запуск сборки
./build_release.fish
```

Результат: `releases/ollama-tray-chat-1.0.0-linux-x86_64.tar.gz`

### Установка

```bash
tar -xzf ollama-tray-chat-1.0.0-linux-x86_64.tar.gz
cd ollama-tray-chat-1.0.0-linux
./install.fish
```

---

## Arch Linux (PKGBUILD)

### Сборка пакета

```bash
# Создание архива исходников
git archive --format=tar.gz --prefix=ollama-tray-chat-1.0.0/ v1.0.0 > ollama-tray-chat-1.0.0.tar.gz

# Сборка пакета
makepkg -si
```

### Установка

```bash
sudo pacman -U ollama-tray-chat-1.0.0-1-x86_64.pkg.tar.zst
```

### Публикация в AUR

```bash
# Клонирование AUR репозитория
git clone ssh://aur@aur.archlinux.org/ollama-tray-chat.git aur-ollama-tray-chat
cd aur-ollama-tray-chat

# Копирование PKGBUILD и .SRCINFO
cp ../PKGBUILD .
makepkg --printsrcinfo > .SRCINFO

# Коммит и пуш
git add PKGBUILD .SRCINFO
git commit -m "Initial import: ollama-tray-chat 1.0.0"
git push
```

---

## Ubuntu/Debian (.deb)

### Требования
- dpkg
- dpkg-dev

### Сборка

```bash
./build_deb.fish
```

Результат: `releases/ollama-tray-chat-1.0.0-amd64.deb`

### Установка

```bash
sudo dpkg -i releases/ollama-tray-chat-1.0.0-amd64.deb
sudo apt-get install -f  # установка зависимостей, если нужно
```

### Удаление

```bash
sudo apt-get remove ollama-tray-chat
```

---

## Windows (.exe)

### Требования
- Windows 10/11
- Python 3.10+ (установлен через официальный установщик)
- PyQt6: `pip install PyQt6`
- PyInstaller: `pip install pyinstaller`

### Сборка

```cmd
build_windows.bat
```

Результат: `releases\ollama-tray-chat-1.0.0-windows-x86_64.zip`

### Установка

1. Распакуйте архив
2. Запустите `ollama-tray-chat.exe`
3. (Опционально) Создайте ярлык в меню Пуск

### Примечания для Windows

- Убедитесь, что Ollama запущен и доступен на `http://127.0.0.1:11434`
- При первом запуске Windows Defender может запросить разрешение
- Для автозапуска создайте ярлык в папке `shell:startup`

---

## 🚀 GitHub Release

### Создание релиза

1. Соберите все версии
2. Создайте тег:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

3. Создайте релиз на GitHub:
   - Перейдите: https://github.com/demon-5656/ollama-tray-chat/releases/new
   - Выберите тег `v1.0.0`
   - Заголовок: `Ollama Tray Chat v1.0.0`
   - Загрузите файлы:
     - `ollama-tray-chat-1.0.0-linux-x86_64.tar.gz`
     - `ollama-tray-chat-1.0.0-amd64.deb`
     - `ollama-tray-chat-1.0.0-windows-x86_64.zip`

4. Опубликуйте релиз

---

## 📦 Структура релизов

```
releases/
├── ollama-tray-chat-1.0.0-linux-x86_64.tar.gz      # Универсальный Linux бинарник
├── ollama-tray-chat-1.0.0-amd64.deb                # Debian/Ubuntu пакет
├── ollama-tray-chat-1.0.0-1-x86_64.pkg.tar.zst     # Arch Linux пакет
└── ollama-tray-chat-1.0.0-windows-x86_64.zip       # Windows исполняемый файл
```

---

## 🛠 Troubleshooting

### PyInstaller не находит модули

```bash
pip install --upgrade PyQt6 requests
```

### Ошибка "hidden imports"

Добавьте в команду PyInstaller:
```bash
--hidden-import=PyQt6.QtCore
--hidden-import=PyQt6.QtGui
--hidden-import=PyQt6.QtWidgets
```

### Windows: "MSVCP140.dll not found"

Установите [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

---

## 📝 License

MIT License - см. [LICENSE](LICENSE)
