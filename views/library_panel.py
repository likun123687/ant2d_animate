from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QTreeWidget,
    QTreeWidgetItem
)
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush

class LibraryPanel(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        line_edit = QtWidgets.QLineEdit(self)
        line_edit.setGeometry(0, 0, 50, 10)

        self.tree = QTreeWidget(self)
        #设置列数
        self.tree.setColumnCount(2)
        #设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key','Value'])

        #设置根节点
        root=QTreeWidgetItem(self.tree)
        root.setText(0,'Root')
        root.setIcon(0,QIcon('./images/root.png'))

        # todo 优化2 设置根节点的背景颜色
        brush_red=QBrush(Qt.red)
        root.setBackground(0,brush_red)
        brush_blue=QBrush(Qt.blue)
        root.setBackground(1,brush_blue)

        #设置树形控件的列的宽度
        self.tree.setColumnWidth(0,150)

        #设置子节点1
        child1=QTreeWidgetItem()
        child1.setText(0,'child1')
        child1.setText(1,'ios')
        child1.setIcon(0,QIcon('./images/IOS.png'))

        #todo 优化1 设置节点的状态
        child1.setCheckState(0,Qt.Checked)

        root.addChild(child1)

        #设置子节点2
        child2=QTreeWidgetItem(root)
        child2.setText(0,'child2')
        child2.setText(1,'')
        child2.setIcon(0,QIcon('./images/android.png'))

        #设置子节点3
        child3=QTreeWidgetItem(child2)
        child3.setText(0,'child3')
        child3.setText(1,'android')
        child3.setIcon(0,QIcon('./images/music.png'))


        #加载根节点的所有属性与子控件
        self.tree.addTopLevelItem(root)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)


