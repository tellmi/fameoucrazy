# dosc/colors_themes.nd
# Color & Theme Architecture

This document describes the three-layer color architecture used in the application.
The goal is strict separation of concerns, full theme flexibility, and long-term
maintainability.

---

## Overview

The application uses three distinct layers for colors:

Widgets
  ↓ (bind to semantic roles)
Intermediate Role Colors
  ↓ (user-editable mapping)
Theme Base Colors

---

## Core Principles

1. Widgets never use absolute colors
2. Widgets never use theme base colors directly
3. Widgets bind only to intermediate semantic roles
4. ThemeManager is the single source of truth
5. Intensity / brightness adjustments live in role mappings, not widgets

---

## 1. Theme Base Colors (Lowest Layer)

Theme base colors are the only actual color values (hex codes).
They define the minimal contract every theme must fulfill.

### Required Theme Keys

REQUIRED_THEME_KEYS = {
    "main",        # primary UI color
    "secondary",   # secondary / accent color
    "handle",      # sliders, toggles, draggable controls
    "background",  # general background surfaces
    "error",       # error and destructive actions
}

These colors:
- are stored and loaded by ThemeManager
- can come from predefined themes, system palette, or user themes
- are never accessed directly by widgets

---

## 2. Intermediate Role Colors (Semantic Layer)

Intermediate role colors form the design language of the application.
They describe meaning, not appearance.

Examples:
- container_backgrounds
- widget_backgrounds
- accent_primary
- border_default
- text_primary
- error_fg

This layer enables:
- consistent UI appearance
- user-customizable mappings
- reuse across widgets and layouts

Widgets and QSS only reference these roles.

---

## 3. Role → Theme Mapping (Hardcoded Defaults)

Intermediate roles are mapped to base theme colors with optional
intensity multipliers.

This mapping lives in ThemeManager and provides sensible defaults.
Users may later override these mappings.

Example mapping:

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

    # Text
    "text_primary":        ("main", 1.0),
    "text_secondary":      ("secondary", 0.85),

    # Errors
    "error_fg":            ("error", 1.0),
    "error_bg":            ("error", 1.15),
}

Intensity rules:
- 1.0 → base color
- < 1.0 → darker
- > 1.0 → lighter

---

## 4. QSS Usage (Only Intermediate Roles)

QSS files use placeholders that correspond to intermediate roles.
No theme keys or hex colors appear in QSS.

Example: Toggle Styling

AdvancedAnimatedToggle {
    qproperty-onColor: ${accent_primary};
    qproperty-offColor: ${accent_secondary};
    qproperty-handleColor: ${control_handle};
    qproperty-borderColor: ${border_default};
}

AdvancedAnimatedToggle:hover {
    qproperty-onColor: ${accent_primary_hover};
}

Example: Containers

#main_panel {
    background-color: ${container_bg};
}

#sidebar {
    background-color: ${container_bg_soft};
}

#popup {
    background-color: ${container_bg_hard};
}

---

## 5. Widgets (Purely Mechanical)

Custom widgets (e.g. AdvancedAnimatedToggle) expose properties only.

They do not:
- know about themes
- know about base colors
- compute intensities
- hardcode any color values

Example widget properties:
- onColor     → color when checked
- offColor    → color when unchecked
- handleColor → handle fill
- borderColor → outline

Widgets simply render what they are given.

---

## Responsibilities Summary

Theme Base Colors:
- Actual color values (hex)

Intermediate Roles:
- Semantic meaning

ThemeManager:
- Mapping, intensity, resolution

QSS:
- Styling using roles

Widgets:
- Painting using provided properties

---

## Design Goals Achieved

- Full theme switching without widget changes
- User-editable color semantics
- Consistent UI across the application
- Clear separation of concerns
- Future-proof theme editor support

---

Rule of thumb:

If a widget knows a hex color or a theme key, the architecture is broken.
