from PySide6.QtWidgets import QRadioButton, QLabel, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from ui.forms.input_form import InputForm
from ui.forms.field_adapters import *

class AppThemesForm(InputForm):
    def __init__(self, ui, settings_manager, theme_manager, widgets=None):
        super().__init__(ui, settings_manager, theme_manager, widgets=widgets)

        # placeholder grid layout for dynamic widgets
        self.widgets['app_themes_grid'] = ui.findChild(QGridLayout, 'app_themes_grid')
        grid_layout = self.widgets.get("app_themes_grid")
        if grid_layout is None:
            raise RuntimeError("Placeholder grid 'app_themes_grid' not found in widgets")

        # --- Column 0: Themes Radio Buttons ---
        self._theme_radios = {}
        top_label = QLabel(self.tr("Themen:"))
        grid_layout.addWidget(top_label, 0, 0, alignment=Qt.AlignLeft)

        for row, theme_name in enumerate(theme_manager.themes.keys(), start=1):
            rb = QRadioButton(theme_name.capitalize())
            grid_layout.addWidget(rb, row, 0, alignment=Qt.AlignLeft)
            self._theme_radios[theme_name] = rb

            # connect toggled signal to preview theme and update colors
            rb.toggled.connect(lambda checked, tn=theme_name:
                               self._on_theme_selected(tn) if checked else None)

        # --- Column 1: Color definitions ---
        color_label = QLabel(self.tr("Farbdefinitionen:"))
        grid_layout.addWidget(color_label, 0, 1, alignment=Qt.AlignLeft)

        self._color_labels = {}
        for row, color_key in enumerate(sorted(theme_manager.REQUIRED_THEME_KEYS), start=1):
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lbl.setStyleSheet("border: 1px solid #888; padding: 2px;")
            grid_layout.addWidget(lbl, row, 1, alignment=Qt.AlignLeft)
            self._color_labels[color_key] = lbl

        # --- Register theme field for InputForm machinery ---
        theme_key = "app_settings.app_theme"
        self.register_field(
            key=theme_key,
            widget=None,  # handled dynamically
            **radio_field(self._theme_radios),
            on_change=self._preview_theme,
        )

        # --- Set the currently active theme ---
        self._set_theme(settings_manager.get(theme_key))
        # Initialize the color labels according to the current theme
        self._update_color_labels(self._get_theme())

    # --- Handle a theme being selected ---
    def _on_theme_selected(self, theme_name):
        self._preview_theme(theme_name)
        self._update_color_labels(theme_name)

    # --- Update the color labels for a given theme ---
    def _update_color_labels(self, theme_name):
        if not self.theme_manager:
            return

        theme_colors = self.theme_manager.themes.get(theme_name, {})
        for color_key, lbl in self._color_labels.items():
            hex_value = theme_colors.get(color_key, "#000000")
            lbl.setText(f"{color_key}: {hex_value}")
            lbl.setStyleSheet(f"border: 1px solid #888; padding: 2px; background-color: {hex_value}; color: {self._text_color_for_bg(hex_value)}")

    # --- Helper to decide text color for contrast ---
    def _text_color_for_bg(self, hex_color):
        """Return 'black' or 'white' depending on bg brightness."""
        try:
            c = QColor(hex_color)
            brightness = (c.red() * 299 + c.green() * 587 + c.blue() * 114) / 1000
            return "black" if brightness > 128 else "white"
        except Exception:
            return "black"

    # helper to get currently selected theme
    def _get_theme(self):
        for name, rb in self._theme_radios.items():
            if rb.isChecked():
                return name
        return "system"

    # helper to set theme by name
    def _set_theme(self, theme_name):
        for name, rb in self._theme_radios.items():
            rb.blockSignals(True)
            rb.setChecked(name == theme_name)
            rb.blockSignals(False)
        self._update_color_labels(theme_name)

    # preview theme via ThemeManager
    def _preview_theme(self, theme_name):
        if self.theme_manager:
            self.theme_manager.apply_theme(theme_name)

    # load from settings
    def load(self):
        for key, field in self._fields.items():
            value = self.settings_manager.get(key)
            field["setter"](field["widget"], value)
