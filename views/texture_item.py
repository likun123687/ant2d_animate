from PySide6.QtCore import QPointF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem


class Outline(QGraphicsRectItem):
    def __init__(self, parent: "TextureItem" = None):
        super().__init__(parent)
        parent_bound = parent.boundingRect()
        self.setRect(parent_bound.left(), parent_bound.top(), parent_bound.width(), parent_bound.height())

    def move_to_center(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        self.setTransformOriginPoint(offset)

        super().moveBy(x - offset.x(), y - offset.y())


class TextureItem(QGraphicsPixmapItem):
    def __init__(self, pos: QPointF, parent=None):
        super().__init__(parent)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)
        self.setPixmap(QPixmap('test_img.png'))
        self.move_to_center(pos.x(), pos.y())

        self._outline = Outline(self)

    def move_to_center(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        self.setTransformOriginPoint(offset)

        super().moveBy(x - offset.x(), y - offset.y())
