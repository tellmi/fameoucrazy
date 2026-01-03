# ui/custom_ui_loader.py
# -*- coding: utf-8 -*-

from PySide6.QtUiTools import QUiLoader
from ui.widgets.advanced_animated_toggle import AdvancedAnimatedToggle


class CustomUiLoader(QUiLoader):
    def createWidget(self, class_name, parent=None, name=""):
        if class_name == "AdvancedAnimatedToggle":
            w = AdvancedAnimatedToggle(parent)
            w.setObjectName(name)
            return w
        return super().createWidget(class_name, parent, name)
