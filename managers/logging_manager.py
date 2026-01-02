# managers/logging_manager.py
# -*- coding: utf-8 -*-

import logging
from pathlib import Path


class LoggingManager:
    LEVEL_MAP = {
        "OFF": logging.CRITICAL + 1,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "VERBOSE": logging.DEBUG  # mapped for future extension
    }

    @classmethod
    def apply_settings(cls, settings_manager):
        level_name = settings_manager.get(
            "app_settings.log_level", "INFO"
        )
        log_to_file = settings_manager.get(
            "app_settings.log_to_file", False
        )

        level = cls.LEVEL_MAP.get(level_name, logging.INFO)

        root = logging.getLogger()
        root.setLevel(level)

        # ---- remove existing handlers ----
        for handler in list(root.handlers):
            root.removeHandler(handler)

        # ---- console handler ----
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(cls._formatter())
        root.addHandler(console)

        # ---- optional file handler ----
        if log_to_file:
            log_file = Path("logs/app.log")
            log_file.parent.mkdir(exist_ok=True)

            file_handler = logging.FileHandler(
                log_file, encoding="utf-8"
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(cls._formatter())
            root.addHandler(file_handler)

        logging.debug(
            "Logging configured: level=%s, file=%s",
            level_name, log_to_file
        )

    @staticmethod
    def _formatter():
        return logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
