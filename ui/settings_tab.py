# ui/settings_tab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from ui.utils import get_all_child_widgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class SettingsTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self.load_ui()

        # Collect all widgets from UI (recursive)
        self.widgets = get_all_child_widgets(self)

    def load_ui(self):
        """Load the UI from the .ui file"""
        ui_file = QFile("ui/settings_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open settings_tab.ui")
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        if loaded_ui is None:
            raise RuntimeError("Failed to load settings_tab.ui")
        ui_file.close()

    # Example method to load settings
    def load_settings(self):
        """Load settings into the UI"""
        pass

    # Example method to save settings
    def save_settings(self):
        """Save settings from the UI"""
        pass
