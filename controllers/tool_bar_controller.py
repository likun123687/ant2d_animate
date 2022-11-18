from typing import Union

from PySide6.QtCore import QObject, Signal

from common.signal_bus import SIGNAL_BUS
from models.tool_bar_model import ToolBarModel
from views.bone import Bone
from views.texture_item import TextureItem


class ToolBarController(QObject):
    signal_item_property_changed_from_scene = Signal(Union[Bone, TextureItem, None])

    def __init__(self, model: ToolBarModel):
        super().__init__()
        self._model = model
        SIGNAL_BUS.select_bone.connect(self.slot_item_property_changed_from_scene)


    def slot_item_property_changed_from_scene(self, item: list) -> None:
        """
        :param item:
        :return:
        """
        self._model.cur_selected_item = item
        # 通知view

    def slot_item_property_changed_from_bar(self):
        """
        在工具条中修改了属性
        :return:
        """
