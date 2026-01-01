# ui/forms/input_form.py
# -*- coding: utf-8 -*-


from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, QObject

class InputForm(QObject):
    changed = Signal()

    def __init__(self, ui=None, settings_manager=None, theme_manager=None, widgets=None):
        super().__init__()
        self.ui = ui
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        # Prefer explicitly passed widgets dict, else fall back to ui.widgets
        if widgets is not None:
            self.widgets = widgets
        elif ui and hasattr(ui, "widgets"):
            self.widgets = ui.widgets
        else:
            self.widgets = {}

        self._fields = {}
        self._initial_snapshot = {}

        # Initialize all fields with optional init function
        for key, field in self._fields.items():
            if "init" in field:
                field["init"](field["widget"])

    def register_field(self, key, widget=None, getter=None, setter=None, on_change=None, **kwargs):
        """Register a form field with getter/setter and optional change callback"""
        self._fields[key] = {
            "widget": widget,
            "getter": getter or (lambda w: w.text().strip()),
            "setter": setter or (lambda w, v: w.setText(str(v) if v is not None else "")),
            "on_change": on_change
        }
        # Merge extra kwargs (like init)
        self._fields[key].update(kwargs)

        if isinstance(widget, (list, tuple)):
            for w in widget:
                self._connect_widget(w, key)
        else:
            self._connect_widget(widget, key)

    def _handle_change(self, key):
        field = self._fields[key]
        value = field["getter"](field["widget"])
        if field["on_change"]:
            field["on_change"](value)
        self.changed.emit()

    # auto-connect signals if possible
    def _connect_widget(self, widget, key):
        for signal_name in ("toggled", "textChanged", "currentIndexChanged"):
            if hasattr(widget, signal_name):
                getattr(widget, signal_name).connect(
                    lambda *_,
                           k=key: self._handle_change(k)
                )
                break

    # ---------- lifecycle ----------
    def load(self):
        raise NotImplementedError

    def save(self):
        """
        Persist all registered fields into the settings manager.
        """
        for key, field in self._fields.items():
            value = field["getter"](field["widget"])
            self.settings_manager.set(key, value)

        self._dirty = False

    def reset(self):
        for form in self.forms:
            form.reset()

        # restore last saved theme snapshot
        self.theme_manager.apply_theme(
            self.settings_manager.get("theme")
        )

    def is_dirty(self) -> bool:
        return False
