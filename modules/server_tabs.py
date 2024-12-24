from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class ServerTabs(QWidget):
    def __init__(self, server_name):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"{server_name} - Login and Auction House"))
        self.setLayout(layout)
