from typing import Optional, Union

from views.bone import VisualProperty, Bone
from views.property import EditMode
from views.texture_item import TextureItem


class ToolBarModel:
    def __init__(self):
        super().__init__()
        self._item_width_height_bound: bool = False
        self._cur_edit_mode: Optional[EditMode] = None
        self._cur_selected_item: Union[Bone, TextureItem, None] = None
        self._tmp_visual_property: Optional[VisualProperty] = None

    @property
    def visual_property(self):
        return self._tmp_visual_property

    @visual_property.setter
    def visual_property(self, value: Optional[VisualProperty]):
        self._tmp_visual_property = value

    @property
    def cur_selected_item(self):
        return self._cur_selected_item

    @cur_selected_item.setter
    def cur_selected_item(self, value):
        self._cur_selected_item = value

    @property
    def cur_edit_mode(self):
        return self._cur_edit_mode

    @cur_edit_mode.setter
    def cur_edit_mode(self, value):
        self._cur_edit_mode = value
