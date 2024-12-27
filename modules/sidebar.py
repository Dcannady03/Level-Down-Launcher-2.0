from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox, QFileDialog, QApplication
import os
import json
import subprocess
import sys


class Sidebar(QWidget):
    SETTINGS_FILE = "settings.json"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.settings = self.load_settings()

        layout = QVBoxLayout()

        # Add buttons with images and labels
        self.add_image_button_with_label(
            layout,
            self.resource_path("assets/images/ashita.png"),
            self.resource_path("assets/images/ashitatxt.png"),
            self.launch_ashita,
        )
        self.add_image_button_with_label(
            layout,
            self.resource_path("assets/images/windower.png"),
            self.resource_path("assets/images/windowertxt.png"),
            self.launch_windower,
        )
        self.add_image_button_with_label(
            layout,
            self.resource_path("assets/images/wiki.png"),
            self.resource_path("assets/images/wikitxt.png"),
            self.open_wiki,
        )

        self.setLayout(layout)
        self.setFixedWidth(150)

    @staticmethod
    def resource_path(relative_path):
        """Get the absolute path to a resource, works for both dev and PyInstaller."""
        if getattr(sys, "frozen", False):  # If running as a PyInstaller bundle
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

    def add_image_button_with_label(self, layout, image_path, label_image_path, callback):
        """Create an image button with a label and an additional image label."""
        container = QWidget()
        container_layout = QVBoxLayout()

        # Main Button Image
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("Image Missing")
            image_label.setStyleSheet("color: red;")
            print(f"Image not found: {image_path}")

        container_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label Image
        label_image = QLabel()
        label_pixmap = QPixmap(label_image_path)
        if not label_pixmap.isNull():
            scaled_label_pixmap = label_pixmap.scaled(100, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label_image.setPixmap(scaled_label_pixmap)
        else:
            label_image.setText("Label Missing")
            label_image.setStyleSheet("color: red;")
            print(f"Label image not found: {label_image_path}")

        container_layout.addWidget(label_image, alignment=Qt.AlignmentFlag.AlignCenter)

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
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def launch_executable(self, dir_key, exe_key, default_message):
        """Launch a user-specified executable or show a message if it's missing."""
        exe_path = self.settings.get(exe_key)  # Full path to the executable
        dir_path = self.settings.get(dir_key)  # Directory containing the executable

        if exe_path and os.path.exists(exe_path):
            try:
                # Ensure the working directory is set to the executable's directory
                working_dir = dir_path if dir_path and os.path.exists(dir_path) else os.path.dirname(exe_path)

                # Launch the executable
                subprocess.Popen([exe_path], cwd=working_dir, shell=True)
                print(f"Successfully launched {exe_path} with working directory {working_dir}.")

                # Close the launcher if required
                if self.settings.get("close_after_launch", False):
                    print("Close after launch is enabled. Closing launcher.")
                    QApplication.quit()
            except Exception as e:
                self.show_popup(f"Failed to launch {exe_path}: {e}")
                print(f"Error launching executable: {e}")  # Debug log
        else:
            self.show_popup(default_message)

    def launch_ashita(self):
        """Launch the executable specified for Ashita."""
        self.launch_executable(
            "ashita_dir",
            "ashita_exe",
            "Ashita directory is not set in settings.json. Please configure it."
        )

    def launch_windower(self):
        """Launch the executable specified for Windower."""
        self.launch_executable(
            "windower_dir",
            "windower_exe",
            "Windower directory is not set in settings.json. Please configure it."
        )

    def open_wiki(self):
        """Open the Wiki URL."""
        wiki_url = "https://ffxileveldown.fandom.com/wiki/FFXILevelDown_Wiki"
        QDesktopServices.openUrl(QUrl(wiki_url))
