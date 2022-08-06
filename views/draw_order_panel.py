from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush

class DrawOrderPanel(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        line_edit = QtWidgets.QLineEdit(self)
        line_edit.setGeometry(0, 0, 50, 10)
        list_widget = QListWidget(self)
        list_widget.addItem("Item 1")
        list_widget.addItem("Item 2")

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)

