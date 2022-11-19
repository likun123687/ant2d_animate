import math
import weakref
from typing import Union

from PySide6 import QtGui
from PySide6.QtCore import QRectF, QPointF, QByteArray, QIODevice, QDataStream, Slot
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPen, QPainter, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent, QGraphicsSceneMouseEvent

from common.signal_bus import SIGNAL_BUS
from views.bone import Bone, RING_RADIUS, RING_BORDER_WIDTH, Arrow
from views.bone_handle import BoneHandle, HANDLER_RADIUS
from views.connect_arrow import ConnectArrow
from views.rotate_bar import RotateBar
from views.texture_item import TextureItem


class DrawScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._grid_space = QSize(25, 25)  # 背景方格大小
        self._cur_bone: Union[Bone, None] = None  # 当前正在操作的bone
        self._bone_start_point: Union[QPointF, None] = None  # bone起始位置
        self._parent_bone: Union[Bone, None] = None  # 父bone
        # self._bone_tree = BoneTree()
        self._is_adding_bone: bool = False

        self._last_hover_bone: Union[Bone, None] = None

        self._pressing_arrow = None  # 点击了哪个箭头
        self._bone_pos_when_arrow_begin_drag: Union[QPointF, None] = None  # 当箭头拖动时圆环的位置
        self._arrow_begin_drag_pos: Union[QPointF, None] = None  # 箭头开始拖动时的鼠标位置
        # self._cur_selected_bone: Optional[Bone] = None  # 当前选中的bone
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

    def _press_bone_or_arrow(self, item: Union[Bone, Arrow], event: QGraphicsSceneMouseEvent) -> None:
        """
        点击了bone或者arrow
        """
        if isinstance(item, Bone):
            target_bone = item
        elif isinstance(item, Arrow):
            target_bone = item.parentItem()

            # 记录拖动箭头所需要的信息
            self._pressing_arrow = item
            bone_parent = target_bone.parentItem()
            if bone_parent is None:
                self._bone_pos_when_arrow_begin_drag = target_bone.pos()
            else:
                self._bone_pos_when_arrow_begin_drag = bone_parent.mapToScene(target_bone.pos())
            self._arrow_begin_drag_pos = event.scenePos()

        else:
            return

        # 发送signal
        SIGNAL_BUS.signal_selected_bone_changed.emit([target_bone])

    def _add_bone(self, event: QGraphicsSceneMouseEvent):
        """
        添加一个bone
        """
        self._bone_start_point = event.scenePos()
        parent_arrow = None

        if self._parent_bone:
            parent_arrow = self._parent_bone.arrow

        self._cur_bone = Bone(event.scenePos(), self, parent_arrow)
        if parent_arrow:
            self._cur_bone.connect_arrow = ConnectArrow(self._parent_bone.tail_point_pos,
                                                        parent_arrow.mapFromScene(event.scenePos()),
                                                        parent_arrow)
            self._cur_bone.connect_arrow.hide()
        # handler操作柄
        handler = BoneHandle(QRectF(-HANDLER_RADIUS, -HANDLER_RADIUS, HANDLER_RADIUS * 2, HANDLER_RADIUS * 2))
        handler.setPos(event.scenePos().x(), event.scenePos().y())
        self.addItem(handler)
        self._cur_bone.handler = handler

        # 旋转操作柄
        rotate_bar = RotateBar(event.scenePos())
        self.addItem(rotate_bar)

        # 发送给signal
        SIGNAL_BUS.signal_add_bone.emit(self._cur_bone, self._parent_bone)
        # 默认选中新增的bone
        SIGNAL_BUS.signal_selected_bone_changed.emit([self._cur_bone])

        self._is_adding_bone = True

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            if item:
                if isinstance(item, Bone) or isinstance(item, Arrow):
                    self._press_bone_or_arrow(item, event)
            else:
                # self.text_img = TextureItem(event.scenePos())
                # self.text_img.setRotation(45)
                # self.addItem(self.text_img)
                # return
                # 增加一个bone
                self._add_bone(event)

    def _stretch_arrow(self, event):
        """
        拉长箭头
        """
        if self._bone_start_point and self._cur_bone:
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

    def _drag_arrow(self, event):
        """
        拖动箭头
        """
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

        self._arrow_begin_drag_pos = cur_pos

    def _hover_bone_enter(self, item: Bone):
        """
        hover一个bone或者arrow
        """
        if item == self._last_hover_bone:
            return

        if self._last_hover_bone:
            SIGNAL_BUS.signal_hover_bone_leave.emit(self._last_hover_bone)

        # do sth
        SIGNAL_BUS.signal_hover_bone_enter.emit(item)

        self._last_hover_bone = item

    def _hover_bone_leave(self):
        if not self._last_hover_bone:
            return

        # do sth
        SIGNAL_BUS.signal_hover_bone_leave.emit(self._last_hover_bone)

        self._last_hover_bone = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if event.buttons() & Qt.LeftButton:
            if self._is_adding_bone:
                # 拉长箭头
                self._stretch_arrow(event)

            # 拖动箭头
            if self._pressing_arrow is not None:
                self._drag_arrow(event)

        elif event.buttons() == Qt.NoButton:
            # hover some item
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            if isinstance(item, Bone):
                self._hover_bone_enter(item)
            elif isinstance(item, Arrow):
                self._hover_bone_enter(item.parentItem())
            else:
                self._hover_bone_leave()

            # if item is not None:
            #     self._hover_bone_enter(item, event)
            # else:
            #     self._hover_bone_leave(None, event)

        event.ignore()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._pressing_arrow = None

        if event.button() == Qt.LeftButton:
            self.auto_adjust()
            if self._is_adding_bone:
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

    @property
    def parent_bone(self):
        return self._parent_bone

    @parent_bone.setter
    def parent_bone(self, bone):
        self._parent_bone = bone
