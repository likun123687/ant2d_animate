import math
from typing import Union

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
    QGraphicsLineItem, QGraphicsSceneHoverEvent
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPolygonF, QPainterPath
from PySide6.QtCore import Qt, QSize, QRectF, QPointF

from views.connect_arrow import ConnectArrow

RING_BORDER_WIDTH = 1
RING_RADIUS = 5
DRAG_POINT_BORDER_WIDTH = 0.2
DRAG_POINT_RADIUS = 0.5


class Ring(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        print("parent bone", parent)
        self.setFlags(QGraphicsItem.ItemIsMovable|QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        # self.__radius = radius

    def setPos(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())


class DragPoint(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setAcceptHoverEvents(True)
        # self.setFlags(QGraphicsItem.ItemIsSelectable)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # print("item change", value)
            pass
        return super().itemChange(change, value)

    def setPos(self, x, y) -> None:
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pass
        # print("hover enter", self)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        pass
        # print("hover leave", self)


class Arrow(QGraphicsPolygonItem):
    def __init__(self, polygon, parent=None):
        super().__init__(polygon, parent)
        self.setAcceptHoverEvents(True)
        self.setFlags(QGraphicsItem.ItemSendsGeometryChanges)


    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemRotationChange:
            #print("arrow angle change", value)
            angle = math.radians(value)
            x = math.cos(angle) * 5
            y = math.sin(angle) * 5
            #print("arrow now pos", x , y)

        return super().itemChange(change, value)

class Bone(Ring):
    def __init__(self, position, scene, parent:Arrow=None):
        super().__init__(QRectF(-RING_RADIUS, -RING_RADIUS, RING_RADIUS * 2, RING_RADIUS * 2), parent)
        self.setAcceptHoverEvents(True)

        pen = QPen(Qt.cyan)
        pen.setWidthF(0.1)
        # line = QGraphicsLineItem()
        # line.setPos(position.x(), position.y())
        # line.setLine(0, 0, 60, 0)
        # line.setPen(pen)
        # scene.addItem(line)
        #
        # line1 = QGraphicsLineItem()
        # line1.setPos(position.x(), position.y())
        # line1.setLine(0, 0, 0, 60)
        # line1.setPen(pen)
        # scene.addItem(line1)

        # 圆圈
        #self._ring = Ring(QRectF(-RING_RADIUS, -RING_RADIUS, RING_RADIUS * 2, RING_RADIUS * 2))
        if parent is not None:
            position = parent.mapFromScene(position)
        else:
            print("scene add item")
            scene.addItem(self)

        self.setPos(position.x(), position.y())

        # Define the pen (line)
        pen.setWidthF(RING_BORDER_WIDTH)
        self.setPen(pen)

        # rect.setPen(pen)
        # scene.addItem(self._ring)

        # 箭头
        p0 = QPointF(0, 0)
        p1 = QPointF(1, -1)
        p2 = QPointF(RING_RADIUS - RING_BORDER_WIDTH / 2, 0)
        p3 = QPointF(1, 1)
        arrow_polygon = QPolygonF([p0, p1, p2, p3])
        self._arrow = Arrow(arrow_polygon, self)
        self._arrow.setPos(0, 0)
        # arrow.setRotation(90)
        pen.setWidthF(0.1)
        pen.setColor(Qt.black)
        self._arrow.setPen(pen)

        #scene.addItem(self._arrow)

        # 拉伸点
        self._drag_point = DragPoint(
            QRectF(-DRAG_POINT_RADIUS / 2, -DRAG_POINT_RADIUS / 2, DRAG_POINT_RADIUS, DRAG_POINT_RADIUS), self._arrow)
        self._drag_point.setPos(RING_RADIUS - RING_BORDER_WIDTH / 2, 0)
        pen = QPen(Qt.red)
        pen.setWidthF(DRAG_POINT_BORDER_WIDTH)
        self._drag_point.setPen(pen)

        # 首尾的坐标什么时候会变
        # 1 移动
        # 2 旋转
        # 3 伸缩
        self._head_point_pos:Union[QPointF, None] = None
        self._tail_point_pos:Union[QPointF, None] = QPointF(0, 0)
        self._arrow_angle_to_scene = 0
        self._connect_arrow:Union[ConnectArrow, None] = None
        print("666666", self._connect_arrow)

        if parent is not None:
            print("ppppp", parent.parentItem())
            self._arrow_angle_to_scene = parent.parentItem().arrow_angle_to_scene

    def rotation_arrow(self, scene_angle, distance):
        self._arrow_angle_to_scene = scene_angle

        parent_bone = self.parent_bone()
        if parent_bone is not None:
            local_angle = scene_angle - parent_bone.arrow_angle_to_scene
        else:
            local_angle = scene_angle
        print("scene_angle", scene_angle, "local_angle", local_angle)
        self._arrow.setRotation(local_angle)

        # if distance <= RING_RADIUS - RING_BORDER_WIDTH / 2:
        #     x = math.cos(local_angle) * (RING_RADIUS - RING_BORDER_WIDTH / 2)
        #     y = math.sin(local_angle) * (RING_RADIUS - RING_BORDER_WIDTH / 2)
        #     self._tail_point_pos = QPointF(x, y)

    def move_drag_point(self, scene_pos: QPointF) -> None:
        """
        move drag point
        :param pos: drag point position
        """
        pos = self._drag_point.mapFromScene(scene_pos)
        self._drag_point.setPos(pos.x(), pos.y())
        self._tail_point_pos = self._arrow.mapFromScene(scene_pos)

    def stretch_arrow(self, distance):
        if self._arrow is not None:
            p0 = QPointF(0, 0)
            p1 = QPointF(1, -1)
            p2 = QPointF(distance, 0)
            p3 = QPointF(1, 1)

            if distance > RING_RADIUS * 2:
                p1 = QPointF(RING_RADIUS * 2, -(RING_RADIUS - RING_BORDER_WIDTH / 2))
                p3 = QPointF(RING_RADIUS * 2, RING_RADIUS - RING_BORDER_WIDTH / 2)

            arrow_polygon = QPolygonF([p0, p1, p2, p3])
            self._arrow.setPolygon(arrow_polygon)

    def hover_enter_process(self):
        brush = QBrush(Qt.gray)

        self.setBrush(brush)
        self.update()

        self._arrow.setBrush(brush)
        self._arrow.update()

    def hover_leave_process(self):
        self.clicked()

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hover_enter_process()
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.hover_leave_process()

    def clicked(self):
        # brush = self.brush()
        # if brush is None:
        #     brush = QBrush()

        brush = QBrush(Qt.yellow)

        self.setBrush(brush)
        self.update()

        self._arrow.setBrush(brush)
        self._arrow.update()

    def itemChange(self, change, value):
        parent_bone = self.parent_bone()
        if parent_bone is None:
            return super().itemChange(change, value)

        if change == QGraphicsItem.ItemPositionHasChanged:
            print("bone pos change", value)
            try:
                if self._connect_arrow is not None:
                    self._connect_arrow.update_line(parent_bone._tail_point_pos, value)
            except AttributeError:
                pass

        elif change == QGraphicsItem.ItemRotationChange:
            print("bone pos change", value)

        return super().itemChange(change, value)

    def parent_bone(self):
        parent_item = self.parentItem()
        if parent_item is None:
            return None
        else:
            return parent_item.parentItem()

    @property
    def arrow(self):
        return self._arrow

    @property
    def arrow_angle_to_scene(self):
        return self._arrow_angle_to_scene

    @property
    def connect_arrow(self):
        return self._connect_arrow
    @connect_arrow.setter
    def connect_arrow(self, value: ConnectArrow):
        print("set connect_arrow")
        self._connect_arrow = value