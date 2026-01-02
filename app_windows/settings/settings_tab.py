# ui/settings_tab.py
# -*- coding: utf-8 -*-

import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea  # import QScrollArea here
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer

from ui.utils import get_all_child_widgets
from managers.action_button_manager import ActionButtonManager

from app_windows.settings.sub_tabs.app_settings_subtab import AppSettingsSubTab
from app_windows.settings.sub_tabs.app_themes_subtab import AppThemesSubTab
#from app_windows.settings.sub_tabs.data_relations_subtab import DataRelationsSubTab


class SettingsTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self.load_ui()
        self._init_subtabs()

        # Load saved settings into forms
        self.populate_forms_from_settings()

        # Initialize ActionButtonManager
        self.action_button_manager = ActionButtonManager(main_window=self)
        self._prepare_action_buttons()

        self.subtabs = [
            self.app_subtab,
            self.theme_subtab,
            self.data_relations_subtab
        ]

    def load_ui(self):
        ui_file = QFile("app_windows/settings/settings_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open settings_tab.ui")

        # --- Load UI ---
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)  # parent=self
        ui_file.close()

        if loaded_ui is None:
            raise RuntimeError("Failed to load settings_tab.ui")

        # --- Root layout for the tab ---
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # --- Scroll area ---
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        root_layout.addWidget(scroll_area)

        # --- Content container ---
        scroll_area.setWidget(loaded_ui)

        # --- Collect all widgets including root ---
        self.widgets = {loaded_ui.objectName(): loaded_ui}  # include root
        self.widgets.update(get_all_child_widgets(loaded_ui))  # include all descendants

        # --- Debug dump ---
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("=== SETTINGS TAB WIDGET DUMP ===")
            for name in sorted(self.widgets.keys()):
                logging.debug(name)
            logging.debug("=== END WIDGET DUMP ===")

        # --- Check required pages ---
        required_pages = (
            "app_settings_page",
            "app_themes_page",
            "data_relations_page",
        )
        for name in required_pages:
            if name not in self.widgets:
                raise RuntimeError(f"Required page '{name}' not found")

    def _init_subtabs(self):
        self.app_subtab = AppSettingsSubTab(
            parent=self,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=get_all_child_widgets(self.widgets["app_settings_groupbox"]),
        )

        self.theme_subtab = AppThemesSubTab(
            parent=self,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=get_all_child_widgets(self.widgets["app_themes_page"]),
        )

        self.data_relations_subtab = DataRelationsSubTab(
            parent=self,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=get_all_child_widgets(self.widgets["data_relations_page"]),
        )

        self.sub_tabs = [
            self.app_subtab,
            self.theme_subtab,
            self.data_relations_subtab,
        ]

    # connect save & cancel
    def _prepare_action_buttons(self):
        # Register buttons
        save_btn = self.widgets["app_settings_save_button"]
        cancel_btn = self.widgets["app_settings_cancel_button"]

        self.action_button_manager.register_button(
            key="app_settings_save",
            button=save_btn,
            role="save",
            handler=self.save_settings,
        )

        self.action_button_manager.register_button(
            key="app_settings_cancel",
            button=cancel_btn,
            role="cancel",
            handler=self.populate_forms_from_settings,
        )

    def populate_forms_from_settings(self):
        for tab in self.sub_tabs:
            tab.load()

    def save_settings(self):
        for tab in self.sub_tabs:
            tab.save()
        self.settings_manager.save_all()

    def is_dirty(self) -> bool:
        return any(tab.is_dirty() for tab in self.sub_tabs)
