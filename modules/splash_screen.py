import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont


class SplashScreen(QMainWindow):
    def __init__(self, updater):
        super().__init__()
        self.updater = updater  # Store the updater instance

        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        pixmap = QPixmap(os.path.join(os.getcwd(), "assets/images/test6.png"))
        self.background = QLabel(self)
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
        self.worker.finished.connect(self.on_update_complete)  # Handle worker completion
        self.worker.start()

    def update_progress(self, progress, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_update_complete(self):
        print("Updates complete. Proceeding to the main application.")
        # Add logic to transition to the main application (e.g., hide splash screen).


class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)

    def __init__(self, updater):
        super().__init__()
        self.updater = updater

    def run(self):
        try:
            print("UpdateWorker started...")  # Debug message

            files_to_update = self.updater.check_for_updates()
            if files_to_update:
                print(f"Files to update: {len(files_to_update)}")  # Debug message
                for i, file in enumerate(files_to_update, start=1):
                    self.update_progress.emit(
                        10 + int((i / len(files_to_update)) * 80), f"Updating {file['name']}..."
                    )
                    self.updater.apply_updates([file])

            self.update_progress.emit(100, "Updates complete!")
            print("UpdateWorker finished.")  # Debug message
        except Exception as e:
            self.update_progress.emit(0, f"Error during updates: {e}")
            print(f"Error in UpdateWorker: {e}")
