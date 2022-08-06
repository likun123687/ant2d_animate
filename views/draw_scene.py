from PySide6.QtWidgets import (
    QGraphicsScene
)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter
import math

class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_space = QSize(25, 25)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        #painter->fillRect(sceneRect(),Qt::white);
        #rect = self.sceneRect().toRect()
        rect = rect.toRect()
        c = QColor(Qt.darkCyan)
        p = QPen(c)
        p.setStyle(Qt.DashLine)
        p.setWidthF(0.2)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing,False)
        painter.fillRect(rect, Qt.white)

        left = math.floor(rect.left()/self.grid_space.width()) * self.grid_space.width()
        right = math.ceil(rect.right()/self.grid_space.width()) * self.grid_space.width()
        top = math.floor(rect.top()/self.grid_space.height()) * self.grid_space.height()
        bottom = math.ceil(rect.bottom()/self.grid_space.height()) * self.grid_space.height()

        for x in range(left, right, int(self.grid_space.width())):
            painter.drawLine(x, top,x, bottom)

        for y in range(top, bottom, int(self.grid_space.height())):
            painter.drawLine(left, y, right, y)

        p.setStyle(Qt.SolidLine)
        p.setColor(Qt.black);
        p.setWidthF(1.0)
        painter.setPen(p)
        #painter.drawLine(rect.right(),rect.top(),rect.right(),rect.bottom())
        #painter.drawLine(rect.left(),rect.bottom(),rect.right(),rect.bottom())
        #画xy轴
        painter.drawLine(left, 0, right, 0)
        painter.drawLine(0, top,0, bottom)

        painter.restore()
