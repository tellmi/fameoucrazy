# ui/forms/settings/paperless_settings_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class PaperlessSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        self.register_field(
            key="paperless_hosts.local",
            widget=ui.widgets["paperless_loc_host_edit"],
            **text_field()
        )

        self.register_field(
            key="paperless_hosts.external",
            widget=ui.widgets["paperless_ext_host_edit"],
            **text_field()
        )

        self.register_field(
            key="paperless.port",
            widget=ui.widgets["paperless_port_edit"],
            **text_field()
        )

    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)
