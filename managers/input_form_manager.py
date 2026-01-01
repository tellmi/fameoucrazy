# ui/managers/input_form_manager.py
# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal
from ui.utils import get_all_child_widgets

class InputFormManager(QObject):
    """
    Base class for all forms, handles field registration and widget collection.
    """
    changed = Signal()

    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__()
        self.ui = ui
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        # Collect all widgets recursively for this form
        self.widgets = get_all_child_widgets(self.ui)

    def _connect_widget(self, widget, key):
        for signal_name in ("toggled", "textChanged", "currentIndexChanged"):
            if hasattr(widget, signal_name):
                getattr(widget, signal_name).connect(
                    lambda *_,
                    k=key: self._handle_change(k)
                )
                break

    def _handle_change(self, key):
        field = self._fields[key]
        value = field["getter"](field["widget"])
        if field["on_change"]:
            field["on_change"](value)
        self.changed.emit()

    def load(self):
        """Load form fields from settings"""
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)

    def save(self):
        """Save form fields into settings"""
        for key, field in self._fields.items():
            value = field["getter"](field["widget"])
            self.settings_manager.set(key, value)

    def reset(self):
        """Reset form fields from settings"""
        self.load()
