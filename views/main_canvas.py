from PySide6.QtWidgets import (
    QTabWidget,
)

from views.canvas_tab_item import CanvasTabItem


class MainCanvas(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cur_tab = CanvasTabItem()
        self.setMovable(True)
        self.addTab(self._cur_tab, "111")
        self.setStyleSheet('''QTabWidget::tab-bar {
    left: 0; 
}''')
        # self.setCurrentIndex(1)
        # self.addTab(QLabel("bbbb"), "222")

    @property
    def cur_tab(self):
        return self._cur_tab

    @cur_tab.setter
    def cur_tab(self, value):
        self._cur_tab = value
