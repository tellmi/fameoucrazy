# app_windows/settings/settings_tab.py
# -*- coding: utf-8 -*-

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from ui.utils import get_all_child_widgets
from app_windows.settings.sub_tabs.app_settings_subtab import AppSettingsSubTab
from app_windows.settings.sub_tabs.app_themes_subtab import AppThemesSubTab
# from app_windows.settings.sub_tabs.data_relations_subtab import DataRelationsSubTab


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

        loader = QUiLoader()
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
        """Initialize all settings subtabs."""
        settings_container = self  # The top-level widget loaded from UI

        # Create subtabs
        self.settings_subtab = AppSettingsSubTab(
            parent=settings_container,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager
        )

        # If you have other subtabs:
        # self.themes_subtab = ThemesSubTab(parent=settings_container, ...)
        # self.data_subtab = DataSubTab(parent=settings_container, ...)

        # Store all subtabs in a list for iteration
        self.subtabs = [
            self.settings_subtab,
            # self.themes_subtab,
            # self.data_subtab
        ]

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
