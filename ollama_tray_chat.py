#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama Tray Chat — минималистичный GUI‑клиент под Arch/Linux для локального чата с моделями Ollama.
Особенности:
- Окно чата (история + ввод), отправка по Enter (Shift+Enter — новая строка)
- Стриминг ответа в реальном времени, кнопка Стоп
- Выбор модели (список из /api/tags), поле системного промпта
- Трей‑иконка (сворачивание в трей, контекстное меню: Показать/Скрыть, Новый чат, Выход)
- Автосохранение истории в ~/.local/share/ollama-tray-chat/history.jsonl
- Конфиг в ~/.config/ollama-tray-chat/config.json

Зависимости:
  pacman -S python python-pyqt6 python-requests

Запуск:
  python3 ollama_tray_chat.py  # по умолчанию
  python3 ollama_tray_chat.py --minimize  # старт сразу в трее

Совет: предварительно установи и запусти Ollama:
  yay -S ollama-bin && systemctl --user enable --now ollama
  ollama pull phi3.5:3.8b-mini-instruct
"""
from __future__ import annotations
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path

import requests
from PyQt6 import QtCore, QtGui, QtWidgets

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
APP_ID = "ollama-tray-chat"
APP_NAME = "Ollama Tray Chat"
APP_VERSION = "1.0.0"
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", APP_ID)
DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", APP_ID)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
HISTORY_PATH = os.path.join(DATA_DIR, "history.jsonl")

# Путь к иконке (относительно директории скрипта)
SCRIPT_DIR = Path(__file__).parent
ICON_PATH = SCRIPT_DIR / "icons" / "ollama-chat.svg"


def ensure_paths():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)


@dataclass
class ChatMessage:
    role: str  # "system" | "user" | "assistant"
    content: str


@dataclass
class ChatState:
    model: str = "phi3.5:3.8b-mini-instruct"
    system_prompt: str = (
        "Ты — локальный помощник по Linux (Arch) и fish. Отвечай кратко, давай команды безопасно."
    )
    messages: List[ChatMessage] = field(default_factory=list)


class ChatWorker(QtCore.QThread):
    chunk = QtCore.pyqtSignal(str)
    started_reply = QtCore.pyqtSignal()
    finished_ok = QtCore.pyqtSignal()
    failed = QtCore.pyqtSignal(str)

    def __init__(self, state: ChatState, user_prompt: str, parent=None):
        super().__init__(parent)
        self.state = state
        self.user_prompt = user_prompt
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def run(self):
        try:
            # Собираем историю в формат Ollama /api/chat
            msgs = []
            if self.state.system_prompt.strip():
                msgs.append({"role": "system", "content": self.state.system_prompt})
            for m in self.state.messages:
                msgs.append({"role": m.role, "content": m.content})
            msgs.append({"role": "user", "content": self.user_prompt})

            payload = {
                "model": self.state.model,
                "messages": msgs,
                "stream": True,
            }
            url = f"{OLLAMA_URL}/api/chat"
            self.started_reply.emit()
            with requests.post(url, json=payload, stream=True, timeout=60) as r:
                r.raise_for_status()
                full = []
                for line in r.iter_lines(decode_unicode=True):
                    if self._stop_flag:
                        break
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if obj.get("done"):
                        break
                    msg = obj.get("message", {})
                    delta = msg.get("content", "")
                    if delta:
                        full.append(delta)
                        self.chunk.emit(delta)
                # если не было принудительной остановки — добавим в историю целиком
                if not self._stop_flag:
                    answer = "".join(full)
                    self.state.messages.append(ChatMessage(role="user", content=self.user_prompt))
                    self.state.messages.append(ChatMessage(role="assistant", content=answer))
                    self.finished_ok.emit()
        except Exception as e:
            self.failed.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        
        # Загружаем иконку
        if ICON_PATH.exists():
            self.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))
        else:
            self.setWindowIcon(QtGui.QIcon.fromTheme("chat"))
        
        self.resize(820, 600)

        self.state = self.load_state()
        self.worker: Optional[ChatWorker] = None

        # Виджеты
        self.history = QtWidgets.QTextEdit(readOnly=True)
        self.history.setStyleSheet("""
            QTextEdit {
                background-color: #d8d8d8;
                border: 1px solid #999;
                border-radius: 4px;
                padding: 8px;
                color: #212121;
            }
        """)
        
        self.input = QtWidgets.QPlainTextEdit()
        self.input.setPlaceholderText("Введите сообщение… (Enter — отправить, Shift+Enter — новая строка)")
        self.input.setStyleSheet("""
            QPlainTextEdit {
                border: 1px solid #999;
                border-radius: 4px;
                padding: 8px;
                background-color: #e8e8e8;
                color: #212121;
                font-size: 11pt;
            }
        """)
        self.input.setMinimumHeight(80)
        self.input.setMaximumHeight(150)
        
        self.send_btn = QtWidgets.QPushButton("📤 Отправить")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        self.stop_btn = QtWidgets.QPushButton("⛔ Стоп")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.model_box = QtWidgets.QComboBox()
        self.model_box.setEditable(False)
        self.model_box.setStyleSheet("""
            QComboBox {
                border: 1px solid #999;
                border-radius: 4px;
                padding: 6px;
                background-color: #e8e8e8;
                color: #212121;
                font-size: 11pt;
            }
        """)
        
        self.refresh_models_btn = QtWidgets.QToolButton()
        self.refresh_models_btn.setIcon(QtGui.QIcon.fromTheme("view-refresh"))
        self.refresh_models_btn.setToolTip("Обновить список моделей из Ollama")
        self.refresh_models_btn.setStyleSheet("""
            QToolButton {
                border: 1px solid #999;
                border-radius: 4px;
                padding: 6px;
                background-color: #e8e8e8;
            }
            QToolButton:hover {
                background-color: #d0d0d0;
            }
        """)

        self.sys_prompt = QtWidgets.QPlainTextEdit()
        self.sys_prompt.setPlaceholderText("Системный промпт (опционально)")
        self.sys_prompt.setPlainText(self.state.system_prompt)
        self.sys_prompt.setFixedHeight(80)
        self.sys_prompt.setStyleSheet("""
            QPlainTextEdit {
                border: 1px solid #999;
                border-radius: 4px;
                padding: 8px;
                background-color: #e8e8e8;
                color: #212121;
                font-size: 11pt;
            }
        """)

        # Разметка
        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addWidget(QtWidgets.QLabel("🤖 Модель:"))
        top_bar.addWidget(self.model_box, 1)
        top_bar.addWidget(self.refresh_models_btn)

        btn_bar = QtWidgets.QHBoxLayout()
        btn_bar.addStretch(1)
        btn_bar.addWidget(self.stop_btn)
        btn_bar.addWidget(self.send_btn)

        central = QtWidgets.QWidget()
        v = QtWidgets.QVBoxLayout(central)
        v.setSpacing(8)
        v.setContentsMargins(12, 12, 12, 12)
        v.addLayout(top_bar)
        v.addWidget(QtWidgets.QLabel("⚙️ Системный промпт:"))
        v.addWidget(self.sys_prompt)
        v.addWidget(QtWidgets.QLabel("💬 История:"))
        v.addWidget(self.history, 1)
        # --- Предложенные команды от ассистента ---
        v.addWidget(QtWidgets.QLabel("🔧 Предложенные команды:"))
        # Контейнер для предложенных команд
        self.suggested_list = QtWidgets.QListWidget()
        self.suggested_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.suggested_list.setFixedHeight(120)
        v.addWidget(self.suggested_list)

        # Панель кнопок для предложенных команд
        sug_btn_bar = QtWidgets.QHBoxLayout()
        self.sug_preview_btn = QtWidgets.QPushButton("Просмотр")
        self.sug_accept_btn = QtWidgets.QPushButton("Одобрить")
        self.sug_reject_btn = QtWidgets.QPushButton("Отклонить")
        sug_btn_bar.addWidget(self.sug_preview_btn)
        sug_btn_bar.addWidget(self.sug_accept_btn)
        sug_btn_bar.addWidget(self.sug_reject_btn)
        v.addLayout(sug_btn_bar)
        v.addWidget(QtWidgets.QLabel("✏️ Сообщение:"))
        v.addWidget(self.input)
        v.addLayout(btn_bar)
        self.setCentralWidget(central)

        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu("📁 Файл")
        
        new_chat_action = file_menu.addAction("🆕 Новый чат")
        new_chat_action.setShortcut("Ctrl+N")
        new_chat_action.triggered.connect(self.new_chat)
        
        file_menu.addSeparator()
        
        quit_action = file_menu.addAction("🚪 Выход")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.on_quit)
        
        help_menu = menubar.addMenu("❓ Помощь")
        about_action = help_menu.addAction("ℹ️ О программе")
        about_action.triggered.connect(self.show_about)

        # Трей
        icon = QtGui.QIcon(str(ICON_PATH)) if ICON_PATH.exists() else QtGui.QIcon.fromTheme("chat")
        self.tray = QtWidgets.QSystemTrayIcon(icon, self)
        self.tray.setToolTip(APP_NAME)
        menu = QtWidgets.QMenu()
        self.action_show_hide = menu.addAction("👁️ Показать/Скрыть")
        self.action_new_chat = menu.addAction("🆕 Новый чат")
        menu.addSeparator()
        self.action_quit = menu.addAction("🚪 Выход")
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

        # Сигналы
        self.send_btn.clicked.connect(self.on_send)
        self.stop_btn.clicked.connect(self.on_stop)
        self.refresh_models_btn.clicked.connect(self.populate_models)
        # suggested commands
        self.sug_preview_btn.clicked.connect(self.on_suggest_preview)
        self.sug_accept_btn.clicked.connect(self.on_suggest_accept)
        self.sug_reject_btn.clicked.connect(self.on_suggest_reject)
        self.action_quit.triggered.connect(self.on_quit)
        self.action_show_hide.triggered.connect(self.toggle_visible)
        self.action_new_chat.triggered.connect(self.new_chat)
        self.input.installEventFilter(self)

        # Данные
        self.populate_models()
        self.restore_history_to_view()
        
        # Статус бар
        self.statusBar().showMessage("✅ Готов к работе")

    # ====== Служебные ======
    def load_state(self) -> ChatState:
        ensure_paths()
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                st = ChatState(
                    model=cfg.get("model", "phi3.5:3.8b-mini-instruct"),
                    system_prompt=cfg.get("system_prompt", ""),
                    messages=[],
                )
                return st
            except Exception:
                pass
        return ChatState()

    def save_state(self):
        ensure_paths()
        cfg = {
            "model": self.state.model,
            "system_prompt": self.sys_prompt.toPlainText(),
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

    def append_history_log(self, role: str, content: str):
        ensure_paths()
        rec = {"ts": int(time.time()), "role": role, "content": content}
        with open(HISTORY_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def restore_history_to_view(self):
        self.history.clear()
        for m in self.state.messages:
            self._append_bubble(m.role, m.content)

    # ====== UI helpers ======
    def _append_bubble(self, role: str, text: str):
        role_tag = {
            "user": ("👤 Вы", "#e3f2fd", "#1565c0"),      # Голубой фон, синий текст
            "assistant": ("🤖 Модель", "#f1f8e9", "#33691e"),  # Светло-зелёный фон, тёмно-зелёный текст
            "system": ("⚙️ System", "#fff9c4", "#f57f17"),     # Жёлтый фон, оранжевый текст
        }.get(role, (role, "#fff", "#000"))
        who, bg, text_color = role_tag
        cursor = self.history.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        fmt = QtGui.QTextBlockFormat()
        fmt.setLeftMargin(8)
        fmt.setRightMargin(8)
        fmt.setTopMargin(4)
        fmt.setBottomMargin(4)
        cursor.insertBlock(fmt)

        # Заголовок (имя роли)
        boxfmt = QtGui.QTextCharFormat()
        boxfmt.setBackground(QtGui.QColor(bg))
        boxfmt.setForeground(QtGui.QColor(text_color))
        boxfmt.setFontWeight(QtGui.QFont.Weight.Bold)
        cursor.insertText(f"{who}:\n", boxfmt)

        # Текст сообщения
        bodyfmt = QtGui.QTextCharFormat()
        bodyfmt.setFontWeight(QtGui.QFont.Weight.Normal)
        bodyfmt.setBackground(QtGui.QColor(bg))
        bodyfmt.setForeground(QtGui.QColor("#212121"))  # Тёмно-серый текст для читаемости
        cursor.insertText(text + "\n\n", bodyfmt)
        self.history.ensureCursorVisible()

    # ====== Модели ======
    def populate_models(self):
        self.model_box.clear()
        self.statusBar().showMessage("🔄 Загрузка моделей...")
        try:
            r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            r.raise_for_status()
            data = r.json()
            models = [m.get("name") for m in data.get("models", []) if m.get("name")]
            if not models:
                raise RuntimeError("models empty")
            for name in models:
                self.model_box.addItem(name)
            # выбрать сохранённую
            idx = self.model_box.findText(self.state.model)
            if idx >= 0:
                self.model_box.setCurrentIndex(idx)
            else:
                self.model_box.setCurrentIndex(0)
                self.state.model = self.model_box.currentText()
            self.statusBar().showMessage(f"✅ Загружено моделей: {len(models)}")
        except Exception as e:
            # Фоллбек: оставить текущую модель
            self.model_box.addItem(self.state.model)
            self.statusBar().showMessage(f"⚠️ Ошибка загрузки моделей: {e}")

    # ====== Отправка ======
    def on_send(self):
        if self.worker and self.worker.isRunning():
            return
        prompt = self.input.toPlainText().strip()
        if not prompt:
            return
        self.state.model = self.model_box.currentText()
        self.state.system_prompt = self.sys_prompt.toPlainText()
        self.save_state()

        # UI
        self._append_bubble("user", prompt)
        self.append_history_log("user", prompt)
        self.input.clear()

        # Плейсхолдер для потока
        self._append_bubble("assistant", "⏳ Думаю...")

        # Запуск воркера
        self.worker = ChatWorker(self.state, prompt, self)
        self.worker.chunk.connect(self.on_chunk)
        self.worker.started_reply.connect(self.on_started_reply)
        self.worker.finished_ok.connect(self.on_finished_ok)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()
        
        self.statusBar().showMessage("💭 Отправляю запрос...")

    def on_chunk(self, delta: str):
        # добавляем текст к последнему блоку ассистента
        cursor = self.history.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.PreviousBlock)
        # переходим на последний блок ("⏳ Думаю...") и заменяем, добавляя дельту
        self.history.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.history.insertPlainText(delta)
        self.history.ensureCursorVisible()

    def on_started_reply(self):
        self.send_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.statusBar().showMessage("🔄 Получаю ответ...")

    def on_finished_ok(self):
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.statusBar().showMessage("✅ Готов к работе")
        # Сохраним последнюю реплику ассистента в лог (из state)
        if self.state.messages and self.state.messages[-1].role == "assistant":
            self.append_history_log("assistant", self.state.messages[-1].content)
            # После получения ответа попробуем извлечь команды и показать их
            commands = self.parse_commands(self.state.messages[-1].content)
            self.suggested_list.clear()
            for cmd in commands:
                item = QtWidgets.QListWidgetItem(cmd)
                self.suggested_list.addItem(item)

    def on_failed(self, err: str):
        self.send_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.statusBar().showMessage(f"❌ Ошибка: {err}")
        QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось получить ответ от Ollama:\n{err}")

    def on_stop(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.statusBar().showMessage("⏹️ Остановлено")

    # ====== Трей/окно ======
    def closeEvent(self, e: QtGui.QCloseEvent):
        # сворачиваем в трей вместо выхода
        e.ignore()
        self.hide()
        self.tray.showMessage(
            APP_NAME, 
            "Приложение свернуто в трей", 
            QtWidgets.QSystemTrayIcon.MessageIcon.Information, 
            2000
        )

    def toggle_visible(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def new_chat(self):
        self.state.messages.clear()
        self.history.clear()
        self.append_history_log("system", "--- new chat ---")
        self.statusBar().showMessage("🆕 Начат новый чат")

    def on_tray_activated(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason):
        if reason in (QtWidgets.QSystemTrayIcon.ActivationReason.Trigger, 
                      QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick):
            self.toggle_visible()

    def on_quit(self):
        QtWidgets.QApplication.quit()

    def show_about(self):
        QtWidgets.QMessageBox.about(
            self,
            f"О программе {APP_NAME}",
            f"""<h3>{APP_NAME}</h3>
            <p>Версия: {APP_VERSION}</p>
            <p>Минималистичный GUI-клиент для Ollama</p>
            <p><b>Возможности:</b></p>
            <ul>
                <li>Стриминг ответов в реальном времени</li>
                <li>Системный трей</li>
                <li>Автосохранение истории</li>
                <li>Настраиваемый системный промпт</li>
            </ul>
            <p><b>Разработано для Arch Linux + KDE</b></p>
            <p>© 2025</p>
            """
        )

    # ====== Парсинг команд из текста ассистента ======
    def parse_commands(self, text: str) -> list:
        """
        Извлекает потенциальные shell-команды из ответа ассистента.
        Правила простые и эмпирические:
        - Блоки ```bash``` или ```sh```
        - Строки, начинающиеся с `$ ` или `sudo `
        - Однострочные команды (без пояснений) — как fallback
        Возвращает список строк (команд).
        """
        cmds = []
        if not text:
            return cmds

        # 1) блоки ```bash``` ```sh```
        import re

        code_blocks = re.findall(r"```(?:bash|sh)?\n(.*?)```", text, flags=re.S | re.I)
        for block in code_blocks:
            for line in block.splitlines():
                line = line.strip()
                if not line:
                    continue
                # игнорируем комментарии
                if line.startswith("#"):
                    continue
                cmds.append(line)

        # 2) строки, начинающиеся с $ или sudo
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("$"):
                candidate = s.lstrip("$ ")
                if candidate:
                    cmds.append(candidate)
            elif s.startswith("sudo "):
                cmds.append(s)

        # 3) fallback: если ничего не найдено, попробуем найти короткие однострочные команды
        if not cmds:
            for line in text.splitlines():
                s = line.strip()
                if not s:
                    continue
                # простая эвристика: строка без пробелов или с одним аргументом
                parts = s.split()
                if 1 <= len(parts) <= 3 and re.match(r"^[a-z0-9_\-./]+$", parts[0], flags=re.I):
                    cmds.append(s)

        # убираем дубликаты, сохраняем порядок
        seen = set()
        out = []
        for c in cmds:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return out

    # ====== Обработчики команд ======
    def on_suggest_preview(self):
        item = self.suggested_list.currentItem()
        if not item:
            QtWidgets.QMessageBox.information(self, "Просмотр", "Выберите команду в списке")
            return
        cmd = item.text()
        QtWidgets.QMessageBox.information(self, "Просмотр команды", f"Команда:\n{cmd}")

    def on_suggest_reject(self):
        item = self.suggested_list.currentItem()
        if not item:
            return
        self.suggested_list.takeItem(self.suggested_list.currentRow())

    def on_suggest_accept(self):
        item = self.suggested_list.currentItem()
        if not item:
            QtWidgets.QMessageBox.information(self, "Одобрение", "Выберите команду для одобрения")
            return
        cmd = item.text()
        # показать подтверждение
        resp = QtWidgets.QMessageBox.question(
            self,
            "Подтвердите выполнение",
            f"Выполнить команду в терминале?\n\n{cmd}",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )
        if resp == QtWidgets.QMessageBox.StandardButton.Yes:
            # Проверим разрешение команды (allowlist)
            allowed = self.is_command_allowed(cmd)
            if not allowed:
                QtWidgets.QMessageBox.critical(self, "Запрещено", "Эта команда не разрешена к автоматическому выполнению")
                return

            # Создадим диалог для вывода логов выполнения
            dlg = QtWidgets.QDialog(self)
            dlg.setWindowTitle(f"Выполнение: {cmd}")
            dlg.resize(700, 400)
            lay = QtWidgets.QVBoxLayout(dlg)
            out_view = QtWidgets.QTextEdit(readOnly=True)
            out_view.setStyleSheet("background:#111; color:#cfc; font-family: monospace;")
            lay.addWidget(out_view)
            btns = QtWidgets.QHBoxLayout()
            stop_btn = QtWidgets.QPushButton("Остановить")
            close_btn = QtWidgets.QPushButton("Закрыть")
            close_btn.setEnabled(False)
            btns.addWidget(stop_btn)
            btns.addStretch(1)
            btns.addWidget(close_btn)
            lay.addLayout(btns)

            # запустим CommandRunner
            runner = CommandRunner(cmd, parent=self)

            def on_stdout(line):
                out_view.append(f"[out] {line}")

            def on_stderr(line):
                out_view.append(f"[err] {line}")

            def on_failed(err):
                out_view.append(f"[failed] {err}")
                close_btn.setEnabled(True)

            def on_finished(rc):
                out_view.append(f"[finished] returncode={rc}")
                close_btn.setEnabled(True)

            runner.line_stdout.connect(on_stdout)
            runner.line_stderr.connect(on_stderr)
            runner.failed.connect(on_failed)
            runner.finished.connect(on_finished)

            def on_stop_clicked():
                runner.stop()
                stop_btn.setEnabled(False)

            def on_close_clicked():
                dlg.accept()

            stop_btn.clicked.connect(on_stop_clicked)
            close_btn.clicked.connect(on_close_clicked)

            runner.start()
            dlg.exec()

            # логируем в историю и удаляем из списка
            self.append_history_log("system", f"Выполнена команда: {cmd}")
            self.suggested_list.takeItem(self.suggested_list.currentRow())

    def is_command_allowed(self, cmd: str) -> bool:
        """Простая проверка разрешённых команд.
        Разрешаем только команды из белого списка или начинающиеся с безопасных утилит.
        Запрещаем явные опасные паттерны.
        """
        import re

        deny_patterns = [r"rm\s+-rf", r":\s*\\" , r">\s*/dev/null 2>&1 &", r"forkbomb", r":(){"]
        for p in deny_patterns:
            if re.search(p, cmd, flags=re.I):
                return False

        # allowlist (проверяем первые токены)
        allowed_bins = {
            "ls", "cat", "echo", "grep", "sed", "awk", "head", "tail",
            "systemctl", "journalctl", "docker", "git", "curl", "wget",
            "ping", "whoami", "id", "ps", "df", "du", "uptime", "free",
            "pacman", "apt", "snap", "uname",
        }
        parts = cmd.strip().split()
        if not parts:
            return False
        bin0 = parts[0]
        # если команда содержит путь — разрешать только если bin в allowlist
        base = bin0.split('/')[-1]
        if base in allowed_bins:
            return True
        # дополнительная проверка для простых выражений: echo "..."
        if base in ("echo",):
            return True
        # иначе запрет
        return False


class CommandRunner(QtCore.QThread):
    """Выполняет одну команду в отдельном потоке, стримит stdout/stderr.
    Сигналы:
      line_stdout(str), line_stderr(str), finished(int returncode), failed(str error)
    """
    line_stdout = QtCore.pyqtSignal(str)
    line_stderr = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(int)
    failed = QtCore.pyqtSignal(str)

    def __init__(self, command: str, parent=None):
        super().__init__(parent)
        self.command = command
        self._proc = None

    def run(self):
        import shlex
        import subprocess

        try:
            # Используем shell=False для безопасности
            args = shlex.split(self.command)
            self._proc = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            # читаем stdout и stderr по строкам
            assert self._proc.stdout is not None
            assert self._proc.stderr is not None
            from threading import Thread

            def read_stream(stream, emitter):
                for ln in iter(stream.readline, ""):
                    emitter.emit(ln.rstrip('\n'))
                stream.close()

            t1 = Thread(target=read_stream, args=(self._proc.stdout, self.line_stdout))
            t2 = Thread(target=read_stream, args=(self._proc.stderr, self.line_stderr))
            t1.start()
            t2.start()
            t1.join()
            t2.join()

            rc = self._proc.wait()
            self.finished.emit(rc)
        except Exception as e:
            self.failed.emit(str(e))

    def stop(self):
        if self._proc and self._proc.poll() is None:
            try:
                self._proc.terminate()
            except Exception:
                pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description=f"{APP_NAME} v{APP_VERSION}")
    parser.add_argument("--minimize", action="store_true", help="Старт свернутым в трей")
    parser.add_argument("--version", action="version", version=f"{APP_NAME} {APP_VERSION}")
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("OllamaChat")
    app.setApplicationVersion(APP_VERSION)
    
    # тема иконок
    QtGui.QIcon.setThemeSearchPaths(QtGui.QIcon.themeSearchPaths() + ["/usr/share/icons", "/usr/local/share/icons"])
    if not QtGui.QIcon.themeName():
        QtGui.QIcon.setThemeName("breeze")

    w = MainWindow()
    if args.minimize:
        w.hide()
    else:
        w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    ensure_paths()
    main()
