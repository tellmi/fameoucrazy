# app_windows/settings/sub_tabs/app_themes_subtab.py
# -*- coding: utf-8 -*-

from ui.forms.settings.app_settings_form import AppSettingsForm

class AppThemesSubTab:
    """
    Handles the App Themes subtab.
    Currently only manages AppSettingsForm for theme-related settings.
    """

    def __init__(self, parent, settings_manager, theme_manager, widgets: dict):
        self.parent = parent
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        self.widgets = widgets

        self._init_forms()

    def _init_forms(self):
        # Currently only AppSettingsForm is relevant here
        self.forms = [
            AppSettingsForm(
                ui=self.parent,
                settings_manager=self.settings_manager,
                theme_manager=self.theme_manager,
                widgets=self.widgets
            ),
        ]

    # ---------- public API ----------

    def load(self):
        """Load settings into all forms"""
        for form in self.forms:
            form.load()

    def save(self):
        """Save settings from all forms"""
        for form in self.forms:
            form.save()
        self.settings_manager.save_all()

    def is_dirty(self) -> bool:
        return any(form.is_dirty() for form in self.forms)
