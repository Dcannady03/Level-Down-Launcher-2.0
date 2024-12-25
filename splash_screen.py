import os
import sys
import shutil
import requests
import hashlib
import subprocess
import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPixmap, QFont
import atexit  # Import atexit for cleanup

# Function to resolve resource paths dynamically
def resource_path(relative_path):
    """Get the absolute path to a resource, works for both dev and PyInstaller."""
    if getattr(sys, "frozen", False):  # If running as a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

# Register a cleanup function to avoid errors
def cleanup_temp():
    temp_dir = getattr(sys, '_MEIPASS', None)
    if temp_dir and os.path.isdir(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Failed to cleanup temp dir {temp_dir}: {e}")

atexit.register(cleanup_temp)  # Register the cleanup function

def apply_dark_theme(app):
    """Load and apply the dark theme stylesheet."""
    theme_path = resource_path(os.path.join("assets", "styles", "dark_theme.qss"))
    print(f"Resolving theme path: {theme_path}")  # Debug path
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as file:
                app.setStyleSheet(file.read())
            print(f"Dark theme loaded successfully from {theme_path}")
        except Exception as e:
            print(f"Error loading dark theme: {e}")
    else:
        print(f"Dark theme file not found at {theme_path}. Using default styles.")

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        background_path = resource_path(os.path.join("assets", "images", "test6.png"))
        print(f"Resolving background image path: {background_path}")  # Debug path
        pixmap = QPixmap(background_path)
        if not pixmap.isNull():
            self.background.setPixmap(pixmap)
            self.background.setScaledContents(True)
            self.background.setGeometry(0, 0, 600, 400)
        else:
            print(f"Error loading background image from {background_path}")

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
        self.worker = UpdateWorker()
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
            self.restart_application()
        else:
            self.status_label.setText("Launching application...")
            time.sleep(2)  # Add a delay before switching to the launcher
            self.load_main_window()

    def restart_application(self):
        """Restart the current application."""
        try:
            executable = sys.executable
            print(f"Restarting application with executable: {executable}")  # Debug
            subprocess.Popen([executable] + sys.argv, close_fds=True)
            sys.exit(0)  # Exit the current process
        except Exception as e:
            print(f"Failed to restart application: {e}")
            self.status_label.setText("Error restarting application. Please restart manually.")

    def load_main_window(self):
        try:
            from launcher import Launcher
            self.hide()
            self.main_window = Launcher()
            self.main_window.show()
        except Exception as e:
            print(f"Error loading launcher: {e}")



class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)  # Signal whether a restart is required

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"
    SKIP_FOLDERS = [".git", ".vs", "__pycache__"]
    SKIP_FILES = ["manifest.py", "manifest.json", ".gitattributes", ".gitignore", "settings.json"]

    def run(self):
        print("UpdateWorker started...")  # Debug message

        try:
            # Step 1: Fetch the manifest
            manifest = self.fetch_manifest()
            if not manifest:
                self.update_progress.emit(0, "Failed to fetch manifest.")
                self.finished.emit(False)
                return

            # Step 2: Check for updates
            files_to_update = self.check_for_updates(manifest)
            total_files = len(files_to_update)

            # Determine if a restart is required
            restart_required = any(file["name"] == "main.py" for file in files_to_update)

            if total_files == 0:
                print("No updates found. All files are up to date.")  # Debug message
                self.update_progress.emit(100, "No updates found.")
                self.finished.emit(False)  # No restart required
                return

            print(f"Files to update: {total_files}")  # Debug message

            # Step 3: Apply updates
            for i, file in enumerate(files_to_update, start=1):
                self.update_progress.emit(
                    int((i / total_files) * 100), f"Updating {file['name']}..."
                )
                self.download_file(file)

            # Step 4: Finalize
            self.update_progress.emit(100, "Updates complete!")
            print("UpdateWorker finished successfully.")  # Debug message
            self.finished.emit(restart_required)
        except Exception as e:
            print(f"Critical error in UpdateWorker: {e}")  # Debug message
            self.update_progress.emit(0, f"Critical error: {e}")
            self.finished.emit(False)

    def fetch_manifest(self):
        """Fetch the manifest from the URL."""
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            print("Manifest fetched successfully.")
            return response.json()
        except Exception as e:
            print(f"Error fetching manifest: {e}")
            return None

    def calculate_checksum(self, file_path):
        """Calculate the checksum of a local file using MD5."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def check_for_updates(self, manifest):
        """Check for files that need updates."""
        updates = []
        for file in manifest.get("files", []):
            local_path = os.path.join(os.getcwd(), file["name"])

            # Skip specified folders and files
            if any(skip in local_path for skip in self.SKIP_FOLDERS) or os.path.basename(local_path) in self.SKIP_FILES:
                print(f"Skipping: {local_path}")  # Debug message
                continue

            if not os.path.exists(local_path):
                print(f"File missing: {file['name']}")  # Debug message
                updates.append(file)
            else:
                # Compare checksums
                local_checksum = self.calculate_checksum(local_path)
                if local_checksum != file["checksum"]:
                    print(f"Checksum mismatch for: {file['name']}")  # Debug message
                    updates.append(file)
                else:
                    print(f"File up to date: {file['name']}")  # Debug message
        return updates

    def download_file(self, file):
        """Download a file from the manifest."""
        local_path = os.path.join(os.getcwd(), file["name"])
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)  # Apply the dark theme before showing any UI
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
