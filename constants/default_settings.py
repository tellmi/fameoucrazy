# constants/default_settings.py
# -*- coding: utf-8 -*-


# ------------------------------------------------------------
# Default Settings
# ------------------------------------------------------------
DEFAULT_SETTINGS = {
    "app_settings": {
        "last_client_id": None,
        "app_language": "de",
        "app_theme": "light",
        "log_level": "INFO",  # can be "OFF", "INFO", "DEBUG", "VERBOSE"
        "log_to_file": False  # separate toggle for writing logs to external file
    },
    "advisor": {
        "salutation": None,
        "given_name": "",
        "middle_name": "",
        "surname": "",
        "birth_date": ""
    },
    "db_hosts": {
        "local": "192.168.178.78",
        "external": "mydyn.dns.name"
        },
    "database": {
        "host_mode": "auto",
        "port": 3309,
        "dbname": "meine_db",
        "user": "user",
        "password": "",
        "charset": "",
        "auto_commit": False
        },
    "paperless_hosts": {
        "local": "192.168.178.78",
        "external": "mydyn.dns.name"
        },
    "paperless": {
        "enabled": False,
        "host_mode": "auto",
        "port": 3309,
    },
    "custom_theme": {
        "main": "#4caf50",
        "secondary": "#cccccc",
        "handle": "#ffffff",
        "background": "#f5f5f5",
        "error": "#a51d2d"
    }
}