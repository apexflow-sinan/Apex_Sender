#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مؤشر التحميل - Loading Indicator"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor

class LoadingIndicator(QWidget):
    """ويدجت مؤشر التحميل"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_animation)
        self._timer.start(30)
        self.setFixedSize(50, 50)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def _update_animation(self):
        self._angle = (self._angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.setBrush(QColor(0, 0, 0, 120))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)
        
        painter.setPen(QColor(255, 255, 255, 200))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        rect = self.rect().adjusted(10, 10, -10, -10)
        painter.drawArc(rect, self._angle * 16, 90 * 16)

    def show_indicator(self):
        if self.parentWidget():
            parent_rect = self.parentWidget().rect()
            self.move(
                parent_rect.center().x() - self.width() // 2,
                parent_rect.center().y() - self.height() // 2
            )
        self.show()
        self.raise_()

    def hide_indicator(self):
        self.hide()
