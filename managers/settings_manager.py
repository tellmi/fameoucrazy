# managers/settings_manager.py
# -*- coding: utf-8 -*-

from constants.paths import SETTINGS_FILE
from constants.default_settings import DEFAULT_SETTINGS
from managers.logging_manager import LoggingManager
import json
import logging
import copy


class SettingsManager:
    def __init__(self):
        self.settings_file = SETTINGS_FILE
        self.defaults = DEFAULT_SETTINGS
        self.settings = {}

        self.load_from_disk()

    def load_from_disk(self):
        loaded_from = None

        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
                loaded_from = "primary"
        except json.JSONDecodeError:
            logging.warning("Settings corrupted, trying backup")
            backup = self.settings_file.with_suffix(".bak")
            try:
                with open(backup, "r", encoding="utf-8") as f:
                    self.settings = json.load(f)
                    loaded_from = "backup"
            except json.JSONDecodeError:
                logging.error("Backup also corrupted, restoring defaults")
                self.settings = copy.deepcopy(self.defaults)
                loaded_from = "defaults"

        # ---- normalization / validation ----
        theme = self.get("app_settings.app_theme")
        if not theme:
            self.set(
                "app_settings.app_theme",
                self.defaults["app_settings"]["app_theme"]
            )

        # ---- persist repaired settings once ----
        if loaded_from in ("backup", "defaults"):
            self.save()

        # apply logging configuration once settings are known
        LoggingManager.apply_settings(self)

    def save(self):
        if self.settings_file.exists():
            backup = self.settings_file.with_suffix(".bak")
            try:
                self.settings_file.replace(backup)
            except OSError:
                logging.warning("Could not create settings backup")

        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

        logging.info(f"settings saved successfully in {self.settings_file}.")

        # apply logging configuration once settings are known and saved
        LoggingManager.apply_settings(self)

        logging.debug("New logging configuration active")

    def get(self, key, default=None):
        keys = key.split(".")
        ref = self.settings
        for k in keys:
            if not isinstance(ref, dict):
                return default
            ref = ref.get(k)
            if ref is None:
                return default
        return ref

    def set(self, key, value):
        ref = self.settings
        keys = key.split(".")
        for k in keys[:-1]:
            if k not in ref or not isinstance(ref[k], dict):
                ref[k] = {}
            ref = ref[k]
        ref[keys[-1]] = value

    # ---------- theme helpers ----------
    def get_current_theme(self):
        return self.get("app_settings.app_theme", self.defaults.get("app_settings", {}).get("app_theme", "light"))

    def set_current_theme(self, theme_name):
        self.set("app_settings.app_theme", theme_name)

    def get_custom_theme(self):
        """Gibt das benutzerdefinierte Theme zurück."""
        return self.get("custom_theme", {})

    def set_custom_theme(self, custom_theme):
        """Setzt ein benutzerdefiniertes Theme und speichert es."""
        self.set("custom_theme", custom_theme)

    def save_all(self):
        self.save()