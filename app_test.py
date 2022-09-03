import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QApplication

from views.time_line.time_line import TimeLineView
from views.time_line_bak.track_view import TrackView
from views.time_line_bak.top_bar import TopBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(1000, 800))
        self.setWindowTitle("app test")
        # top_bar = TopBar()
        # self.setCentralWidget(top_bar)
        time_line = TimeLineView()
        self.setCentralWidget(time_line)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
