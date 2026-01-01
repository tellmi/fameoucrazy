# ui/managers/action_button_manager.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QPushButton
import logging

from ui.widgets.action_button import ActionButton


class ActionButtonManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self._buttons: dict[str, ActionButton] = {}
        self._handlers: dict[str, callable] = {}
        self._roles: dict[str, str] = {}  # key -> role ("save"/"cancel")

    def register_button(
        self,
        *,
        key: str,
        button,
        role: str,
        handler: callable,
    ):
        """
        registering a button and connect a click signal
        """
        if button is None:
            logging.warning(f"[ActionButtonManager] Button '{key}' is None")
            return

        action_button = ActionButton(button, default_text=button.text())
        self._buttons[key] = action_button
        self._handlers[key] = handler
        self._roles[key] = role

        button.clicked.connect(lambda _, k=key: self._on_clicked(k))

    def _on_clicked(self, key: str):
        action_button = self._buttons.get(key)
        handler = self._handlers.get(key)
        role = self._roles.get(key)

        if not action_button or not handler:
            return

        logging.info(f"[ActionButton] {role.upper()} clicked ({key})")

        if role == "save":
            action_button.show_busy("Saving…")
            handler()
            action_button.show_success("Saved")

        elif role == "cancel":
            handler()
            action_button.show_cancelled("Canceled")

        self.update_buttons_state()

        logging.info(f"Button '{action_button.button.text()}' clicked with Key '{key}'")

    def update_buttons_state(self):
        """
        setting buttons to enabled only if settings were changed (Dirty-State).
        """
        dirty = hasattr(self.main_window, "is_dirty") and self.main_window.is_dirty()

        for btn in self._buttons.values():
            btn.set_enabled(dirty)

