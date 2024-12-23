from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QProgressBar, QWidget, QApplication
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import sys
import requests
import time


# Worker Thread for Simulating Updates
class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)

    def run(self):
        # Simulated update process
        steps = [
            ("Checking for updates...", 20),
            ("Downloading manifest...", 40),
            ("Downloading files...", 70),
            ("Finalizing update...", 100),
        ]
        for message, progress in steps:
            self.update_progress.emit(progress, message)
            time.sleep(1)  # Simulate time for each step


# Splash Screen with Image
class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        pixmap = QPixmap("path_to_your_image.jpg")  # Replace with your image path
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)

        # Overlay Layout
        self.overlay = QVBoxLayout()

        # Status Label
        self.status_label = QLabel("Initializing...")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #222;
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
            }
        """)

        # Add widgets to layout
        self.overlay.addWidget(self.status_label)
        self.overlay.addWidget(self.progress_bar)

        # Central Widget for Overlay
        overlay_widget = QWidget(self)
        overlay_widget.setLayout(self.overlay)
        overlay_widget.setGeometry(50, 250, 500, 100)  # Adjust position of overlay

        # Start the update process
        self.worker = UpdateWorker()
        self.worker.update_progress.connect(self.update_progress)
        self.worker.start()

        # Finish signal to close splash screen
        self.worker.finished.connect(self.load_main_window)

    def update_progress(self, progress, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def load_main_window(self):
        # Close splash and load main application
        self.close()
        main_window = Launcher()
        main_window.show()


# Main Application Window Placeholder
class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Down Launcher 2.0")
        self.setGeometry(100, 100, 800, 600)
        self.status = QLabel("Main Launcher")
        self.status.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.status)


# Main Function
def main():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
