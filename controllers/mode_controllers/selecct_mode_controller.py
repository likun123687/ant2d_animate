from typing import Union, Optional

from PySide6 import QtGui
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QCursor, QPixmap
from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QGraphicsView

from models.draw_scene_model import DrawSceneModel
from views.bone import Bone, Arrow
from views.draw_scene import DrawScene
from views.property import ActionType


class SelectModeController:
    def __init__(self, view: DrawScene, model: DrawSceneModel):
        self._view = view
        self._model = model

        # 0 没有选中  1 hover in选中 2 hover in空白 3 hover in 其他没选中
        self._cursor_list = [
            [Qt.ArrowCursor, None],
            [Qt.SizeAllCursor, None],
            ["assets/icons/arrow-circle.png", None],
            [Qt.ArrowCursor, None],
        ]

    def _press_bone_or_arrow(self, item: Union[Bone, Arrow], event: QGraphicsSceneMouseEvent) -> None:
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

    def _cal_action_type(self, pos: QPointF):
        item = self._view.itemAt(pos, QtGui.QTransform())
        if item in self._model.cur_selected_bones.values():
            return ActionType.MOVE

        return ActionType.ROTATE

    def mouse_press(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            item = self._view.itemAt(event.scenePos(), QtGui.QTransform())
            if item:
                if isinstance(item, Bone) or isinstance(item, Arrow):
                    self._press_bone_or_arrow(item, event)

            # 记录拖动箭头所需要的信息
            if len(self._model.cur_selected_bones) > 0:
                self._model.drag_begin_pos = event.scenePos()
                for bone in self._model.cur_selected_bones.values():
                    self._model.drag_begin_pos[1].append(bone.scenePos())

    def _drag_process(self, scene_pos: QPointF):
        # 判断是移动还是旋转
        if len(self._model.cur_selected_bones) == 0:
            return
        action_type = self._cal_action_type(scene_pos)
        if action_type == ActionType.MOVE:
            self._model.move_selected_bones()
        elif action_type == ActionType.ROTATE:
            self._model.rotate_selected_bones()

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
        pass

    def get_draw_view(self) -> QGraphicsView:
        return self._view.views()[0]

    def update_cursor(self):
        draw_view = self.get_draw_view()
        cursor_list = self._model.cursor_map[self._model.cur_edit_mode]
        if len(self._model.cur_selected_bones) == 0:  # 没有选中
            result = cursor_list[0]
        else:
            if not self._model.cur_hover_bone:  # 有选中 hover 空白
                result = cursor_list[2]
            else:
                if self._model.cur_hover_bone in self._model.cur_selected_bones.values():
                    # 有选中 hover 选中bone
                    result = cursor_list[1]
                else:
                    # 有选中 hover 没选中bone
                    result = cursor_list[3]

        cursor = result[1]
        if not cursor:
            if isinstance(result[0], str):
                cursor = QCursor(QPixmap(result[0]))
            else:
                cursor = QCursor(result[0])
        draw_view.setCursor(cursor)

    def update_ctrl_handler(self):
        bone = self._model.get_selected_bone_tail()
