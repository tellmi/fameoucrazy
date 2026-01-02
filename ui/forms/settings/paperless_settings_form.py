# ui/forms/settings/paperless_settings_form.py
# -*- coding: utf-8 -*-


from PySide6.QtWidgets import QLineEdit, QCheckBox
import logging
from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class PaperlessSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        # Local host
        self.register_field(
            key="paperless_hosts.local",
            widget=ui.findChild(QLineEdit, "paperless_loc_host_edit"),
            **text_field()
        )

        # External host
        self.register_field(
            key="paperless_hosts.external",
            widget=ui.findChild(QLineEdit, "paperless_ext_host_edit"),
            **text_field()
        )

        # Port
        self.register_field(
            key="paperless.port",
            widget=ui.findChild(QLineEdit, "paperless_port_edit"),
            **text_field()
        )

        # AutoCommit toggle (if you have a toggle for it)
        # self.register_field(
        #     key="paperless.autocommit",
        #     widget=ui.findChild(QCheckBox, "paperless_auto_commit_toggle"),
        #     **toggle_field()
        # )

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)
