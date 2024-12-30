import sys
import os
import requests
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from launcher import Launcher

class UpdateWorker(QThread):
    update_progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool)

    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def run(self):
        try:
            self.update_progress.emit(10, "Fetching manifest...")
            manifest = self.fetch_manifest()
            if not manifest:
                self.update_progress.emit(0, "Error fetching manifest.")
                self.finished.emit(False)
                return

            self.update_progress.emit(30, "Checking for updates...")
            files_to_update = self.check_for_updates(manifest)
            total_files = len(files_to_update)

            if total_files == 0:
                self.update_progress.emit(100, "No updates required.")
                self.finished.emit(False)
                return

            for i, file in enumerate(files_to_update, start=1):
                self.update_progress.emit(
                    int(30 + (i / total_files) * 60),
                    f"Downloading {file['name']}..."
                )
                self.download_file(file)

            self.update_progress.emit(100, "Updates complete!")
            self.finished.emit(True)
        except Exception as e:
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
            else:
                local_hash = self.calculate_hash(local_path)
                if local_hash != file.get("hash"):
                    updates.append(file)
        return updates

    def calculate_hash(self, file_path):
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
            print(f"Downloaded: {file['name']}")
        except Exception as e:
            print(f"Error downloading {file['name']}: {e}")


class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Level Down Launcher - Updating")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.worker = UpdateWorker()
        self.worker.update_progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_updates_complete)
        self.worker.start()

    def update_progress(self, progress, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)

    def on_updates_complete(self, success):
        if success:
            self.status_label.setText("Launching application...")
        else:
            self.status_label.setText("No updates needed. Launching...")

        self.launch_main_window()

    def launch_main_window(self):
        self.close()
        self.main_window = Launcher()
        self.main_window.show()


class LauncherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("Welcome to the Launcher!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec())
