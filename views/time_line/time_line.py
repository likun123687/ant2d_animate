from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from views.time_line.common import LEFT_PANEL_WIDTH, TRACK_VIEW_HEIGHT, DIVISIONS_BAR_HEIGHT
from views.time_line.divisions_bar import DivisionsBar
from views.time_line.left_panel import LeftPanel
from views.time_line.track_view import TrackScene, TrackGraphicsView


class TimeLineView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_panel = LeftPanel(self)

        self.scene = TrackScene(0, 0, 800, 600)

        self.graphics_view = TrackGraphicsView(self.scene, self)
        self.graphics_view.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.divisions_bar = DivisionsBar(self.graphics_view, self)
        self.graphics_view.divisions_bar = self.divisions_bar

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.left_panel.resize(LEFT_PANEL_WIDTH, TRACK_VIEW_HEIGHT)

        self.divisions_bar.resize(self.size().width() - LEFT_PANEL_WIDTH, DIVISIONS_BAR_HEIGHT)
        self.divisions_bar.move(LEFT_PANEL_WIDTH, 0)

        self.graphics_view.resize(self.size().width() - LEFT_PANEL_WIDTH,
                                  TRACK_VIEW_HEIGHT - DIVISIONS_BAR_HEIGHT)
        self.graphics_view.move(LEFT_PANEL_WIDTH, DIVISIONS_BAR_HEIGHT)
