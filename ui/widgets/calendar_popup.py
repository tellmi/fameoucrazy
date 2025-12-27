# ui/witgets/calendar_popup.py
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, QPoint, QDate
from PySide6.QtWidgets import QWidget, QCalendarWidget, QVBoxLayout, QDateEdit

class CalendarPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup)
        self.setFocusPolicy(Qt.StrongFocus)

        # Calendar Widget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self._on_date_selected)
        self._target_edit = None

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.calendar)

    def show_for(self, qdate_edit: QDateEdit):
        self._target_edit = qdate_edit

        date = qdate_edit.date()
        if not date.isValid() or date.year() == 1900:
            date = QDate.currentDate()
        self.calendar.setSelectedDate(date)

        global_pos = qdate_edit.mapToGlobal(QPoint(0, qdate_edit.height()))
        self._adjust_position(global_pos)

        self.show()
        self.raise_()
        self.activateWindow()

    def _adjust_position(self, pos: QPoint):
        self.adjustSize()
        screen = QGuiApplication.screenAt(pos)
        if screen is None:
            screen = QGuiApplication.primaryScreen()
        screen_rect = screen.availableGeometry()

        popup_size = self.size()

        x = max(screen_rect.left(), min(pos.x(), screen_rect.right() - popup_size.width()))

        space_below = screen_rect.bottom() - pos.y()
        space_above = pos.y() - screen_rect.top()
        if space_below >= popup_size.height():
            y = pos.y()
        elif space_above >= popup_size.height():
            y = pos.y() - popup_size.height() - self._target_edit.height()
        else:
            y = max(screen_rect.top(), screen_rect.bottom() - popup_size.height())

        self.move(x, y)

    def _on_date_selected(self, date):
        if self._target_edit:
            self._target_edit.setDate(date)
        self.close()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.underMouse():
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)