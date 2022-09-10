from typing import Union

from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsItemGroup
)

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsPolygonItem, \
    QGraphicsLineItem, QGraphicsEllipseItem

from PySide6.QtCore import Qt, QSize, QRectF, QPointF
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter
from PySide6 import QtGui

import math
from views.bone import Bone


class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_space = QSize(25, 25)
        self._bone: Union[Bone, None] = None
        self._bone_start_point: Union[QPointF, None] = None

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        # painter->fillRect(sceneRect(),Qt::white);
        # rect = self.sceneRect().toRect()
        rect = rect.toRect()
        c = QColor(Qt.darkCyan)
        p = QPen(c)
        p.setStyle(Qt.DashLine)
        p.setWidthF(0.2)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing, False)
        painter.fillRect(rect, Qt.white)

        left = math.floor(rect.left() / self._grid_space.width()) * self._grid_space.width()
        right = math.ceil(rect.right() / self._grid_space.width()) * self._grid_space.width()
        top = math.floor(rect.top() / self._grid_space.height()) * self._grid_space.height()
        bottom = math.ceil(rect.bottom() / self._grid_space.height()) * self._grid_space.height()

        for x in range(left, right, int(self._grid_space.width())):
            painter.drawLine(x, top, x, bottom)

        for y in range(top, bottom, int(self._grid_space.height())):
            painter.drawLine(left, y, right, y)

        p.setStyle(Qt.SolidLine)
        p.setColor(Qt.black)
        p.setWidthF(1.0)
        painter.setPen(p)
        # painter.drawLine(rect.right(),rect.top(),rect.right(),rect.bottom())
        # painter.drawLine(rect.left(),rect.bottom(),rect.right(),rect.bottom())
        # 画xy轴
        painter.drawLine(left, 0, right, 0)
        painter.drawLine(0, top, 0, bottom)

        painter.restore()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.itemAt(event.scenePos(), QtGui.QTransform()):
                print("at item")
            else:
                self._bone_start_point = event.scenePos()
                self._bone = Bone(event.scenePos(), self)
                print("mouse press")



    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            print("mouse move")
            if self._bone_start_point is not None and self._bone is not None:
                start_pos = self._bone_start_point
                cur_pos = event.scenePos()
                angle = math.atan2((cur_pos.y()-start_pos.y()), (cur_pos.x()-start_pos.x()))*(180/math.pi)
                print("angle", angle)
                self._bone.rotation_arrow(angle)

                distance = math.sqrt(math.pow((cur_pos.x() - start_pos.x()), 2) + math.pow((cur_pos.y() - start_pos.y()), 2))
                if distance > 4.5:
                    self._bone.stretch_arrow(distance)
                    self._bone.move_drag_point(cur_pos)

                event.accept()
                return
        super().mouseMoveEvent(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton:
            self._bone_start_point = None
            self._bone = None
            event.accept()
            return
        event.ignore()
