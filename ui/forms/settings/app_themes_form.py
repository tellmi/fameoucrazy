# ui/app_themes_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class AppThemesForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager, widgets=None):
        super().__init__(ui, settings_manager, theme_manager, widgets=widgets)

        theme_key = "app_settings.app_theme"
        lang_key = "app_settings.app_language"

        # Register theme radio buttons
        self._theme_radios = {
            "system": self.widgets["app_settings_color_theme_radio_system"],
            "light": self.widgets["app_settings_color_theme_radio_light"],
            "dark": self.widgets["app_settings_color_theme_radio_dark"],
            "green": self.widgets["app_settings_color_theme_radio_green"],
            "orange": self.widgets["app_settings_color_theme_radio_orange"],
            "custom": self.widgets["app_settings_color_theme_radio_custom"],
        }

        self.register_field(
            key=theme_key,
            widget=None,  # no automatic signal connections
            **radio_field(self._theme_radios),
            on_change=self._preview_theme,
        )

        # connect toggled signals
        for rb in self._theme_radios.values():
            rb.toggled.connect(lambda checked, key=theme_key:
                               self._handle_change(key) if checked else None)


    # helper methods for radio buttons
    def _get_theme(self):
        for name, rb in self._theme_radios.items():
            if rb.isChecked():
                return name
        return "system"

    def _set_theme(self, theme_name):
        for name, rb in self._theme_radios.items():
            rb.setChecked(name == theme_name)

    def _preview_theme(self, theme_name):
        if self.theme_manager:
            self.theme_manager.apply_theme(theme_name)

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)