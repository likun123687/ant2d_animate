import weakref

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap

from models.draw_scene_model import DrawSceneModel
from views.bone import Bone
from views.draw_scene import DrawScene
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
