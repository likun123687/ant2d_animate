from views.rule_bar import RuleBar, CornerBox, RULER_SIZE
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QWheelEvent, QMouseEvent

from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QStackedLayout
)


class DrawView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.__h_ruler = RuleBar(Qt.Horizontal, self, self)
        self.__v_ruler = RuleBar(Qt.Vertical, self, self)
        self.__box = CornerBox(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.__pan = False
        self.__pan_start_x = 0
        self.__pan_start_y = 0
        # self.viewport().installEventFilter(self)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)           #启用拖动

    def zoom_in(self):
        self.scale(1.2, 1.2)
        self.update_ruler()

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)
        self.update_ruler()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.__pan:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self.__pan_start_x))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self.__pan_start_y))
            self.__pan_start_x = event.x()
            self.__pan_start_y = event.y()
            event.accept()

        event.ignore()

        # ps = self.mapToScene(event.pos())
        self.__h_ruler.update_position(event.pos())
        self.__v_ruler.update_position(event.pos())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setViewportMargins(RULER_SIZE - 1, RULER_SIZE - 1, 0, 0)
        # self.setViewportMargins(300,0,0,0)
        self.__h_ruler.resize(self.size().width() - RULER_SIZE - 1, RULER_SIZE)
        self.__h_ruler.move(RULER_SIZE, 0)
        self.__v_ruler.resize(RULER_SIZE, self.size().height() - RULER_SIZE - 1)
        self.__v_ruler.move(0, RULER_SIZE)
        self.__box.resize(RULER_SIZE, RULER_SIZE)
        self.__box.move(0, 0)
        self.update_ruler()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.update_ruler()

    def update_ruler(self):
        if self.scene() is None:
            return

        view_box = self.rect()
        offset = self.mapFromScene(self.scene().sceneRect().center())  # scene原点在中点了
        factor = 1 / self.transform().m11()
        lower_x = factor * (view_box.left() - offset.x())  # 计算出x轴最左边的scene坐标
        upper_x = factor * (view_box.right() - RULER_SIZE - offset.x())
        self.__h_ruler.set_range(lower_x, upper_x, upper_x - lower_x)
        self.__h_ruler.update()

        lower_y = factor * (view_box.top() - offset.y()) * 1
        upper_y = factor * (view_box.bottom() - RULER_SIZE - offset.y()) * 1
        self.__v_ruler.set_range(lower_y, upper_y, upper_y - lower_y)
        self.__v_ruler.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        curPoint = event.position()
        scenePos = self.mapToScene(QPoint(curPoint.x(), curPoint.y()))

        viewWidth = self.viewport().width()
        viewHeight = self.viewport().height()

        hScale = curPoint.x() / viewWidth
        vScale = curPoint.y() / viewHeight

        wheelDeltaValue = event.angleDelta().y()
        scaleFactor = self.transform().m11()
        if (scaleFactor < 0.05 and wheelDeltaValue < 0) or (scaleFactor > 50 and wheelDeltaValue > 0):
            return

        if wheelDeltaValue > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        viewPoint = self.transform().map(scenePos)
        self.horizontalScrollBar().setValue(int(viewPoint.x() - viewWidth * hScale))
        self.verticalScrollBar().setValue(int(viewPoint.y() - viewHeight * vScale))
        self.update()
        super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.__pan = True
            self.__pan_start_x = event.x()
            self.__pan_start_y = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return

        super().mousePressEvent(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.__pan = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)
        event.ignore()
