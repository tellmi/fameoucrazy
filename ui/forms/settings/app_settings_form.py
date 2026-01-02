# ui/forms/settings/app_settings_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class AppSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager, widgets=None):
        super().__init__(ui, settings_manager, theme_manager, widgets=widgets)

        # --- App Language combo field ---
        lang_key = "app_settings.app_language"
        self.register_field(
            key=lang_key,
            widget=self.widgets["app_settings_language_combo"],
            **combo_field()
        )

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)