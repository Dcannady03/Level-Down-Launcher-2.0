from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
import os
import sys


class SplashScreen(QMainWindow):
    def __init__(self, updater):
        super().__init__()
        self.updater = updater

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
        self.status_label = QLabel("Initializing updates...")
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
        self.worker = UpdateWorker(self.updater)
        self.worker.update_progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_update_complete)
        self.worker.start()

    def update_progress(self, progress, message):
        """Update progress bar and status label."""
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_update_complete(self, restart_required):
        """Handle completion of updates."""
        if restart_required:
            print("main.exe updated. Restarting application...")
            python_executable = sys.executable
            script_path = sys.argv[0]
            os.execv(python_executable, [python_executable, script_path])
        else:
            self.load_main_window()

    def load_main_window(self):
        """Transition to the main launcher."""
        from modules.launcher import Launcher  # Import here to avoid circular imports
        self.hide()  # Hide the splash screen
        self.main_window = Launcher()  # Initialize the launcher
        self.main_window.show()  # Show the launcher window


from PyQt5.QtCore import QThread, pyqtSignal

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