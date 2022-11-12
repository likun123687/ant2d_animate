from typing import Optional, Union

from PySide6.QtCore import QObject

from views.bone import VisualProperty, Bone
from views.texture_item import TextureItem


class ToolBarModel(QObject):
    def __init__(self):
        super().__init__()
        self._item_width_height_bound: bool = False
        self._cur_edit_mode: bool = False
        self._cur_selected_item: Union[Bone, TextureItem, None] = None

    @property
    def visual_property(self):
        return

    @visual_property.setter
    def visual_property(self, value: Optional[VisualProperty]):
        pass
