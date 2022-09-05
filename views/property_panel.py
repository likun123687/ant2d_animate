from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel
)
from PySide6.QtGui import QPalette, QColor


class PropertyPanel(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QGridLayout()

        label_1 = QLabel("1111", self)
        label_1.setStyleSheet("background-color: lightgreen")
        label_1.setGeometry(0, 0, 50, 10)

        label_2 = QLabel("2222", self)
        label_2.setStyleSheet("background-color: red")

        label_2.setGeometry(0, 20, 50, 10)

        canvas_checkbox = QtWidgets.QCheckBox("canvas", self)
        canvas_checkbox.setCheckState(Qt.Checked)
        canvas_checkbox.setGeometry(0, 40, 50, 15)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)
