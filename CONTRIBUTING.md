# 🔧 Руководство разработчика

## Разработка и модификация

### Структура кода

```python
ollama_tray_chat.py
├── Константы и настройки (строки 1-50)
├── Dataclasses (ChatMessage, ChatState)
├── ChatWorker (QThread для асинхронности)
├── MainWindow (основной UI)
│   ├── __init__() - инициализация UI
│   ├── load_state() / save_state() - работа с конфигом
│   ├── populate_models() - загрузка моделей
│   ├── on_send() - отправка сообщения
│   ├── on_chunk() - обработка streaming ответа
│   └── eventFilter() - обработка Enter/Shift+Enter
└── main() - точка входа
```

### Локальная разработка

```fish
# Клонируйте проект
cd /home/pc243/Программы/ollama-tray-chat

# Создайте виртуальное окружение (опционально)
python -m venv venv
source venv/bin/activate.fish

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python3 ollama_tray_chat.py
```

### Отладка

```python
# Включите детальное логирование
import logging
logging.basicConfig(level=logging.DEBUG)

# Или добавьте print() в нужных местах
def on_chunk(self, delta: str):
    print(f"DEBUG: Получен chunk: {delta}")
    # ...
```

### Тестирование

```fish
# Проверка зависимостей
python3 -c "import PyQt6, requests; print('OK')"

# Проверка подключения к Ollama
curl http://127.0.0.1:11434/api/tags

# Тест импорта модуля
python3 -c "from ollama_tray_chat import ChatState; print('OK')"
```

### Модификация UI

Основные стили задаются через `setStyleSheet()`:

```python
self.send_btn.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;  /* Зелёный */
        color: white;
        /* ... */
    }
""")
```

Для глобальных изменений темы модифицируйте стили в `__init__()`.

### Добавление новых функций

#### Пример: Добавление кнопки "Очистить историю"

1. **Добавьте кнопку в UI:**
```python
self.clear_btn = QtWidgets.QPushButton("🗑️ Очистить")
btn_bar.addWidget(self.clear_btn)
```

2. **Подключите сигнал:**
```python
self.clear_btn.clicked.connect(self.clear_history)
```

3. **Реализуйте метод:**
```python
def clear_history(self):
    reply = QtWidgets.QMessageBox.question(
        self, 'Подтверждение',
        'Очистить историю чата?',
        QtWidgets.QMessageBox.StandardButton.Yes |
        QtWidgets.QMessageBox.StandardButton.No
    )
    if reply == QtWidgets.QMessageBox.StandardButton.Yes:
        self.history.clear()
        self.state.messages.clear()
        self.statusBar().showMessage("🗑️ История очищена")
```

### Работа с Ollama API

#### Получение списка моделей
```python
response = requests.get(f"{OLLAMA_URL}/api/tags")
models = response.json()["models"]
```

#### Отправка запроса (без streaming)
```python
response = requests.post(
    f"{OLLAMA_URL}/api/chat",
    json={
        "model": "phi3.5:3.8b-mini-instruct",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": False
    }
)
answer = response.json()["message"]["content"]
```

#### Streaming запрос
```python
with requests.post(url, json=payload, stream=True) as r:
    for line in r.iter_lines(decode_unicode=True):
        if line:
            obj = json.loads(line)
            if not obj.get("done"):
                print(obj["message"]["content"], end='')
```

### Настройка конфигурации

Конфиг хранится в `~/.config/ollama-tray-chat/config.json`:

```json
{
  "model": "phi3.5:3.8b-mini-instruct",
  "system_prompt": "Ты — помощник..."
}
```

Для добавления новых параметров:

1. Модифицируйте `save_state()`:
```python
cfg = {
    "model": self.state.model,
    "system_prompt": self.sys_prompt.toPlainText(),
    "new_param": self.new_value  # Добавлено
}
```

2. Модифицируйте `load_state()`:
```python
st = ChatState(
    model=cfg.get("model", "phi3.5:3.8b-mini-instruct"),
    system_prompt=cfg.get("system_prompt", ""),
    new_param=cfg.get("new_param", default_value)  # Добавлено
)
```

### Работа с историей

История хранится в JSONL (JSON Lines) формате:

```jsonl
{"ts": 1729436400, "role": "user", "content": "Привет"}
{"ts": 1729436401, "role": "assistant", "content": "Здравствуйте!"}
{"ts": 1729436500, "role": "system", "content": "--- new chat ---"}
```

Чтение истории:
```python
with open(HISTORY_PATH, 'r') as f:
    for line in f:
        record = json.loads(line)
        print(f"{record['role']}: {record['content']}")
```

### Сборка и упаковка

#### Создание standalone исполняемого файла (PyInstaller)

```fish
# Установите PyInstaller
pip install pyinstaller

# Создайте исполняемый файл
pyinstaller --onefile \
    --windowed \
    --name ollama-tray-chat \
    --icon icons/ollama-chat.svg \
    --add-data "icons:icons" \
    ollama_tray_chat.py

# Результат в dist/ollama-tray-chat
```

#### Создание Arch пакета (PKGBUILD)

```bash
# Создайте PKGBUILD файл
pkgname=ollama-tray-chat
pkgver=1.0.0
pkgrel=1
pkgdesc="GUI client for Ollama with system tray support"
arch=('any')
depends=('python' 'python-pyqt6' 'python-requests' 'ollama')
# ...

# Соберите пакет
makepkg -si
```

### Отладка проблем

#### Приложение не запускается
```fish
# Проверьте Python версию
python3 --version  # Должно быть >= 3.10

# Проверьте импорты
python3 -c "from PyQt6 import QtWidgets; print('OK')"

# Запустите с трассировкой
python3 -v ollama_tray_chat.py 2>&1 | less
```

#### Не подключается к Ollama
```fish
# Проверьте сервис
systemctl --user status ollama

# Проверьте порт
ss -tlnp | grep 11434

# Проверьте API
curl http://127.0.0.1:11434/api/tags
```

#### Проблемы с иконкой
```fish
# Обновите кэш
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor

# Проверьте установку
ls -l ~/.local/share/icons/hicolor/scalable/apps/ollama-chat.svg
```

### Код-стайл

Проект следует PEP 8 с некоторыми исключениями:

```python
# Длина строки: 100 символов (не 79)
# Используйте type hints где возможно
def on_send(self) -> None:
    pass

# Docstrings для публичных методов
def populate_models(self):
    """Загружает список доступных моделей из Ollama."""
    pass

# Группировка импортов
import sys      # stdlib
import requests # third-party
from PyQt6 import QtWidgets  # third-party
```

### Линтинг и форматирование

```fish
# Установите инструменты
pip install black flake8 mypy

# Форматирование кода
black ollama_tray_chat.py

# Проверка стиля
flake8 ollama_tray_chat.py --max-line-length=100

# Проверка типов
mypy ollama_tray_chat.py
```

### Контрибьюция

1. Форкните проект
2. Создайте ветку фичи: `git checkout -b feature/amazing-feature`
3. Закоммитьте изменения: `git commit -m 'Add amazing feature'`
4. Запушьте в ветку: `git push origin feature/amazing-feature`
5. Откройте Pull Request

### Git workflow

```fish
# Создайте ветку для разработки
git checkout -b develop

# Работайте над фичей
git add .
git commit -m "feat: добавлена новая функция"

# Перед коммитом проверьте
python3 ollama_tray_chat.py  # Тест запуска
flake8 ollama_tray_chat.py   # Линтинг

# Слейте в main когда готово
git checkout main
git merge develop
```

### Версионирование

Следуем [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.x.x) - несовместимые изменения API
- **MINOR** (x.1.x) - новые функции, совместимые с предыдущими
- **PATCH** (x.x.1) - исправления багов

Обновляйте версию в:
- `ollama_tray_chat.py` (константа `APP_VERSION`)
- `CHANGELOG.md`

### Полезные ресурсы

- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [XDG Base Directory](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)

---

**Happy Coding! 🚀**
