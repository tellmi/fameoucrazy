# app_windows/settings/settings_tab.py
# -*- coding: utf-8 -*-

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from ui.utils import get_all_child_widgets
from app_windows.settings.sub_tabs.app_settings_subtab import AppSettingsSubTab
from app_windows.settings.sub_tabs.app_themes_subtab import AppThemesSubTab
# from app_windows.settings.sub_tabs.data_relations_subtab import DataRelationsSubTab
from ui.form_helpers.custom_ui_loader import CustomUiLoader


class SettingsTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self._load_ui()
        self._init_subtabs()
        self.populate_forms_from_settings()

    def _load_ui(self):
        """Load the main settings_tab UI (container for all subtabs)."""
        ui_file = QFile("app_windows/settings/settings_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open settings_tab.ui")

        loader = CustomUiLoader()
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        if self.ui is None:
            raise RuntimeError("Failed to load settings_tab.ui")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        # Collect all widgets for debug
        self.widgets = {self.ui.objectName(): self.ui}
        self.widgets.update(get_all_child_widgets(self.ui))

        logging.debug("=== SETTINGS TAB WIDGET DUMP ===")
        for name in sorted(self.widgets.keys()):
            logging.debug(name)
        logging.debug("=== END WIDGET DUMP ===")

    def _init_subtabs(self):
        app_settings_page = self.findChild(QWidget, "app_settings_page")
        app_themes_page = self.findChild(QWidget, "app_themes_page")
        data_relations_page = self.findChild(QWidget, "data_relations_page")

        #if not all([app_settings_page, app_themes_page, data_relations_page]):
        #    raise RuntimeError("Settings subtab pages not found")
        if not app_settings_page:
            raise RuntimeError("app_settings_page not found")

        if not app_themes_page:
            raise RuntimeError("app_themes_page not found")

        self.subtabs = []

        self.subtabs.append(
            AppSettingsSubTab(
                parent=app_settings_page,
                settings_manager=self.settings_manager,
                theme_manager=self.theme_manager,
            )
        )

        self.subtabs.append(
            AppThemesSubTab(
                parent=app_themes_page,
                settings_manager=self.settings_manager,
                theme_manager=self.theme_manager,
            )
        )

        #self.subtabs.append(
        #    DataRelationsSubTab(
        #        parent=data_page,
        #        settings_manager=self.settings_manager,
        #        theme_manager=self.theme_manager,
        #    )
        #)

    def populate_forms_from_settings(self):
        """Load saved settings into all subtabs."""
        for subtab in self.subtabs:
            subtab.load()

    def save_settings(self):
        """Save all subtab forms to settings manager."""
        for subtab in self.subtabs:
            subtab.save()
        self.settings_manager.save_all()

    def is_dirty(self) -> bool:
        """Return True if any subtab has unsaved changes."""
        return any(subtab.is_dirty() for subtab in self.subtabs)
