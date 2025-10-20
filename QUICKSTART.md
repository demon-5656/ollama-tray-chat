# 🚀 Быстрый старт

## Установка (уже сделана!)

✅ Приложение установлено и готово к работе!

## 📍 Где найти приложение

### В меню KDE:
1. Откройте меню приложений (кнопка K или Alt+F1)
2. Найдите **"Ollama Tray Chat"** в разделе **Интернет** или через поиск
3. Запустите приложение

### Из терминала:
```fish
# Обычный запуск
./run.fish

# Или напрямую
python3 ollama_tray_chat.py

# Свёрнутым в трей
python3 ollama_tray_chat.py --minimize
```

## ⚠️ Важно: Установка Ollama

Приложение работает с **локальным сервером Ollama**. Если он ещё не установлен:

```fish
# 1. Установка Ollama
yay -S ollama-bin

# 2. Запуск сервиса
systemctl --user enable --now ollama

# 3. Скачивание модели (на выбор)
ollama pull phi3.5:3.8b-mini-instruct  # Быстрая малая модель (2.3GB)
ollama pull llama2                      # Классическая модель (3.8GB)
ollama pull mistral                     # Мощная модель (4.1GB)

# 4. Проверка
ollama list
```

## 🎯 Первый запуск

1. Запустите приложение из меню KDE
2. Выберите модель из списка
3. Напишите сообщение и нажмите Enter
4. Готово! 🎉

## 💡 Полезные команды

```fish
# Показать установленные модели
ollama list

# Удалить модель
ollama rm model-name

# Проверить статус Ollama
systemctl --user status ollama

# Перезапустить Ollama
systemctl --user restart ollama

# Посмотреть логи Ollama
journalctl --user -u ollama -f
```

## 🎨 Иконка в трее

После запуска приложение появится в системном трее KDE:
- **Клик** - показать/скрыть окно
- **ПКМ** - контекстное меню (Новый чат, Выход)
- **Закрытие окна** - сворачивание в трей (не выход!)

## 🆘 Проблемы?

### Приложение не находит модели
```fish
# Проверьте что Ollama запущен
systemctl --user status ollama

# Если не запущен:
systemctl --user start ollama

# Скачайте хотя бы одну модель
ollama pull phi3.5:3.8b-mini-instruct
```

### Приложение не видно в меню
```fish
# Обновите базу приложений
update-desktop-database ~/.local/share/applications
kbuildsycoca6  # Для KDE6
```

### Python ошибки
```fish
# Проверьте зависимости
python3 -c "import PyQt6, requests; print('OK')"

# Если ошибка:
sudo pacman -S python-pyqt6 python-requests
```

## 📚 Полная документация

Смотрите [README.md](README.md) для подробной информации.

---

**Наслаждайтесь локальным AI! 🤖**
