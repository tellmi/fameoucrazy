# ui/forms/settings/advisor_settings_form.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QComboBox, QLineEdit, QDateEdit
import logging
from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *
from ui.utils import get_all_child_widgets  # ✅ import your helper

class AdvisorSettingsForm(InputForm):
    def __init__(self, ui: QWidget, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        # --- Find widgets in this subtab ---
        self._widgets = {
            "salutation": ui.findChild(QComboBox, "advisor_salutation_combo"),
            "given_name": ui.findChild(QLineEdit, "advisor_given_name_edit"),
            "middle_name": ui.findChild(QLineEdit, "advisor_middle_name_edit"),
            "surname": ui.findChild(QLineEdit, "advisor_surname_edit"),
            "birth_date": ui.findChild(QDateEdit, "advisor_birth_date_edit"),
        }

        # --- Check that all widgets exist ---
        missing = [k for k, w in self._widgets.items() if w is None]
        if missing:
            all_children = list(get_all_child_widgets(ui).keys())
            raise RuntimeError(
                f"AdvisorSettingsForm widgets not found: {missing}\n"
                f"Available widgets in subtab: {all_children}"
            )

        # --- Register fields with adapters ---
        self.register_field("advisor.salutation", widget=self._widgets["salutation"], **combo_field())
        self.register_field("advisor.given_name", widget=self._widgets["given_name"], **text_field())
        self.register_field("advisor.middle_name", widget=self._widgets["middle_name"], **text_field())
        self.register_field("advisor.surname", widget=self._widgets["surname"], **text_field())
        self.register_field("advisor.birth_date", widget=self._widgets["birth_date"], **date_field())

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            logging.debug(f"[LOAD] {key} = {value}")
            field["setter"](field["widget"], value)
