# ui/witgets/action_button.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QTimer


class ActionButton:
    """
    UI feedback wrapper for a QPushButton.
    Handles text changes, disabled states, and auto-reset.
    """
    def __init__(self, button: QPushButton, default_text: str | None = None):
        self.button = button
        self.default_text = default_text or button.text()

        self._reset_timer = QTimer()
        self._reset_timer.setSingleShot(True)
        self._reset_timer.timeout.connect(self.reset)

    # -----------------------------
    # State helpers
    # -----------------------------
    def set_enabled(self, enabled: bool):
        self.button.setEnabled(enabled)

    def show_busy(self, text="Working…"):
        self.button.setText(text)
        self.button.setEnabled(False)

    def show_success(self, text="Done", timeout=1200):
        self.button.setText(text)
        self.button.setEnabled(False)
        self._reset_timer.start(timeout)

    def show_cancelled(self, text="Canceled", timeout=1200):
        self.button.setText(text)
        self.button.setEnabled(False)
        self._reset_timer.start(timeout)

    def reset(self):
        self.button.setText(self.default_text)
        self.button.setEnabled(True)