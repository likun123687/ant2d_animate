import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtGui import QPalette, QColor
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStackedLayout, QToolBar, QStatusBar, \
    QGraphicsItemGroup
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsLineItem, QGraphicsItem


# class AAA(QGraphicsRectItem):
#     def __init__(self, x, y, width, height, parent=None):
#         super().__init__(x, y, width, height, parent)
#         self.setAcceptHoverEvents(True)
#
#     def hoverEnterEvent(self, event) -> None:
#         print("hover enter")
#
#     def hoverLeaveEvent(self, event) -> None:
#         print("hover leave")
#
#     # def setPos(self, x, y):
#     #     rect = self.boundingRect()
#     #     offset = rect.center()
#     #     super().moveBy(x - offset.x(), y - offset.y())

class BBB(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event) -> None:
        print("hover item group enter")

    def hoverLeaveEvent(self, event) -> None:
        print("hover item group leave\n")

class CustomQGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

class CustomScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setMinimumSize(QSize(800, 600))

        # Defining a scene rect of 400x200, with it's origin at 0,0.
        # If we don't set this on creation, we can set it later with .setSceneRect
        self.scene = CustomScene(0, 0, 400, 200)

        # Draw a rectangle item, setting the dimensions.
        self.rect = QGraphicsRectItem(0, 0, 50, 50)
        # Set the origin (position) of the rectangle in the scene.
        self.rect.setPos(0, 0)

        self.group = BBB()
        self.group.addToGroup(self.rect)

        self.rect2 = QGraphicsRectItem(0, 0, 50, 50)
        # Set the origin (position) of the rectangle in the scene.
        self.rect2.setPos(0, 0)

        self.rect1 = QGraphicsRectItem(0, 0, 50, 50)
        # Set the origin (position) of the rectangle in the scene.
        self.rect1.setPos(100, 0)

        self.line = QGraphicsLineItem()
        self.line.setLine(0, 0, 100, 100)

        self.line1 = QGraphicsLineItem(self.rect1)
        self.line1.setLine(10, 10, 60, 60)
        pen = QPen(Qt.cyan)
        pen.setWidth(2)
        self.line1.setPen(pen)

        self.rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.rect1.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.line.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.line1.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        # ring = QGraphicsEllipseItem(QRectF(0,0, 10, 10))
        # polygon_item = QGraphicsPolygonItem(QPolygonF(QRectF(-10, -10, 50, 50)), ring)
        # polygon_item.setPen(pen)

        ## Define the brush (fill).
        # brush = QBrush(Qt.red)
        # rect.setBrush(brush)

        ## Define the pen (self.line)
        # pen = QPen(Qt.cyan)
        # pen.setWidth(10)
        # rect.setPen(pen)

        self.scene.addItem(self.group)
        # self.scene.addItem(self.rect1)
        # self.scene.addItem(self.rect2)
        # self.scene.addItem(self.line)
        # self.scene.addItem(self.line1)
        # self.scene.addItem(polygon_item)
        # self.scene.addItem(ring)

        self.view = CustomQGraphicsView(self.scene)
        self.view.setAutoFillBackground(True)
        palette = self.view.palette()
        palette.setColor(QPalette.Window, QColor('blue'))
        self.view.setPalette(palette)

        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setMovable(True)
        self.tabs.addTab(self.view, "111")
        print(self.view.size())

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

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print("rect", self.rect.pos(), self.rect.scenePos())
            print("line", self.line.pos(), self.line.scenePos())
            print("rect1", self.rect1.pos(), self.rect1.scenePos())
            print("line1", self.line1.pos(), self.line1.scenePos())
            print("rect2", self.rect2.pos(), self.rect2.scenePos())
            print("=================")
        super().mousePressEvent(event)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
