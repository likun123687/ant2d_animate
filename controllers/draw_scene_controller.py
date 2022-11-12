from PySide6.QtCore import QObject, Signal

from models.draw_scene_model import DrawSceneModel
from views.bone import Bone


class DrawSceneController(QObject):
    signal_add_bone = Signal(Bone, Bone)
    signal_selected_bone_change = Signal(list)
    signal_hover_bone_enter = Signal(Bone)
    signal_hover_bone_leave = Signal(Bone)

    def __init__(self, model: DrawSceneModel):
        super().__init__()
        self._model: DrawSceneModel = model

        self.signal_add_bone.connect(self.slot_add_bone)
        self.signal_selected_bone_change.connect(self.slot_selected_bone_change)
        self.signal_hover_bone_enter.connect(self.slot_hover_bone_enter)
        self.signal_hover_bone_leave.connect(self.slot_hover_bone_leave)

    def slot_selected_bone_change(self, bones: list[Bone]):
        for bone in bones:
            bone.is_selected = True

        for selected_item in self._model.cur_selected_bones:
            if not bones.count(selected_item):
                selected_item.is_selected = False
                selected_item.hover_leave_process()

        self._model.cur_selected_bones = bones

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
