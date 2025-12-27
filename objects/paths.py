# objects/paths.py
# -*- coding: utf-8 -*-

"""
Directory structure and important paths of the application

ROOT_DIR        - Root directory of the app
UI_DIR          - Folder containing all UI files
UI_FORMS_DIR    - Subfolder for UI forms (.ui files)
THEMES_FILE      - JSON file with default themes (read-only for users)
QSS_FILE        - Stylesheet template for themes (.qss)
DB_FILE         - Main SQLite file in the project folder
APP_HOME        - User-specific app data folder (~/.fameoucrazy)
CONFIG_DIR      - Subfolder in APP_HOME for settings
SETTINGS_FILE   - JSON file with user settings
DB_DIR          - Subfolder in ROOT_DIR for local database files
LOCAL_DB_PATH   - Path to the local SQLite database
"""
import platform
from pathlib import Path

# ------------------------------------------------------------
# app folder structure
# ------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent  # geht vom /objects Ordner aus
UI_DIR = ROOT_DIR / "ui"
UI_FORMS_DIR = UI_DIR / "forms"
DB_DIR = ROOT_DIR / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
OBJECTS_DIR = ROOT_DIR / "objects"


# ------------------------------------------------------------
# app files structure
# ------------------------------------------------------------
#
THEMES_FILE = OBJECTS_DIR / "themes.json"
QSS_FILE = OBJECTS_DIR / "stylesheet.qss"

# SQLite-database path
LOCAL_DB_PATH = DB_DIR /  "db.sqlite3"


# ------------------------------------------------------------
# base dir for all user-app-data
# ------------------------------------------------------------
if platform.system() == "Windows":
    APP_HOME = Path.home() / "AppData" / "Local" / "fameoucrazy"
else:
    APP_HOME = Path.home() / ".config" / "fameoucrazy"
APP_HOME.mkdir(parents=True, exist_ok=True)

# user settings-file
SETTINGS_FILE = APP_HOME / "fameoucrazy_settings.json"

