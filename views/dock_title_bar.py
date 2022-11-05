from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class DockTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self._left_pm: Optional[QPixmap] = QPixmap("./bug.png")
        # self._center_pm: Optional[QPixmap] = QPixmap("./bug.png")
        # self._right_pm: Optional[QPixmap] = QPixmap("./bug.png")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        label1 = QLabel()
        label1.setPixmap(QPixmap('./bug.png'))
        label1.setText("aaaa")
        label1.setStyleSheet("background-color: yellow")
        layout.addWidget(label1)

        label2 = QLabel()
        label2.setPixmap(QPixmap('./bug.png'))
        label2.setStyleSheet("background-color: yellow")
        layout.addWidget(label2)

        layout.addStretch()

        label3 = QLabel()
        label3.setPixmap(QPixmap('./bug.png'))
        label3.setStyleSheet("background-color: yellow")
        layout.addWidget(label3)

        self.setLayout(layout)

