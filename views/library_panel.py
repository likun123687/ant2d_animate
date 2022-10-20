from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QSizePolicy
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPixmap


class LibraryPanel(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._line_edit = QLineEdit()
        # self._line_edit.setGeometry(0, 0, 50, 10)

        self.tree = QTreeWidget()
        # 设置列数
        self.tree.setColumnCount(2)
        # 设置树形控件头部的标题
        # self.tree.setHeaderLabels(['Key', 'Value'])
        self.tree.setHeaderHidden(True)

        # 设置根节点
        root = QTreeWidgetItem(self.tree)
        root.setText(0, 'Root')
        root.setIcon(0, QIcon('./bug.png'))

        self.ctrl_btn = QWidget()
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

        # label_policy = label.sizePolicy()
        # label_policy.setHorizontalPolicy(QSizePolicy.Fixed)
        # label.setSizePolicy(label_policy)

        # label1 = QLabel()
        # label1.setPixmap(QPixmap('./bug.png'))
        #
        # layout.addWidget(label, 0, Qt.AlignRight)
        # layout.addWidget(label1, 0, Qt.AlignRight)

        self.ctrl_btn.setLayout(layout)

        self.tree.setItemWidget(root, 1, self.ctrl_btn)

        # todo 优化2 设置根节点的背景颜色
        brush_red = QBrush(Qt.red)
        root.setBackground(0, brush_red)
        brush_blue = QBrush(Qt.blue)
        root.setBackground(1, brush_blue)

        # 设置树形控件的列的宽度
        self.tree.setColumnWidth(0, 150)
        self.tree.setColumnWidth(1, 50)

        # 设置子节点1
        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')
        child1.setIcon(0, QIcon('./bug.png'))

        # todo 优化1 设置节点的状态
        child1.setCheckState(0, Qt.Checked)

        root.addChild(child1)

        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '')
        child2.setIcon(0, QIcon('./bug.png'))

        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, 'android')
        child3.setIcon(0, QIcon('./bug.png'))

        # 加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._line_edit)
        layout.addWidget(self.tree)
        self.setLayout(layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)
