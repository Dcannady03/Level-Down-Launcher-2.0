from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")  # For QSS styling

        layout = QVBoxLayout()

        # Add buttons with images and labels
        self.add_button_with_label(
            layout, "assets/images/ashita.png", "assets/images/ashitatxt.png", self.launch_ashita
        )
        self.add_button_with_label(
            layout, "assets/images/wiki.png", "assets/images/wikitxt.png", self.open_wiki
        )
        self.add_button_with_label(
            layout, "assets/images/windower.png", "assets/images/windowertxt.png", self.launch_windower
        )

        # Add XI Updater Button
        self.add_button_with_label(
            layout, "assets/images/xiupdater.png", "assets/images/xiupdatetxt.png", self.launch_xi_updater
        )

        self.setLayout(layout)
        self.setFixedWidth(125)  # Adjust sidebar width if needed

    def add_button_with_label(self, layout, button_img, label_img, callback):
        """Helper function to add an image button with a label."""
        # Button with image
        btn = QPushButton()
        btn.setCursor(Qt.PointingHandCursor)  # Hand cursor for clickable buttons
        btn.setFlat(True)  # Remove button borders
        btn.setIcon(QIcon(button_img))
        btn.setIconSize(QSize(100, 100))  # Adjust button size
        btn.clicked.connect(callback)

        # Label with image
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(120, 40)  # Set the label size (width, height)
        label_pixmap = QPixmap(label_img).scaled(label.width(), label.height(), Qt.KeepAspectRatio)
        label.setPixmap(label_pixmap)

        # Add button and label to layout
        layout.addWidget(btn)
        layout.addWidget(label)

    def launch_ashita(self):
        print("Launching Ashita...")

    def open_wiki(self):
        print("Opening Wiki...")

    def launch_windower(self):
        print("Launching Windower...")

    def launch_xi_updater(self):
        print("Launching XI Updater...")

