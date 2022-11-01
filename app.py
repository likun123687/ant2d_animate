import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,
    QDockWidget, QStackedLayout, QWidget,
)
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QSize

from views.dock_title_bar import DockTitleBar
from views.property_panel import PropertyPanel
from views.scene_panel import ScenePanel
from views.draw_order_panel import DrawOrderPanel
from views.library_panel import LibraryPanel
from views.main_canvas import MainCanvas


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
        self._stack_layout.addWidget(MainCanvas())
        self._central_widget.setLayout(self._stack_layout)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "Armature", self)
        button_action.setStatusTip("Armature")
        button_action.setToolTip("Armature")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

        button_action1 = QAction(QIcon("bug.png"), "Animation", self)
        button_action1.setStatusTip("Animation")
        button_action1.setToolTip("Animation")
        button_action1.triggered.connect(self.onMyToolBarButtonClick)
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)

        self.create_tool_bar2()

        self.setStatusBar(QStatusBar(self))

        # 菜单栏
        menu = self.menuBar()
        file_menu = menu.addMenu("文件")
        file_menu.addAction(button_action)

        edit_menu = menu.addMenu("编辑")
        window_menu = menu.addMenu("窗口")
        help_menu = menu.addMenu("帮助")

        # 左侧属性面板
        self._property_panel_dock = QDockWidget('Property', self)
        self._property_panel_dock.setWidget(PropertyPanel())
        self._property_panel_dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._property_panel_dock)

        # 右侧面板
        self._scene_panel_dock = QDockWidget('Scene', self)
        self._scene_panel_dock.setWidget(ScenePanel())
        self._scene_panel_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self._scene_panel_dock)

        # draw order panel
        self._draw_order_panel_dock = QDockWidget('draw order', self)
        self._draw_order_panel_dock.setWidget(DrawOrderPanel())
        self._draw_order_panel_dock.setFloating(False)
        self.tabifyDockWidget(self._scene_panel_dock, self._draw_order_panel_dock)

        # library panel
        self._library_panel_dock = QDockWidget('library', self)
        self._library_panel_dock.setWidget(LibraryPanel())
        self._library_panel_dock.setFloating(False)
        self._library_panel_dock.setTitleBarWidget(DockTitleBar())
        self._library_panel_dock.setStyleSheet("QDockWidget::title{padding-left: 0px; }")
        self.addDockWidget(Qt.RightDockWidgetArea, self._library_panel_dock)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

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

    def create_tool_bar2(self):
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        button_action = QAction(QIcon("bug.png"), "Select", self)
        button_action.setStatusTip("Select")
        button_action.setToolTip("Select")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        toolbar.addSeparator()

        button_action1 = QAction(QIcon("bug.png"), "Pose", self)
        button_action1.setStatusTip("Pose")
        button_action1.setToolTip("Pose")
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
