# app_windows/settings/sub_tabs/app_themes_subtab.py
# -*- coding: utf-8 -*-

import logging
from ui.forms.settings.app_settings_form import AppSettingsForm
from ui.utils import get_all_child_widgets

class AppThemesSubTab:
    def __init__(self, parent, settings_manager, theme_manager, container):
        self.parent = parent
        self.settings_manager = settings_manager
        self.theme_manager = theme_manager

        # container is the page for themes, e.g., parent.widgets['app_themes_page']
        self.container = container
        self.widgets = {container.objectName(): container}
        self.widgets.update(get_all_child_widgets(container))

        self._init_forms()

    def _init_forms(self):
        """Initialize the theme settings form."""
        # Only registers fields if the corresponding widget exists
        self.form = AppSettingsForm(
            ui=self.container,
            settings_manager=self.settings_manager,
            theme_manager=self.theme_manager,
            widgets=self.widgets
        )

    def load(self):
        self.form.load()

    def save(self):
        self.form.save()

    def is_dirty(self) -> bool:
        return self.form.is_dirty()
