from PySide6.QtWidgets import QLabel, QWidget


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