# ui/witgets/action_button_manager.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QPushButton
import logging


class ActionButtonManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self._save_handlers = {}
        self._cancel_handlers = {}
        self._buttons = {}

    def register_button(self, key: str, button: QPushButton, save_handler=None, cancel_handler=None):
        """
        Registriert einen Button und verbindet das Klick-Signal.
        """
        if button is None:
            logging.warning(f"Button für Key '{key}' ist None!")
            return

        self._buttons[key] = button

        # Klick-Signal verbinden, Button wird übergeben
        button.clicked.connect(lambda _, k=key, btn=button: self._on_button_clicked(k, btn))

        # Optional Handler speichern
        if save_handler:
            self._save_handlers[key] = save_handler
        if cancel_handler:
            self._cancel_handlers[key] = cancel_handler

    def _on_button_clicked(self, key: str, button: QPushButton):
        """
        Wird ausgeführt, wenn ein registrierter Button geklickt wird.
        Button wird explizit übergeben, kein self.sender() nötig.
        """
        if button is None:
            logging.warning(f"Kein Button übergeben für Key '{key}'")
            return

        text = button.text() or ""
        text_lower = text.lower()

        # Save-Handler ausführen
        if text_lower.startswith("save") and key in self._save_handlers:
            handler = self._save_handlers[key]
            if callable(handler):
                handler()

        # Cancel-Handler ausführen
        elif text_lower.startswith("cancel") and key in self._cancel_handlers:
            handler = self._cancel_handlers[key]
            if callable(handler):
                handler()

        # Optional: Buttons updaten
        self.update_buttons_state()

        logging.info(f"Button '{text}' mit Key '{key}' geklickt")

    def update_buttons_state(self):
        """
        Setzt Buttons auf enabled nur, wenn Settings geändert wurden (Dirty-State).
        """
        main_window = self.main_window
        dirty = main_window.settings != getattr(main_window, "_initial_settings", {})

        for key, button in self._buttons.items():
            button.setEnabled(dirty)