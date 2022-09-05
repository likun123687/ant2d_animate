from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
    QGraphicsLineItem
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPolygonF
from PySide6.QtCore import Qt, QSize, QRectF, QPointF


class Ring(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        # self.__radius = radius


class DragPoint(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            print("item change", value)
        return super().itemChange(change, value)


'''
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)
        r = self.rect()
        r1 = QRectF(r)
        r.setSize(QSize(r.width()-2, r.height()-2))
        r.translate(1, 1)

        r1.setSize(QSize(r1.width()+2, r1.height()+2))
        r1.translate(-1, -1)

        p = painter.pen()
        p.setColor(Qt.black)
        p.setStyle(Qt.SolidLine)
        p.setWidthF(0.1)
        painter.setPen(p)

        painter.drawEllipse(r)
        painter.drawEllipse(r1)
'''


class Arrow(QGraphicsPolygonItem):
    def __init__(self, polygon, parent=None):
        super().__init__(polygon, parent)


class Bone(QGraphicsItemGroup):
    def __init__(self, position, scene, parent=None):
        super().__init__(parent)

        # 圆圈
        self.__ring = Ring(QRectF(0, 0, 10, 10))
        self.__ring.setPos(position.x() - 5, position.y() - 5)

        # Define the pen (line)
        pen = QPen(Qt.cyan)
        pen.setWidthF(2)
        self.__ring.setPen(pen)

        # rect.setPen(pen)

        scene.addItem(self.__ring)

        # 箭头
        p0 = QPointF(0, 0)
        p1 = QPointF(2, -2)
        p2 = QPointF(5, 0)
        p3 = QPointF(2, 2)
        arrow_polygon = QPolygonF([p0, p1, p2, p3])
        arrow = Arrow(arrow_polygon)
        arrow.setPos(position)
        arrow.setRotation(30)
        pen.setWidthF(0.2)
        pen.setColor(Qt.black)
        arrow.setPen(pen)

        scene.addItem(arrow)
        # self.addToGroup(self.__circle)

        # 拉伸点
        self.__drag_point = DragPoint(QRectF(5, -0.25, 0.5, 0.5), arrow)
        pen = QPen(Qt.red)
        pen.setWidthF(0.2)
        self.__drag_point.setPen(pen)
        print(self.__drag_point.pos(), self.__drag_point.scenePos())
