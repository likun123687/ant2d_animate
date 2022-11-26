from PySide6.QtWidgets import QApplication

from common.signal_bus import SIGNAL_BUS
from controllers.draw_scene_controller import DrawSceneController
from controllers.scene_panel_controller import ScenePanelController
from controllers.tool_bar_controller import ToolBarController
from models.draw_scene_model import DrawSceneModel
from models.main_model import MainModel
from models.scene_panel_model import ScenePanelModel
from models.tool_bar_model import ToolBarModel
from views.main_window import MainWindow


class MainController:
    def __init__(self):
        super().__init__()
        self._app = QApplication([])

        self._view: MainWindow = MainWindow()
        self._model: MainModel = MainModel()
        self._init_controllers()

    # 初始化controller
    def _init_controllers(self):
        # toolbar
        self._tool_bar_controller = ToolBarController(self._view.tool_bar, ToolBarModel())
        SIGNAL_BUS.signal_selected_bone_changed.connect(self._tool_bar_controller.slot_selected_items_changed)
        SIGNAL_BUS.signal_item_property_changed_from_toolbar.connect(self._tool_bar_controller.slot_items_property_changed)
        SIGNAL_BUS.signal_items_property_changed_from_scene.connect(
            self._tool_bar_controller.slot_items_property_changed_from_scene)
        SIGNAL_BUS.signal_change_edit_mode.connect(self._tool_bar_controller.slot_change_mode)

        # draw scene
        self._draw_scenes = {}
        draw_scene_controller = DrawSceneController(self._view.main_canvas.cur_tab.scene, DrawSceneModel())
        # SIGNAL_BUS.signal_add_bone.connect(draw_scene_controller.slot_add_bone)
        # SIGNAL_BUS.signal_selected_bone_changed.connect(draw_scene_controller.slot_selected_bone_changed)
        # SIGNAL_BUS.signal_hover_bone_enter.connect(draw_scene_controller.slot_hover_bone_enter)
        # SIGNAL_BUS.signal_hover_bone_leave.connect(draw_scene_controller.slot_hover_bone_leave)
        SIGNAL_BUS.signal_add_texture_to_bone.connect(draw_scene_controller.slot_add_texture_to_bone)
        SIGNAL_BUS.signal_update_sub_bone_scene_angle.connect(draw_scene_controller.slot_update_bone_scene_angle)
        self._draw_scenes[1] = draw_scene_controller

        SIGNAL_BUS.signal_change_edit_mode.connect(draw_scene_controller.slot_change_mode)

        # scene panel
        self._scene_panel_controller = ScenePanelController(self._view.scene_panel.tree, ScenePanelModel())
        SIGNAL_BUS.signal_add_bone.connect(self._scene_panel_controller.slot_bone_added)
        SIGNAL_BUS.signal_selected_bone_changed.connect(self._scene_panel_controller.on_bone_selected)

    def run(self):
        self._view.show()
        self._app.exec()
