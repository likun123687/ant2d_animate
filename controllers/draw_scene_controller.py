import weakref
from typing import Union

from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsView
from prompt_toolkit.cursor_shapes import CursorShape

from models.draw_scene_model import DrawSceneModel
from views.bone import Bone
from views.draw_scene import DrawScene
from views.property import EditMode
from views.texture_item import TextureItem


class DrawSceneController:

    def __init__(self, view: DrawScene, model: DrawSceneModel):
        super().__init__()
        self._view: DrawScene = view
        self._model: DrawSceneModel = model

    def slot_selected_bone_changed(self, bones: list[Bone]):
        for bone in bones:
            print("angle info", bone.arrow.rotation(), bone.scene_angle)
            bone.is_selected = True

        for selected_item in self._model.cur_selected_bones:
            if not bones.count(selected_item):
                selected_item.is_selected = False
                selected_item.hover_leave_process()

        self._model.cur_selected_bones = bones
        self._view.parent_bone = bones[0]

    def slot_add_bone(self, bone: Bone, parent: Bone):
        self._model.bone_tree.add_bone(bone, parent)

        # 发送给scene panel
        # SIGNAL_BUS.add_bone.emit(self._cur_bone, self._parent_bone)

    def slot_hover_bone_enter(self, bone: Bone):
        bone.hover_enter_process()
        if bone.connect_arrow:
            bone.connect_arrow.show()

        node = self._model.bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                if sub_bone.connect_arrow:
                    sub_bone.connect_arrow.show()

            for up_bone in node.get_parents_bone():
                if up_bone.connect_arrow:
                    up_bone.connect_arrow.show()

        # 记录当前hover bone
        self._model.cur_hover_bone = bone
        self.set_cursor()

    def slot_hover_bone_leave(self, bone: Bone):
        bone.hover_leave_process()
        if bone.connect_arrow:
            bone.connect_arrow.hide()

        node = self._model.bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                if sub_bone.connect_arrow:
                    sub_bone.connect_arrow.hide()
            for up_bone in node.get_parents_bone():
                if up_bone.connect_arrow:
                    up_bone.connect_arrow.hide()

    @Slot(Bone)
    def slot_add_texture_to_bone(self, bone: Bone, pixmap: QPixmap):
        texture_item = TextureItem(bone.scenePos(), pixmap)
        self._view.addItem(texture_item)
        bone.texture_item = texture_item
        texture_item.bind_bone = weakref.ref(bone)

    def slot_update_bone_scene_angle(self, bone: Bone, offset):
        """
        更新bone相对scene的角度
        """
        bone.scene_angle = bone.scene_angle + offset
        node = self._model.bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                sub_bone.scene_angle = sub_bone.scene_angle + offset

    def get_draw_view(self) -> QGraphicsView:
        return self._view.views()[0]

    def set_cursor(self):
        draw_view = self.get_draw_view()
        cursor_list = self._model.cursor_map[self._model.cur_edit_mode]
        try:
            if len(self._model.cur_selected_bones) == 0:  # 没有选中
                result = cursor_list[0]
            else:
                if not self._model.cur_hover_bone:  # 有选中 hover 空白
                    result = cursor_list[2]
                else:
                    if self._model.cur_hover_bone in self._model.cur_selected_bones:
                        # 有选中 hover 选中bone
                        result = cursor_list[1]
                    else:
                        # 有选中 hover 没选中bone
                        result = cursor_list[3]
            cursor = result[1]
            if not cursor:
                cursor = QPixmap(result[0])
            draw_view.setCursor(cursor)
        except IndexError:
            pass

    def slot_hover_space(self):
        """
        hover空白
        """
        print("hover empty space")
        self._model.cur_hover_bone = None
        self.set_cursor()

    def slot_change_mode(self, cur_model: EditMode):
        """
        改变toolbar的选择模式
        """
        self._model.cur_edit_mode = cur_model
        self.set_cursor()
