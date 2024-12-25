from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QIcon  # For setting background
from PyQt5.QtCore import Qt
import os
from modules.sidebar import Sidebar
from modules.dashboard import Dashboard
from modules.server_tabs.level_down_99 import LevelDown99Tab
from modules.server_tabs.level_down_75 import LevelDown75Tab
from modules.server_tabs.level_down_75_era import LevelDown75ERATab
from modules.settings import Settings
from modules.xi_updater import XIUpdaterTab  # Assuming XI Updater tab exists
import sys

def resource_path(relative_path):
    """Get the absolute path to a resource, works for both dev and PyInstaller."""
    if getattr(sys, "frozen", False):  # If running as a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            print("Setting up Launcher...")
            # Existing code
            print("Launcher setup complete.")
        except Exception as e:
            print(f"Error initializing Launcher: {e}")

        # Set application icon
        icon_path = resource_path(os.path.join("assets", "images", "test6.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            print(f"Launcher icon set from {icon_path}")
        else:
            print(f"Launcher icon not found: {icon_path}")

        self.setWindowTitle("Level Down Launcher")
        self.setGeometry(100, 100, 800, 600)

        # Set the background image
        background_path = resource_path("assets/images/wallpaper3.png")
        self.set_background(background_path)

        # Main layout
        main_layout = QHBoxLayout()
        self.sidebar = Sidebar(self)
        self.tabs = self.create_tabs()

        # Add widgets to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.tabs)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        print("Launcher initialized successfully.")  # Debug message

    def set_background(self, image_path):
        """Set the background image for the launcher."""
        if os.path.exists(image_path):
            palette = QPalette()
            pixmap = QPixmap(image_path).scaled(
                self.size(), 
                Qt.IgnoreAspectRatio, 
                Qt.SmoothTransformation
            )
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            print(f"Background image set from {image_path}")  # Debug message
        else:
            print(f"Background image not found: {image_path}")  # Debug message

    def create_tabs(self):
        """Create the main tabs for the launcher."""
        print("Creating tabs...")  # Debug message
        tabs = QTabWidget()

        try:
            # Add Dashboard Tab
            tabs.addTab(Dashboard(), "Dashboard")
            print("Dashboard tab added.")  # Debug message

            # Add Server Tabs
            tabs.addTab(LevelDown99Tab(), "Level Down 99")
            tabs.addTab(LevelDown75Tab(), "Level Down 75")
            tabs.addTab(LevelDown75ERATab(), "Level Down 75 ERA")
            print("Server tabs added.")  # Debug message

            # Add Settings Tab
            tabs.addTab(Settings(), "Settings")
            print("Settings tab added.")  # Debug message

            # Add XI Updater Tab
            tabs.addTab(XIUpdaterTab(), "XI Updater")
            print("XI Updater tab added.")  # Debug message
        except Exception as e:
            print(f"Error creating tabs: {e}")  # Debug message

        return tabs
