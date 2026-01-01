# managers/widget_manager.py
# -*- coding: utf-8 -*-

from .dashboard_tab import DashboardTab
from .client_tab import ClientTab
from .settings_tab import SettingsTab

class WidgetManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self._widgets = {}

        # Liste der Widgets, die verwaltet werden
        self._widgets['calendar_popup'] = CalendarPopup(main_window)
        self._widgets['toggle_button'] = AdvancedAnimatedToggle(main_window)
        self._widgets['haptic_button'] = HapticButton(main_window)

    def register_widget(self, widget_name: str, widget_instance):
        """
        Registriert ein Widget für die spätere Verwendung.
        """
        self._widgets[widget_name] = widget_instance

    def show_calendar_popup_for(self, qdate_edit: QDateEdit):
        """
        Zeigt das CalendarPopup für ein QDateEdit-Widget.
        """
        calendar_popup = self._widgets.get('calendar_popup')
        if calendar_popup:
            calendar_popup.show_for(qdate_edit)

    def toggle_advanced_toggle(self, toggle_name: str):
        """
        Umschaltet den AdvancedAnimatedToggle.
        """
        toggle = self._widgets.get(toggle_name)
        if toggle and isinstance(toggle, AdvancedAnimatedToggle):
            toggle.setChecked(not toggle.isChecked())

    def register_haptic_button(self, key: str, button: QPushButton, press_offset: int = 1, shadow: bool = True):
        """
        Registriert einen HapticButton.
        """
        haptic_button = HapticButton(
            button.text(),
            press_offset=press_offset,
            shadow=shadow
        )
        self._widgets[key] = haptic_button

    def update_widget_state(self, widget_name: str, state):
        """
        Aktualisiert den Zustand eines bestimmten Widgets (z. B. Toggle-State).
        """
        widget = self._widgets.get(widget_name)
        if widget:
            # Beispiel: Toggle State ändern
            if isinstance(widget, AdvancedAnimatedToggle):
                widget.setChecked(state)

    def get_widget(self, widget_name: str):
        """
        Gibt ein registriertes Widget zurück.
        """
        return self._widgets.get(widget_name)

    def toggle_advanced_toggle(self, toggle_name: str):
        """
        Umschaltet den AdvancedAnimatedToggle.
        """
        toggle = self._widgets.get(toggle_name)
        if toggle and isinstance(toggle, AdvancedAnimatedToggle):
            toggle.setChecked(not toggle.isChecked())

    def register_haptic_button(self, key: str, button: QPushButton, press_offset: int = 1, shadow: bool = True):
        """
        Registriert einen HapticButton.
        """
        haptic_button = HapticButton(
            button.text(),
            press_offset=press_offset,
            shadow=shadow
        )
        self._widgets[key] = haptic_button

    def update_widget_state(self, widget_name: str, state):
        """
        Aktualisiert den Zustand eines bestimmten Widgets (z. B. Toggle-State).
        """
        widget = self._widgets.get(widget_name)
        if widget:
            # Beispiel: Toggle State ändern
            if isinstance(widget, AdvancedAnimatedToggle):
                widget.setChecked(state)

    def get_widget(self, widget_name: str):
        """
        Gibt ein registriertes Widget zurück.
        """
        return self._widgets.get(widget_name)