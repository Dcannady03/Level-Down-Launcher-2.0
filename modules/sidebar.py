from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton
import os


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        buttons = [
            ("Ashita Launcher", self.launch_ashita),
            ("Windower Launcher", self.launch_windower),
            ("WIKI", self.open_wiki),
            ("XI Updater", self.open_updater),
            ("Settings", self.open_settings),
        ]

        for name, callback in buttons:
            btn = QPushButton(name)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        self.setLayout(layout)
        self.setFixedWidth(200)

    def launch_ashita(self):
        print("Launching Ashita...")  # Replace with actual logic

    def launch_windower(self):
        print("Launching Windower...")  # Replace with actual logic

    def open_wiki(self):
        print("Opening WIKI...")  # Replace with actual logic

    def open_updater(self):
        print("Opening XI Updater...")  # Replace with actual logic

    def open_settings(self):
        print("Opening Settings...")
