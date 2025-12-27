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
    widgets = []

    for child in root.findChildren(QWidget):
        widgets.append(child)
        widgets.extend(get_all_child_widgets(child))

    return widgets
