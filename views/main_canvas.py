from PySide6.QtWidgets import (
    QTabWidget,
)

from views.canvas_tab_item import CanvasTabItem


class MainCanvas(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # tabs = QtWidgets.QTabWidget(self)
        self.setMovable(True)
        self.addTab(CanvasTabItem(), "111")
        self.setStyleSheet('''QTabWidget::tab-bar {
    left: 0; 
}''')
        # self.setCurrentIndex(1)
        # self.addTab(QLabel("bbbb"), "222")
