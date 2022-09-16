import math

from PySide6.QtCore import QPointF


def rotate_point(point:QPointF,rotate_point:QPointF, angle):
    angle = math.radians(angle)
    x0 = (point.x() - rotate_point.x()) * math.cos(angle) - (point.y() - rotate_point.y()) * math.sin(angle) + rotate_point.x()
    y0 = (point.x() - rotate_point.x()) * math.sin(angle) + (point.y() - rotate_point.y()) * math.cos(angle) + rotate_point.y()
    return QPointF(x0, y0)

print(rotate_point(QPointF(5, 0), QPointF(0, 0), -90))
