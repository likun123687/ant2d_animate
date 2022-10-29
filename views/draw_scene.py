import math
from typing import Union

from PySide6 import QtGui
from PySide6.QtCore import QRectF, QPointF, QByteArray, QIODevice, QDataStream
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPen, QPainter, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent

from views.bone import Bone, RING_RADIUS, RING_BORDER_WIDTH, Arrow
from views.bone_handle import BoneHandle, HANDLER_RADIUS
from views.bone_tree import BoneTree, Node
from views.connect_arrow import ConnectArrow
from views.texture_item import TextureItem


class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_space = QSize(25, 25)  # 背景方格大小
        self._cur_bone: Union[Bone, None] = None  # 当前正在操作的bone
        self._bone_start_point: Union[QPointF, None] = None  # bone起始位置
        self._parent_bone: Union[Bone, None] = None  # 父bone
        self._bone_tree = BoneTree()
        self._total_rotation = 0
        self._is_adding_bone = False
        self._last_hover_bone: Union[Bone, None] = None
        self._pressing_arrow = None  # 点击了哪个箭头
        self._bone_pos_when_arrow_begin_drag: Union[QPointF, None] = None  # 当箭头拖动时圆环的位置
        self._arrow_begin_drag_pos: Union[QPointF, None] = None  # 箭头开始拖动时的鼠标位置
        # self._old_rect = self.itemsBoundingRect()

    def drawBackground(self, painter, rect):
        """
        draw background grid
        :param painter:
        :param rect:
        :return:
        """
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
                    self._parent_bone = item
                elif isinstance(item, Arrow):
                    item.parentItem().clicked()
                    self._parent_bone = item.parentItem()
                    self._pressing_arrow = item
                    bone_parent = item.parentItem().parentItem()
                    if bone_parent is None:
                        self._bone_pos_when_arrow_begin_drag = item.parentItem().pos()
                    else:
                        self._bone_pos_when_arrow_begin_drag = bone_parent.mapToScene(item.parentItem().pos())
                    self._arrow_begin_drag_pos = event.scenePos()
            else:
                # self.text_img = TextureItem(event.scenePos())
                # self.text_img.setRotation(45)
                # self.addItem(self.text_img)
                # return

                # 增加一个bone
                self._bone_start_point = event.scenePos()
                parent_arrow = None

                if self._parent_bone is not None:
                    parent_arrow = self._parent_bone.arrow

                self._cur_bone = Bone(event.scenePos(), self, parent_arrow)
                if parent_arrow is not None:
                    # self.connect_arrow = ConnectArrow(self._parent_bone._tail_point_pos, parent.mapFromScene(event.scenePos()), parent)
                    self._cur_bone.connect_arrow = ConnectArrow(self._parent_bone._tail_point_pos,
                                                                parent_arrow.mapFromScene(event.scenePos()),
                                                                parent_arrow)
                    self._cur_bone.connect_arrow.hide()
                # handler操作柄
                handler = BoneHandle(QRectF(-HANDLER_RADIUS, -HANDLER_RADIUS, HANDLER_RADIUS * 2, HANDLER_RADIUS * 2))
                handler.setPos(event.scenePos().x(), event.scenePos().y())
                self.addItem(handler)
                self._cur_bone.handler = handler

                # self._bone_list.append(self._cur_bone)
                self._bone_tree.add_bone(self._cur_bone, self._parent_bone)
                self._is_adding_bone = True

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self._bone_start_point is not None and self._cur_bone is not None:
                start_pos = self._bone_start_point
                cur_pos = event.scenePos()
                distance = math.sqrt(
                    math.pow((cur_pos.x() - start_pos.x()), 2) + math.pow((cur_pos.y() - start_pos.y()), 2))
                # print("distance", distance)
                angle = math.atan2((cur_pos.y() - start_pos.y()), (cur_pos.x() - start_pos.x())) * (180 / math.pi)
                self._cur_bone.rotation_arrow(angle, distance)

                if distance > RING_RADIUS - RING_BORDER_WIDTH / 2:
                    self._cur_bone.stretch_arrow(distance)
                    self._cur_bone.move_drag_point(cur_pos)
                event.accept()
                return

            # 拖动箭头
            if self._pressing_arrow is not None:
                ring = self._pressing_arrow.parentItem()
                cur_pos = event.scenePos()
                ring_parent = ring.parentItem()
                if ring_parent is None:
                    ring.moveBy(cur_pos.x() - self._arrow_begin_drag_pos.x(),
                                cur_pos.y() - self._arrow_begin_drag_pos.y())
                else:
                    dx = cur_pos.x() - self._arrow_begin_drag_pos.x()
                    dy = cur_pos.y() - self._arrow_begin_drag_pos.y()

                    new_scene_pos = QPointF(self._bone_pos_when_arrow_begin_drag.x() + dx,
                                            self._bone_pos_when_arrow_begin_drag.y() + dy)
                    new_pos = ring_parent.mapFromScene(new_scene_pos)
                    ring.setPos(new_pos)
                    self._bone_pos_when_arrow_begin_drag = new_scene_pos

                    # cur_pos = ring_parent.mapFromScene(cur_pos)
                    # begin_pos = ring_parent.mapFromScene(self._begin_bone_pos)
                    #
                    # ring.moveBy(cur_pos.x() - begin_pos.x(), cur_pos.y() - begin_pos.y())
                self._arrow_begin_drag_pos = cur_pos


        elif event.buttons() == Qt.NoButton:
            # hover some item
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            node: Union[Node, None] = None
            if item is not None:
                if isinstance(item, Bone):
                    node = self._bone_tree.get_node(item)
                    self._last_hover_bone = item
                elif isinstance(item, Arrow):
                    node = self._bone_tree.get_node(item.parentItem())
                    self._last_hover_bone = item.parentItem()
                else:
                    super().mouseMoveEvent(event)
                    event.ignore()
                    return

                self._last_hover_bone.hover_enter_process()
                if self._last_hover_bone.connect_arrow:
                    self._last_hover_bone.connect_arrow.show()
                if node is not None:
                    for sub_bone in node.get_all_sub_bones():
                        if sub_bone.connect_arrow:
                            sub_bone.connect_arrow.show()

                    for up_bone in node.get_parents_bone():
                        if up_bone.connect_arrow:
                            up_bone.connect_arrow.show()

            else:
                if self._last_hover_bone is not None:
                    self._last_hover_bone.hover_leave_process()
                    if self._last_hover_bone.connect_arrow:
                        self._last_hover_bone.connect_arrow.hide()
                    node = self._bone_tree.get_node(self._last_hover_bone)
                    if node is not None:
                        for sub_bone in node.get_all_sub_bones():
                            if sub_bone.connect_arrow:
                                sub_bone.connect_arrow.hide()
                        for up_bone in node.get_parents_bone():
                            if up_bone.connect_arrow:
                                up_bone.connect_arrow.hide()
                self._last_hover_bone = None

        super().mouseMoveEvent(event)
        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._pressing_arrow = None

        if event.button() == Qt.LeftButton:
            self.auto_adjust()
            if self._is_adding_bone:
                self._parent_bone = self._cur_bone

                self._bone_start_point = None
                self._cur_bone = None
                self._is_adding_bone = False
            event.accept()
            return
        event.ignore()

    def auto_adjust(self):
        """
        自动调整画布大小
        """
        old_rect = self.sceneRect()
        top = old_rect.top()
        left = old_rect.left()
        bottom = old_rect.bottom()
        right = old_rect.right()

        items_bounding_rect = self.itemsBoundingRect()
        bounding_rect_top = items_bounding_rect.top()
        bounding_rect_left = items_bounding_rect.left()
        bounding_rect_bottom = items_bounding_rect.bottom()
        bounding_rect_right = items_bounding_rect.right()

        if bounding_rect_left - 200 < left:
            old_rect.setLeft(bounding_rect_left - 200)

        if bounding_rect_right + 200 > right:
            old_rect.setRight(bounding_rect_right + 200)

        if bounding_rect_top - 200 < top:
            old_rect.setTop(bounding_rect_top - 200)

        if bounding_rect_bottom + 200 > bottom:
            old_rect.setBottom(bounding_rect_bottom + 200)

        self.setSceneRect(old_rect)

    def dragEnterEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            item_data: QByteArray = event.mimeData().data("application/x-slot_data")
            data_stream = QDataStream(item_data, QIODevice.ReadOnly)
            pixmap = QPixmap()
            data_stream >> pixmap

            text_img = TextureItem(event.scenePos(), pixmap)
            self.addItem(text_img)

            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
