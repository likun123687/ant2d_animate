import copy
from typing import Union, Optional

from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QBrush, QPen, QPolygonF
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsEllipseItem,
    QGraphicsPolygonItem,
    QGraphicsSceneHoverEvent
)

from common.signal_bus import SIGNAL_BUS
from views.bone_handle import BoneHandle
from views.connect_arrow import ConnectArrow
from views.property import VisualProperty
from views.texture_item import TextureItem

RING_BORDER_WIDTH = 1
RING_RADIUS = 5
DRAG_POINT_BORDER_WIDTH = 0.2
DRAG_POINT_RADIUS = 0.5


class Ring(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges)
        brush = QBrush(Qt.yellow)
        self.setBrush(brush)
        # self.setAcceptHoverEvents(True)
        # self.__radius = radius

    def move_center_to(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        super().moveBy(x - offset.x(), y - offset.y())


class DragPoint(QGraphicsEllipseItem):
    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        # self.setAcceptHoverEvents(True)
        # self.setFlags(QGraphicsItem.ItemIsSelectable)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # print("item change", value)
            pass
        return super().itemChange(change, value)

    def move_center_to(self, x, y) -> None:
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
        brush = QBrush(Qt.yellow)
        self.setBrush(brush)
        self.setFlags(QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsScenePositionChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemRotationChange:
            bone = self.parentItem()
            if bone:
                SIGNAL_BUS.signal_items_property_changed_from_scene.emit(bone)

        return super().itemChange(change, value)


class Bone(Ring):
    bone_count: int = 0

    def __init__(self, position, scene: 'DrawScene', parent: Arrow = None):
        super().__init__(QRectF(-RING_RADIUS, -RING_RADIUS, RING_RADIUS * 2, RING_RADIUS * 2), parent)
        # self.setAcceptHoverEvents(True)
        self._scene = scene
        pen = QPen(Qt.cyan)
        pen.setWidthF(0.1)

        # 圆圈
        # self._ring = Ring(QRectF(-RING_RADIUS, -RING_RADIUS, RING_RADIUS * 2, RING_RADIUS * 2))
        if parent is not None:
            position = parent.mapFromScene(position)
        else:
            print("scene add item")
            scene.addItem(self)

        self.move_center_to(position.x(), position.y())

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

        # scene.addItem(self._arrow)

        # 拉伸点
        self._drag_point = DragPoint(
            QRectF(-DRAG_POINT_RADIUS / 2, -DRAG_POINT_RADIUS / 2, DRAG_POINT_RADIUS, DRAG_POINT_RADIUS), self._arrow)
        self._drag_point.move_center_to(RING_RADIUS - RING_BORDER_WIDTH / 2, 0)
        pen = QPen(Qt.red)
        pen.setWidthF(DRAG_POINT_BORDER_WIDTH)
        self._drag_point.setPen(pen)

        # 首尾的坐标什么时候会变
        # 1 移动
        # 2 旋转
        # 3 伸缩
        self._head_point_pos: Union[QPointF, None] = None
        self._tail_point_pos: Optional[QPointF] = QPointF(0, 0)
        self._arrow_angle_to_scene = 0
        self._connect_arrow: Union[ConnectArrow, None] = None
        self._handle: Union[BoneHandle, None] = None
        self._is_selected: bool = False  # 是否选中
        self._texture_item: Optional[TextureItem] = None
        self._scene_width_scale: float = 1
        self._scene_height_scale: float = 1
        self._visual_property: Optional[VisualProperty] = VisualProperty()
        self.setZValue(2)

        if parent is not None:
            self._arrow_angle_to_scene = parent.parentItem().arrow_angle_to_scene
        self._bone_num = Bone.bone_count + 1
        Bone.bone_count += 1

    def rotation_arrow(self, scene_angle, distance):
        self._arrow_angle_to_scene = scene_angle

        parent_bone = self.parent_bone()
        if parent_bone is not None:
            local_angle = scene_angle - parent_bone.arrow_angle_to_scene
        else:
            local_angle = scene_angle
        self._arrow.setRotation(local_angle)

        # if distance <= RING_RADIUS - RING_BORDER_WIDTH / 2:
        #     x = math.cos(local_angle) * (RING_RADIUS - RING_BORDER_WIDTH / 2)
        #     y = math.sin(local_angle) * (RING_RADIUS - RING_BORDER_WIDTH / 2)
        #     self._tail_point_pos = QPointF(x, y)

    def move_drag_point(self, scene_pos: QPointF) -> None:
        pos = self._drag_point.mapFromScene(scene_pos)
        self._drag_point.move_center_to(pos.x(), pos.y())
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
        brush = QBrush(Qt.darkGray)

        self.setBrush(brush)
        self.update()

        self._arrow.setBrush(brush)
        self._arrow.update()

    def hover_leave_process(self):
        brush = QBrush(Qt.lightGray)
        if self._is_selected:
            brush = QBrush(Qt.yellow)

        self.setBrush(brush)
        self.update()

        self._arrow.setBrush(brush)
        self._arrow.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            try:
                if self._is_selected:
                    SIGNAL_BUS.signal_items_property_changed_from_scene.emit(self)
            except AttributeError:
                pass

            parent_bone = self.parent_bone()
            if parent_bone is None:
                return super().itemChange(change, value)

            try:
                if self._connect_arrow is not None:
                    self._connect_arrow.update_line(parent_bone.tail_point_pos, value)
            except AttributeError:
                pass

        elif change == QGraphicsItem.ItemRotationChange:
            print("bone pos change", value)
        elif change == QGraphicsItem.ItemScenePositionHasChanged:
            # print("bone scene pos change", self._handle, value)
            try:
                self._handle.setPos(value.x(), value.y())
                if self._texture_item:
                    self._texture_item.bone_pos = value

            except AttributeError:
                pass

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
    def connect_arrow(self) -> ConnectArrow:
        return self._connect_arrow

    @connect_arrow.setter
    def connect_arrow(self, value: ConnectArrow):
        self._connect_arrow = value

    @property
    def handler(self):
        return self._handle

    @handler.setter
    def handler(self, value: BoneHandle):
        self._handle = value

    @property
    def bone_num(self):
        return self._bone_num

    @property
    def tail_point_pos(self):
        return self._tail_point_pos

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value: bool):
        self._is_selected = value
        if self._is_selected:
            brush = QBrush(Qt.yellow)
            self.setBrush(brush)
            self.update()

            self._arrow.setBrush(brush)
            self._arrow.update()

    @property
    def texture_item(self) -> TextureItem:
        return self._texture_item

    @texture_item.setter
    def texture_item(self, texture_item: TextureItem) -> None:
        self._texture_item = texture_item

    def disable_changes(self):
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self._arrow.setFlags(QGraphicsItem.ItemIsMovable)

    def enable_changes(self):
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges)
        self._arrow.setFlags(
            QGraphicsItem.ItemSendsGeometryChanges | QGraphicsItem.ItemSendsScenePositionChanges)

    @property
    def scene_angle(self):
        return self._arrow_angle_to_scene

    @scene_angle.setter
    def scene_angle(self, value):
        self._arrow_angle_to_scene = value

    @property
    def scene_width_scale(self):
        return self._scene_width_scale

    @property
    def scene_height_scale(self):
        return self._scene_height_scale

    @property
    def visual_property(self) -> VisualProperty:
        p = self._visual_property
        p.position = self.pos()
        p.local_angle = self._arrow.rotation()
        p.scene_angle = self._arrow_angle_to_scene

        rect = self.boundingRect()
        p.width = rect.width()
        p.height = rect.height()
        p.local_width_scale = self.transform().m11()
        p.local_height_scale = self.transform().m22()
        p.scene_width_scale = self._scene_width_scale
        p.scene_height_scale = self._scene_height_scale
        return p

    def notify_visual_property_changed(self):
        try:
            self.disable_changes()  # no need send item change info again
            p = self._visual_property
            self.setPos(p.position.x(), p.position.y())
            self._arrow.setRotation(p.local_angle)
        finally:
            self.enable_changes()
