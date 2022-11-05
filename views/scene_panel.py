from PySide6.QtCore import Qt, Slot, QByteArray, QDataStream, QIODevice
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPixmap, QDragEnterEvent, QDragMoveEvent, QDropEvent
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QHeaderView
)

from common.signal_bus import SIGNAL_BUS
from views.bone import Bone


class SceneAssetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(0, QIcon('./bug.png'))
        self.setText(0, "0000")

        self.setIcon(1, QIcon('./bug.png'))
        self.setText(1, "1111")


class SceneBoneItem(QTreeWidgetItem):
    def __init__(self, bone: Bone, tree: QTreeWidget, parent=None):
        super().__init__(parent)
        if not parent:
            tree.addTopLevelItem(self)
        self._bone = bone
        self._init_ui(tree)

    def _init_ui(self, tree: QTreeWidget):
        # 设置子节点1
        self.setIcon(0, QIcon('./bug.png'))
        self.setText(0, str(self._bone.bone_num))

        ctrl_btn = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        label = QLabel()
        label.setPixmap(QPixmap('./bug.png'))
        label.setStyleSheet("background-color: yellow")
        layout.addWidget(label)

        label1 = QLabel()
        label1.setPixmap(QPixmap('./bug.png'))
        label1.setStyleSheet("background-color: yellow")
        layout.addWidget(label1)

        ctrl_btn.setLayout(layout)
        tree.setItemWidget(self, 1, ctrl_btn)

    @property
    def bone(self) -> Bone:
        return self._bone


class SceneTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.header().setStretchLastSection(False)
        self.setIndentation(5)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        # self.setStyleSheet(
        #     "QTreeView::branch::selected{background-color:green;} QTreeView::item::selected{background-color:green;} ")

        self._item_map: dict[int, QTreeWidgetItem] = {}
        self._init_ui()
        self.currentItemChanged.connect(self.cur_item_changed_cb)

    def _init_ui(self):
        # 设置列数
        self.setColumnCount(2)
        # 设置树形控件头部的标题
        # self.tree.setHeaderLabels(['Key', 'Value'])
        self.setHeaderHidden(True)

        # 设置根节点
        root = QTreeWidgetItem(self)

        root.setText(0, 'Root')
        root.setIcon(0, QIcon('./bug.png'))

        ctrl_btn = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        label = QLabel()
        label.setPixmap(QPixmap('./bug.png'))
        label.setStyleSheet("background-color: yellow")
        layout.addWidget(label)

        label1 = QLabel()
        label1.setPixmap(QPixmap('./bug.png'))
        label1.setStyleSheet("background-color: yellow")
        layout.addWidget(label1)

        ctrl_btn.setLayout(layout)
        self.setItemWidget(root, 1, ctrl_btn)

        # root.setIcon(0, QIcon('./bug.png'))
        # root.setIcon(1, QIcon('./bug.png'))
        #
        # root.setText(2, 'Root')
        # root.setIcon(2, QIcon('./bug.png'))
        #
        # # todo 优化2 设置根节点的背景颜色
        # brush_red = QBrush(Qt.red)
        # root.setBackground(0, brush_red)
        # brush_blue = QBrush(Qt.blue)
        # root.setBackground(1, brush_blue)

        # 设置树形控件的列的宽度
        # self.setColumnWidth(0, 150)
        # self.setColumnWidth(1, 50)

        # 设置子节点1
        # child1 = QTreeWidgetItem()
        # child1.setText(0, 'child1')
        # child1.setIcon(0, QIcon('./bug.png'))
        #
        # self.ctrl_btn1 = QWidget()
        # layout = QHBoxLayout()
        # layout.setSpacing(2)
        # layout.setContentsMargins(0, 0, 0, 0)
        #
        # layout.addStretch()
        #
        # label = QLabel()
        # label.setPixmap(QPixmap('./bug.png'))
        # label.setStyleSheet("background-color: yellow")
        # layout.addWidget(label)
        #
        # label1 = QLabel()
        # label1.setPixmap(QPixmap('./bug.png'))
        # label1.setStyleSheet("background-color: yellow")
        # layout.addWidget(label1)
        #
        # # todo 优化1 设置节点的状态
        # child1.setCheckState(0, Qt.Checked)
        #
        # root.addChild(child1)
        # self.ctrl_btn1.setLayout(layout)
        # self.setItemWidget(child1, 1, self.ctrl_btn1)
        #
        # # 设置子节点2
        # child2 = QTreeWidgetItem(root)
        # child2.setText(0, 'child2')
        # child2.setText(1, '')
        # child2.setIcon(0, QIcon('./bug.png'))
        #
        # # 设置子节点3
        # child3 = QTreeWidgetItem(child2)
        # child3.setText(0, 'child3')
        # child3.setText(1, 'android')
        # child3.setIcon(0, QIcon('./bug.png'))
        # 加载根节点的所有属性与子控件
        self.addTopLevelItem(root)

    def on_bone_added(self, bone: Bone, parent: Bone) -> None:
        """
        :param bone:
        :param parent:
        :return:
        """
        if parent:
            if parent.bone_num in self._item_map:
                parent_item = self._item_map[parent.bone_num]
                item = SceneBoneItem(bone, self, parent_item)
                self.setCurrentItem(item)
                self._item_map[bone.bone_num] = item

        else:
            item = SceneBoneItem(bone, self)
            self.setCurrentItem(item)
            self._item_map[bone.bone_num] = item

    def on_bone_selected(self, bone: Bone) -> None:
        item = self._item_map[bone.bone_num]
        self.setCurrentItem(item)

    @Slot(QTreeWidgetItem, QTreeWidgetItem)
    def cur_item_changed_cb(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        if isinstance(current, SceneBoneItem):
            SIGNAL_BUS.select_bone_from_scene_panel.emit(current.bone)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            item = self.itemAt(event.pos())
            if isinstance(item, SceneBoneItem):
                event.setDropAction(Qt.CopyAction)
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasFormat("application/x-slot_data"):
            item = self.itemAt(event.pos())
            if isinstance(item, SceneBoneItem):
                item_data: QByteArray = event.mimeData().data("application/x-slot_data")
                data_stream = QDataStream(item_data, QIODevice.ReadOnly)
                pixmap = QPixmap()
                data_stream >> pixmap

                item.addChild(SceneAssetItem())
                SIGNAL_BUS.add_texture_to_bone.emit(item.bone, pixmap)

                event.setDropAction(Qt.CopyAction)
                event.accept()
        else:
            event.ignore()


class ScenePanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._line_edit = QLineEdit()
        self._tree = SceneTreeWidget()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._line_edit)
        layout.addWidget(self._tree)
        self.setLayout(layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)

    @property
    def tree(self):
        return self._tree
