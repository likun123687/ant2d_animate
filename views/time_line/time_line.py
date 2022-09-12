from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from views.time_line.common import LEFT_PANEL_WIDTH, TRACK_VIEW_HEIGHT, DIVISIONS_BAR_HEIGHT
from views.time_line.divisions_bar import DivisionsBar
from views.time_line.left_panel import LeftPanel
from views.time_line.track_view import TrackScene, TrackGraphicsView


class TimeLineView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._left_panel: LeftPanel = LeftPanel(self)

        self._scene: TrackScene = TrackScene(0, 0, 1000, 800)

        self._graphics_view: TrackGraphicsView = TrackGraphicsView(self._scene, self)
        self._graphics_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self._divisions_bar: DivisionsBar = DivisionsBar(self._graphics_view, self)
        self._graphics_view.divisions_bar = self._divisions_bar

        # track_tree_ctrl位置跟随
        self._graphics_view.track_tree_ctrl = self._left_panel.track_tree_ctrl

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._left_panel.resize(LEFT_PANEL_WIDTH, TRACK_VIEW_HEIGHT)

        self._divisions_bar.resize(self.size().width() - LEFT_PANEL_WIDTH, DIVISIONS_BAR_HEIGHT)
        self._divisions_bar.move(LEFT_PANEL_WIDTH, 0)

        self._graphics_view.resize(self.size().width() - LEFT_PANEL_WIDTH,
                                   TRACK_VIEW_HEIGHT - DIVISIONS_BAR_HEIGHT)
        self._graphics_view.move(LEFT_PANEL_WIDTH, DIVISIONS_BAR_HEIGHT)
