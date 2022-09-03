import math

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QIcon, QBrush, Qt, QPalette, QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsView, QTreeWidget, QTreeWidgetItem, QGraphicsScene, QWidget, QGraphicsRectItem, \
    QGraphicsItemGroup, QGraphicsItem

from views.time_line_bak.common import DIVISIONS_WIDTH, LEFT_BAR_WIDTH, TOP_BAR_HEIGHT


class TimeLineScene(QGraphicsScene):
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
        scroll_bar_width = 0
        # graphics_views = self.views()
        # if len(graphics_views) > 0:
        #     graphics_view = graphics_views[0]
        #     scroll_bar_width = graphics_view.verticalScrollBar().width()

        for x in range(left, right, int(DIVISIONS_WIDTH)):
            painter.drawLine(x, top, x, bottom)
        painter.restore()


class TimeLineGraphicsView(QGraphicsView):
    sig_scroll = Signal(int, int)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.sig_scroll.emit(dx, dy)


class TimeLineView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = TimeLineScene(0, 0, 800, 600)
        self.__time_line_graphics_view = TimeLineGraphicsView(self.scene, self)
        self.__time_line_graphics_view.sig_scroll.connect(self.slot_scroll_content)

        self.rect1 = QGraphicsRectItem()
        self.rect2 = QGraphicsRectItem()
        self.rect1.setRect(0, 40, 100, 30)
        self.rect2.setRect(110, 40, 100, 30)
        self.group1 = QGraphicsItemGroup()
        self.group1.addToGroup(self.rect1)
        self.group1.addToGroup(self.rect2)
        self.group1.setFlags(QGraphicsItem.ItemIsSelectable)
        self.group1.setPos(0, 0)

        self.scene.addItem(self.group1)

    @Slot(int, int)
    def slot_scroll_content(self, dx, dy):
        print(dx, dy)
        self.group1.setPos(self.__time_line_graphics_view.mapToScene(0, 0))

