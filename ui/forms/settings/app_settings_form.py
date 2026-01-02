# ui/forms/settings/app_settings_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class AppSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager, widgets=None):
        super().__init__(ui, settings_manager, theme_manager, widgets=widgets)
        self._theme_radios = {}

        # Register theme radio buttons if they exist
        for key in ["system", "light", "dark", "green", "orange", "custom"]:
            rb_name = f"app_settings_color_theme_radio_{key}"
            rb = self.widgets.get(rb_name)
            if rb:
                self._theme_radios[key] = rb

        if self._theme_radios:
            self.register_field(
                key="app_settings.app_theme",
                widget=None,
                **radio_field(self._theme_radios),
                on_change=self._preview_theme,
            )
            for rb in self._theme_radios.values():
                rb.toggled.connect(lambda checked, key="app_settings.app_theme":
                                   self._handle_change(key) if checked else None)

        # Register language combo if exists
        combo = self.widgets.get("app_settings_language_combo")
        if combo:
            self.register_field(
                key="app_settings.app_language",
                widget=combo,
                **combo_field()
            )

    def _preview_theme(self, theme_name):
        if self.theme_manager:
            self.theme_manager.apply_theme(theme_name)

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)
