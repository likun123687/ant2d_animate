from typing import Union

from PySide6.QtCore import QObject

from views.bone import Bone
from views.texture_item import TextureItem


class ToolBarController(QObject):
    def __init__(self):
        super().__init__()

    def slot_item_property_changed_from_scene(self, item: Union[Bone, TextureItem, None]) -> None:
        """
        :param item:
        :return:
        """
        pass

    def slot_item_property_changed_from_bar(self):
        """
        在工具条中修改了属性
        :return:
        """