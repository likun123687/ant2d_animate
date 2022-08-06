from typing import List, Dict, Tuple
import math
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter, QFontMetrics
from PySide6.QtCore import Qt,QPoint, QRect

MINIMUM_INCR = 5
class SPRulerMetric:
    def __init__(self, ruler_scale, subdivide):
        self.ruler_scale = ruler_scale
        self.subdivide = subdivide

ruler_metric_general = SPRulerMetric(
    ( 1, 2, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000 ),
    ( 1, 5, 10, 50, 100 ))

ruler_metric_inches = SPRulerMetric(
  ( 1, 2, 4,  8, 16, 32,  64, 128, 256,  512, 1024, 2048, 4096, 8192, 16384, 32768 ),
  ( 1, 2,  4,  8,  16 ))

RULER_SIZE = 16

class RuleBar(QtWidgets.QWidget):
    def __init__(self, direction, view, parent = None):
        super().__init__(parent)
        self.__direction = direction
        self.__view = view
        self.__face_color = QColor(0xFF, 0xFF, 0xFF)
        self.__lower = self.upper = self.max_size = 0
        self.__last_pos = QPoint(0,0)

        font = self.font()
        font.setBold(False);
        font.setPixelSize(10);
        self.setFont(font);

    def set_range(self, lower, upper, max_size):
        self.__lower = lower
        self.__upper = upper
        self.__max_size = max_size

    def update_position(self, pos):
        self.__last_pos = pos
        super().update()

    def paintEvent(self, event):
        ruler_rect = self.rect()
        painter = QPainter(self)
        painter.fillRect(ruler_rect, self.__face_color)
        if self.__direction == Qt.Horizontal:
            painter.drawLine(ruler_rect.bottomLeft(),ruler_rect.bottomRight())
        else:
            painter.drawLine(ruler_rect.topRight(),ruler_rect.bottomRight());

        self.draw_ticker(painter)
        self.draw_pos(painter)
        painter.end()

    def draw_ticker(self, painter):
        i:int = 0
        width:int = 0
        height:int = 0
        length:int = 0
        ideal_length:int = 0
        lower:float = self.__lower
        upper:float = self.__upper
        increment:float = 0.0
        scale:int = 0
        start:float
        end:float
        cur:float
        digit_str:str = "\0\0"
        digit_height:int
        digit_offset:int
        text_size:int
        pos:int
        max_size:float = self.__max_size;
        ruler_metric:SPRulerMetric = ruler_metric_general
        allocation = self.rect()

        fm = QFontMetrics(self.font())
        digit_height = fm.height()
        digit_offset = 0
        if self.__direction == Qt.Horizontal:
            width = allocation.width()
            height = allocation.height()
        else:
            width = allocation.height()
            height = allocation.width()

        if upper == lower:
            return
        increment = width / (upper - lower)
        print("increment", increment)
        scale = math.ceil(max_size)
        text_size = len(str(scale)) * digit_height + 1
        print("text_size", text_size)

        scale = 0
        for item in ruler_metric.ruler_scale:
            if item * math.fabs(increment) > 2 * text_size:
                break
            scale += 1

        print("scale", scale)
        length = 0

        for i in range(len(ruler_metric.subdivide) - 1, -1, -1):
            subd_incr:float
            if scale == 1 and i == 1:
                subd_incr = 1.0
            else:
                subd_incr = ruler_metric.ruler_scale[scale] / ruler_metric.subdivide[i]
                print("subd_incr", i, subd_incr)

            if subd_incr * math.fabs(increment) <= MINIMUM_INCR:
                continue

            ideal_length = height / (i + 1) - 1
            length+=1
            if ideal_length > length:
                length = ideal_length

            if lower < upper:
                start = math.floor(lower/subd_incr) * subd_incr
                end = math.ceil(upper /subd_incr) *subd_incr
            else:
                start = math.floor(upper/subd_incr) * subd_incr
                end = math.ceil(lower /subd_incr) *subd_incr
            print("length", length, i, ruler_metric.subdivide[i])

            tick_index:int = 0
            cur = start
            while cur < end:
            #for cur in range(start, end, subd_incr) :
                pos = int(round(cur-lower) * increment + 1e-12)
                if self.__direction == Qt.Horizontal:
                    rt = QRect(pos,height-length,1,length)
                    print("pos", pos)
                    painter.drawLine(rt.topLeft(), rt.bottomLeft())
                else:
                    rt = QRect(height-length,pos,length,1);
                    painter.drawLine(rt.topLeft(), rt.topRight())

                label_spacing_px = math.fabs(increment*ruler_metric.ruler_scale[scale]/ruler_metric.subdivide[i])
                if (i == 0 and
                        (label_spacing_px > 6*digit_height or tick_index%2 == 0 or cur == 0) and
                        (label_spacing_px > 3*digit_height or tick_index%4 == 0 or cur == 0)):
                    if (math.fabs(int(cur)) >= 2000 and ((int(cur))/1000)*1000 == (int(cur))):
                        unit_str = str((int(cur))/1000) + "k";
                    else:
                        unit_str = str(int(cur))
                    if self.__direction == Qt.Horizontal:
                       w:int = fm.horizontalAdvance(unit_str)
                       painter.drawText(pos + 2,
                                         allocation.top(),
                                         w,
                                         RULER_SIZE,
                                         Qt.AlignLeft|Qt.AlignTop,unit_str)
                    else:
                        w:int = fm.horizontalAdvance(unit_str);
                        textRect = QRect(-w/2,-RULER_SIZE/2,w,RULER_SIZE)
                        painter.save()
                        painter.translate(4, pos + w/2+2)
                        painter.rotate(90);
                        painter.drawText(textRect,Qt.AlignRight,unit_str)
                        painter.restore()

                tick_index+=1
                if i == 0:
                    print("i=0 cur ", cur, subd_incr)
                cur += subd_incr

    def draw_pos(self, painter):
        x:int
        y:int
        width:int
        height:int
        bs_width:int
        bs_height:int
        allocation = self.rect()
        position:float
        lower = self.__lower
        upper = self.__upper
        if self.__direction == Qt.Horizontal:
            width = allocation.width()
            height = allocation.height()
            bs_width = height / 2 + 2
            bs_width != 1
            bs_height = bs_width / 2 +1
            position = lower + (upper - lower) * self.__last_pos.x()/width
        else:
            width = allocation.height()
            height = allocation.width()
            bs_height = width / 2 + 2
            bs_height != 1
            bs_width = bs_height / 2 +1
            position = lower + (upper - lower) * self.__last_pos.y()/height

        if (bs_width > 0 and bs_height > 0) :
            increment:float = 0.0
            if self.__direction == Qt.Horizontal:
                increment = width / (upper - lower)
                x = round((position - lower) * increment) + bs_width / 2 - 1
                y = (height + bs_height) / 2
                painter.drawLine(self.__last_pos.x(),0, self.__last_pos.x() , height)
            else:
                increment = height / (upper - lower)
                x = (width + bs_width) / 2 ;
                y = round((position - lower) * increment) + (bs_height) / 2 - 1
                painter.drawLine(0 , self.__last_pos.y() , width , self.__last_pos.y())


class CornerBox(QtWidgets.QWidget):
    def __init__(self,  parent = None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        painter.fillRect(rect,QColor(0xFF, 0xFF, 0xFF))
        painter.setPen(Qt.DashLine)
        painter.drawLine(rect.center().x(),rect.top(),rect.center().x(),rect.bottom())
        painter.drawLine(rect.left(),rect.center().y(),rect.right(),rect.center().y())
        painter.drawLine(rect.topRight(),rect.bottomRight());
        painter.drawLine(rect.bottomLeft(),rect.bottomRight());
