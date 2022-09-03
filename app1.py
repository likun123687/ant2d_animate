import sys
from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,
    QDockWidget, QStackedLayout, QWidget, QGraphicsScene,
    QGraphicsScene, QGraphicsView, QGraphicsRectItem, QStackedLayout
)
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QIcon, QBrush, QPen
from PySide6 import QtCore, QtGui, QtWidgets

from views.property_panel import PropertyPanel
from views.scene_panel import ScenePanel
from views.draw_order_panel import DrawOrderPanel
from views.library_panel import LibraryPanel
from views.main_canvas import MainCanvas


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        self.setMinimumSize(QSize(800, 600))

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = QGraphicsScene(0, 0, 400, 200)

        # Draw a rectangle item, setting the dimensions.
        rect = QGraphicsRectItem(0, 0, 200, 50)

        # Set the origin (position) of the rectangle in the scene.
        rect.setPos(50, 20)

        # Define the brush (fill).
        brush = QBrush(Qt.red)
        rect.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.cyan)
        pen.setWidth(10)
        rect.setPen(pen)

        self.scene.addItem(rect)

        self.view = QGraphicsView(self.scene)
        self.view.setAutoFillBackground(True)
        palette = self.view.palette()
        palette.setColor(QPalette.Window, QColor('blue'))
        self.view.setPalette(palette)

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setMovable(True)
        self.tabs.addTab(self.view, "111")

        self.central_widget = QWidget()  # define central widget
        self.setCentralWidget(self.central_widget)

        self.stacklayout = QStackedLayout()
        self.stacklayout.addWidget(self.tabs)
        self.central_widget.setLayout(self.stacklayout)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        toolbar.addSeparator()
        button_action1 = QAction(QIcon("bug.png"), "Your button", self)
        button_action1.setStatusTip("This is your button")
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)

        self.setStatusBar(QStatusBar(self))

        # 菜单栏
        menu = self.menuBar()
        file_menu = menu.addMenu("文件")
        file_menu.addAction(button_action)

        edit_menu = menu.addMenu("编辑")
        window_menu = menu.addMenu("窗口")
        help_menu = menu.addMenu("帮助")

        # 左侧属性面板
        self.property_panel_dock = QDockWidget('Property', self)
        self.property_panel_dock.setWidget(PropertyPanel())
        self.property_panel_dock.setFloating(False)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.property_panel_dock)

        # 右侧面板
        self.scene_panel_dock = QDockWidget('Scene', self)
        self.scene_panel_dock.setWidget(ScenePanel())
        self.scene_panel_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.scene_panel_dock)

        # draw order panel
        self.draw_order_panel_dock = QDockWidget('draw order', self)
        self.draw_order_panel_dock.setWidget(DrawOrderPanel())
        self.draw_order_panel_dock.setFloating(False)
        self.tabifyDockWidget(self.scene_panel_dock, self.draw_order_panel_dock)

        # library panel
        self.library_panel_dock = QDockWidget('library', self)
        self.library_panel_dock.setWidget(LibraryPanel())
        self.library_panel_dock.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.library_panel_dock)

    def onMyToolBarButtonClick(self, s):
        print("click", s)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
