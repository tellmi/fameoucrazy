# ui/main_window.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QMainWindow, QTabWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from managers.settings_manager import SettingsManager
from managers.theme_manager import ThemeManager
from .dashboard_tab import DashboardTab
from .client_tab import ClientTab
from .settings_tab import SettingsTab
from managers.logging_manager import LoggingManager


class MainWindow(QMainWindow):
    def __init__(self, settings_manager=None, theme_manager=None):
        super().__init__()

        if settings_manager is None:
            raise RuntimeError("MainWindow requires SettingsManager")
        self.settings_manager = settings_manager

        # Automatically create ThemeManager if not passed
        if theme_manager is None:
            self.theme_manager = ThemeManager(widget=self, settings_manager=settings_manager)
        else:
            self.theme_manager = theme_manager

        LoggingManager.apply_settings(settings_manager.settings)

        # Load UI and init tabs
        self.load_ui()
        self.init_tabs()

        # Apply last theme
        last_theme = self.settings_manager.get_current_theme()
        self.theme_manager.apply_theme(last_theme)
        self.theme_manager._saved_theme_snapshot = self.theme_manager.current_theme.copy()


    def load_ui(self):
        ui_file = QFile("ui/main_window.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open main_window.ui")

        loader = QUiLoader()
        loaded_ui = loader.load(ui_file)  # Do NOT pass self
        ui_file.close()

        if loaded_ui is None:
            raise RuntimeError("Failed to load main_window.ui")

        # The loaded_ui is actually the 'centralwidget' in your .ui
        self.setCentralWidget(loaded_ui)
        self.ui = loaded_ui

    def init_tabs(self):
        central_tab = self.ui.findChild(QTabWidget, "central_tab")
        if central_tab is None:
            raise RuntimeError("Cannot find QTabWidget named 'central_tab'")

        # Replace placeholder tabs with your actual widgets
        self.dashboard_tab = DashboardTab(settings_manager=self.settings_manager,
                                          theme_manager=self.theme_manager, parent=self)
        self.client_tab = ClientTab(settings_manager=self.settings_manager,
                                    theme_manager=self.theme_manager, parent=self)
        self.settings_tab = SettingsTab(settings_manager=self.settings_manager,
                                        theme_manager=self.theme_manager, parent=self)

        # Clear placeholders
        while central_tab.count():
            central_tab.removeTab(0)

        # Add real tabs
        central_tab.addTab(self.dashboard_tab, "Dash")
        central_tab.addTab(self.client_tab, "Client")
        central_tab.addTab(self.settings_tab, "Settings")
