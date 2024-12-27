from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import os
import sys
import requests
import hashlib

def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and PyInstaller."""
    if hasattr(sys, "_MEIPASS"):  # Running in PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing SplashScreen...")  # Debug message

        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        background_path = resource_path("assets/images/test6.png")
        if not os.path.exists(background_path):
            print(f"Background image not found: {background_path}")  # Debug error
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
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        print("SplashScreen initialized.")  # Debug message

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

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def run(self):
        print("UpdateWorker started...")  # Debug message

        try:
            # Fetch the manifest
            manifest = self.fetch_manifest()
            if not manifest:
                print("No manifest available. Skipping update check.")
                self.finished.emit(False)
                return

            # Check for updates
            files_to_update = self.check_for_updates(manifest)
            total_files = len(files_to_update)

            restart_required = any(file["name"] == "main.py" for file in files_to_update)

            if total_files > 0:
                print(f"Files to update: {total_files}")  # Debug message

                # Apply updates with progress tracking
                for i, file in enumerate(files_to_update, start=1):
                    self.update_progress.emit(
                        int((i / total_files) * 100), f"Updating {file['name']}..."
                    )
                    self.download_file(file)

            self.update_progress.emit(100, "Updates complete!")
            print("UpdateWorker finished.")  # Debug message

            # Emit finished signal
            self.finished.emit(restart_required)
        except Exception as e:
            print(f"Error in UpdateWorker: {e}")
            self.update_progress.emit(0, f"Error: {e}")
            self.finished.emit(False)

    def fetch_manifest(self):
        try:
            response = requests.get(self.MANIFEST_URL, timeout=10)
            response.raise_for_status()
            manifest = response.json()
            if not isinstance(manifest, dict) or "files" not in manifest:
                raise ValueError("Invalid manifest format.")
            print("Manifest fetched and validated successfully.")
            return manifest
        except Exception as e:
            print(f"Error fetching or validating manifest: {e}")
            return None

    def calculate_checksum(self, file_path):
        """Calculate the checksum of a local file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def check_for_updates(self, manifest):
        """Check for files that need updates."""
        updates = []
        for file in manifest.get("files", []):
            # Define local_path to refer to the current directory
            local_path = os.path.join(os.path.dirname(__file__), file["name"])
            if not os.path.exists(local_path) or self.calculate_checksum(local_path) != file["checksum"]:
                updates.append(file)
        return updates

    def download_file(self, file):
        """Download a file from the manifest."""
        # Ensure local_path is properly defined
        local_path = os.path.join(os.path.dirname(__file__), file["name"])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            response = requests.get(file["url"], stream=True)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Updated: {file['name']}")
        except Exception as e:
            print(f"Error downloading {file['name']}: {e}")

    def resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and PyInstaller."""
        if hasattr(sys, "_MEIPASS"):  # Running in PyInstaller bundle
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

if __name__ == "__main__":
    print("Starting splash screen...")  # Debug message
    app = QApplication(sys.argv)
    splash = SplashScreen()  # Create the splash screen
    splash.show()  # Show the splash screen
    sys.exit(app.exec_())  # Run the application event loop
