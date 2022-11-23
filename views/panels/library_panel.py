import json
import pathlib
from enum import Enum
from typing import Union, List, Optional

from PySide6.QtCore import Qt, QBuffer, QIODevice, QRect, QPoint, QMimeData, QByteArray, QDataStream, QEvent
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPixmap, QDragEnterEvent, QDropEvent, QDragMoveEvent, \
    QMouseEvent, QDrag
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QApplication, QHeaderView
)


class AssetType(Enum):
    single_image = 0
    atlas = 1
    sub_image = 2


class AssetItem(QTreeWidgetItem):
    """
    asset item that drag
    """
    max_thumb_width = 500

    def __init__(self, asset_type: AssetType, name: str, image: Union[str, QPixmap], desc_path: str = "", parent=None):
        super().__init__(parent)
        self._type: AssetType = asset_type
        self._name: str = name
        self._description_path: str = desc_path
        self._file_path: str = ""
        self._click_point: Optional[QPoint] = None
        if isinstance(image, QPixmap):
            self._pixmap = image
        else:
            self._file_path = image
            self._pixmap = QPixmap(image)
        thumb_pixmap: Optional[QPixmap] = self._pixmap
        if self._pixmap.width() > AssetItem.max_thumb_width or self._pixmap.height() > AssetItem.max_thumb_width:
            if self._pixmap.width() > self._pixmap.height():
                thumb_pixmap = self._pixmap.scaledToWidth(AssetItem.max_thumb_width)
            else:
                thumb_pixmap = self._pixmap.scaledToHeight(AssetItem.max_thumb_width)

        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        thumb_pixmap.save(buffer, "PNG", quality=100)
        base64 = bytes(buffer.data().toBase64()).decode()
        self.setText(0, name)
        # self.setText(1, '')
        self.setIcon(0, QIcon('assets/icons/bug.png'))
        size_str = "{}x{}".format(self._pixmap.width(), self._pixmap.height())
        self.setToolTip(0, '<img src="data:image/png;base64,{}"><br>{}'.format(base64, size_str))

    @property
    def pixmap(self):
        return self._pixmap


class AssetTreeWidget(QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.header().setStretchLastSection(False)

        self._start_drag_point: Optional[QPoint] = None
        self._file_list: List[str] = []
        self._root: Optional[QTreeWidgetItem] = None
        self._init_ui()

    def _init_ui(self):
        # 设置列数
        self.setColumnCount(2)
        # 设置树形控件头部的标题
        # self.tree.setHeaderLabels(['Key', 'Value'])
        self.setHeaderHidden(True)

        # 设置根节点
        self._root = QTreeWidgetItem(self)
        self._root.setText(0, 'Root')
        self._root.setIcon(0, QIcon('assets/icons/bug.png'))

        ctrl_btn = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addStretch()

        label = QLabel()
        label.setPixmap(QPixmap('assets/icons/bug.png'))
        label.setStyleSheet("background-color: yellow")
        layout.addWidget(label)

        label1 = QLabel()
        label1.setPixmap(QPixmap('assets/icons/bug.png'))
        label1.setStyleSheet("background-color: yellow")
        layout.addWidget(label1)

        ctrl_btn.setLayout(layout)
        self.setItemWidget(self._root, 1, ctrl_btn)

        # todo 优化2 设置根节点的背景颜色
        brush_red = QBrush(Qt.red)
        self._root.setBackground(0, brush_red)
        brush_blue = QBrush(Qt.blue)
        self._root.setBackground(1, brush_blue)

        # 设置树形控件的列的宽度
        self.setColumnWidth(0, 150)
        self.setColumnWidth(1, 50)

        # 设置子节点1
        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')
        child1.setIcon(0, QIcon('assets/icons/bug.png'))

        # todo 优化1 设置节点的状态
        child1.setCheckState(0, Qt.Checked)

        self._root.addChild(child1)

        # 设置子节点2
        child2 = QTreeWidgetItem(self._root)
        child2.setText(0, 'child2')
        child2.setText(1, '')
        child2.setIcon(0, QIcon('assets/icons/bug.png'))

        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, 'android')
        child3.setIcon(0, QIcon('assets/icons/bug.png'))

        # 加载根节点的所有属性与子控件
        self.addTopLevelItem(self._root)
        self._root.setExpanded(True)

    def add_asset_list(self, file_list: List[str]):
        trim_file_list = []
        for file_item in file_list:
            if [".png", ".jpg", ".jpeg", ".json"].count(pathlib.Path(file_item).suffix.lower()):
                trim_file_list.append(file_item)

        trim_file_list = list(set(trim_file_list))  # 去重,删除不支持格式

        for item in trim_file_list:
            item_suffix = pathlib.Path(item).suffix
            if [".png", ".jpg", ".jpeg"].count(item_suffix.lower()):
                desc_file = item.removesuffix(item_suffix) + ".json"
                if trim_file_list.count(desc_file):
                    self.add_asset_item(item, desc_file)
                else:
                    self.add_asset_item(item, "")

    def check_asset_exist(self):
        pass

    def add_asset_item(self, file: str, desc_file: str = ""):
        if not desc_file:
            AssetItem(AssetType.single_image, pathlib.Path(file).name, file, "", self._root)
        else:
            image = QPixmap(file)
            atlas = AssetItem(AssetType.atlas, pathlib.Path(file).name, image, desc_file, self._root)
            with open(desc_file, 'r') as f:
                desc_dict = json.load(f)
                for name, frame_item in desc_dict["frames"].items():
                    frame = frame_item["frame"]
                    sub_image = image.copy(QRect(frame["x"], frame["y"], frame["w"], frame["h"]))
                    AssetItem(AssetType.atlas, name, sub_image, "", atlas)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._start_drag_point = event.pos()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.LeftButton:
            drag_dis = (event.pos() - self._start_drag_point).manhattanLength()
            if drag_dis > QApplication.startDragDistance():
                self.perform_drag()
        elif event.buttons() == Qt.NoButton:
            item = self.itemAt(event.pos())
            if item:
                print(item)
            else:
                print("cccc")
        super().mouseMoveEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        print("i leave tree")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.source() == self:
            event.ignore()
            return

        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                file_extension = pathlib.Path(file_path).suffix
                if [".png", ".jpg", ".jpeg", ".json"].count(file_extension.lower()):
                    self._file_list.append(file_path)

            if len(self._file_list) > 0:
                event.setDropAction(Qt.CopyAction)
                event.accept()
                print(self._file_list)

        elif event.mimeData().hasImage():
            event.acceptProposedAction()
            event.accept()
        else:
            event.ignore()
            print("not support file format 1111")

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if len(self._file_list) > 0:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if len(self._file_list) > 0:
            event.setDropAction(Qt.CopyAction)
            self.add_asset_list(self._file_list)
            event.accept()
        else:
            event.ignore()

        self._file_list = []

    def perform_drag(self) -> None:
        item: AssetItem = self.currentItem()
        if not item:
            return

        pixmap = item.pixmap

        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        data_stream << pixmap

        mime_data = QMimeData()
        mime_data.setData('application/x-slot_data', item_data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))

        drop_action = drag.exec(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)


class LibraryPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._line_edit: Optional[QLineEdit] = None
        self._tree: Optional[AssetTreeWidget] = None
        self.init_ui()

    def init_ui(self) -> None:
        self._line_edit = QLineEdit()
        # self._line_edit.setGeometry(0, 0, 50, 10)
        self._tree = AssetTreeWidget()

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
