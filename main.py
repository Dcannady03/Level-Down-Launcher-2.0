from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
import os
import sys
import requests
import hashlib
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

        # Overlay Layout
        self.overlay = QVBoxLayout()
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

        self.overlay.addWidget(self.status_label)
        self.overlay.addWidget(self.progress_bar)

        overlay_widget = QWidget(self)
        overlay_widget.setLayout(self.overlay)
        overlay_widget.setGeometry(50, 250, 500, 100)

        self.worker = UpdateWorker()
        self.worker.update_progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_update_complete)
        self.worker.start()

        print("SplashScreen initialized.")

    def update_progress(self, progress, message):
        print(f"Progress updated: {progress}, Message: {message}")
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_update_complete(self, restart_required):
        if restart_required:
            self.status_label.setText("Restarting application...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            self.status_label.setText("Launching application...")
            print("Update complete. Launching launcher...")
            os.system("python launcher.py")  # Adjust the path if necessary


class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def run(self):
        try:
            self.update_progress.emit(10, "Fetching manifest...")
            manifest = self.fetch_manifest()

            if not manifest:
                self.update_progress.emit(0, "Failed to fetch manifest.")
                self.finished.emit(False)
                return

            self.update_progress.emit(20, "Comparing files...")
            files_to_update = self.compare_files(manifest)
            if not files_to_update:
                self.update_progress.emit(100, "No updates required.")
                self.finished.emit(False)
                return

            total_files = len(files_to_update)
            for i, file in enumerate(files_to_update, 1):
                self.update_progress.emit(
                    int((i / total_files) * 80) + 20,
                    f"Updating {file['name']}..."
                )
                self.download_file(file)

            self.update_progress.emit(100, "Updates complete!")
            self.finished.emit(any(file["name"] == "launcher.py" for file in files_to_update))
        except Exception as e:
            self.update_progress.emit(0, f"Error: {e}")
            self.finished.emit(False)

    def fetch_manifest(self):
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to fetch manifest: {e}")
            return None

    def compare_files(self, manifest):
        updates = []
        for file in manifest.get("files", []):
            local_path = os.path.join(os.getcwd(), file["name"])
            if not os.path.exists(local_path) or self.calculate_hash(local_path) != file["hash"]:
                updates.append(file)
        return updates

    @staticmethod
    def calculate_hash(file_path):
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return None

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
