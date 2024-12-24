from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
import os
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    from modules.updater import Updater  # Import the updater
    updater = Updater(enable_updates=True)  # Enable updates

    splash = SplashScreen(updater)  # Create the splash screen
    splash.show()  # Show the splash screen

    sys.exit(app.exec_())  # Run the application event loop

class SplashScreen(QMainWindow):
    def __init__(self, updater):
        super().__init__()
        self.updater = updater  # Store the updater instance

        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        background_path = os.path.join("assets", "images", "test6.png")
        pixmap = QPixmap(background_path)
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
        self.worker.finished.connect(self.on_update_complete)
        self.worker.start()

    def update_progress(self, progress, message):
        """Update the progress bar and status label."""
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_update_complete(self, restart_required):
        """Handle the completion of the update process."""
        if restart_required:
            self.status_label.setText("Restarting application...")
            print("Restart required. Exiting splash screen.")  # Debug message
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            self.status_label.setText("Launching application...")
            print("Update completed. Ready to launch.")  # Debug message
            self.close()  # Close the splash screen


class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)  # Signal whether a restart is required

    def __init__(self, updater):
        super().__init__()
        self.updater = updater

    def run(self):
        print("UpdateWorker started...")  # Debug message

        try:
            # Check for updates
            files_to_update = self.updater.check_for_updates()
            total_files = len(files_to_update)

            restart_required = any(file["name"] == "main.exe" for file in files_to_update)

            if total_files > 0:
                print(f"Files to update: {total_files}")  # Debug message

                # Apply updates with progress tracking
                for i, file in enumerate(files_to_update, start=1):
                    self.update_progress.emit(
                        int((i / total_files) * 100), f"Updating {file['name']}..."
                    )
                    self.updater.download_file(file)

            self.update_progress.emit(100, "Updates complete!")
            print("UpdateWorker finished.")  # Debug message

            # Emit finished signal
            self.finished.emit(restart_required)
        except Exception as e:
            print(f"Error in UpdateWorker: {e}")
            self.update_progress.emit(0, f"Error: {e}")
            self.finished.emit(False)
