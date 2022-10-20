from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QListWidget, QPushButton, QHBoxLayout, QToolButton, QFrame
)
from PySide6.QtGui import QPalette, QColor

from views.Spoiler import Spoiler


class PropertyPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_property = QGridLayout()

        label_1 = QLabel("1111")
        label_1.setStyleSheet("background-color: lightgreen")
        common_property.addWidget(label_1, 0, 0)

        line_edit = QLineEdit()
        common_property.addWidget(line_edit, 0, 1)

        label_2 = QLabel("2222")
        label_2.setStyleSheet("background-color: lightgreen")
        line_edit2 = QLineEdit()

        common_property.addWidget(label_2, 1, 0)
        common_property.addWidget(line_edit2, 1, 1)

        self._more_property = QVBoxLayout()
        label_1 = QLabel("3333")
        label_1.setStyleSheet("background-color: lightgreen")
        self._more_property.addWidget(label_1)

        label_2 = QLabel("4444")
        label_2.setStyleSheet("background-color: lightgreen")
        line_edit2 = QLineEdit()

        label_3 = QLabel("4444")
        label_3.setStyleSheet("background-color: yellow")

        list_widget = QListWidget()
        list_widget.addItem("Item 1")
        list_widget.addItem("Item 2")

        self._more_property.addWidget(label_2)
        self._more_property.addWidget(line_edit2)
        self._more_property.addWidget(label_3)
        self._more_property.addWidget(list_widget)

        bottom_btn = QPushButton("click me")
        self._more_property.addWidget(bottom_btn)

        self._frame = QFrame()
        self._frame.setLayout(self._more_property)

        split_line = QHBoxLayout()

        self._toggle_btn = QToolButton()
        self._toggle_btn.setStyleSheet("QToolButton { border: none; }")
        self._toggle_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self._toggle_btn.setArrowType(QtCore.Qt.RightArrow)
        self._toggle_btn.setText("more")
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(False)

        self._toggle_btn.clicked.connect(self.btn_click)

        header_line = QFrame()
        header_line.setFrameShape(QtWidgets.QFrame.HLine)
        header_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        header_line.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        split_line.addWidget(self._toggle_btn)
        split_line.addWidget(header_line)

        main_layout = QVBoxLayout()
        main_layout.addLayout(common_property)
        main_layout.addLayout(split_line)
        main_layout.addWidget(self._frame)
        size_policy = self._frame.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self._frame.setSizePolicy(size_policy)

        self._frame.hide()
        # main_layout.addLayout(self._more_property)



        self.setLayout(main_layout)

        #
        # layout = QtWidgets.QGridLayout()
        #
        # label_1 = QLabel("1111", self)
        # label_1.setStyleSheet("background-color: lightgreen")
        #
        # label_2 = QLabel("2222", self)
        # label_2.setStyleSheet("background-color: red")
        #
        # label_2.setGeometry(0, 20, 50, 10)
        #
        # canvas_checkbox = QtWidgets.QCheckBox("canvas", self)
        # canvas_checkbox.setCheckState(Qt.Checked)
        # canvas_checkbox.setGeometry(0, 40, 50, 15)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)

    def btn_click(self, checked):
        arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
        self._toggle_btn.setArrowType(arrow_type)
        if checked:
            self._frame.show()
        else:
            self._frame.hide()
            
