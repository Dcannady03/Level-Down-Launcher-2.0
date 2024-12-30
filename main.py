from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import os
import sys
import requests
import hashlib
import subprocess
import json

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing SplashScreen...")

        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        # Background Image
        self.background = QLabel(self)
        background_path = os.path.join("assets", "images", "test6.png")
        if not os.path.exists(background_path):
            print(f"Background image not found: {background_path}")
        pixmap = QPixmap(background_path)
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)
        self.background.setGeometry(0, 0, 600, 400)

        # Status and Progress
        self.status_label = QLabel("Initializing...")
        self.status_label.setFont(QFont("Arial", 14))
        self.status_label.setStyleSheet("color: white;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        overlay_widget = QWidget(self)
        overlay_widget.setLayout(layout)
        overlay_widget.setGeometry(50, 250, 500, 100)

        # Update Worker
        self.worker = UpdateWorker()
        self.worker.update_progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_update_complete)
        self.worker.start()
        print("UpdateWorker started.")

    def update_progress(self, progress, message):
        print(f"Progress updated: {progress}, Message: {message}")
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_update_complete(self, restart_required):
        """Handle completion of the update process."""
        self.status_label.setText("Launching application...")
        print("Update completed. Launching the launcher...")

        launcher_path = os.path.join(os.getcwd(), "launcher.py")
        if os.path.exists(launcher_path):
            subprocess.run([sys.executable, launcher_path])
        else:
            print("Launcher script not found. Exiting.")

        self.close()


class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def run(self):
        try:
            manifest = self.fetch_manifest()
            if not manifest:
                self.update_progress.emit(0, "Failed to fetch manifest.")
                self.finished.emit(False)
                return

            self.update_progress.emit(10, "Checking for updates...")
            files_to_update = self.check_for_updates(manifest)

            if not files_to_update:
                self.update_progress.emit(100, "No updates required.")
                self.finished.emit(False)
                return

            self.update_progress.emit(50, "Downloading updates...")
            for i, file in enumerate(files_to_update, start=1):
                self.download_file(file)
                self.update_progress.emit(50 + int((i / len(files_to_update)) * 50), f"Updating {file['name']}...")

            self.update_progress.emit(100, "Updates completed.")
            self.finished.emit(True if any(f['name'] == "launcher.py" for f in files_to_update) else False)

        except Exception as e:
            print(f"Error during update: {e}")
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
            if not os.path.exists(local_path) or self.calculate_checksum(local_path) != file["checksum"]:
                updates.append(file)
        return updates

    def calculate_checksum(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def download_file(self, file):
        local_path = os.path.join(os.getcwd(), file["name"])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            response = requests.get(file["url"], stream=True)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded and replaced: {file['name']}")
        except Exception as e:
            print(f"Failed to download {file['name']}: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
