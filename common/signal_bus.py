from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from views.bone import Bone


class SignalBus(QObject):
    add_bone = Signal(Bone, Bone)  # 增加了一个Bone
    select_bone = Signal(Bone)  # 选择了哪个bone
    select_bone_from_scene_panel = Signal(Bone)  # 从面板选择了bone
    add_texture_to_bone = Signal(Bone, QPixmap)


SIGNAL_BUS = SignalBus()