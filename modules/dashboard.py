from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard - Displaying RSS Updates"))
        self.setLayout(layout)
