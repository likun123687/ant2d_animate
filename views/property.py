from enum import IntEnum

from PySide6.QtCore import QPointF


class PropertyType(IntEnum):
    """
    工具栏的哪个属性
    """
    POS_X = 0
    POS_Y = 1
    ANGLE = 2


class VisualProperty:
    def __init__(self):
        self.position: QPointF = QPointF(0, 0)
        self.local_angle: float = 0.0
        self.scene_angle: float = 0.0
        self.local_width_scale: float = 1
        self.local_height_scale: float = 1
        self.scene_width_scale: float = 1
        self.scene_height_scale: float = 1
        self.width: float = 0
        self.height: float = 0


class EditMode(IntEnum):
    SELECT = 0
    CREATE_BONE = 1
