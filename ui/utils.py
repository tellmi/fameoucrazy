# ui/utils.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget


def get_all_child_widgets(parent: QWidget) -> dict:
    """
    Recursively collect all child widgets of a given root widget.

    This is used as a foundation for:
    - generic UI updates
    - field mapping
    - validation logic

    Returns dict of all child widgets recursively by objectName
    """
    widgets = {}
    for child in parent.findChildren(QWidget):
        name = child.objectName()
        if name:
            widgets[name] = child
        # Recursively include grandchildren
        widgets.update(get_all_child_widgets(child))
    return widgets
