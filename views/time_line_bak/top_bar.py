import math
from typing import Union

import PySide6
from PySide6.QtGui import Qt, QPen, QColor, QPainter
from PySide6.QtWidgets import QWidget, QGraphicsView, QLabel, QGraphicsScene

from views.time_line_bak.common import DIVISIONS_WIDTH, LEFT_BAR_WIDTH, TOP_BAR_HEIGHT


class TopBarLeft(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        label_1 = QLabel("1111", self)
        label_1.setStyleSheet("background-color: yellow")
        label_1.setGeometry(0, 0, 50, 10)

        label_2 = QLabel("222", self)
        label_2.setStyleSheet("background-color: blue")
        label_2.setGeometry(50, 0, 50, 10)

        label_3 = QLabel("333", self)
        label_3.setStyleSheet("background-color: gray")
        label_3.setGeometry(0, 10, 50, 10)


class DivisionsScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        rect = rect.toRect()
        c = QColor(Qt.black)
        p = QPen(c)
        p.setStyle(Qt.SolidLine)
        p.setWidthF(1)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing, False)
        painter.fillRect(rect, Qt.white)

        left = math.floor(rect.left() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        right = math.ceil(rect.right() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        top = math.floor(rect.top() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        bottom = math.ceil(rect.bottom() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        print("aaa", left, right)

        for x in range(left, right, int(DIVISIONS_WIDTH)):
            painter.drawLine(x, top + 50, x, bottom)
        painter.restore()


class AnimationDivisions(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)


class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__top_bar_left = TopBarLeft(self)
        self.scene = DivisionsScene(0, 0, 600, TOP_BAR_HEIGHT-20)
        self.__animation_divisions = AnimationDivisions(self.scene, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.__top_bar_left.resize(LEFT_BAR_WIDTH, TOP_BAR_HEIGHT)
        self.__animation_divisions.resize(self.size().width() - LEFT_BAR_WIDTH, TOP_BAR_HEIGHT)
        self.__animation_divisions.move(LEFT_BAR_WIDTH, 0)
