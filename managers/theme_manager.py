# managers/theme_manager.py
# -*- coding: utf-8 -*-

import logging
import inspect
from string import Template
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication, QPalette
from constants.paths import QSS_FILE
from constants.themes import THEMES
from constants.intermediate_rolemapping import INTERMEDIATE_ROLE_MAPPING
from .settings_manager import SettingsManager


class ThemeManager:
    REQUIRED_THEME_KEYS = frozenset({
        "main", "secondary", "handle", "background", "error"
    })

    def __init__(self, settings_manager: SettingsManager = None):
        self.settings_manager = settings_manager
        self.qss_file = QSS_FILE

        # Base theme storage
        self.themes = self._load_and_prepare_themes()
        self.current_theme_name = None
        self.current_theme = None
        self._saved_theme_snapshot = None

        # Semantic role mapping (user-editable)
        self.semantic_roles = {
            "widget_backgrounds": "background",
            "container_backgrounds": "background",
            "text": "main",
            "text_secondary": "secondary",
            "border": "handle",
            "error_text": "error",
        }

        # Widget-specific intensity multipliers
        self.widget_multipliers = {
            "main_panel": ["container_backgrounds", 1.0],
            "sidebar": ["container_backgrounds", 0.95],
            "popup": ["container_backgrounds", 1.05],
        }

    # ---------------- Base Theme Loading ----------------
    def _load_and_prepare_themes(self) -> dict:
        base_theme = THEMES.get("light")
        if not base_theme:
            raise RuntimeError("THEMES must include a 'light' theme")

        themes = {}
        for name, theme in THEMES.items():
            themes[name] = self._normalize_theme(theme, base_theme)

        # Add system theme
        system_theme = self.get_system_theme_colors()
        if system_theme:
            themes["system"] = self._normalize_theme(system_theme, base_theme)

        # Merge custom theme
        custom_theme = {}
        if self.settings_manager:
            custom_theme = self.settings_manager.get_custom_theme() or {}
        themes["custom"] = self._normalize_theme(custom_theme, base_theme)

        return themes

    def _normalize_theme(self, theme: dict, fallback: dict) -> dict:
        keys = set(fallback) | set(theme)
        return {
            key: theme.get(key, fallback.get(key, "#ff00ff"))  # visible pink if missing
            for key in keys
        }

    def get_system_theme_colors(self):
        palette = QGuiApplication.palette()
        return {
            "main": palette.color(QPalette.Highlight).name(),
            "secondary": palette.color(QPalette.Button).name(),
            "handle": palette.color(QPalette.Base).name(),
            "background": palette.color(QPalette.Window).name(),
            "error": "#d32f2f",
        }

    # ---------------- Intensity / Color Helpers ----------------
    def _apply_intensity(self, color_hex: str, intensity: float) -> str:
        """Adjust color brightness using intensity multiplier."""
        color_hex = color_hex.lstrip("#")
        r, g, b = [int(color_hex[i:i + 2], 16) for i in (0, 2, 4)]
        r = min(max(int(r * intensity), 0), 255)
        g = min(max(int(g * intensity), 0), 255)
        b = min(max(int(b * intensity), 0), 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _lighten(self, color_hex: str, factor=1.15) -> str:
        """Lighten color by factor."""
        return self._apply_intensity(color_hex, factor)

    # ---------------- QSS Building ----------------
    def _build_qss(self, theme: dict) -> str:
        """
        Build QSS from:
        - Base theme colors
        - Intermediate role mapping
        - Widget multipliers
        - Auto hover variants
        """
        roles = {}

        # 1️⃣ Compute intermediate roles using mapping
        for role, (base_key, intensity) in INTERMEDIATE_ROLE_MAPPING.items():
            base_color = theme.get(base_key, "#ff00ff")
            roles[role] = self._apply_intensity(base_color, intensity)

        # 2️⃣ Add hover variants for all roles
        for role_name in list(roles.keys()):
            hover_name = f"{role_name}_hover"
            roles[hover_name] = self._lighten(roles[role_name])

        # 3️⃣ Apply widget-specific multipliers
        for widget_name, (role_name, intensity) in self.widget_multipliers.items():
            base_color = roles.get(role_name, "#ff00ff")
            roles[widget_name] = self._apply_intensity(base_color, intensity)

        # 4️⃣ Load QSS template and substitute
        with self.qss_file.open(encoding="utf-8") as f:
            qss_content = f.read()
        template = Template(qss_content)
        try:
            return template.safe_substitute(roles)
        except KeyError as e:
            logging.error(f"Missing QSS placeholder: {e}")
            return ""

    # ---------------- Apply Theme ----------------
    def apply_theme(self, theme_name: str, mark_saved: bool = False):
        theme = self.themes.get(theme_name)
        if self.current_theme_name == theme_name:
            # Already applied, skip redundant call
            logging.debug(f"[SKIP] Theme '{theme_name}' already applied")
            return

        if not theme:
            logging.error(f"Theme '{theme_name}' does not exist")
            return

        self.current_theme_name = theme_name
        self.current_theme = theme.copy()

        # --- DEBUG: show caller ---
        stack = inspect.stack()
        caller = stack[1]
        logging.info(f"[DEBUG] apply_theme called from {caller.filename}:{caller.lineno} - {caller.function}")

        qss = self._build_qss(self.current_theme)
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)
            print("skipped not app stylesheet")

        if mark_saved:
            self._saved_theme_snapshot = self.current_theme.copy()
        logging.info(f"Theme '{theme_name}' applied")

    # ---------------- Update / Save ----------------
    def update_current_color(self, key: str, value: str):
        if not self.current_theme:
            return
        self.current_theme[key] = value
        self.apply_theme(self.current_theme_name)

    def save_current_theme(self):
        if not self.settings_manager:
            return
        self.settings_manager.set_current_theme(self.current_theme_name)
        if self.current_theme_name == "custom":
            self.settings_manager.set_custom_theme(self.current_theme)
        self._saved_theme_snapshot = self.current_theme.copy()

    def is_dirty(self) -> bool:
        if self.current_theme is None or self._saved_theme_snapshot is None:
            return False
        return self.current_theme != self._saved_theme_snapshot
