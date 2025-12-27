# ui/witgets/advanced_animated_toggle.py
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QAbstractButton, QPushButton, QGraphicsDropShadowEffect, QWidget, QCalendarWidget, QVBoxLayout, QDateEdit
from PySide6.QtGui import QGuiApplication, QPainter, QColor, QPen

class AdvancedAnimatedToggle(QAbstractButton):
    def __init__(self, parent=None, theme="light", animation_duration=0.2, hover_duration=0.1, *args, **kwargs):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)

        # Animation
        self._position = 1.0 if self.isChecked() else 0.0
        self.animation_duration = animation_duration
        self._animation_task = None

        # Hover Animation
        self._hover_position = 0.0
        self.hover_duration = hover_duration
        self._hover_task = None

        # Theme
        self.theme = self._load_theme(theme)

        self.toggled.connect(lambda _: asyncio.create_task(self.animate_async()))
        self._hover = False

    # Q_PROPERTYs
    def getOffColor(self): return self._theme_color("off")
    def setOffColor(self, c): self.theme["off"] = QColor(c); self.update()
    offColor = Property(QColor, getOffColor, setOffColor)

    def getOnColor(self): return self._theme_color("on")
    def setOnColor(self, c): self.theme["on"] = QColor(c); self.update()
    onColor = Property(QColor, getOnColor, setOnColor)

    def getHandleColor(self): return self._theme_color("handle")
    def setHandleColor(self, c): self.theme["handle"] = QColor(c); self.update()
    handleColor = Property(QColor, getHandleColor, setHandleColor)

    def getBorderColor(self): return self._theme_color("border")
    def setBorderColor(self, c): self.theme["border"] = QColor(c); self.update()
    borderColor = Property(QColor, getBorderColor, setBorderColor)

    def _theme_color(self, key):
        val = self.theme.get(key)
        return val if isinstance(val, QColor) else QColor(val)

    # ---------------- Theme -----------------
    def _load_theme(self, name):
        if isinstance(name, dict):
            return name
        themes = {
            "light": {"off": QColor("#cccccc"), "on": QColor("#4caf50"), "handle": QColor("#ffffff")},
            "dark": {"off": QColor("#555555"), "on": QColor("#81c784"), "handle": QColor("#eeeeee")},
            "material": {"off": QColor("#9e9e9e"), "on": QColor("#00c853"), "handle": QColor("#ffffff")}
        }
        return themes.get(name, themes["light"])

    # ---------------- Farben helper -----------------
    def _effective_color(self, prop_name, fallback):
        val = self.property(prop_name)
        return QColor(val) if val else fallback


    # Hover Events
    def enterEvent(self, event):
        self._hover = True
        asyncio.create_task(self.animate_hover())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        asyncio.create_task(self.animate_hover())
        super().leaveEvent(event)

    async def animate_hover(self):
        if self._hover_task and not self._hover_task.done():
            self._hover_task.cancel()
            try:
                await self._hover_task
            except asyncio.CancelledError:
                pass

        start = self._hover_position
        end = 1.0 if self._hover else 0.0
        steps = max(int(self.hover_duration / 0.016), 1)
        self._hover_task = asyncio.create_task(self._animate_hover_steps(start, end, steps))

    async def _animate_hover_steps(self, start, end, steps):
        for i in range(1, steps + 1):
            self._hover_position = start + (end - start) * (i / steps)
            self.update()
            await asyncio.sleep(self.hover_duration / steps)
        self._hover_position = end
        self.update()

    # PaintEvent mit Hover Animation
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        off_color = self._effective_color("offColor", self.theme.get("off", QColor("#cccccc")))
        on_color = self._effective_color("onColor", self.theme.get("on", QColor("#4caf50")))
        handle_color = self._effective_color("handleColor", self.theme.get("handle", QColor("#ffffff")))
        border_color = self._effective_color("borderColor", on_color)

        # Hintergrund interpolieren Toggle
        bg = QColor(
            off_color.red() + (on_color.red() - off_color.red()) * self._position,
            off_color.green() + (on_color.green() - off_color.green()) * self._position,
            off_color.blue() + (on_color.blue() - off_color.blue()) * self._position,
        )

        # Hover Effekt (sanft animiert)
        if self._hover_position > 0:
            hover_bg = bg.lighter(120)
            bg.setRed(bg.red() + (hover_bg.red() - bg.red()) * self._hover_position)
            bg.setGreen(bg.green() + (hover_bg.green() - bg.green()) * self._hover_position)
            bg.setBlue(bg.blue() + (hover_bg.blue() - bg.blue()) * self._hover_position)

        # Schalterleiste
        radius = self.height() / 2
        bar_rect = QRectF(0, 0, self.width(), self.height())
        p.setBrush(bg)
        p.drawRoundedRect(bar_rect, radius, radius)

        # Handle
        handle_diam = self.height() - 4
        x_pos = 2 + (self.width() - handle_diam - 4) * self._position
        p.setBrush(handle_color)
        p.drawEllipse(QRectF(x_pos, 2, handle_diam, handle_diam))

        # Rahmen nur bei aktiv
        if self.isChecked():
            p.setPen(QPen(border_color, 2))
            p.setBrush(Qt.NoBrush)
            p.drawRoundedRect(bar_rect.adjusted(1, 1, -1, -1), radius, radius)

    # Toggle Animation (wird beim Umschalten aufgerufen)
    async def animate_async(self):
        if hasattr(self, "_animation_task") and self._animation_task and not self._animation_task.done():
            self._animation_task.cancel()
            try:
                await self._animation_task
            except asyncio.CancelledError:
                pass

        start = self._position
        end = 1.0 if self.isChecked() else 0.0
        steps = max(int(self.animation_duration / 0.016), 1)
        self._animation_task = asyncio.create_task(self._animate_steps(start, end, steps))

    async def _animate_steps(self, start, end, steps):
        for i in range(1, steps + 1):
            self._position = start + (end - start) * (i / steps)
            self.update()
            await asyncio.sleep(self.animation_duration / steps)
        self._position = end
        self.update()
