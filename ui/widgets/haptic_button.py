# ui/witgets/haptic_button.py
# -*- coding: utf-8 -*-

from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect


class HapticButton(QPushButton):
    """
    Leichte 'Haptik' für Buttons:
    - kleiner Press-Offset
    - optionaler Schatten
    - kein eigenes Painting
    """

    def __init__(
        self,
        *args,
        press_offset: int = 1,
        shadow: bool = True,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._press_offset = press_offset
        self._base_geometry = None
        self._anim = None

        if shadow:
            self._init_shadow()

        self.pressed.connect(self._on_pressed)
        self.released.connect(self._on_released)

    # -------------------------------
    # Shadow (optische Tiefe)
    # -------------------------------
    def _init_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)

    # -------------------------------
    # Haptic handling
    # -------------------------------
    def _on_pressed(self):
        if not self.isEnabled():
            return

        self._base_geometry = self.geometry()
        self._animate(down=True)

    def _on_released(self):
        if not self.isEnabled():
            return

        self._animate(down=False)

    def _animate(self, down: bool):
        if not self._base_geometry:
            return

        end = self._base_geometry
        if down:
            end = end.adjusted(
                self._press_offset,
                self._press_offset,
                -self._press_offset,
                -self._press_offset
            )

        self._anim = QPropertyAnimation(self, b"geometry", self)
        self._anim.setDuration(70)
        self._anim.setEasingCurve(QEasingCurve.OutQuad)
        self._anim.setStartValue(self.geometry())
        self._anim.setEndValue(end)
        self._anim.start()