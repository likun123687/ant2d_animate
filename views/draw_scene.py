import math
from typing import Optional

from PySide6.QtCore import QByteArray, QIODevice, QDataStream
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPen, QPainter, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent

from controllers.draw_scene_controller import DrawSceneController
from views.texture_item import TextureItem


class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_space = QSize(25, 25)  # 背景方格大小
        self._controller: Optional[DrawSceneController] = None

    def drawBackground(self, painter, rect):
        """
        draw background grid
        :param painter:
        :param rect:
        :return:
        """
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
        self._controller.mouse_press(event)
        event.ignore()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self._controller.mouse_move(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._controller.mouse_release(event)
        event.ignore()

    def auto_adjust(self):
        """
        自动调整画布大小
        """
        old_rect = self.sceneRect()
        top = old_rect.top()
        left = old_rect.left()
        bottom = old_rect.bottom()
        right = old_rect.right()

        items_bounding_rect = self.itemsBoundingRect()
        bounding_rect_top = items_bounding_rect.top()
        bounding_rect_left = items_bounding_rect.left()
        bounding_rect_bottom = items_bounding_rect.bottom()
        bounding_rect_right = items_bounding_rect.right()

        if bounding_rect_left - 200 < left:
            old_rect.setLeft(bounding_rect_left - 200)

        if bounding_rect_right + 200 > right:
            old_rect.setRight(bounding_rect_right + 200)

        if bounding_rect_top - 200 < top:
            old_rect.setTop(bounding_rect_top - 200)

        if bounding_rect_bottom + 200 > bottom:
            old_rect.setBottom(bounding_rect_bottom + 200)

        self.setSceneRect(old_rect)

    def dragEnterEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            item_data: QByteArray = event.mimeData().data("application/x-slot_data")
            data_stream = QDataStream(item_data, QIODevice.ReadOnly)
            pixmap = QPixmap()
            data_stream >> pixmap

            text_img = TextureItem(event.scenePos(), pixmap)
            self.addItem(text_img)

            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        self._controller = value
