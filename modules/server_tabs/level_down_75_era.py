from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class LevelDown75ERATab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Level Down 75 ERA - Login and Auction House"))
        self.setLayout(layout)