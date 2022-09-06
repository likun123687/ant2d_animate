from PySide6.QtGui import QBrush, Qt, QIcon, QPalette, QColor
from PySide6.QtWidgets import QLabel, QWidget, QTreeWidget, QTreeWidgetItem

from views.time_line.common import DIVISIONS_BAR_HEIGHT, LEFT_PANEL_WIDTH, GRID_HEIGHT, TRACK_VIEW_HEIGHT


class TrackTreeCtrl(QTreeWidget):
    """
    左侧的tree
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置列数
        self.setColumnCount(2)
        # 设置树形控件头部的标题
        # self.setHeaderLabels(['Key', 'Value'])

        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')

        child1_1 = QTreeWidgetItem()
        child1_1.setText(0, 'child1_1')
        child1_1.setText(1, 'windows')
        child1.addChild(child1_1)

        child2 = QTreeWidgetItem()
        child2.setText(0, 'child2')
        child2.setText(1, 'android')

        self.addTopLevelItem(child1)
        self.addTopLevelItem(child2)
        self.setHeaderHidden(True)

        self.setStyleSheet("QTreeWidget::item{height:30px}")

        # # 设置根节点
        # root = QTreeWidgetItem(self)
        # root.setText(0, 'Root')
        #
        # # todo 优化2 设置根节点的背景颜色
        # brush_red = QBrush(Qt.red)
        # root.setBackground(0, brush_red)
        # brush_blue = QBrush(Qt.blue)
        # root.setBackground(1, brush_blue)
        #
        # # 设置树形控件的列的宽度
        # self.setColumnWidth(0, 150)
        #
        # # 设置子节点1
        # child1 = QTreeWidgetItem()
        # child1.setText(0, 'child1')
        # child1.setText(1, 'ios')
        #
        # # todo 优化1 设置节点的状态
        # # child1.setCheckState(0, Qt.Checked)
        # root.addChild(child1)
        #
        # # 设置子节点2
        # child2 = QTreeWidgetItem(root)
        # child2.setText(0, 'child2')
        # child2.setText(1, '')
        #
        # # 设置子节点3
        # child3 = QTreeWidgetItem(child2)
        # child3.setText(0, 'child3')
        # child3.setText(1, 'android')
        # child3.setIcon(0, QIcon('./images/music.png'))
        #
        # # 加载根节点的所有属性与子控件
        # self.addTopLevelItem(root)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)


class LeftPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        label_1 = QLabel("1111", self)
        label_1.setStyleSheet("background-color: yellow")
        label_1.setGeometry(0, 0, 50, 10)

        label_2 = QLabel("222", self)
        label_2.setStyleSheet("background-color: blue")
        label_2.setGeometry(50, 0, 50, 10)

        label_3 = QLabel("333", self)
        label_3.setStyleSheet("background-color: gray")
        label_3.setGeometry(0, 10, 50, 10)

        label_4 = QLabel("4444", self)
        label_4.setStyleSheet("background-color: red")
        label_4.setGeometry(0, DIVISIONS_BAR_HEIGHT, LEFT_PANEL_WIDTH, GRID_HEIGHT)

        self._track_tree_ctrl: TrackTreeCtrl = TrackTreeCtrl(self)
        self._track_tree_ctrl.setGeometry(0, DIVISIONS_BAR_HEIGHT + GRID_HEIGHT,
                                          LEFT_PANEL_WIDTH, TRACK_VIEW_HEIGHT - DIVISIONS_BAR_HEIGHT - GRID_HEIGHT)
        self._track_tree_ctrl.lower()

    @property
    def track_tree_ctrl(self):
        return self._track_tree_ctrl
