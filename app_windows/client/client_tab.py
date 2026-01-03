# ui/client_tab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout
from ui.utils import get_all_child_widgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys
from ui.form_helpers.custom_ui_loader import CustomUiLoader

class ClientTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self.load_ui()

        # Collect all widgets from UI (recursive)
        self.widgets = get_all_child_widgets(self)

    def load_ui(self):
        ui_file = QFile("app_windows/client/client_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open client_tab.ui")

        loader = CustomUiLoader()
        loaded_ui = loader.load(ui_file)
        ui_file.close()

        if loaded_ui is None:
            raise RuntimeError("Failed to load client_tab.ui")

        layout = QVBoxLayout(self)
        layout.addWidget(loaded_ui)
        self.setLayout(layout)

    # Example async method for loading client data
    async def load_client_data(self):
        """Load client data asynchronously"""
        pass

    # Example method to update UI from data mapping
    def update_ui_from_data(self, data_mapping):
        """Generic method to update UI from client data"""
        pass
