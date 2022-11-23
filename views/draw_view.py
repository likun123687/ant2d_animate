from typing import Union, Optional

from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QWheelEvent, QPainter
from PySide6.QtWidgets import (
    QGraphicsView
)

from views.rule_bar import RuleBar, CornerBox, RULER_SIZE


class DrawView(QGraphicsView):
    def __init__(self, scene, h_ruler=None, v_ruler=None, box=None):
        super().__init__(scene)
        self._h_ruler = h_ruler
        self._v_ruler = v_ruler
        self._box = box
        self.setAttribute(Qt.WA_DeleteOnClose)
        self._pan = False
        self._pan_start_x = 0
        self._pan_start_y = 0
        self.setMouseTracking(True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # self.viewport().installEventFilter(self)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)           #启用拖动

    def zoom_in(self):
        self.scale(1.2, 1.2)
        self.update_ruler()

    def zoom_out(self):
        self.scale(1 / 1.2, 1 / 1.2)
        self.update_ruler()

    @property
    def h_ruler(self) -> Union[RuleBar, None]:
        return self._h_ruler

    @h_ruler.setter
    def h_ruler(self, value: RuleBar):
        self._h_ruler = value

    @property
    def v_ruler(self) -> Union[RuleBar, None]:
        return self._v_ruler

    @v_ruler.setter
    def v_ruler(self, value: RuleBar):
        self._v_ruler = value

    @property
    def box(self) -> Optional[CornerBox]:
        return self._box

    @box.setter
    def box(self, value: CornerBox):
        self._box = value

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setViewportMargins(RULER_SIZE - 1, RULER_SIZE - 1, 0, 0)
        # self.setViewportMargins(300,0,0,0)
        self._h_ruler.resize(self.size().width() - RULER_SIZE - 1, RULER_SIZE)
        self._h_ruler.move(RULER_SIZE, 0)
        self._v_ruler.resize(RULER_SIZE, self.size().height() - RULER_SIZE - 1)
        self._v_ruler.move(0, RULER_SIZE)
        self._box.resize(RULER_SIZE, RULER_SIZE)
        self._box.move(0, 0)
        self.update_ruler()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.update_ruler()

    def update_ruler(self):
        if self.scene() is None:
            return

        view_box = self.rect()
        # offset = self.mapFromScene(self.scene().sceneRect().center())  # scene原点在中点了
        offset = self.mapFromScene(QPointF(0, 0))  # scene原点在中点了

        factor = 1 / self.transform().m11()
        lower_x = factor * (view_box.left() - offset.x())  # 计算出x轴最左边的scene坐标
        upper_x = factor * (view_box.right() - RULER_SIZE - offset.x())
        # upper_x = factor * (view_box.right() - offset.x())

        self._h_ruler.set_range(lower_x, upper_x, upper_x - lower_x)
        self._h_ruler.update()

        lower_y = factor * (view_box.top() - offset.y()) * 1
        upper_y = factor * (view_box.bottom() - RULER_SIZE - offset.y()) * 1
        # upper_y = factor * (view_box.bottom() - offset.y()) * 1
        self._v_ruler.set_range(lower_y, upper_y, upper_y - lower_y)
        self._v_ruler.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        cur_point = event.position()
        scene_pos = self.mapToScene(QPoint(cur_point.x(), cur_point.y()))

        view_width = self.viewport().width()
        view_height = self.viewport().height()

        h_scale = cur_point.x() / view_width
        v_scale = cur_point.y() / view_height

        wheel_delta_value = event.angleDelta().y()
        scale_factor = self.transform().m11()
        if (scale_factor < 0.05 and wheel_delta_value < 0) or (scale_factor > 50 and wheel_delta_value > 0):
            return

        if wheel_delta_value > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        view_point = self.transform().map(scene_pos)
        self.horizontalScrollBar().setValue(int(view_point.x() - view_width * h_scale))
        self.verticalScrollBar().setValue(int(view_point.y() - view_height * v_scale))
        self.update()
        super().wheelEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._pan = True
            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return

        super().mousePressEvent(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        # self.auto_adjust(event)
        if event.button() == Qt.RightButton:
            self._pan = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return

        super().mouseReleaseEvent(event)
        event.ignore()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._pan:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self._pan_start_x))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self._pan_start_y))
            self._pan_start_x = event.x()
            self._pan_start_y = event.y()
            event.accept()
            return

        event.ignore()
