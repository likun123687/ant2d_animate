from typing import Optional, Union

from PySide6.QtCore import Qt, QPointF

from views.bone import Bone
from views.bone_tree import BoneTree
from views.property import EditMode


class DrawSceneModel:
    def __init__(self):
        super().__init__()
        self._cur_selected_bones: dict[int, Bone] = {}  # 当前选中的bone
        self._bone_tree: Optional[BoneTree] = BoneTree()  # bone树
        self._cur_edit_mode: Optional[EditMode] = EditMode.SELECT
        self._cur_hover_bone: Optional[Bone] = None

        self._is_adding_bone: bool = False
        self._parent_bone: Union[Bone, None] = None  # 父bone

        self._last_hover_bone: Union[Bone, None] = None
        self._hovering_space: bool = True
        self._drag_begin_pos: Optional[QPointF] = None  # 0 鼠标位置

        # 0 没有选中  1 hover in选中 2 hover in空白 3 hover in 其他没选中
        self._cursor_map = {
            EditMode.SELECT: [
                [Qt.ArrowCursor, None],
                [Qt.SizeAllCursor, None],
                ["assets/icons/arrow-circle.png", None],
                [Qt.ArrowCursor, None],
            ],
            EditMode.CREATE_BONE: [
                ["assets/icons/create_bone.png", None]
            ]
        }

    def hover_bone_enter(self, item: Bone):
        """
        hover一个bone或者arrow
        """
        if item == self._last_hover_bone:
            return

        if self._last_hover_bone:
            self.hover_bone_leave_process(self._last_hover_bone)

        # do sth
        self.hover_bone_enter_process(item)

        self._last_hover_bone = item
        self._hovering_space = False

    def hover_bone_leave(self):
        if not self._last_hover_bone:
            return

        # do sth
        self.hover_bone_leave_process(self._last_hover_bone)
        self.hover_space_process()

        self._last_hover_bone = None

    def hover_space(self):
        if not self._hovering_space:
            self.hover_space_process()
        self._hovering_space = True

    def hover_bone_enter_process(self, bone: Bone):
        bone.hover_enter_process()
        if bone.connect_arrow:
            bone.connect_arrow.show()

        node = self._bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                if sub_bone.connect_arrow:
                    sub_bone.connect_arrow.show()

            for up_bone in node.get_parents_bone():
                if up_bone.connect_arrow:
                    up_bone.connect_arrow.show()

        # 记录当前hover bone
        self._cur_hover_bone = bone

    def hover_bone_leave_process(self, bone: Bone):
        bone.hover_leave_process()
        if bone.connect_arrow:
            bone.connect_arrow.hide()

        node = self._bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                if sub_bone.connect_arrow:
                    sub_bone.connect_arrow.hide()
            for up_bone in node.get_parents_bone():
                if up_bone.connect_arrow:
                    up_bone.connect_arrow.hide()

    def hover_space_process(self):
        """
        hover空白
        """
        print("hover empty space")
        self._cur_hover_bone = None

    def selected_bone_changed(self, bones: list[Bone]):
        for bone in bones:
            print("angle info", bone.arrow.rotation(), bone.scene_angle)
            bone.is_selected = True

        for selected_item in self._cur_selected_bones.values():
            if not bones.count(selected_item):
                selected_item.is_selected = False
                selected_item.hover_leave_process()

        self.cur_selected_bones = bones

    def move_selected_bones(self, cur_pos: QPointF):
        for bone in self._cur_selected_bones.values():
            bone.moveBy(cur_pos.x() - self._drag_begin_pos.x(), cur_pos.y() - self._drag_begin_pos.y())
            # update record position
        self._drag_begin_pos = cur_pos

    def rotate_selected_bones(self, cur_pos: QPointF):
        for bone in self._cur_selected_bones:
            pass
            # bone.moveBy(cur_pos.x() - self._drag_begin_pos.x(), cur_pos.y() - self._drag_begin_pos.y())
            # update record position
        self._drag_begin_pos = cur_pos

    def get_selected_bone_head(self):
        key = max(self._cur_selected_bones.keys())
        return self._cur_selected_bones[key]

    def get_selected_bone_tail(self):
        key = min(self._cur_selected_bones.keys())
        return self._cur_selected_bones[key]

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

    @property
    def parent_bone(self):
        return self._parent_bone

    @parent_bone.setter
    def parent_bone(self, value):
        self._parent_bone = value

    @property
    def is_adding_bone(self):
        return self._is_adding_bone

    @is_adding_bone.setter
    def is_adding_bone(self, value):
        self._is_adding_bone = value

    @property
    def drag_begin_pos(self):
        return self._drag_begin_pos

    @drag_begin_pos.setter
    def drag_begin_pos(self, value):
        self._drag_begin_pos = value

    @property
    def drag_move_pos(self):
        return self._drag_move_pos

    @drag_move_pos.setter
    def drag_move_pos(self, value):
        self._drag_move_pos = value
