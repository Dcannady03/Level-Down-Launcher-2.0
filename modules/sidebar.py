from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
import os
import json
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
import subprocess  # For launching executables
import sys


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")

        layout = QVBoxLayout()

        # Add buttons with images and labels
        self.add_image_button_with_label(
            layout,
            "assets/images/ashita.png",
            "assets/images/ashitatxt.png",
            self.launch_ashita,
        )
        self.add_image_button_with_label(
            layout,
            "assets/images/windower.png",
            "assets/images/windowertxt.png",
            self.launch_windower,
        )
        self.add_image_button_with_label(
            layout,
            "assets/images/wiki.png",
            "assets/images/wikitxt.png",
            self.open_wiki,
        )

        self.setLayout(layout)
        self.setFixedWidth(150)

    def add_image_button_with_label(self, layout, image_path, label_image_path, callback):
        """Create an image button with a label and an additional image label."""
        container = QWidget()
        container_layout = QVBoxLayout()

        # Main Button Image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("Image Missing")
            image_label.setStyleSheet("color: red;")
        container_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Label Image
        label_image = QLabel()
        label_pixmap = QPixmap(label_image_path)
        if not label_pixmap.isNull():
            scaled_label_pixmap = label_pixmap.scaled(100, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label_image.setPixmap(scaled_label_pixmap)
        else:
            label_image.setText("Label Missing")
            label_image.setStyleSheet("color: red;")
        container_layout.addWidget(label_image, alignment=Qt.AlignCenter)

        # Clickable Button
        btn = QPushButton()
        btn.setFixedSize(120, 150)  # Adjust button size to fit main image and label
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 50%);  /* Light green hover */
            }
        """)
        btn.clicked.connect(callback)
        btn.setLayout(container_layout)

        layout.addWidget(btn)

    def show_popup(self, message):
        """Show a popup message."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Directory Not Set")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def load_settings(self):
        """Load settings from settings.json file."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
        return {}

    def launch_executable(self, directory, executable_name):
        """Launch the executable if the directory is valid."""
        executable_path = os.path.join(directory, executable_name)
        if os.path.exists(executable_path):
            subprocess.Popen([executable_path])
        else:
            self.show_popup(f"The executable '{executable_name}' was not found in the directory:\n{directory}")

    def launch_ashita(self):
        settings = self.load_settings()
        ashita_dir = settings.get("ashita_dir")
        if not ashita_dir:
            self.show_popup("Please set the directory for Ashita in the Settings tab.")
        else:
            self.launch_executable(ashita_dir, "Ashita.exe")

    def launch_windower(self):
        settings = self.load_settings()
        windower_dir = settings.get("windower_dir")
        if not windower_dir:
            self.show_popup("Please set the directory for Windower in the Settings tab.")
        else:
            self.launch_executable(windower_dir, "Windower.exe")

    def open_wiki(self):
        """Open the Wiki URL."""
        wiki_url = "https://ffxileveldown.fandom.com/wiki/FFXILevelDown_Wiki"
        QDesktopServices.openUrl(QUrl(wiki_url))
