# ui/dashboard_tab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from ui.utils import get_all_child_widgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class DashboardTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self.load_ui()

        # Collect all widgets from UI (recursive)
        self.widgets = get_all_child_widgets(self)

    def load_ui(self):
        """Load the UI from the .ui file"""
        ui_file = QFile("ui/dashboard_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open dashboard_tab.ui")
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        if loaded_ui is None:
            raise RuntimeError("Failed to load dashboard_tab.ui")
        ui_file.close()

    # Example async method for loading dashboard data
    async def load_dashboard_data(self):
        """Load dashboard data asynchronously"""
        pass

    # Example method to update UI from data mapping
    def update_ui_from_data(self, data_mapping):
        """Generic method to update UI from dashboard data"""
        pass
