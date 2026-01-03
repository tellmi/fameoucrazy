# ui/widgets/advanced_animated_toggle.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QAbstractButton
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QEasingCurve


class AdvancedAnimatedToggle(QAbstractButton):
    def __init__(self, parent=None, animation_duration=200, hover_duration=100):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)

        # ---------------- Animations ----------------
        self._position_value = 0.0
        self._hover_value = 0.0
        self.animation_duration = animation_duration
        self.hover_duration = hover_duration

        self._position_anim = QPropertyAnimation(self, b"_position", self)
        self._position_anim.setDuration(self.animation_duration)
        self._position_anim.setEasingCurve(QEasingCurve.InOutCubic)

        self._hover_anim = QPropertyAnimation(self, b"_hover", self)
        self._hover_anim.setDuration(self.hover_duration)
        self._hover_anim.setEasingCurve(QEasingCurve.InOutCubic)

        # ---------------- Colors ----------------
        self._onColor = QColor("#4caf50")
        self._offColor = QColor("#cccccc")
        self._handleColor = QColor("#ffffff")
        self._borderColor = QColor("#cccccc")

        # Connect toggle animation
        self.toggled.connect(self.start_toggle_animation)

    # ----------------- Qt Properties -----------------
    def getOnColor(self): return self._onColor
    def setOnColor(self, color):
        self._onColor = color
        self.update()
    onColor = Property(QColor, getOnColor, setOnColor)

    def getOffColor(self): return self._offColor
    def setOffColor(self, color):
        self._offColor = color
        self.update()
    offColor = Property(QColor, getOffColor, setOffColor)

    def getHandleColor(self): return self._handleColor
    def setHandleColor(self, color):
        self._handleColor = color
        self.update()
    handleColor = Property(QColor, getHandleColor, setHandleColor)

    def getBorderColor(self): return self._borderColor
    def setBorderColor(self, color):
        self._borderColor = color
        self.update()
    borderColor = Property(QColor, getBorderColor, setBorderColor)

    # ----------------- Position / Hover Properties -----------------
    def getPosition(self): return self._position_value
    def setPosition(self, val): self._position_value = val; self.update()
    _position = Property(float, getPosition, setPosition)

    def getHover(self): return self._hover_value
    def setHover(self, val): self._hover_value = val; self.update()
    _hover = Property(float, getHover, setHover)

    # ----------------- Hover Events -----------------
    def enterEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_value)
        self._hover_anim.setEndValue(1.0)
        self._hover_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_value)
        self._hover_anim.setEndValue(0.0)
        self._hover_anim.start()
        super().leaveEvent(event)

    # ----------------- Toggle Animation -----------------
    def start_toggle_animation(self):
        self._position_anim.stop()
        self._position_anim.setStartValue(self._position_value)
        self._position_anim.setEndValue(1.0 if self.isChecked() else 0.0)
        self._position_anim.start()

    # ----------------- Paint -----------------
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        radius = h / 2

        # ---------------- Background ----------------
        bg = self._onColor if self.isChecked() else self._offColor
        bg = QColor(bg)  # make a copy
        alpha_multiplier = 1.0 + 0.3 * self._hover_value
        bg.setAlphaF(min(bg.alphaF() * alpha_multiplier, 1.0))
        p.setBrush(QBrush(bg))
        p.setPen(self._borderColor)
        p.drawRoundedRect(0, 0, w, h, radius, radius)

        # ---------------- Handle ----------------
        handle_radius = h * 0.9 / 2
        handle_x = self._position_value * (w - 2 * handle_radius - 2) + 1
        handle_y = (h - 2 * handle_radius) / 2
        p.setBrush(QBrush(self._handleColor))
        p.setPen(Qt.NoPen)
        p.drawEllipse(handle_x, handle_y, 2 * handle_radius, 2 * handle_radius)

        p.end()
