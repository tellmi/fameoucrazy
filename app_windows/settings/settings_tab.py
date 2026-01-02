# ui/settings_tab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer

from ui.utils import get_all_child_widgets
from ui.forms.settings.app_settings_form import AppSettingsForm
from ui.forms.settings.mysql_settings_form import MySQLSettingsForm
from ui.forms.settings.paperless_settings_form import PaperlessSettingsForm
from ui.forms.settings.advisor_settings_form import AdvisorSettingsForm

from managers.action_button_manager import ActionButtonManager


class SettingsTab(QWidget):
    def __init__(self, parent, settings_manager, theme_manager):
        super().__init__(parent)

        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self.load_ui()
        self._init_forms()

        # Load saved settings into forms
        self.populate_forms_from_settings()

        # Initialize ActionButtonManager
        self.action_button_manager = ActionButtonManager(main_window=self)
        self._prepare_acction_buttons()

    def load_ui(self):
        """Load the UI from the .ui file"""
        ui_file = QFile("app_windows/settings/settings_tab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open settings_tab.ui")
        loader = QUiLoader()
        loaded_ui = loader.load(ui_file, self)
        if loaded_ui is None:
            raise RuntimeError("Failed to load settings_tab.ui")
        ui_file.close()

        # get all child widgets
        self.widgets = get_all_child_widgets(self)

        assert "app_settings_save_button" in self.widgets, \
            "Save button not found in settings_tab.ui"

    def populate_forms_from_settings(self):
        # Load settings into each form
        for form in self.forms:
            form.load()

    def save_settings(self):
        """Save settings from all forms"""
        for form in self.forms:
            form.save()
        self.settings_manager.save_all()

    def _init_forms(self):
        self.app_form = AppSettingsForm(
            ui=self,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=self.widgets  # pass the fully populated dict
        )

        self.mysql_form = MySQLSettingsForm(
            ui=self,
            settings_manager=self.settings_manager
        )

        self.paperless_form = PaperlessSettingsForm(
            ui=self,
            settings_manager=self.settings_manager
        )

        self.advisor_form = AdvisorSettingsForm(
            ui=self,
            settings_manager=self.settings_manager
        )

        self.forms = [
            self.app_form,
            self.mysql_form,
            self.paperless_form,
            self.advisor_form,
        ]

    # connect save & cancel
    def _prepare_acction_buttons(self):
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

    def is_dirty(self) -> bool:
        return any(form.is_dirty() for form in self.forms)
