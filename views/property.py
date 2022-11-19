from PySide6.QtCore import QPointF

from enum import Enum


class PropertyType(Enum):
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
