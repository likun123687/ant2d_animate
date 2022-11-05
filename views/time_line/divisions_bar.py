import math

from PySide6.QtCore import QPoint, QRect
from PySide6.QtGui import QColor, QPainter, QFontMetrics, QPen, Qt
from PySide6.QtWidgets import QWidget

from views.time_line.common import SUB_DIVIDE_INC, DIVISIONS_BAR_HEIGHT, TICK_HEIGHT


class DivisionsBar(QWidget):
    def __init__(self, view, parent=None):
        super().__init__(parent)
        self._view = view
        self._face_color = QColor(0xFF, 0xFF, 0xFF)
        self._lower = self._upper = self._max_size = 0
        self._last_pos = QPoint(0, 0)

        font = self.font()
        font.setBold(False)
        font.setPixelSize(10)
        self.setFont(font)

    def set_range(self, lower, upper, max_size):
        self._lower = lower
        self._upper = upper
        self._max_size = max_size

    def update_position(self, pos):
        self._last_pos = pos
        super().update()

    def paintEvent(self, event):
        ruler_rect = self.rect()
        painter = QPainter(self)
        p = QPen()
        p.setStyle(Qt.GlobalColor.SolidLine)
        p.setWidthF(1)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.fillRect(ruler_rect, self._face_color)
        painter.drawLine(ruler_rect.bottomLeft(), ruler_rect.bottomRight())
        self.draw_ticker(painter)
        painter.end()

    def draw_ticker(self, painter):
        lower: float = self._lower
        upper: float = self._upper
        start: float
        end: float
        cur: float
        digit_height: int
        digit_offset: int
        text_size: int
        pos: int
        max_size: float = self._max_size
        allocation = self.rect()

        fm = QFontMetrics(self.font())
        digit_height = fm.height()
        width = allocation.width()
        height = allocation.height()
        if upper == lower:
            return

        start = math.floor(lower / SUB_DIVIDE_INC) * SUB_DIVIDE_INC
        end = math.ceil(upper / SUB_DIVIDE_INC) * SUB_DIVIDE_INC
        # print("start end", start, end)
        for cur in range(start, end, SUB_DIVIDE_INC):
            if cur == 0:
                continue
            pos = self._view.mapFromScene(cur, 0).x() + 1
            rt = QRect(pos, DIVISIONS_BAR_HEIGHT - TICK_HEIGHT, 1, TICK_HEIGHT)
            painter.drawLine(rt.topLeft(), rt.bottomLeft())

            unit_str = str(int(cur / SUB_DIVIDE_INC) - 1)
            w = fm.horizontalAdvance(unit_str)
            painter.drawText(pos - 2,
                             allocation.top() + 25,
                             w,
                             DIVISIONS_BAR_HEIGHT,
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, unit_str)
