# objects/settings.py
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import logging

# ------------------------------------------------------------
# Default Settings
# ------------------------------------------------------------
default_settings = {
    "app_settings": {
        "last_client_id": None,
        "app_language": "de",
        "app_theme": "light"   # hier speichern wir den aktuell gewählten Theme-Namen
    },
    "advisor": {
        "salutation": None,
        "given_name": "",
        "middle_name": "",
        "surname": "",
        "birthdate": ""
    },
    "database": {
        "host": "localhost",
        "port": 3309,
        "dbname": "meine_db",
        "user": "user",
        "password": ""
    },
    "paperless": {
        "host": "localhost",
        "port": 3309,
        "dbname": "meine_db",
        "user": "user",
        "password": ""
    },
    "custom": {
        "main": "#4caf50",
        "secondary": "#cccccc",
        "handle": "#ffffff",
        "background": "#f5f5f5",
        "error": "#a51d2d"
    }
}

# ------------------------------------------------------------
# Settings laden / speichern
# ------------------------------------------------------------
def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.warning("Settings-Datei defekt oder nicht vorhanden – Defaults werden verwendet")
        loaded = {}

    return merge_defaults(default_settings, loaded)

def save_settings(settings):
    tmp_file = SETTINGS_FILE.with_suffix(".tmp")

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

    tmp_file.replace(SETTINGS_FILE)

# ------------------------------------------------------------
# Theme-Helfer
# ------------------------------------------------------------
def get_current_theme() -> str:
    """Gibt das aktuell gespeicherte Theme zurück"""
    if settings:
        return settings.get("theme", "light")

def set_current_theme(theme_name: str):
    """Speichert ein neues Theme"""
    settings = load_settings()
    settings.setdefault("app_settings", {})["app_theme"] = theme_name
    save_settings(settings)

def merge_defaults(defaults: dict, loaded: dict) -> dict:
    result = defaults.copy()
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_defaults(result[key], value)
        else:
            result[key] = value
    return result


class SettingsManager:
    def __init__(self, settings_file=None):
        self.settings_file = settings_file or Path.home() / ".fameoucrazy" / "config" / "fameoucrazy_settings.json"
        self.settings = self.load_settings()

    def load_settings(self):
        """Lädt die Einstellungen aus der JSON-Datei und kombiniert sie mit den Standardwerten."""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning("Settings-Datei nicht gefunden oder beschädigt, Standardwerte werden verwendet.")
            loaded = {}

        # Default-Werte hinzufügen, falls sie nicht vorhanden sind
        return self.merge_defaults(self.default_settings(), loaded)

    def default_settings(self):
        """Standardwerte für die Einstellungen."""
        return {
            "app_settings": {
                "last_client_id": None,
                "app_language": "de",
                "app_theme": "light"  # Standard-Theme
            },
            "advisor": {
                "salutation": None,
                "given_name": "",
                "middle_name": "",
                "surname": "",
                "birthdate": ""
            },
            "database": {
                "host": "localhost",
                "port": 3306,
                "dbname": "meine_db",
                "user": "root",
                "password": ""
            },
            "custom_theme": {
                "main": "#4caf50",
                "secondary": "#cccccc",
                "handle": "#ffffff",
                "background": "#f5f5f5",
                "error": "#a51d2d"
            }
        }

    def merge_defaults(self, default, loaded):
        """Vereint Standardwerte mit geladenen Werten."""
        result = default.copy()
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = self.merge_defaults(result[key], value)
            else:
                result[key] = value
        return result

    def save_settings(self):
        """Speichert die aktuellen Einstellungen in der JSON-Datei."""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            logging.info(f"Einstellungen erfolgreich in {self.settings_file} gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Einstellungen: {e}")

    def get(self, key, default=None):
        """Gibt den Wert einer Einstellung zurück."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Setzt einen neuen Wert für eine Einstellung und speichert die Änderungen."""
        keys = key.split(".")
        settings_ref = self.settings
        for k in keys[:-1]:
            settings_ref = settings_ref.get(k, {})
        settings_ref[keys[-1]] = value
        self.save_settings()

    def get_current_theme(self):
        """Gibt das aktuell gespeicherte Theme zurück."""
        return self.get("app_settings.app_theme", "light")

    def set_current_theme(self, theme_name):
        """Setzt ein neues Theme und speichert die Änderung."""
        self.set("app_settings.app_theme", theme_name)

    def get_custom_theme(self):
        """Gibt das benutzerdefinierte Theme zurück."""
        return self.get("custom_theme", {})

    def set_custom_theme(self, custom_theme):
        """Setzt ein benutzerdefiniertes Theme und speichert es."""
        self.set("custom_theme", custom_theme)