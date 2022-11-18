from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap

from views.bone import Bone


class SignalBus(QObject):
    """
    用于不同界面的controller之间通讯
    """
    add_bone = Signal(Bone, Bone)  # 增加了一个Bone
    select_bone = Signal(list)  # 选择了哪个bone
    select_bone_from_scene_panel = Signal(Bone)  # 从面板选择了bone
    add_texture_to_bone = Signal(Bone, QPixmap)


SIGNAL_BUS = SignalBus()
