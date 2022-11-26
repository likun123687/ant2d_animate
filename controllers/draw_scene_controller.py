import weakref

from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsSceneMouseEvent

from controllers.mode_controllers.create_bone_mode_controller import CreateBoneModeController
from controllers.mode_controllers.mode_interface import ModeActionInterface
from controllers.mode_controllers.selecct_mode_controller import SelectModeController
from models.draw_scene_model import DrawSceneModel
from views.bone import Bone
from views.draw_scene import DrawScene
from views.property import EditMode
from views.texture_item import TextureItem


class DrawSceneController:

    def __init__(self, view: DrawScene, model: DrawSceneModel):
        super().__init__()
        self._view: DrawScene = view
        self._model: DrawSceneModel = model
        self._mode_controller: dict[EditMode, ModeActionInterface] = {
            EditMode.SELECT: SelectModeController(view, model),
            EditMode.CREATE_BONE: CreateBoneModeController(view, model),
        }

    def mouse_press(self, event: QGraphicsSceneMouseEvent) -> None:
        self._mode_controller[self._model.cur_edit_mode].mouse_press(event)

    def mouse_move(self, event: QGraphicsSceneMouseEvent) -> None:
        self._mode_controller[self._model.cur_edit_mode].mouse_move(event)

    def mouse_release(self, event: QGraphicsSceneMouseEvent) -> None:
        self._mode_controller[self._model.cur_edit_mode].mouse_release(event)

    @Slot(Bone)
    def slot_add_texture_to_bone(self, bone: Bone, pixmap: QPixmap):
        texture_item = TextureItem(bone.scenePos(), pixmap)
        self._view.addItem(texture_item)
        bone.texture_item = texture_item
        texture_item.bind_bone = weakref.ref(bone)

    def slot_update_bone_scene_angle(self, bone: Bone, offset):
        """
        更新bone相对scene的角度
        """
        bone.scene_angle = bone.scene_angle + offset
        node = self._model.bone_tree.get_node(bone)
        if node:
            for sub_bone in node.get_all_sub_bones():
                sub_bone.scene_angle = sub_bone.scene_angle + offset

    def slot_change_mode(self, cur_model: EditMode):
        """
        改变toolbar的选择模式
        """
        self._model.cur_edit_mode = cur_model
        self._mode_controller[self._model.cur_edit_mode].update_cursor()