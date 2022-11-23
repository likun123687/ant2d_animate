from common.signal_bus import SIGNAL_BUS
from models.tool_bar_model import ToolBarModel
from views.bone import Bone
from views.property import PropertyType, EditMode
from views.tool_bar import ToolBar


class ToolBarController:
    def __init__(self, view: ToolBar, model: ToolBarModel):
        super().__init__()
        self._view: ToolBar = view
        self._model: ToolBarModel = model

    def slot_items_property_changed(self, value: float, p_type: PropertyType, source: str) -> None:
        # print(value, p_type, source)

        # 通知view
        if p_type == PropertyType.POS_X:
            self._model.visual_property.position.setX(value)

        if p_type == PropertyType.POS_Y:
            self._model.visual_property.position.setY(value)

        if p_type == PropertyType.ANGLE:
            SIGNAL_BUS.signal_update_sub_bone_scene_angle.emit(self._model.cur_selected_item,
                                                               value - self._model.visual_property.local_angle)
            self._model.visual_property.local_angle = value

        self._model.cur_selected_item.notify_visual_property_changed()

    def slot_selected_items_changed(self, items: list):
        if len(items) > 1 or len(items) == 0:
            return

        item = items[0]
        self._model.cur_selected_item = items[0]
        if isinstance(item, Bone):
            self.set_toolbar_value(item)

    def slot_items_property_changed_from_scene(self, item):
        if isinstance(item, Bone) and item is self._model.cur_selected_item:
            self.set_toolbar_value(item)

    def set_toolbar_value(self, item):
        visual_property = item.visual_property
        self._model.visual_property = visual_property
        try:
            self._view.pos_x_spin_box.blockSignals(True)
            self._view.pos_y_spin_box.blockSignals(True)
            self._view.angle_spin_box.blockSignals(True)

            self._view.pos_x_spin_box.setValue(visual_property.position.x())
            self._view.pos_y_spin_box.setValue(visual_property.position.y())
            self._view.angle_spin_box.setValue(visual_property.local_angle)
        finally:
            self._view.pos_x_spin_box.blockSignals(False)
            self._view.pos_y_spin_box.blockSignals(False)
            self._view.angle_spin_box.blockSignals(False)

    def slot_change_mode(self, cur_model: EditMode):
        """
        改变toolbar的选择模式
        """
        self._model.cur_edit_mode = cur_model
        for mode, action in self._view.tool_map.items():
            if mode != cur_model:
                action.setChecked(False)



