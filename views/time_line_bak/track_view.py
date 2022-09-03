import math

from PySide6.QtGui import QIcon, QBrush, Qt, QPalette, QColor, QPen, QPainter
from PySide6.QtWidgets import QGraphicsView, QTreeWidget, QTreeWidgetItem, QGraphicsScene, QWidget

from views.time_line_bak.common import DIVISIONS_WIDTH, LEFT_BAR_WIDTH, TOP_BAR_HEIGHT


class TrackTreeCtrl(QTreeWidget):
    """
    左侧的tree
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置列数
        self.setColumnCount(2)
        # 设置树形控件头部的标题
        self.setHeaderLabels(['Key', 'Value'])

        # 设置根节点
        root = QTreeWidgetItem(self)
        root.setText(0, 'Root')
        root.setIcon(0, QIcon('./images/root.png'))

        # todo 优化2 设置根节点的背景颜色
        brush_red = QBrush(Qt.red)
        root.setBackground(0, brush_red)
        brush_blue = QBrush(Qt.blue)
        root.setBackground(1, brush_blue)

        # 设置树形控件的列的宽度
        self.setColumnWidth(0, 150)

        # 设置子节点1
        child1 = QTreeWidgetItem()
        child1.setText(0, 'child1')
        child1.setText(1, 'ios')
        child1.setIcon(0, QIcon('./images/IOS.png'))

        # todo 优化1 设置节点的状态
        child1.setCheckState(0, Qt.Checked)

        root.addChild(child1)

        # 设置子节点2
        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'child2')
        child2.setText(1, '')
        child2.setIcon(0, QIcon('./images/android.png'))

        # 设置子节点3
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, 'child3')
        child3.setText(1, 'android')
        child3.setIcon(0, QIcon('./images/music.png'))

        # 加载根节点的所有属性与子控件
        self.addTopLevelItem(root)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('gray'))
        self.setPalette(palette)


class TrackScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        rect = rect.toRect()
        c = QColor(Qt.black)
        p = QPen(c)
        p.setStyle(Qt.SolidLine)
        p.setWidthF(1)
        p.setCosmetic(True)
        painter.setPen(p)
        painter.save()
        painter.setRenderHints(QPainter.Antialiasing, False)
        painter.fillRect(rect, Qt.white)

        left = math.floor(rect.left() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        right = math.ceil(rect.right() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        top = math.floor(rect.top() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        bottom = math.ceil(rect.bottom() / DIVISIONS_WIDTH) * DIVISIONS_WIDTH
        scroll_bar_width = 0
        # graphics_views = self.views()
        # if len(graphics_views) > 0:
        #     graphics_view = graphics_views[0]
        #     scroll_bar_width = graphics_view.verticalScrollBar().width()

        for x in range(left, right, int(DIVISIONS_WIDTH)):
            painter.drawLine(x, top, x, bottom)
        painter.restore()


class TrackGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)


class TrackView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__track_tree_ctrl = TrackTreeCtrl(self)
        self.scene = TrackScene(0, 0, 3000, 1500)
        self.__track_view = TrackGraphicsView(self.scene, self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        track_view_height = 500
        parent = self.parentWidget()
        # 父节点的高度
        if parent is not None:
            track_view_height = parent.rect().height() - TOP_BAR_HEIGHT
        self.__track_tree_ctrl.resize(LEFT_BAR_WIDTH, track_view_height)
        self.__track_view.resize(self.size().width() - LEFT_BAR_WIDTH, track_view_height)
        self.__track_view.move(LEFT_BAR_WIDTH, 0)
