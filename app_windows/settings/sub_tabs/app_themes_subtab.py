# app_windows/settings/sub_tabs/app_themes_subtab.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

from ui.forms.settings.app_themes_form import AppThemesForm
from ui.utils import get_all_child_widgets
from ui.form_helpers.custom_ui_loader import CustomUiLoader


class AppThemesSubTab:
    def __init__(self, parent, settings_manager, theme_manager):
        self.parent = parent
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        self._load_ui()
        self._init_forms()

    def _load_ui(self):
        ui_file = QFile("app_windows/settings/sub_tabs/app_themes_subtab.ui")
        if not ui_file.open(QFile.ReadOnly):
            raise RuntimeError("Cannot open app_themes_subtab.ui")

        loader = CustomUiLoader()
        self.container = loader.load(ui_file, self.parent)
        ui_file.close()

        if self.container is None:
            raise RuntimeError("Failed to load app_themes_subtab.ui")

        layout = QVBoxLayout(self.parent)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

        # collect widgets
        self.widgets = {self.container.objectName(): self.container}
        self.widgets.update(get_all_child_widgets(self.container))

        # --- DEBUG: list all widgets found ---
        print("[DEBUG] widgets keys:", list(self.widgets.keys()))

    def _init_forms(self):
        self.form = AppThemesForm(
            ui=self.container,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=self.widgets,
        )

    def load(self):
        self.form.load()

    def save(self):
        self.form.save()

    def is_dirty(self) -> bool:
        return self.form.is_dirty()
