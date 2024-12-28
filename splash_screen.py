from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import os
import sys
import requests
import hashlib
import subprocess

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing SplashScreen...")  # Debug message

        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        background_path = os.path.join("assets", "images", "test6.png")
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

        # Initialize UpdateWorker and connect signals
        self.worker = UpdateWorker()
        self.worker.update_progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_update_complete)
        self.worker.start()
        print("UpdateWorker started.")  # Debug message

        print("SplashScreen initialized.")  # Debug message

    def update_progress(self, progress, message):
        print(f"Progress updated: {progress}, Message: {message}")  # Debugging progress
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
            print("Update completed. Attempting to launch main.py...")  # Debug message

            # Attempt to launch main.py
            try:
                main_path = os.path.join(os.getcwd(), "main.py")
                if not os.path.exists(main_path):
                    print(f"main.py not found at {main_path}")
                    return

                # Print debug information
                print(f"Using Python executable: {sys.executable}")
                print(f"Launching main.py from: {main_path}")

                # Use subprocess to execute main.py
                import subprocess
                result = subprocess.run([sys.executable, main_path], capture_output=True, text=True)

                # Log stdout and stderr
                print("stdout:", result.stdout)
                print("stderr:", result.stderr)
            except Exception as e:
                print(f"Failed to launch main.py: {e}")

            # Keep splash screen open for debugging
            self.status_label.setText("main.py execution attempt complete. Check logs.")
            print("Splash screen will remain open for debugging.")


            


class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)  # Signal whether a restart is required

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def run(self):
        print("UpdateWorker started...")  # Debug message

        try:
            print("Fetching manifest...")
            manifest = self.fetch_manifest()
            if not manifest:
                print("No manifest available. Skipping update check.")
                self.update_progress.emit(0, "Manifest fetch failed.")
                self.finished.emit(False)
                return

            print("Manifest fetched successfully.")
            self.update_progress.emit(10, "Manifest fetched successfully.")

            print("Checking for updates...")
            files_to_update = self.check_for_updates(manifest)
            total_files = len(files_to_update)

            if total_files == 0:
                print("No updates required.")
                self.update_progress.emit(100, "No updates found.")
                self.finished.emit(False)
                return

            print(f"Files to update: {total_files}")

            for i, file in enumerate(files_to_update, start=1):
                print(f"Updating {file['name']}...")
                self.update_progress.emit(
                    int((i / total_files) * 100), f"Updating {file['name']}..."
                )
                self.download_file(file)

            self.update_progress.emit(100, "Updates complete!")
            self.finished.emit(any(file["name"] == "main.py" for file in files_to_update))
        except Exception as e:
            print(f"Error in UpdateWorker: {e}")
            self.update_progress.emit(0, f"Error: {e}")
            self.finished.emit(False)

    def fetch_manifest(self):
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching manifest: {e}")
            return None

    def check_for_updates(self, manifest):
        updates = []
        for file in manifest.get("files", []):
            local_path = os.path.join(os.getcwd(), file["name"])
            if not os.path.exists(local_path):
                updates.append(file)
        return updates

    def download_file(self, file):
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
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
