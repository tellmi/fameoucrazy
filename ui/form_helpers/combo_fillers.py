# ui/form_helpers/combo_fillers.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QComboBox
from domain.salutation_service import SalutationService

class FormHelper:
    """
    Provides utility methods to fill form widgets with data.
    """

    def __init__(self, salutation_service: SalutationService):
        self.salutation_service = salutation_service

    def fill_salutation_combo(self, combo: QComboBox):
        """
        Fills a QComboBox with salutations from the service.
        """
        combo.clear()
        salutations = self.salutation_service.get_salutations()
        combo.addItems(salutations)
