from typing import Union

from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsItemGroup
)

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsPolygonItem, \
    QGraphicsLineItem, QGraphicsEllipseItem

from PySide6.QtCore import Qt, QSize, QRectF, QPointF
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen, QPainter
from PySide6 import QtGui

import math
from views.bone import Bone, RING_RADIUS, RING_BORDER_WIDTH, Ring, Arrow
from views.bone_handle import BoneHandle, HANDLER_RADIUS
from views.connect_arrow import ConnectArrow
from views.texture_item import TextureItem


class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_space = QSize(25, 25)
        self._cur_bone: Union[Bone, None] = None
        self._bone_start_point: Union[QPointF, None] = None
        self._parent_bone: Union[Bone, None] = None
        self._bone_list = []
        self._total_rotation = 0
        self._add_bone = False

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        # painter->fillRect(sceneRect(),Qt::white);
        # rect = self.sceneRect().toRect()
        rect = rect.toRect()
        c = QColor(Qt.darkCyan)
        p = QPen(c)
        p.setStyle(Qt.DashLine)
        p.setWidthF(0.2)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing, False)
        painter.fillRect(rect, Qt.white)

        left = math.floor(rect.left() / self._grid_space.width()) * self._grid_space.width()
        right = math.ceil(rect.right() / self._grid_space.width()) * self._grid_space.width()
        top = math.floor(rect.top() / self._grid_space.height()) * self._grid_space.height()
        bottom = math.ceil(rect.bottom() / self._grid_space.height()) * self._grid_space.height()

        for x in range(left, right, int(self._grid_space.width())):
            painter.drawLine(x, top, x, bottom)

        for y in range(top, bottom, int(self._grid_space.height())):
            painter.drawLine(left, y, right, y)

        p.setStyle(Qt.SolidLine)
        p.setColor(Qt.black)
        p.setWidthF(1.0)
        painter.setPen(p)
        # painter.drawLine(rect.right(),rect.top(),rect.right(),rect.bottom())
        # painter.drawLine(rect.left(),rect.bottom(),rect.right(),rect.bottom())
        # 画xy轴
        painter.drawLine(left, 0, right, 0)
        painter.drawLine(0, top, 0, bottom)

        painter.restore()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            if item is not None:
                # print("at item", item)
                if isinstance(item, Bone):
                    item.clicked()
                    print(item.arrow_angle_to_scene)
                elif isinstance(item, Arrow):
                    item.parentItem().clicked()
            else:
                # self.text_img = TextureItem(event.scenePos())
                # self.text_img.setRotation(45)
                # self.addItem(self.text_img)
                # return

                self._bone_start_point = event.scenePos()
                parent = None

                if self._parent_bone is not None:
                    parent = self._parent_bone.arrow

                self._cur_bone = Bone(event.scenePos(), self, parent)
                if parent is not None:
                    # self.connect_arrow = ConnectArrow(self._parent_bone._tail_point_pos, parent.mapFromScene(event.scenePos()), parent)
                    self._cur_bone.connect_arrow = ConnectArrow(self._parent_bone._tail_point_pos,
                                                                parent.mapFromScene(event.scenePos()), parent)
                # handler
                handler = BoneHandle(QRectF(-HANDLER_RADIUS, -HANDLER_RADIUS, HANDLER_RADIUS * 2, HANDLER_RADIUS * 2))
                handler.setPos(event.scenePos().x(), event.scenePos().y())
                self.addItem(handler)
                self._cur_bone.handler = handler

                self._bone_list.append(self._cur_bone)
                self._add_bone = True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self._bone_start_point is not None and self._cur_bone is not None:
                start_pos = self._bone_start_point
                cur_pos = event.scenePos()
                distance = math.sqrt(
                    math.pow((cur_pos.x() - start_pos.x()), 2) + math.pow((cur_pos.y() - start_pos.y()), 2))
                print("distance", distance)
                angle = math.atan2((cur_pos.y() - start_pos.y()), (cur_pos.x() - start_pos.x())) * (180 / math.pi)
                self._cur_bone.rotation_arrow(angle, distance)

                if distance > RING_RADIUS - RING_BORDER_WIDTH / 2:
                    self._cur_bone.stretch_arrow(distance)
                    self._cur_bone.move_drag_point(cur_pos)
                event.accept()
                return
        super().mouseMoveEvent(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton:
            if self._add_bone:
                self._parent_bone = self._cur_bone

                self._bone_start_point = None
                self._cur_bone = None
                self._add_bone = False
            event.accept()
            return
        event.ignore()
