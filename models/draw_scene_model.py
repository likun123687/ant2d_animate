from typing import Optional

from views.bone import Bone
from views.bone_tree import BoneTree


class DrawSceneModel:
    def __init__(self):
        super().__init__()
        self._cur_selected_bones: list[Bone] = []  # 当前选中的bone
        self._bone_tree: Optional[BoneTree] = BoneTree()  # bone树

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
