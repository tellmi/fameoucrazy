# app_windows/dashboard/dashboard_tab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QVBoxLayout, QAbstractButton
from ui.utils import get_all_child_widgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QFile, QPropertyAnimation, QEasingCurve, Property, QRectF
from ui.widgets.advanced_animated_toggle import AdvancedAnimatedToggle  # import toggle
from PySide6.QtGui import QColor, QPainter, QPen
import asyncio  # for animation tasks
from ui.form_helpers.custom_ui_loader import CustomUiLoader

class DashboardTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager, widget_manager=None):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager
        self.widget_manager = widget_manager

        self.load_ui()

        # Collect all widgets from UI (recursive)
        self.widgets = get_all_child_widgets(self)

        # Inject test toggle
        # self._add_test_toggle()

    def load_ui(self):
        ui_file = QFile("app_windows/dashboard/dashboard_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open dashboard_tab.ui")
        loader = CustomUiLoader()
        loaded_ui = loader.load(ui_file, self)
        if loaded_ui is None:
            raise RuntimeError("Failed to load dashboard_tab.ui")
        ui_file.close()

        # Use the layout from loaded_ui, don't overwrite
        self.main_layout = loaded_ui.layout()
        if self.main_layout is None:
            self.main_layout = QVBoxLayout(self)
            self.main_layout.setContentsMargins(0, 0, 0, 0)
            self.main_layout.addWidget(loaded_ui)

        # Collect all widgets recursively from self
        self.widgets = get_all_child_widgets(self)

        #assert "dashboard_scrollArea" in self.widgets, \
        #    "dashboard_scrollArea not found in dashboard_tab.ui"

    # Example async method for loading dashboard data
    async def load_dashboard_data(self):
        """Load dashboard data asynchronously"""
        pass

    # Example method to update UI from data mapping
    def update_ui_from_data(self, data_mapping):
        """Generic method to update UI from dashboard data"""
        pass

    # -----------------------------
    # Test Toggle
    # -----------------------------
    def _add_test_toggle(self):
        toggle = AdvancedAnimatedToggle(parent=self)
        toggle.setFixedSize(120, 60)
        toggle.setChecked(True)
        self.main_layout.addWidget(toggle)