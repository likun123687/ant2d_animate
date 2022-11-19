from models.scene_panel_model import ScenePanelModel
from views.bone import Bone
from views.panels.scene_panel import SceneBoneItem, SceneTreeWidget


class ScenePanelController:
    def __init__(self, view: SceneTreeWidget, model: ScenePanelModel):
        super().__init__()
        self._view: SceneTreeWidget = view
        self._model: ScenePanelModel = model

    def slot_bone_added(self, bone: Bone, parent: Bone) -> None:
        item_map = self._model.item_map
        if parent:
            if parent.bone_num in item_map:
                parent_item = item_map[parent.bone_num]
                item = SceneBoneItem(bone, self._view, parent_item)
                self._view.setCurrentItem(item)
                item_map[bone.bone_num] = item

        else:
            item = SceneBoneItem(bone, self._view)
            self._view.setCurrentItem(item)
            item_map[bone.bone_num] = item

    def on_bone_selected(self, bones: list[Bone]) -> None:
        item_map = self._model.item_map
        for bone in bones:
            if bone.bone_num in item_map:  # 可能还没有bone插入
                item = item_map[bone.bone_num]
                self._view.blockSignals(True)
                self._view.setCurrentItem(item)
                self._view.blockSignals(False)
