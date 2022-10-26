from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtWidgets import (
    QLabel,
    QGraphicsRectItem, QGraphicsLineItem, QWidget, QHBoxLayout
)

from views.draw_scene import DrawScene
from views.draw_view import DrawView
from views.rule_bar import RuleBar, CornerBox


class CanvasTabItem(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Defining a scene rect of 400x200, with its origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = DrawScene(-400, -200, 800, 400)
        # self.scene = QGraphicsScene(0, 0, 800, 400)
        # self.scene = QGraphicsScene()

        # Draw a rectangle item, setting the dimensions.
        rect = QGraphicsRectItem(0, 0, 100, 100)

        # Set the origin (position) of the rectangle in the scene.
        rect.setPos(0, 0)

        # Define the brush (fill).
        brush = QBrush(Qt.red)
        rect.setBrush(brush)

        # Define the pen (line)
        # pen = QPen(Qt.cyan)
        # pen.setWidth(10)
        # rect.setPen(pen)

        line = QGraphicsLineItem()
        line.setLine(0, 0, 200, 0)

        line1 = QGraphicsLineItem()
        line1.setLine(-100, -100, 0, 0)

        self.scene.addItem(rect)
        self.scene.addItem(line)
        self.scene.addItem(line1)

        view = DrawView(self.scene)

        # h_ruler = RuleBar(Qt.Horizontal, view)
        # v_ruler = RuleBar(Qt.Vertical, view)
        # box = CornerBox(view)
        view.h_ruler = RuleBar(Qt.Horizontal, view)
        assert view.h_ruler is not None

        view.v_ruler = RuleBar(Qt.Vertical, view)
        assert view.v_ruler is not None

        view.box = CornerBox(view)
        assert view.box is not None

        # main_window.view = view
        self._stack_layout = QtWidgets.QStackedLayout()
        self._stack_layout.addWidget(view)
        self.setLayout(self._stack_layout)
        # self.setStyleSheet("background-color: black")

        # 切换armature和animation
        switch_bar = QWidget(self)
        switch_bar.setGeometry(-20, 20, 200, 20)
        switch_bar.setStyleSheet("background-color: yellow")

        armature_label = QLabel("armature", switch_bar)
        armature_label.setStyleSheet("background-color: lightgreen")

        animation_label = QLabel("animation", switch_bar)
        animation_label.setStyleSheet("background-color: blue")

        layout = QHBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(armature_label)
        layout.addWidget(animation_label)

        switch_bar.setLayout(layout)
        switch_bar.raise_()

        # 右上角工具条
        self.right_tool_bar = QLabel("tool bar", self)
        self.right_tool_bar.setGeometry(self.width() - 50, 20, 50, 10)
        self.right_tool_bar.setStyleSheet("background-color: yellow")

        # 左下角工具栏
        self.left_tool_bar = QLabel("tool bar", self)
        self.left_tool_bar.setGeometry(0, self.height() - 10, 50, 10)
        self.left_tool_bar.setStyleSheet("background-color: yellow")

        # 底部中间工具
        self.bottom_center_bar = QtWidgets.QWidget(self)
        self.bottom_center_bar.setGeometry(self.width() / 2 - 200 / 2, self.height() - 50, 200, 50)
        # self.bottom_center_bar.setGeometry(20,20, 200, 50)
        self.bottom_center_bar.setStyleSheet("background-color: blue")

    def resizeEvent(self, event):
        print("canvas tab item view resize")
        super().resizeEvent(event)
        self.right_tool_bar.setGeometry(self.width() - 50, 20, 50, 10)
        self.left_tool_bar.setGeometry(0, self.height() - 10, 50, 10)
        self.bottom_center_bar.setGeometry(self.width() / 2 - 200 / 2, self.height() - 50, 200, 50)
