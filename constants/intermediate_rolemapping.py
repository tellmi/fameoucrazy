# constants/intermediate_rolemapping.py
# -*- coding: utf-8 -*-

INTERMEDIATE_ROLE_MAPPING = {
    # Accents
    "accent_primary":      ("main", 1.0),
    "accent_secondary":    ("secondary", 1.0),

    # Handles & borders
    "control_handle":      ("handle", 1.0),
    "border_default":      ("handle", 0.9),

    # Containers
    "container_bg":        ("background", 1.0),
    "container_bg_soft":   ("background", 0.95),
    "container_bg_hard":   ("background", 1.05),

    # Widgets
    "widget_bg":           ("background", 0.9),
    "surface_widget":      ("background", 1.0),

    # Text
    "text_primary":        ("main", 1.0),
    "text_secondary":      ("secondary", 0.85),

    # Errors
    "error_fg":            ("error", 1.0),
    "error_bg":            ("error", 1.15),
}
