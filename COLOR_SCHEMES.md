# 🎨 Цветовые схемы для Ollama Tray Chat

## Текущая схема (Серая, высококонтрастная) ⭐ РЕКОМЕНДУЕТСЯ

```python
# В методе _append_bubble():
role_tag = {
    "user": ("👤 Вы", "#e3f2fd", "#1565c0"),           # Голубой фон, синий текст
    "assistant": ("🤖 Модель", "#f1f8e9", "#33691e"),  # Зелёный фон, тёмно-зелёный текст
    "system": ("⚙️ System", "#fff9c4", "#f57f17"),     # Жёлтый фон, оранжевый текст
}

# Текст сообщений:
bodyfmt.setForeground(QtGui.QColor("#212121"))  # Тёмно-серый

# Фон истории чата:
background-color: #d8d8d8;  # Светло-серый
border: 1px solid #999;

# Поля ввода (системный промпт, сообщение, выбор модели):
background-color: #e8e8e8;  # Серый
color: #212121;  # Тёмный текст
font-size: 11pt;
border: 1px solid #999;
```

---

## Альтернативные схемы

### 1. Тёмная схема (Dark Theme)

```python
# _append_bubble():
role_tag = {
    "user": ("👤 Вы", "#1e3a5f", "#90caf9"),           # Тёмно-синий фон, светло-синий текст
    "assistant": ("🤖 Модель", "#1b5e20", "#81c784"),  # Тёмно-зелёный фон, светло-зелёный текст
    "system": ("⚙️ System", "#4a3f00", "#ffd54f"),     # Тёмно-жёлтый фон, светло-жёлтый текст
}

bodyfmt.setForeground(QtGui.QColor("#e0e0e0"))  # Светло-серый текст

# История чата:
background-color: #2b2b2b;  # Тёмно-серый
color: #e0e0e0;
```

### 2. Пастельная схема (Soft Pastels)

```python
role_tag = {
    "user": ("👤 Вы", "#e1f5fe", "#01579b"),           # Очень светло-голубой, тёмно-синий
    "assistant": ("🤖 Модель", "#f1f8e9", "#1b5e20"),  # Светло-зелёный, тёмно-зелёный
    "system": ("⚙️ System", "#fff3e0", "#e65100"),     # Персиковый, оранжевый
}

bodyfmt.setForeground(QtGui.QColor("#263238"))  # Очень тёмно-серый

background-color: #fafafa;
```

### 3. Высокий контраст (High Contrast)

```python
role_tag = {
    "user": ("👤 Вы", "#bbdefb", "#0d47a1"),           # Голубой, очень тёмно-синий
    "assistant": ("🤖 Модель", "#c8e6c9", "#1b5e20"),  # Светло-зелёный, очень тёмно-зелёный
    "system": ("⚙️ System", "#fff59d", "#f57c00"),     # Жёлтый, оранжевый
}

bodyfmt.setForeground(QtGui.QColor("#000000"))  # Чёрный

background-color: #ffffff;  # Белый
```

### 4. Приглушённые тона (Muted)

```python
role_tag = {
    "user": ("👤 Вы", "#cfd8dc", "#37474f"),           # Серо-голубой
    "assistant": ("🤖 Модель", "#dcedc8", "#558b2f"),  # Приглушённо-зелёный
    "system": ("⚙️ System", "#ffe0b2", "#ef6c00"),     # Приглушённо-оранжевый
}

bodyfmt.setForeground(QtGui.QColor("#424242"))  # Тёмно-серый

background-color: #eceff1;  # Светло-серый
```

### 5. Монохромная (Grayscale)

```python
role_tag = {
    "user": ("👤 Вы", "#e0e0e0", "#424242"),
    "assistant": ("🤖 Модель", "#f5f5f5", "#616161"),
    "system": ("⚙️ System", "#eeeeee", "#757575"),
}

bodyfmt.setForeground(QtGui.QColor("#212121"))

background-color: #fafafa;
```

### 6. Сепия (Sepia - тёплые тона)

```python
role_tag = {
    "user": ("👤 Вы", "#fff3e0", "#bf360c"),
    "assistant": ("🤖 Модель", "#f1f8e9", "#33691e"),
    "system": ("⚙️ System", "#fffde7", "#f57f17"),
}

bodyfmt.setForeground(QtGui.QColor("#3e2723"))  # Коричневый

background-color: #faf8f3;  # Бежевый
```

---

## Как применить схему

1. Откройте файл `ollama_tray_chat.py`
2. Найдите метод `_append_bubble()` (примерно строка 375)
3. Замените словарь `role_tag` на выбранную схему
4. Найдите строку с `bodyfmt.setForeground()` и измените цвет текста
5. Найдите `self.history.setStyleSheet()` (примерно строка 152) и измените `background-color`
6. Сохраните и перезапустите приложение

---

## Генератор цветовых схем

Используйте онлайн инструменты для подбора цветов:
- **Material Design Colors**: https://material.io/design/color/
- **Coolors**: https://coolors.co/
- **Adobe Color**: https://color.adobe.com/

---

## Советы по выбору цветов

✅ **Контрастность**: Разница между фоном и текстом должна быть > 4.5:1  
✅ **Читаемость**: Тёмный текст на светлом фоне или наоборот  
✅ **Согласованность**: Используйте цвета из одной палитры  
✅ **Доступность**: Избегайте только красного/зелёного (дальтонизм)  

❌ **Не используйте**: Белый текст на белом, низкий контраст, кислотные цвета

---

## Проверка контрастности

```fish
# Установите инструмент проверки контраста
pip install colorspacious

# Проверьте соотношение
python3 -c "
from colorspacious import deltaE
# Пример: синий текст #1565c0 на голубом фоне #e3f2fd
# Коэффициент контраста должен быть > 4.5
"
```

Или используйте онлайн: https://contrast-ratio.com/

---

**Текущая схема оптимизирована для максимальной читаемости! 📖**
