# Application Architecture Overview

This project follows a layered architecture with clearly separated responsibilities.

---

## Folder Overview

### domain/
Contains business logic and rules. Defines *what the application means*, not how it is displayed or stored.  

Examples:
- Salutation selection logic
- Fallback rules
- Validation decisions

> **Rule:** Must not depend on UI frameworks, databases, or storage mechanisms.

---

### managers/
Coordinates application behavior. Orchestrates interactions between UI, domain services, and infrastructure.  

Examples:
- `ActionButtonManager` – centralizes Save/Cancel button actions
- `WidgetManager` – handles dynamic widget interactions
- `SettingsManager` – loads, saves, and normalizes settings, including debug/logging configuration

---

### app_windows/
Contains main application windows and their tabs.  

Main navigation: 3 primary tabs → Dashboard, Client, Settings.  
Settings tab itself: 3 subtabs → Settings, Themes, Data & Relations.  
Each subtab has its own form class and registers Save/Cancel buttons with `ActionButtonManager`.  

app_windows/
├─ main_window.py
├─ dashboard/
│ └─ dashboard_tab.py
├─ client/
│ └─ client_tab.py
└─ settings/
├─ settings_tab.py # main settings tab, handles subtab switching
└─ sub_tabs/
├─ app_settings_subtab.py
├─ theme_subtab.py
└─ data_relations_subtab.py

---

### ui/
User interface components.  

Subfolders:
- `forms/` – form logic and field adapters  
- `forms/settings/` – settings-specific forms  
- `form_helpers/` – UI data helpers  
- `widgets/` – reusable UI elements  
- `dialogues/` – modal dialogs (About, Help, Debug Console)  
- `utils.py` – general UI utility functions  

ui/
├─ forms/
│ ├─ input_form.py
│ ├─ field_adapters.py
│ └─ settings/
│ ├─ app_settings_form.py
│ ├─ advisor_settings_form.py
│ ├─ mysql_settings_form.py
│ └─ paperless_settings_form.py
└─ utils.py


Notes:
- UI code must not contain business logic  
- Forms interact with `SettingsManager` for persistence  
- `.ui` files are co-located with their corresponding `.py` classes  
- Dialogues live in `ui/dialogues/`  

---

### constants/
Static values representing business facts or defaults.  

Examples:
- Default settings (`DEFAULT_SETTINGS`)  
- Static salutations  
- Theme definitions (`THEMES`)  

> Contains no logic.

---

### db/
Database access and persistence. Includes repositories, connection pools, and async operations.

---

### Debug / Logging Integration
Debugging and logging are configurable through settings.  

Settings:
- `debug_slider_position` – horizontal slider controlling debug level  
  - 0 = Off  
  - 1 = INFO  
  - 2 = DEBUG  
  - 3 = VERBOSE  
- `log_to_file` – toggle to write logs externally  
- Future toggle: open optional `DebugConsole` dialog to view runtime logs  

Behavior:
- Slider position defines debug/logging level  
- `SettingsManager` persists slider state and maps it to `log_level`  
- Logging affects console output, file output, and optional debug dialogs  

Example snippet from `DEFAULT_SETTINGS`:

DEFAULT_SETTINGS = {
"app_settings": {
"last_client_id": None,
"app_language": "de",
"app_theme": "light",
"debug_slider_position": 0, # 0 = off, 1 = INFO, 2 = DEBUG, 3 = VERBOSE
"log_to_file": False
},
...
}


---

### Guiding Principle
- **Domain** decides *what*  
- **Managers** decide *when*  
- **UI** decides *how*  
- **DB** decides *where*
