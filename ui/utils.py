# ui/utils.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget


def get_all_child_widgets(root: QWidget) -> list[QWidget]:
    """
    Recursively collect all child widgets of a given root widget.

    This is used as a foundation for:
    - generic UI updates
    - field mapping
    - validation logic
    """
    widgets = {}
    for w in root.findChildren(QWidget):
        if w.objectName():
            widgets[w.objectName()] = w
    return widgets
