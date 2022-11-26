import math
from typing import Union

from PySide6 import QtGui
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsView

from models.draw_scene_model import DrawSceneModel
from views.bone import Bone, RING_RADIUS, RING_BORDER_WIDTH, Arrow
from views.ctrl_handles.select_handles import SelectHandles, HANDLER_RADIUS
from views.connect_arrow import ConnectArrow
from views.draw_scene import DrawScene
from views.property import EditMode
from views.ctrl_handles.rotate_handles import RotateHandles


class CreateBoneModeController:
    def __init__(self, view: DrawScene, model: DrawSceneModel):
        self._view = view
        self._model = model

    def _add_bone_process(self, bone: Bone, parent: Bone):
        self._model.bone_tree.add_bone(bone, parent)

    def _add_bone(self, scene_pos: QPointF):
        """
        添加一个bone
        """
        parent_arrow = None

        if self._model.parent_bone:
            parent_arrow = self._model.parent_bone.arrow

        self._cur_bone = Bone(scene_pos, self, parent_arrow)
        if parent_arrow:
            self._cur_bone.connect_arrow = ConnectArrow(self._model.parent_bone.tail_point_pos,
                                                        parent_arrow.mapFromScene(scene_pos),
                                                        parent_arrow)
            self._cur_bone.connect_arrow.hide()
        # handler操作柄
        handler = SelectHandles(QRectF(-HANDLER_RADIUS, -HANDLER_RADIUS, HANDLER_RADIUS * 2, HANDLER_RADIUS * 2))
        handler.setPos(scene_pos.x(), scene_pos.y())
        self._view.addItem(handler)
        self._cur_bone.handler = handler

        # 旋转操作柄
        rotate_bar = RotateHandles(scene_pos)
        self._view.addItem(rotate_bar)

        self._add_bone_process(self._cur_bone, self._model.parent_bone)
        # 默认选中新增的bone
        self._model.selected_bone_changed([self._cur_bone])
        self._model.is_adding_bone = True

    def _stretch_arrow(self, scene_pos: QPointF):
        """
        拉长箭头
        """
        assert len(self._model.cur_selected_bones) == 1
        cur_bone = self._model.cur_selected_bones.values()[0]
        # start_pos = self._bone_start_point
        start_pos = cur_bone.scenePos()
        cur_pos = scene_pos
        distance = math.sqrt(
            math.pow((cur_pos.x() - start_pos.x()), 2) + math.pow((cur_pos.y() - start_pos.y()), 2))
        # print("distance", distance)
        angle = math.atan2((cur_pos.y() - start_pos.y()), (cur_pos.x() - start_pos.x())) * (180 / math.pi)
        self._cur_bone.rotation_arrow(angle, distance)

        if distance > RING_RADIUS - RING_BORDER_WIDTH / 2:
            self._cur_bone.stretch_arrow(distance)
            self._cur_bone.move_drag_point(cur_pos)

    def _press_bone_or_arrow(self, item: Union[Bone, Arrow]) -> None:
        """
        点击了bone或者arrow
        """
        if isinstance(item, Bone):
            target_bone = item
        elif isinstance(item, Arrow):
            target_bone = item.parentItem()

        else:
            return
        self._model.selected_bone_changed([target_bone])

    def mouse_press(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            item = self._view.itemAt(event.scenePos(), QtGui.QTransform())
            if item:
                if isinstance(item, Bone) or isinstance(item, Arrow):
                    self._press_bone_or_arrow(item)
                    # 记录信息
                    self._model.drag_begin_pos = event.scenePos()
            else:
                # 增加一个bone
                self._add_bone(event.scenePos())

    def _drag_process(self, scene_pos: QPointF):
        if self._model.is_adding_bone:
            # 拉长箭头
            self._stretch_arrow(scene_pos)
        else:
            # 新增bone
            if self._model.drag_begin_pos:
                self._add_bone(self._model.drag_begin_pos)

    def mouse_move(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            self._drag_process(event.scenePos())

        elif event.buttons() == Qt.NoButton:
            # hover some item
            item = self._view.itemAt(event.scenePos(), QtGui.QTransform())
            if isinstance(item, Bone):
                self._model.hover_bone_enter(item)
            elif isinstance(item, Arrow):
                self._model.hover_bone_enter(item.parentItem())
            else:
                self._model.hover_bone_leave()
                self._model.hover_space()

    def mouse_release(self, event: QGraphicsSceneMouseEvent) -> None:
        self._model.is_adding_bone = False
        self._model.drag_begin_pos = None

    def get_draw_view(self) -> QGraphicsView:
        return self._view.views()[0]

    def update_cursor(self):
        draw_view = self.get_draw_view()
        result = self._model.cursor_map[EditMode.CREATE_BONE]
        cursor = result[1]
        if not cursor:
            if isinstance(result[0], str):
                cursor = QCursor(QPixmap(result[0]))
            else:
                cursor = QCursor(result[0])
        draw_view.setCursor(cursor)
