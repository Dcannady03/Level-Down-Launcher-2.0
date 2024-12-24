from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class SplashScreen(QMainWindow):
    def __init__(self, updater):
        super().__init__()
        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        pixmap = QPixmap(r"I:\git\Level-Down-Launcher-2.0\assets\images\test6.png")
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
        overlay_widget.setGeometry(50, 250, 500, 100)

        # Start the update process
        self.worker = UpdateWorker(updater)
        self.worker.update_progress.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, progress, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)
class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)

    def __init__(self, updater):
        super().__init__()
        self.updater = updater

    def run(self):
        # Use the updater to check and apply updates
        steps = self.updater.get_update_steps()
        total_steps = len(steps)

        for index, (message, progress_func) in enumerate(steps, start=1):
            self.update_progress.emit(int((index / total_steps) * 100), message)
            progress_func()  # Perform the update step