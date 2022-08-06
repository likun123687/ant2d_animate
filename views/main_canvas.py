from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush
from views.canvas_tab_item import CanvasTabItem
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
QGraphicsScene, QGraphicsView, QGraphicsRectItem,QStackedLayout
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen
import sys

class MainCanvas(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #tabs = QtWidgets.QTabWidget(self)
        self.setMovable(True)
        self.addTab(CanvasTabItem(), "111")
        #tabs.setCurrentIndex(1)
        #tabs.addTab(QLabel("bbbb"), "222")
