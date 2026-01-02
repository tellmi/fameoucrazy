# app_windows/settings/sub_tabs/app_settings_subtab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from ui.forms.settings.app_settings_form import AppSettingsForm
from ui.forms.settings.advisor_settings_form import AdvisorSettingsForm
from ui.forms.settings.mysql_settings_form import MySQLSettingsForm
from ui.forms.settings.paperless_settings_form import PaperlessSettingsForm

class AppSettingsSubTab:
    """
    Manages the forms for the App Settings subtab:
    - AppSettingsForm
    - AdvisorSettingsForm
    - MySQLSettingsForm
    - PaperlessSettingsForm
    """

    def __init__(self, parent: QWidget, settings_manager, theme_manager, widgets: dict):
        self.parent = parent
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        self.widgets = widgets

        self._init_forms()

    def _init_forms(self):
        # Instantiate all forms that belong to this subtab
        self.forms = [
            AppSettingsForm(
                ui=self,
                settings_manager=self.settings_manager,
                theme_manager=self.theme_manager,
                widgets=self.widgets,
            ),
            AdvisorSettingsForm(
                ui=self.parent,
                settings_manager=self.settings_manager,
            ),
            MySQLSettingsForm(
                ui=self.parent,
                settings_manager=self.settings_manager,
            ),
            PaperlessSettingsForm(
                ui=self.parent,
                settings_manager=self.settings_manager,
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
