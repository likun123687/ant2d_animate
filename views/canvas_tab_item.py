from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QGraphicsScene, QGraphicsView, QGraphicsRectItem,QStackedLayout,QGraphicsLineItem
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen
import sys
from views.draw_view import DrawView
from views.draw_scene import DrawScene

class CanvasTabItem(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = DrawScene(-400, -200, 800, 400)
        #self.scene = QGraphicsScene(0, 0, 800, 400)
        #self.scene = QGraphicsScene()

        # Draw a rectangle item, setting the dimensions.
        rect = QGraphicsRectItem(0, 0, 100, 100)

        # Set the origin (position) of the rectangle in the scene.
        rect.setPos(0, 0)

        # Define the brush (fill).
        brush = QBrush(Qt.red)
        rect.setBrush(brush)

        # Define the pen (line)
        #pen = QPen(Qt.cyan)
        #pen.setWidth(10)
        #rect.setPen(pen)


        line = QGraphicsLineItem()
        line.setLine(0, 0, 200, 0)

        line1 = QGraphicsLineItem()
        line1.setLine(-100, -100, 0, 0)

        self.scene.addItem(rect)
        self.scene.addItem(line)
        self.scene.addItem(line1)

        view = DrawView(self.scene)
        #main_window.view = view
        self.stacklayout = QtWidgets.QStackedLayout()
        self.stacklayout.addWidget(view)
        self.setLayout(self.stacklayout)
        #self.setStyleSheet("background-color: black")

        #切换armature和animation
        armature_label = QLabel("armature", self)
        armature_label.setGeometry(0, 20, 50, 10)
        armature_label.setStyleSheet("background-color: lightgreen")

        animation_label = QLabel("animation", self)
        animation_label.setGeometry(60, 20, 50, 10)
        animation_label.setStyleSheet("background-color: yellow")

        #右上角工具条
        self.right_tool_bar = QLabel("tool bar", self)
        self.right_tool_bar.setGeometry(self.width()-50, 20, 50, 10)
        self.right_tool_bar.setStyleSheet("background-color: yellow")

        #左下角工具栏
        self.left_tool_bar = QLabel("tool bar", self)
        self.left_tool_bar.setGeometry(0, self.height() - 10, 50, 10)
        self.left_tool_bar.setStyleSheet("background-color: yellow")

        #底部中间工具
        self.bottom_center_bar = QtWidgets.QWidget(self) 
        self.bottom_center_bar.setGeometry(self.width()/2 - 200/2, self.height() - 50, 200, 50)
        #self.bottom_center_bar.setGeometry(20,20, 200, 50)
        self.bottom_center_bar.setStyleSheet("background-color: blue")

    def resizeEvent(self, event):
        print("canvas tab item view resize")
        super().resizeEvent(event)
        self.right_tool_bar.setGeometry(self.width()-50, 20, 50, 10)
        self.left_tool_bar.setGeometry(0, self.height() - 10, 50, 10)
        self.bottom_center_bar.setGeometry(self.width()/2 - 200/2, self.height() - 50, 200, 50)
