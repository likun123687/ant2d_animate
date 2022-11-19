from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsEllipseItem

from views.property import PropertyType


class SignalBus(QObject):
    """
    用于不同界面的controller之间通讯
    """
    signal_add_bone = Signal(QGraphicsEllipseItem, QGraphicsEllipseItem)  # 增加了一个Bone
    signal_selected_bone_changed = Signal(list)  # 从面板选择了bone
    signal_add_texture_to_bone = Signal(QGraphicsEllipseItem, QPixmap)  # 添加texture
    signal_hover_bone_enter = Signal(QGraphicsEllipseItem)
    signal_hover_bone_leave = Signal(QGraphicsEllipseItem)
    signal_item_property_changed = Signal(float, PropertyType, str)  # list, str代表来源
    signal_items_property_changed_from_scene = Signal(QGraphicsEllipseItem)
    signal_update_sub_bone_scene_angle = Signal(QGraphicsEllipseItem, float)


SIGNAL_BUS = SignalBus()
