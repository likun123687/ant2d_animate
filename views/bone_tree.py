from typing import List, Dict, Union

from views.bone import Bone


class Node:
    def __init__(self, bone: Bone, parent: 'Node' = None):
        self._bone: Bone = bone
        self._parent: Node = parent
        self._children: List[Node] = []
        if parent is not None:
            parent.add_child(self)

    def get_bone(self) -> Bone:
        return self._bone

    def get_parent_bone(self) -> Union[Bone, None]:
        if self._parent is not None:
            return self._parent.get_bone()
        return None

    def get_parent_node(self) -> Union['Node', None]:
        return self._parent

    def get_children_bone(self) -> List[Bone]:
        bone_list = []
        if self._children is not None:
            for item in self._children:
                bone_list.append(item.get_bone())
        return bone_list

    def get_children_node(self) -> List['Node']:
        return self._children

    def get_all_sub_bones(self) -> List[Bone]:
        bone_list: List[Bone] = []
        node_list: List[Node] = []
        self.get_all_sub_nodes(node_list)
        for node in node_list:
            bone_list.append(node.get_bone())

        return bone_list

    def get_all_sub_nodes(self, node_list: List['Node']) -> None:
        for item in self._children:
            node_list.append(item)
            item.get_all_sub_nodes(node_list)

    def add_child(self, child: 'Node') -> None:
        self._children.append(child)

    def get_parents_bone(self) -> List[Bone]:
        bone_list: List[Bone] = []
        node_list: List[Node] = []
        self.get_parents_node(node_list)
        for node in node_list:
            bone_list.append(node.get_bone())

        return bone_list

    def get_parents_node(self, node_list: List['Node']):
        if self._parent is not None:
            node_list.append(self._parent)
            self._parent.get_parents_node(node_list)


class BoneTree:
    """
    a bone tree to store all tree
    """

    def __init__(self):
        self._root_bone: Union[Bone, None] = None
        self._node_list: Dict[int, Node] = {}

    def add_bone(self, bone: Bone, parent: Bone):
        if self._root_bone is None:
            self._root_bone = Bone

        parent_node = None
        if parent is not None:
            parent_node = self._node_list[parent.bone_num]

        self._node_list[bone.bone_num] = Node(bone, parent_node)
        print("add bone ", self._node_list)

    def del_bone(self, bone: Bone):
        """
        delete all the sub node
        :param bone:
        :return:
        """
        bone_node = self._node_list[bone.bone_num]
        for item in bone_node.get_all_sub_bones():
            del self._node_list[item.bone_num]

    def get_node(self, bone: Bone) -> Node:
        return self._node_list[bone.bone_num]

    def get_root_node(self) -> Union[Node, None]:
        if self._root_bone is None:
            return None
        else:
            return self._node_list[self._root_bone.bone_num]
