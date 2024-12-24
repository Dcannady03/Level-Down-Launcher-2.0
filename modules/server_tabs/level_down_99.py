from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class LevelDown99Tab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Level Down 99 - Login and Auction House"))
        self.setLayout(layout)
