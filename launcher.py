from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QWidget
from PyQt5.QtGui import QPixmap, QPainter
from modules.sidebar import Sidebar
from modules.dashboard import Dashboard
#from modules.server_tabs.level_down_99 import LevelDown99Tab
#from modules.server_tabs.level_down_75 import LevelDown75Tab
#from modules.server_tabs.level_down_75_era import LevelDown75ERATab
from modules.settings import Settings
from PyQt5.QtCore import Qt
from modules.xi_updater import XIUpdaterTab  # Or XIUpdaterWindow if that's the class name


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing Launcher...")  # Debug message
        self.setWindowTitle("Level Down Launcher")
        self.setGeometry(100, 100, 1100, 760)

        # Store the wallpaper path
        self.wallpaper_path = "assets/images/wallpaper3.png"

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

    def paintEvent(self, event):
        """Override paintEvent to draw the wallpaper."""
        painter = QPainter(self)
        background = QPixmap(self.wallpaper_path)

        if background.isNull():
            print(f"Error: Background image '{self.wallpaper_path}' not loaded.")
        else:
            # Scale the image to completely fill the window
            scaled_background = background.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_background)


    def create_tabs(self):
        tabs = QTabWidget()

        tabs.addTab(Dashboard(), "Dashboard")
        #tabs.addTab(LevelDown99Tab(), "Level Down 99")
        #tabs.addTab(LevelDown75Tab(), "Level Down 75")
        #tabs.addTab(LevelDown75ERATab(), "Level Down 75 ERA")
        tabs.addTab(XIUpdaterTab(), "XI Updater")  # Add the updater tab
        tabs.addTab(Settings(), "Settings")

        return tabs

