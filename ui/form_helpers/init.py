# ui/form_helpers/init.py
# -*- coding: utf-8 -*-

from .combo_fillers import *
from .date_helpers import *
from .line_edit_helpers import *

from constants.salutations import SALUTATIONS
from constants.settings import DEFAULT_LANGUAGE

def fill_salutation_combo(combo, language=DEFAULT_LANGUAGE):
    combo.clear()
    for value, label in SALUTATIONS.get(language, []):
        combo.addItem(label, value)