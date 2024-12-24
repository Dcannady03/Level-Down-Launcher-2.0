from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QWidget
from modules.sidebar import Sidebar
from modules.dashboard import Dashboard
from modules.server_tabs.level_down_99 import LevelDown99Tab
from modules.server_tabs.level_down_75 import LevelDown75Tab
from modules.server_tabs.level_down_75_era import LevelDown75ERATab
from modules.settings import Settings


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing Launcher...")  # Debug message
        self.setWindowTitle("Level Down Launcher 2.0")
        self.setGeometry(100, 100, 800, 600)

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

    def create_tabs(self):
        print("Creating tabs...")  # Debug message
        tabs = QTabWidget()

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

        return tabs

