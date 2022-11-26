from PySide6.QtCore import Qt, QPointF, QRectF, QSizeF
from PySide6.QtGui import QPen, QPolygonF, QBrush
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsPolygonItem


class RotateHandles(QGraphicsEllipseItem):
    def move_to_center(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())
        # self.setPos(x - offset.width() / 2, y - offset.height() / 2)

    def __init__(self, pos: QPointF, parent=None):
        super().__init__(QRectF(QPointF(-8, -8), QSizeF(8 * 2, 8 * 2)), parent)
        # self.setPos(pos)
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsScenePositionChanges)
        pen = QPen(Qt.red)
        pen.setWidthF(1.2)
        self.setPen(pen)

        self.move_to_center(pos.x(), pos.y())
        print(self.pos())

        p0 = QPointF(1 + 8 + 1.2 / 2 + 4, 0)
        p1 = QPointF(1 + 8 + 1.2 / 2, -4)
        p2 = QPointF(1 + 8 + 1.2 / 2, 4)

        polygon = QGraphicsPolygonItem(QPolygonF([p0, p1, p2]), self)
        pen.setWidthF(0.1)
        polygon.setPen(pen)
        brush = QBrush(Qt.red)
        polygon.setBrush(brush)
        self.setZValue(4)
        self.setRotation(45)
