# Application Flows and Navigation

This document provides both a **high-level overview** of the application’s navigation and a **detailed flow** showing managers, forms, and logging/debug paths.

---

## 1. Compact Navigation Overview

+-----------------------+
|      MainWindow       |
+-----------------------+
   |          |          |
   v          v          v
+---------+ +--------+ +------------------------+
|Dashboard| | Client | |      SettingsTab       |
+---------+ +--------+ |------------------------|
                        | - SettingsMainTab      |
                        | - ThemesTab            |
                        | - DataRelationsTab     |
                        +------------------------+
                               |
                               v
                     +--------------------+
                     |    InputForms      |
                     |--------------------|
                     | - Tracks field     |
                     |   changes          |
                     | - save()/load()    |
                     +--------------------+
                               |
                               v
                     +--------------------+
                     | SettingsManager    |
                     |--------------------|
                     | - get()/set()      |
                     | - save_all()       |
                     | - debug_mode/logs  |
                     +--------------------+
                               ^
                               |
                     +--------------------+
                     | ThemeManager       |
                     +--------------------+

**Notes:**

- Save / Cancel buttons in SettingsTab trigger `InputForm.save()` or `InputForm.reset()`.
- Debug / Logging options controlled via `SettingsManager`.
- Themes applied via `ThemeManager`.

---

## 2. Detailed Data / Event Flow

### Main Flow

1. **App start**
   - `main.py` → creates QApplication and qasync loop
   - `SettingsManager.load_from_disk()` loads settings
   - `MainWindow` loads `.ui` and initializes tabs
   - `ThemeManager` applies last saved theme

2. **SettingsTab user input**
   - User edits fields → `InputForm` tracks changes
   - Getters/setters read/write values
   - `InputForm.save()` persists values via `SettingsManager.set()`
   - `SettingsManager.save_all()` writes JSON file

3. **Theme changes**
   - `ThemeManager.update_current_color()` → applies QSS
   - UI updates immediately

4. **Save/Cancel buttons**
   - Managed by `ActionButtonManager`
   - Triggers callbacks:
     - Save → `InputForm.save()` → `SettingsManager.save_all()`
     - Cancel → `InputForm.reset()` → restore previous values

---

### Tab/Subtab Flow

- `MainWindow`
  - Tabs:
    - `DashboardTab`
    - `ClientTab`
    - `SettingsTab`  
      - Subtabs:
        - `SettingsMainTab`
        - `ThemesTab`
        - `DataRelationsTab`
  - Each subtab has its own `InputForm` or specialized form
  - Save/Cancel buttons registered in **ActionButtonManager** but share the same signals

---

### Logging / Debug Mode Flow

- Controlled via `app_settings.debug_mode`, `log_level`, and slider (`debug_slider_position`)
- Console output reflects the level selected:
  - INFO / DEBUG / VERBOSE
- Future:
  - Optional logging to file (`log_to_file`)
  - Optional console QDialog widget

---

### Managers & Utilities

- **SettingsManager**
  - Handles JSON storage
  - get()/set() for nested keys
  - save_all() for persisting all forms
  - Normalizes missing values (e.g., theme)
- **ThemeManager**
  - Applies QSS dynamically
  - Tracks current and custom themes
- **ActionButtonManager**
  - Connects Save/Cancel buttons to handlers
- **InputForm**
  - Generic form handling
  - Registers fields with getter/setter
  - Emits `changed` signal on modification
- **Field adapters**
  - Provide standard getter/setter for widgets like QLineEdit, QComboBox, QCheckBox, QDateEdit, etc.

---

### Guiding Principles

- **Domain decides “what”** – business rules, validations, fallbacks
- **Managers decide “when”** – when to save, apply themes, trigger actions
- **UI decides “how”** – widget layout, tabs, signals
- **DB decides “where”** – persistence location

---

