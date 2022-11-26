from typing import Protocol

from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QGraphicsSceneMouseEvent


class ModeActionInterface(Protocol):
    def mouse_press(self, event: QGraphicsSceneMouseEvent) -> None:
        pass

    def mouse_move(self, event: QGraphicsSceneMouseEvent) -> None:
        pass

    def mouse_release(self, event: QGraphicsSceneMouseEvent) -> None:
        pass

    def update_cursor(self):
        pass

    def update_ctrl_handler(self):
        pass

    def _drag_process(self, scene_pos: QPointF):
        pass