
from views.rule_bar import RuleBar, CornerBox, RULER_SIZE
from PySide6.QtCore import Qt,QPoint
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QWheelEvent 

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
        self.__hruler = RuleBar(Qt.Horizontal, self, self)
        self.__vruler = RuleBar(Qt.Vertical, self, self)
        self.__box =  CornerBox(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setDragMode(QGraphicsView.ScrollHandDrag)           #启用拖动

    def zoom_in(self):
        self.scale(1.2, 1.2)
        self.update_ruler()

    def zoom_out(self):
        self.scale(1/1.2, 1/1.2)
        self.update_ruler()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        ps = self.mapToScene(event.pos())
        self.__hruler.update_position(event.pos())
        self.__vruler.update_position(event.pos())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setViewportMargins(RULER_SIZE-1,RULER_SIZE-1,0,0)
        #self.setViewportMargins(300,0,0,0)
        self.__hruler.resize(self.size().width() - RULER_SIZE - 1, RULER_SIZE)
        self.__hruler.move(RULER_SIZE,0)
        self.__vruler.resize(RULER_SIZE,self.size().height() - RULER_SIZE - 1)
        self.__vruler.move(0, RULER_SIZE)
        self.__box.resize(RULER_SIZE, RULER_SIZE)
        self.__box.move(0, 0)
        self.update_ruler();

    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        self.update_ruler()

    def update_ruler(self):
        if self.scene() == None:
            return

        viewbox = self.rect()
        offset = self.mapFromScene(self.scene().sceneRect().center()) #scene原点在中点了
        print("offset==", viewbox, self.scene().sceneRect().topLeft(), offset)
        factor = 1 / self.transform().m11()
        lower_x = factor * ( viewbox.left()  - offset.x() ) #计算出x轴最左边的scene坐标
        upper_x = factor * ( viewbox.right() - RULER_SIZE - offset.x())
        self.__hruler.set_range(lower_x,upper_x,upper_x - lower_x )
        print("set_range===", lower_x,upper_x,upper_x - lower_x )
        self.__hruler.update()

        lower_y = factor * ( viewbox.top() - offset.y()) * 1
        upper_y = factor * ( viewbox.bottom() - RULER_SIZE - offset.y() ) * 1
        self.__vruler.set_range(lower_y,upper_y,upper_y - lower_y )
        self.__vruler.update()

    def wheelEvent(self, event: QWheelEvent) -> None:
        curPoint = event.position()
        scenePos = self.mapToScene(QPoint(curPoint.x(), curPoint.y()))
    
        viewWidth = self.viewport().width()
        viewHeight = self.viewport().height()
    
        hScale = curPoint.x() / viewWidth
        vScale = curPoint.y() / viewHeight
    
        wheelDeltaValue = event.angleDelta().y()
        scaleFactor = self.transform().m11()
        if (scaleFactor < 0.05 and wheelDeltaValue<0) or (scaleFactor>50 and wheelDeltaValue>0):
            return

        if wheelDeltaValue > 0:
            self.zoom_in()
        else:
            self.zoom_out()

        viewPoint = self.transform().map(scenePos)
        self.horizontalScrollBar().setValue(int(viewPoint.x() - viewWidth * hScale ))
        self.verticalScrollBar().setValue(int(viewPoint.y() - viewHeight * vScale ))
        self.update()
        super().wheelEvent(event)


