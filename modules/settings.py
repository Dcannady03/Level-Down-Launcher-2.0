from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Settings Page"))
        self.setLayout(layout)
