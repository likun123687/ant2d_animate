from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem


class ConnectArrow(QGraphicsItemGroup):
    def __init__(self, start_point:QPointF, end_point:QPointF, parent=None):
        super().__init__(parent)
        self._start_point = start_point
        self._end_point = end_point

        self._main_line = QGraphicsLineItem(self)
        self._main_line.setLine(start_point.x(), start_point.y(), end_point.x(), end_point.y())