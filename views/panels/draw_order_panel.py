from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush


class DrawOrderPanel(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItem("Item 1")
        self.addItem("Item 2")

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)
