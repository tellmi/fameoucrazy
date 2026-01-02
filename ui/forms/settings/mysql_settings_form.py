# ui/forms/settings/mysql_settings_form.py
# -*- coding: utf-8 -*-


from PySide6.QtWidgets import QLineEdit, QCheckBox
import logging
from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class MySQLSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        # Local host
        self.register_field(
            key="mysql.local_host",
            widget=ui.findChild(QLineEdit, "mysql_loc_host_edit"),
            **text_field()
        )

        # External host
        self.register_field(
            key="mysql.external_host",
            widget=ui.findChild(QLineEdit, "mysql_ext_host_edit"),
            **text_field()
        )

        # Username
        self.register_field(
            key="mysql.username",
            widget=ui.findChild(QLineEdit, "mysql_user_edit"),
            **text_field()
        )

        # Password
        self.register_field(
            key="mysql.password",
            widget=ui.findChild(QLineEdit, "mysql_password_edit"),
            **text_field()
        )

        # Port
        self.register_field(
            key="mysql.port",
            widget=ui.findChild(QLineEdit, "mysql_port_edit"),
            **text_field()
        )

        # Database name
        self.register_field(
            key="mysql.db_name",
            widget=ui.findChild(QLineEdit, "mysql_db_edit"),
            **text_field()
        )

        # Charset
        self.register_field(
            key="mysql.charset",
            widget=ui.findChild(QLineEdit, "mysql_charset_edit"),
            **text_field()
        )

        # AutoCommit
        self.register_field(
            key="mysql.autocommit",
            widget=ui.findChild(QCheckBox, "mysql_auto_commit_toggle"),
            **toggle_field()  # ✅ now uses your adapter
        )

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            logging.debug(f"[LOAD] {key} = {value}")
            field["setter"](field["widget"], value)


