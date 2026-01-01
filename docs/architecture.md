# Application Architecture Overview

This project follows a layered architecture with clearly separated responsibilities.

## Folder Overview

### domain/
Contains business logic and rules.
The domain defines *what the application means*, not how it is displayed or stored.

Examples:
- Salutation selection logic
- Fallback rules
- Validation decisions

The domain must not depend on UI frameworks, databases, or storage mechanisms.

---

### managers/
Coordinates application behavior.
Managers orchestrate interactions between UI, domain services, and infrastructure.

Examples:
- ActionButtonManager
- WidgetManager
- SettingsManager

---

### ui/
User interface components.

Subfolders:
- widgets/ – reusable UI elements
- forms/ – form logic
- form_helpers/ – UI data helpers
- tabs/ – application tabs

UI must not contain business logic.

---

### constants/
Static values that represent business facts or defaults.

Examples:
- Default settings
- Static salutations
- Theme definitions

Constants contain no logic.

---

### db/
Database access and persistence.
Includes repositories and connection management.

---

### Guiding Principle

- Domain decides **what**
- Managers decide **when**
- UI decides **how**
- DB decides **where**
