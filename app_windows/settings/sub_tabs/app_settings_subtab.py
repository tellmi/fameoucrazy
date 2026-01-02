# app_windows/settings/sub_tabs/app_settings_subtab.py
# -*- coding: utf-8 -*-
import logging
from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from ui.forms.settings.advisor_settings_form import AdvisorSettingsForm
from ui.forms.settings.mysql_settings_form import MySQLSettingsForm
from ui.forms.settings.paperless_settings_form import PaperlessSettingsForm

class AppSettingsSubTab:
    def __init__(self, parent, settings_manager, theme_manager):
        self.parent = parent
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        # Load the UI file
        ui_file = QFile("app_windows/settings/sub_tabs/app_settings_subtab.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.container = loader.load(ui_file, parent)
        ui_file.close()

        # Init forms with the container
        self._init_forms()

    def _load_ui(self, ui_file_path: str) -> QWidget:
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError(f"Cannot open UI file: {ui_file_path}")
        try:
            container = loader.load(ui_file)
        finally:
            ui_file.close()

        if container is None:
            raise RuntimeError(f"Failed to load UI from: {ui_file_path}")

        return container

    def _init_forms(self):
        """Create and register all input forms."""
        self.forms = [
            AdvisorSettingsForm(ui=self.container, settings_manager=self.settings_manager, theme_manager=self.theme_manager),
            MySQLSettingsForm(ui=self.container, settings_manager=self.settings_manager, theme_manager=self.theme_manager),
            PaperlessSettingsForm(ui=self.container, settings_manager=self.settings_manager, theme_manager=self.theme_manager)
        ]

    def load(self):
        """Load all forms from settings."""
        for form in self.forms:
            form.load()

    def save(self):
        """Save all forms to settings."""
        for form in self.forms:
            form.save()

    def is_dirty(self) -> bool:
        """Return True if any form has unsaved changes."""
        return any(form.is_dirty() for form in self.forms)
