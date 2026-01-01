# ui/forms/settings/mysql_settings_form.py
# -*- coding: utf-8 -*-

from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class AdvisorSettingsForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager=None):
        super().__init__(ui, settings_manager, theme_manager)

        self.register_field(
            key="advisor.salutation",
            widget=ui.widgets["advisor_salutation_combo"],
            **combo_field()
        )

        self.register_field(
            key="advisor.given_name",
            widget=ui.widgets["advisor_given_name_edit"],
            **text_field()
        )

        self.register_field(
            key="advisor.middle_name",
            widget=ui.widgets["advisor_middle_name_edit"],
            **text_field()
        )

        self.register_field(
            key="advisor.surname",
            widget=ui.widgets["advisor_surname_edit"],
            **text_field()
        )

        self.register_field(
            key="advisor.birth_date",
            widget=ui.widgets["advisor_birth_date_edit"],
            **date_field()
        )



    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            logging.debug(f"[LOAD] {key} = {value}")
            field["setter"](field["widget"], value)


