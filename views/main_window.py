import weakref

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow, QStatusBar,
    QDockWidget, QStackedLayout, QWidget, )

from views.dock_title_bar import DockTitleBar
from views.main_canvas import MainCanvas
from views.panels.draw_order_panel import DrawOrderPanel
from views.panels.library_panel import LibraryPanel
from views.panels.property_panel import PropertyPanel
from views.panels.scene_panel import ScenePanel
from views.tool_bar import ToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("ant2d bone")

        # label = QLabel("Hello!")
        # label.setAlignment(Qt.AlignCenter)

        self.setMinimumSize(QSize(1000, 800))
        # self.setCentralWidget(MainCanvas(self))

        self._central_widget = QWidget(self)  # define central widget
        self.setCentralWidget(self._central_widget)

        self._stack_layout = QStackedLayout()
        self._main_canvas = MainCanvas()
        self._stack_layout.addWidget(self._main_canvas)
        self._central_widget.setLayout(self._stack_layout)
        self._tool_bar = ToolBar(weakref.ref(self))

        self.setStatusBar(QStatusBar(self))

        # 菜单栏
        menu = self.menuBar()
        file_menu = menu.addMenu("文件")
        edit_menu = menu.addMenu("编辑")
        window_menu = menu.addMenu("窗口")
        help_menu = menu.addMenu("帮助")

        # 左侧属性面板
        self._property_panel_dock = QDockWidget('Property', self)
        self._property_panel_dock.setWidget(PropertyPanel())
        self._property_panel_dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._property_panel_dock)

        # 右侧面板
        self._scene_panel = ScenePanel()
        scene_panel_dock = QDockWidget('Scene', self)
        scene_panel_dock.setWidget(self._scene_panel)
        scene_panel_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, scene_panel_dock)

        # draw order panel
        self._draw_order_panel_dock = QDockWidget('draw order', self)
        self._draw_order_panel_dock.setWidget(DrawOrderPanel())
        self._draw_order_panel_dock.setFloating(False)
        self.tabifyDockWidget(scene_panel_dock, self._draw_order_panel_dock)
        scene_panel_dock.raise_()  # 默认选中scene

        # library panel
        self._library_panel_dock = QDockWidget('library', self)
        self._library_panel_dock.setWidget(LibraryPanel())
        self._library_panel_dock.setFloating(False)
        self._library_panel_dock.setTitleBarWidget(DockTitleBar())
        self._library_panel_dock.setStyleSheet("QDockWidget::title{padding-left: 0px; margin-left:0px}")
        self.addDockWidget(Qt.RightDockWidgetArea, self._library_panel_dock)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    @property
    def tool_bar(self):
        return self._tool_bar

    @tool_bar.setter
    def tool_bar(self, value):
        self._tool_bar = value

    @property
    def main_canvas(self):
        return self._main_canvas

    @property
    def scene_panel(self):
        return self._scene_panel

    # def resizeEvent(self, event):
    # print("Window has been resized")
    # super().resizeEvent(event)
    # self.scene.setSceneRect(-(self.width()/2), -(self.height()/2), self.width(), self.height())
    # self.view.setSceneRect(-(self.width()/2), -(self.height()/2), self.width(), self.height())
    # self.view.setFrameStyle(0);
    # self.view.viewport().setFixedSize(self.width(), self.height())
    # print("1111", self.width(), self.height())
    # print("2222", self.view.viewport().width(), self.view.viewport().height())
    # self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # self.view.fitInView(-(self.width()/2), -(self.height()/2), self.width(), self.height(), Qt.KeepAspectRatio)
