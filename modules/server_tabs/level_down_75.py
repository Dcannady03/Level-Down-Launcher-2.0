from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class LevelDown75Tab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Level Down 75 - Login and Auction House"))
        self.setLayout(layout)
