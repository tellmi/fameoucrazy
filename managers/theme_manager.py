# managers/theme_manager.py
# -*- coding: utf-8 -*-

import json
import logging
from PySide6.QtGui import QGuiApplication, QPalette, QColor
from constants.paths import QSS_FILE
from .settings_manager import SettingsManager
from constants.themes import THEMES


class ThemeManager:
    REQUIRED_THEME_KEYS = frozenset({
        "main", "secondary", "handle", "background", "error"
    })

    def __init__(self, widget=None, settings_manager=None):
        """
        :param widget: Optional QWidget reference for theme application
        :param settings_manager: Required to fetch custom theme & saved theme
        """
        self.widget = widget
        self.settings_manager = settings_manager
        self.qss_file = QSS_FILE

        self.themes = self._load_and_prepare_themes()
        self.current_theme_name = None
        self.current_theme = None
        self._saved_theme_snapshot = None

    def _load_and_prepare_themes(self) -> dict:
        """Load themes from the THEMES dict and merge custom theme from settings."""
        if "light" not in THEMES:
            raise RuntimeError("THEMES must include a 'light' theme")

        base_theme = THEMES["light"]
        themes = {}

        # normalize all predefined themes
        for name, theme in THEMES.items():
            themes[name] = self._normalize_theme(theme, base_theme)

        # add system theme
        system_theme = self.get_system_theme_colors()
        if system_theme:
            themes["system"] = self._normalize_theme(system_theme, base_theme)

        # merge custom theme from settings
        custom_theme = {}
        if self.settings_manager:
            custom_theme = self.settings_manager.get_custom_theme() or {}
        themes["custom"] = self._normalize_theme(custom_theme, base_theme)

        return themes

    def _normalize_theme(self, theme: dict, fallback: dict) -> dict:
        """
        complement missing keys from fallback (light)
        """
        keys = set(fallback) | set(theme)
        return {
            key: theme.get(key, fallback.get(key, "#ff00ff"))  # Pink = Fehler sichtbar
            for key in keys
        }

    def get_system_theme_colors(self):
        palette = QGuiApplication.palette()

        def hex_color(role):
            return palette.color(role).name()

        system_theme = {
            "main": hex_color(QPalette.Highlight),
            "secondary": hex_color(QPalette.Button),
            "handle": hex_color(QPalette.Base),
            "background": hex_color(QPalette.Window),
            "error": "#d32f2f"  # Fallback (System hat meist keine Error-Farbe)
        }

        return system_theme

    def _fade_color(self, color: str, alpha=0.3):
        c = QColor(color)
        c.setAlphaF(alpha)
        return c.name(QColor.HexArgb)

    def _lighten(self, color: str, factor=1.15) -> str:
        color = color.lstrip("#")
        r, g, b = [int(color[i:i + 2], 16) for i in (0, 2, 4)]
        r = min(int(r * factor), 255)
        g = min(int(g * factor), 255)
        b = min(int(b * factor), 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _build_qss(self, theme: dict) -> str:
        """
        reads stylesheet.qss and replaces placeholders by Theme-colors.
        all theme-values are converted to strings
        hover-colors are complemented automaticly
        """
        # save all values as strings
        theme_safe = {}
        for key, value in theme.items():
            if isinstance(value, QColor):
                theme_safe[key] = value.name()
            elif value is None:
                theme_safe[key] = ""
            else:
                theme_safe[key] = str(value)

        # calculate hover-colors, if not present
        if "main_hover" not in theme_safe:
            theme_safe["main_hover"] = self._lighten(theme_safe.get("main", "#ffffff"))
        if "secondary_hover" not in theme_safe:
            theme_safe["secondary_hover"] = self._lighten(theme_safe.get("secondary", "#cccccc"))

        # load stylesheet.qss

        with self.qss_file.open(encoding="utf-8") as f:
            qss_content = f.read()

        # 4implement templates
        from string import Template
        t = Template(qss_content)
        qss_final = t.safe_substitute(theme_safe)

        return qss_final

    def apply_theme(self, theme_name: str, mark_saved: bool = False):
        theme = self.themes.get(theme_name)
        if not theme:
            logging.error(f"Theme '{theme_name}' does not exist")
            return

        self.current_theme_name = theme_name
        self.current_theme = theme.copy()

        self._apply_qss(self.current_theme)

        if mark_saved:
            self._saved_theme_snapshot = self.current_theme.copy()

        logging.info(f"Theme '{theme_name}' applied")

    def update_current_color(self, key: str, value: str):
        if not self.current_theme:
            return
        self.current_theme[key] = value
        self._apply_qss(self.current_theme)

    def save_current_theme(self, settings: SettingsManager):
        self.settings_manager.set_current_theme(self.current_theme_name)

        if self.current_theme_name == "custom":
            self.settings_manager.set_custom_theme(self.current_theme)

        # update snapshot → clean state
        self._saved_theme_snapshot = self.current_theme.copy()

    def reset_to_last_saved(self, settings: SettingsManager):
        # reload settings from disk
        self.settings_manager.load_settings()

        # rebuild themes (custom may have changed)
        self.themes = self._load_and_prepare_themes()

        # reapply last saved theme
        theme_name = self.settings_manager.get_current_theme()
        self.apply_theme(theme_name, mark_saved=True)

    def update_current_color(self, key: str, value: str):
        if not self.current_theme:
            return

        self.current_theme[key] = value
        self._apply_qss(self.current_theme)

    def is_dirty(self) -> bool:
        if self.current_theme is None or self._saved_theme_snapshot is None:
            return False
        return self.current_theme != self._saved_theme_snapshot

    def _apply_qss(self, theme: dict):
        qss = self._build_qss(theme)

        from PySide6.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            app.setStyleSheet(qss)