import math

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen, Qt
from PySide6.QtWidgets import QGraphicsLineItem, QGraphicsItem


def rotate_point_by_angle(point: QPointF, rotate_point: QPointF, angle):
    angle = math.radians(angle)
    x0 = (point.x() - rotate_point.x()) * math.cos(angle) - (point.y() - rotate_point.y()) * math.sin(
        angle) + rotate_point.x()
    y0 = (point.x() - rotate_point.x()) * math.sin(angle) + (point.y() - rotate_point.y()) * math.cos(
        angle) + rotate_point.y()
    return QPointF(x0, y0)


class ConnectArrow(QGraphicsLineItem):
    def __init__(self, start_point: QPointF, end_point: QPointF, parent: QGraphicsItem):
        """
        :param start_point: 都是local pos
        :param end_point: 都是local pos
        :param parent:
        """
        super().__init__(parent)

        self._start_point = start_point
        self._end_point = end_point
        p1, p2, p3 = self.update_point(start_point, end_point)

        pen = QPen(Qt.GlobalColor.black)
        pen.setWidthF(0.2)
        self.setPen(pen)
        self.setLine(self._start_point.x(), self._start_point.y(), self._end_point.x(), self._end_point.y())

        self._up_line = QGraphicsLineItem(self)
        self._up_line.setLine(p1.x(), p1.y(), p3.x(), p3.y())
        self._up_line.setPen(pen)

        #
        self._down_line = QGraphicsLineItem(self)
        self._down_line.setLine(p2.x(), p2.y(), p3.x(), p3.y())
        self._down_line.setPen(pen)

    def update_point(self, start_point: QPointF, end_point: QPointF):
        self._start_point = start_point
        self._end_point = end_point

        parent = self.parentItem()
        if parent is None:
            raise Exception("parent not found")

        scene_start_point = parent.mapToScene(self._start_point)
        scene_end_point = parent.mapToScene(self._end_point)

        distance = math.sqrt(
            math.pow((scene_start_point.x() - scene_end_point.x()), 2) + math.pow(
                (scene_start_point.y() - scene_end_point.y()), 2))
        angle = math.atan2((scene_end_point.y() - scene_start_point.y()),
                           (scene_end_point.x() - scene_start_point.x())) * (180 / math.pi)

        new_scene_end_point = rotate_point_by_angle(scene_end_point, scene_start_point, -angle)

        p1 = QPointF(new_scene_end_point.x() - 10, new_scene_end_point.y() - 4)
        p1 = rotate_point_by_angle(p1, scene_start_point, angle)
        p1 = parent.mapFromScene(p1)

        p2 = QPointF(new_scene_end_point.x() - 10, new_scene_end_point.y() + 4)
        p2 = rotate_point_by_angle(p2, scene_start_point, angle)
        p2 = parent.mapFromScene(p2)

        p3 = QPointF(new_scene_end_point.x() - 6, new_scene_end_point.y())
        p3 = rotate_point_by_angle(p3, scene_start_point, angle)
        p3 = parent.mapFromScene(p3)

        return p1, p2, p3

    def update_line(self, start_point: QPointF, end_point: QPointF):
        p1, p2, p3 = self.update_point(start_point, end_point)
        self.setLine(self._start_point.x(), self._start_point.y(), self._end_point.x(), self._end_point.y())
        self._up_line.setLine(p1.x(), p1.y(), p3.x(), p3.y())
        self._down_line.setLine(p2.x(), p2.y(), p3.x(), p3.y())
