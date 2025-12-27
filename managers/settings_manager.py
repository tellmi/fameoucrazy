# managers/settings_manager.py
# -*- coding: utf-8 -*-

from objects.paths import SETTINGS_FILE
import json
import logging


class SettingsManager:
    def __init__(self, settings_file=None):
        self.settings_file = settings_file or SETTINGS_FILE
        self.settings = self.load_settings()

    def load_settings(self):
        """Loading settings from JSON-file and merging with standard values."""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning("Settngs file not found or corrupted, using standard values instead.")
            loaded = {}

        # adding default values if not present
        return self.merge_defaults(self.default_settings(), loaded)

    def default_settings(self):
        """standard values for settings."""
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
        """uniting standard values with loades settings values."""
        result = default.copy()
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = self.merge_defaults(result[key], value)
            else:
                result[key] = value
        return result

    def save_settings(self):
        """saving recent settings in JSON-file."""
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=4)
            logging.info(f"settings saved successfully in {self.settings_file}.")
        except Exception as e:
            logging.error(f"error saving settings: {e}")

    def get(self, key, default=None):
        """return value of a setting"""
        return self.settings.get(key, default)

    def set(self, key, value):
        """ setting new value of a particular setting saving it permanently """
        keys = key.split(".")
        settings_ref = self.settings
        for k in keys[:-1]:
            settings_ref = settings_ref.get(k, {})
        settings_ref[keys[-1]] = value
        self.save_settings()

    def get_current_theme(self):
        """returns recently saved theme"""
        return self.get("app_settings.app_theme", "light")

    def set_current_theme(self, theme_name):
        """setting a new theme and saving the change"""
        self.set("app_settings.app_theme", theme_name)

    def get_custom_theme(self):
        """returns custom user theme"""
        return self.get("custom_theme", {})

    def set_custom_theme(self, custom_theme):
        """setting custom user theme and saving it"""
        self.set("custom_theme", custom_theme)