from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, Qt, QPolygonF
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsPolygonItem

HANDLER_BORDER_WIDTH = 0.1
HANDLER_RADIUS = 0.2

class BoneHandle(QGraphicsEllipseItem):

    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setAcceptHoverEvents(True)
        # self.setFlags(QGraphicsItem.ItemIsSelectable)
        pen = QPen(Qt.red)
        pen.setWidthF(0.1)
        self.setPen(pen)

        self._horizontal_line = QGraphicsLineItem(self)
        self._horizontal_line.setLine(0, 0, 3, 0)
        pen.setWidthF(0.2)
        self._horizontal_line.setPen(pen)

        p0 = QPointF(3, -1)
        p1 = QPointF(6, 0)
        p2 = QPointF(3, 1)
        arrow_polygon = QPolygonF([p0, p1, p2])
        self._horizontal_arrow = QGraphicsPolygonItem(arrow_polygon, self)
        self._horizontal_arrow.setPos(0, 0)
        self._horizontal_arrow.setPen(pen)


        self._vertical_line = QGraphicsLineItem(self)
        self._vertical_line.setLine(0, 0, 0, 3)
        pen.setWidthF(0.2)
        self._vertical_line.setPen(pen)

        p0 = QPointF(-1, 3)
        p1 = QPointF(0, 6)
        p2 = QPointF(1, 3)
        arrow_polygon = QPolygonF([p0, p1, p2])
        self._vertical_arrow = QGraphicsPolygonItem(arrow_polygon, self)
        self._vertical_arrow.setPos(0, 0)
        self._vertical_arrow.setPen(pen)

        self._scale_bar_line = QGraphicsLineItem(self)
        self._scale_bar_line.setLine(0, 0, -6, -6)
        pen.setWidthF(0.2)
        self._scale_bar_line.setPen(pen)

        p0 = QPointF(-7, -6)
        p1 = QPointF(-6, -5)
        p2 = QPointF(-5, -6)
        p3 = QPointF(-6, -7)

        arrow_polygon = QPolygonF([p0, p1, p2, p3])
        self._scale_bar_arrow = QGraphicsPolygonItem(arrow_polygon, self)
        self._scale_bar_arrow.setPos(0, 0)
        self._scale_bar_arrow.setPen(pen)
