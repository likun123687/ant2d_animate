from _weakref import ReferenceType
from typing import Union

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsItem

from views.property import VisualProperty


class Outline(QGraphicsRectItem):
    def __init__(self, parent: "TextureItem" = None):
        super().__init__(parent)
        parent_bound = parent.boundingRect()
        self.setRect(parent_bound.left(), parent_bound.top(), parent_bound.width(), parent_bound.height())

    def move_to_center(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.center()
        # self.setTransformOriginPoint(offset)

        super().moveBy(x - offset.x(), y - offset.y())


class TextureItem(QGraphicsPixmapItem):
    def __init__(self, pos: QPointF, image: Union[QPixmap, str], parent=None):
        super().__init__(parent)
        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges
            | QGraphicsItem.ItemSendsScenePositionChanges)
        self.setPixmap(image)
        self.move_to_center(pos.x(), pos.y())

        self._outline = Outline(self)
        self._bone_pos: QPointF = pos
        self._bone_offset: QPointF = QPointF(0, 0)
        self._is_bone_moved: bool = False

        self._bind_bone = None

    def move_to_center(self, x, y) -> None:
        """
        使该item的原点为中心
        """
        rect = self.boundingRect()
        offset = rect.size()
        # self.setTransformOriginPoint(offset)
        self.setPos(x - offset.width() / 2, y - offset.height() / 2)
        # super().moveBy(x - offset.width() / 2, y - offset.height() / 2)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            if not self._is_bone_moved:
                rect = self.boundingRect().size()
                self._bone_offset = value - self._bone_pos + QPointF(rect.width() / 2, rect.height() / 2)
            else:
                self._is_bone_moved = False
        return super().itemChange(change, value)

    @property
    def bone_pos(self):
        return self._bone_pos

    @bone_pos.setter
    def bone_pos(self, bone_pos) -> None:
        self._bone_pos = bone_pos
        self._is_bone_moved = True
        new_pos = self._bone_offset + bone_pos
        self.move_to_center(new_pos.x(), new_pos.y())

    @property
    def bind_bone(self):
        return self._bind_bone

    @bind_bone.setter
    def bind_bone(self, bone) -> None:
        self._bind_bone = bone

    def visual_property(self) -> VisualProperty:
        p = VisualProperty()
        p.position = self._bind_bone.mapFromScene(self.scenePos())
        p.local_angle = self.rotation() - self._bind_bone.scene_angle
        p.scene_angle = self.rotation()

        rect = self.boundingRect()
        p.width = rect.width()
        p.height = rect.height()
        p.local_width_scale = self.transform().m11()
        p.local_height_scale = self.transform().m22()

        p.scene_width_scale = self._bind_bone.scene_width_scale * p.local_width_scale
        p.scene_height_scale = self._bind_bone.scene_height_scale * p.local_height_scale
        return p
