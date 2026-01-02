# UI Architecture – Settings & SubTabs

This document describes the **final, working architecture** for the Settings tab and its subtabs. It replaces earlier experimental approaches and reflects the *stable mental model* now implemented in the codebase.

---

## 1. High‑level concept

* **MainWindow** owns top‑level tabs (e.g. Settings)
* **SettingsTab** is a *container* loaded from `settings_tab.ui`
* `settings_tab.ui` already defines **empty pages** inside a `QTabWidget`
* Each page acts as a **dock target** for exactly one subtab
* Each subtab loads *its own UI* into its assigned page

> SettingsTab manages *composition*, not UI details.

---

## 2. File & responsibility overview

```
app_windows/
└─ settings/
   ├─ settings_tab.py           # orchestrator
   ├─ settings_tab.ui           # QTabWidget + empty pages
   └─ sub_tabs/
      ├─ app_settings_subtab.py
      ├─ app_settings_subtab.ui
      ├─ app_themes_subtab.py
      ├─ app_themes_subtab.ui
      └─ data_relations_subtab.py (future)
```

```
ui/forms/settings/
├─ app_settings_form.py
├─ app_themes_form.py
└─ ...
```

---

## 3. settings_tab.ui (the docking contract)

`settings_tab.ui` defines:

* A `QTabWidget`
* One empty `QWidget` **per subtab**
* Each widget has a **stable objectName**

Example:

* `app_settings_page`
* `app_themes_page`
* `data_relations_page`

These widgets are **never replaced** — they are docking containers.

---

## 4. SettingsTab responsibilities

`SettingsTab` does **three things only**:

1. Load `settings_tab.ui`
2. Find docking pages by objectName
3. Instantiate subtabs and attach them

```python
class SettingsTab(QWidget):
    def __init__(...):
        self._load_ui()
        self._init_subtabs()
        self.populate_forms_from_settings()
```

### `_init_subtabs()`

```python
app_settings_page = self.findChild(QWidget, "app_settings_page")
app_themes_page   = self.findChild(QWidget, "app_themes_page")
```

Each page is passed **as parent** to its subtab.

SettingsTab never loads subtab UIs itself.

---

## 5. SubTab responsibilities

Each `*SubTab` class:

* Receives **exactly one parent container**
* Loads its own `.ui` file
* Inserts itself into the parent via a layout
* Creates exactly one `Form`

Example flow:

```python
AppThemesSubTab(parent=app_themes_page, ...)
```

### SubTab internal lifecycle

1. Load `app_themes_subtab.ui`
2. Attach UI to `parent` using `QVBoxLayout`
3. Collect widgets via `get_all_child_widgets`
4. Instantiate its Form

SubTabs **never**:

* Touch QTabWidget
* Switch tabs
* Know about other subtabs

---

## 6. Forms (leaf layer)

Forms:

* Bind widgets to settings keys
* Implement `load()`, `save()`, `is_dirty()`

They know nothing about:

* Tabs
* Subtabs
* UI loading

They receive a *ready-to-use widget tree*.

---

## 7. Adding a new subtab (official recipe)

1. Add an empty page to `settings_tab.ui`

   * Set objectName (e.g. `network_page`)
2. Create `network_subtab.ui`
3. Create `NetworkSubTab` class
4. Create `NetworkForm`
5. Register subtab in `_init_subtabs()`

No existing code must be modified.

---

## 8. Why this architecture works

✔ No dynamic tab creation
✔ No implicit parenting
✔ Stable objectName contracts
✔ UI and logic are cleanly separated
✔ Subtabs are independently testable

This is **intentional static composition**, not magic.

---

## 9. What this architecture explicitly avoids

* Loading `.ui` files into other `.ui` files
* Creating QTabWidgets dynamically
* Subtabs knowing about each other
* Forms managing layouts

---

## 10. Status

✅ Implemented
✅ Stable
✅ Debugged

This document is the **single source of truth** for the Settings UI architecture.
