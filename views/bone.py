from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
    QGraphicsLineItem, QGraphicsSceneHoverEvent
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPolygonF
from PySide6.QtCore import Qt, QSize, QRectF, QPointF

RING_BORDER_WIDTH = 1
RING_RADIUS = 5
DRAG_POINT_BORDER_WIDTH = 0.2
DRAG_POINT_RADIUS = 0.5

class Ring(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        # self.__radius = radius

    def setPos(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())


class DragPoint(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            print("item change", value)
        return super().itemChange(change, value)

    def setPos(self, x, y) -> None:
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())


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
        self.setAcceptHoverEvents(True)
        pen = QPen(Qt.cyan)
        pen.setWidthF(0.1)
        # line = QGraphicsLineItem()
        # line.setPos(position.x(), position.y())
        # line.setLine(0, 0, 60, 0)
        # line.setPen(pen)
        # scene.addItem(line)
        #
        # line1 = QGraphicsLineItem()
        # line1.setPos(position.x(), position.y())
        # line1.setLine(0, 0, 0, 60)
        # line1.setPen(pen)
        # scene.addItem(line1)

        # 圆圈
        self._ring = Ring(QRectF(-RING_RADIUS, -RING_RADIUS, RING_RADIUS*2, RING_RADIUS*2))
        self._ring.setPos(position.x(), position.y())

        # Define the pen (line)
        pen.setWidthF(RING_BORDER_WIDTH)

        self._ring.setPen(pen)

        # rect.setPen(pen)

        scene.addItem(self._ring)

        # 箭头
        p0 = QPointF(0, 0)
        p1 = QPointF(1, -1)
        p2 = QPointF(RING_RADIUS-RING_BORDER_WIDTH/2, 0)
        p3 = QPointF(1, 1)
        arrow_polygon = QPolygonF([p0, p1, p2, p3])
        self._arrow = Arrow(arrow_polygon)
        self._arrow.setPos(position)
        # arrow.setRotation(90)
        pen.setWidthF(0.1)
        pen.setColor(Qt.black)
        self._arrow.setPen(pen)

        scene.addItem(self._arrow)
        # self.addToGroup(self.__circle)

        # 拉伸点
        self._drag_point = DragPoint(QRectF(-DRAG_POINT_RADIUS/2, -DRAG_POINT_RADIUS/2, DRAG_POINT_RADIUS, DRAG_POINT_RADIUS), self._arrow)
        self._drag_point.setPos(RING_RADIUS-RING_BORDER_WIDTH/2, 0)
        pen = QPen(Qt.red)
        pen.setWidthF(DRAG_POINT_BORDER_WIDTH)
        self._drag_point.setPen(pen)

    def hoverEnterEvent(self, event:QGraphicsSceneHoverEvent) -> None:
        print("hover enter", self)
    def hoverLeaveEvent(self, event:QGraphicsSceneHoverEvent) -> None:
        print("hover leave", self)

    def rotation_arrow(self, angle):
        if self._arrow is not None:
            self._arrow.setRotation(angle)

    def move_drag_point(self, scene_pos:QPointF)->None:
        """
        move drag point
        :param pos: drag point position
        """
        pos = self._drag_point.mapFromScene(scene_pos)
        self._drag_point.setPos(pos.x(), pos.y())


    def stretch_arrow(self, distance):
        if self._arrow is not None:
            p0 = QPointF(0, 0)
            p1 = QPointF(1, -1)
            p2 = QPointF(distance, 0)
            p3 = QPointF(1, 1)

            if distance > RING_RADIUS*2:
                p1 = QPointF(RING_RADIUS*2, -(RING_RADIUS - RING_BORDER_WIDTH/2))
                p3 = QPointF(RING_RADIUS*2, RING_RADIUS - RING_BORDER_WIDTH/2)

            arrow_polygon = QPolygonF([p0, p1, p2, p3])
            self._arrow.setPolygon(arrow_polygon)