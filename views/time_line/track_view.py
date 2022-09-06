import math
from typing import Union

from PySide6.QtGui import QIcon, QBrush, Qt, QPalette, QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsView, QTreeWidget, QTreeWidgetItem, QGraphicsScene, QWidget

from views.time_line.common import SUB_DIVIDE_INCR, GRID_SPACE
from views.time_line.divisions_bar import DivisionsBar
from views.time_line.left_panel import TrackTreeCtrl


class TrackScene(QGraphicsScene):
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

        left = math.floor(rect.left() / GRID_SPACE.width()) * GRID_SPACE.width()
        right = math.ceil(rect.right() / GRID_SPACE.width()) * GRID_SPACE.width()
        top = math.floor(rect.top() / GRID_SPACE.height()) * GRID_SPACE.height()
        bottom = math.ceil(rect.bottom() / GRID_SPACE.height()) * GRID_SPACE.height()

        for x in range(left, right, int(GRID_SPACE.width())):
            if x == 0:
                continue
            painter.drawLine(x, top, x, bottom)

        for y in range(top, bottom, int(GRID_SPACE.height())):
            if y == 0:
                continue
            painter.drawLine(left, y, right, y)
        painter.restore()


class TrackGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._divisions_bar: Union[DivisionsBar, None] = None
        self._track_tree_ctrl: Union[TrackTreeCtrl, None] = None

    def update_ruler(self):
        if self.scene() is None:
            return

        view_box = self.rect()
        offset = self.mapFromScene(self.scene().sceneRect().topLeft())
        lower_x = view_box.left() - offset.x()
        upper_x = view_box.right() - offset.x()

        self._divisions_bar.set_range(lower_x, upper_x, upper_x - lower_x)
        self._divisions_bar.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # self.setViewportMargins(5, 0, 0, 0)

        self.update_ruler()

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.update_ruler()
        scene = self.scene()
        if scene is not None:
            scene.update()
        if self._track_tree_ctrl is not None:
            pos = self._track_tree_ctrl.pos()
            old_size = self._track_tree_ctrl.size()
            print(old_size.width(), old_size.height() + dy)
            self._track_tree_ctrl.resize(old_size.width(), old_size.height() - dy)
            self._track_tree_ctrl.move(pos.x(), pos.y() + dy)

    @property
    def track_tree_ctrl(self) -> Union[TrackTreeCtrl, None]:
        return self._track_tree_ctrl

    @track_tree_ctrl.setter
    def track_tree_ctrl(self, value: TrackTreeCtrl):
        self._track_tree_ctrl = value

    @property
    def divisions_bar(self) -> Union[DivisionsBar, None]:
        return self._divisions_bar

    @divisions_bar.setter
    def divisions_bar(self, value: DivisionsBar):
        self._divisions_bar = value
