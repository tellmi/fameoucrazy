# ui/forms/settings/mysql_settings_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class MySQLSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        self.register_field(
            key="db_hosts.local",
            widget=ui.widgets["mysql_loc_host_edit"],
            **text_field()
        )

        self.register_field(
            key="db_hosts.external",
            widget=ui.widgets["mysql_ext_host_edit"],
            **text_field()
        )

        self.register_field(
            key="database.port",
            widget=ui.widgets["mysql_port_edit"],
            **text_field()
        )

        self.register_field(
            key="database.user",
            widget=ui.widgets["mysql_user_edit"],
            **text_field()
        )

        self.register_field(
            key="database.password",
            widget=ui.widgets["mysql_password_edit"],
            **password_field()
        )

        self.register_field(
            key="database.dbname",
            widget=ui.widgets["mysql_db_edit"],
            **text_field()
        )

        self.register_field(
            key="database.charset",
            widget=ui.widgets["mysql_charset_edit"],
            **text_field()
        )

        self.register_field(
            key="database.auto_commit",
            widget=ui.widgets["mysql_auto_commit_toggle"],
            **toggle_field()
        )

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)


