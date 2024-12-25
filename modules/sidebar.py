from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
import os
import json
import ctypes
import subprocess
import sys


class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")

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
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("Image Missing")
            image_label.setStyleSheet("color: red;")
            print(f"Image not found: {image_path}")  # Debugging

        container_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Label Image
        label_image = QLabel()
        label_pixmap = QPixmap(label_image_path)
        if not label_pixmap.isNull():
            scaled_label_pixmap = label_pixmap.scaled(100, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label_image.setPixmap(scaled_label_pixmap)
        else:
            label_image.setText("Label Missing")
            label_image.setStyleSheet("color: red;")
            print(f"Label image not found: {label_image_path}")  # Debugging

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
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def load_settings(self):
        """Load settings from settings.json file."""
        settings_path = self.resource_path("settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r") as f:
                return json.load(f)
        return {}

    def launch_executable(self, directory, executable_name):
        """Launch the executable with elevated privileges if required."""
        executable_path = os.path.join(directory, executable_name)

        if os.path.exists(executable_path):
            try:
                # Elevate the process
                response = ctypes.windll.shell32.ShellExecuteW(None, "runas", executable_path, None, None, 1)
                if response <= 32:
                    raise OSError(f"Failed to launch {executable_name} with elevation.")
                print(f"Successfully launched {executable_name} with elevation.")
            except Exception as e:
                self.show_popup(f"Failed to launch {executable_name}: {e}")
                print(f"Error launching {executable_name}: {e}")
        else:
            self.show_popup(f"The executable '{executable_name}' was not found in the directory:\n{directory}")
            print(f"Executable not found: {executable_path}")

    def launch_ashita(self):
        """Launch Ashita with the settings directory."""
        settings = self.load_settings()
        ashita_dir = settings.get("ashita_dir")
        close_after_launch = settings.get("close_after_launch", False)

        if not ashita_dir:
            self.show_popup("Please set the directory for Ashita in the Settings tab.")
        else:
            self.launch_executable(ashita_dir, "Ashita.exe")
            if close_after_launch:
                self.parentWidget().close()  # Close the launcher

    def launch_windower(self):
        """Launch Windower with the settings directory."""
        settings = self.load_settings()
        windower_dir = settings.get("windower_dir")
        close_after_launch = settings.get("close_after_launch", False)

        if not windower_dir:
            self.show_popup("Please set the directory for Windower in the Settings tab.")
        else:
            self.launch_executable(windower_dir, "Windower.exe")
            if close_after_launch:
                self.parentWidget().close()  # Close the launcher

    def open_wiki(self):
        """Open the Wiki URL."""
        wiki_url = "https://ffxileveldown.fandom.com/wiki/FFXILevelDown_Wiki"
        QDesktopServices.openUrl(QUrl(wiki_url))
