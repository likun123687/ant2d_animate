from typing import Optional

from PySide6.QtGui import QCursor

from views.bone import Bone
from views.bone_tree import BoneTree
from views.property import EditMode


class DrawSceneModel:
    def __init__(self):
        super().__init__()
        self._cur_selected_bones: list[Bone] = []  # 当前选中的bone
        self._bone_tree: Optional[BoneTree] = BoneTree()  # bone树
        self._cur_edit_mode: Optional[EditMode] = EditMode.SELECT
        self._cur_hover_bone: Optional[Bone] = None
        # 0 没有选中  1 hover in选中 2 hover in空白 3 hover in 其他没选中
        self._cursor_map = {
            EditMode.SELECT: [
                ["assets/icons/create_bone.png", None],
                ["assets/icons/create_bone.png", None],
                ["assets/icons/create_bone.png", None],
                ["assets/icons/create_bone.png", None],
            ],
            EditMode.CREATE_BONE: [
                ["assets/icons/create_bone.png", None]
            ]
        }

    @property
    def cur_selected_bones(self):
        return self._cur_selected_bones

    @cur_selected_bones.setter
    def cur_selected_bones(self, value):
        self._cur_selected_bones = value

    @property
    def bone_tree(self):
        return self._bone_tree

    @bone_tree.setter
    def bone_tree(self, value):
        self._bone_tree = value

    @property
    def cur_edit_mode(self):
        return self._cur_edit_mode

    @cur_edit_mode.setter
    def cur_edit_mode(self, value):
        self._cur_edit_mode = value

    @property
    def cursor_map(self):
        return self._cursor_map

    @property
    def cur_hover_bone(self):
        return self._cur_hover_bone

    @cur_hover_bone.setter
    def cur_hover_bone(self, value):
        self._cur_hover_bone = value
