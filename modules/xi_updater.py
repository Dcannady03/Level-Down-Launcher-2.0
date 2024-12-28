from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter
import os
import json
import hashlib
import requests


REMOTE_MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-updates/main/manifest.json"
BASE_FILE_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-updates/main/update/FINAL%20FANTASY%20XI/"
SETTINGS_FILE = "settings.json"


class FileCheckThread(QThread):
    check_progress = pyqtSignal(int)  # Emit file checking progress
    download_progress = pyqtSignal(int)  # Emit download progress
    download_status = pyqtSignal(str)  # Emit download status
    finished = pyqtSignal(bool)  # Emit when finished

    def __init__(self, local_dir):
        super().__init__()
        self.local_dir = local_dir
        self.total_files_to_check = 0
        self.files_checked = 0
        self.total_files_to_download = 0
        self.downloaded_files = 0

    def fetch_remote_manifest(self):
        try:
            response = requests.get(REMOTE_MANIFEST_URL)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching remote manifest: {e}")
            return None

    def calculate_sha256(self, file_path):
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def download_file(self, file_entry):
        url = BASE_FILE_URL + file_entry["filename"].replace("\\", "/")
        local_path = os.path.join(self.local_dir, file_entry["filename"])
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.downloaded_files += 1
            self.download_progress.emit(int((self.downloaded_files / self.total_files_to_download) * 100))
            self.download_status.emit(f"Downloaded {self.downloaded_files} of {self.total_files_to_download} files")
        except Exception as e:
            print(f"Failed to download {file_entry['filename']} from {url}: {e}")

    def run(self):
        manifest = self.fetch_remote_manifest()
        if not manifest:
            self.finished.emit(False)
            return

        # Step 1: Check files
        self.total_files_to_check = len(manifest["manifest"])
        files_to_update = []

        for entry in manifest["manifest"]:
            local_path = os.path.join(self.local_dir, entry["filename"])
            if not os.path.exists(local_path):
                files_to_update.append(entry)
            else:
                local_hash = self.calculate_sha256(local_path)
                if local_hash != entry["sha256"]:
                    files_to_update.append(entry)

            self.files_checked += 1
            self.check_progress.emit(int((self.files_checked / self.total_files_to_check) * 100))

        # Step 2: Download updates
        self.total_files_to_download = len(files_to_update)
        self.downloaded_files = 0

        for file_entry in files_to_update:
            self.download_file(file_entry)

        self.finished.emit(True)


class XIUpdaterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("XIUpdaterTab")
        self.wallpaper_path = "assets/images/wallpaper3.png"
        self.local_dir = self.load_settings()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel(f"Selected Directory: {self.local_dir or 'None'}")
        self.label.setStyleSheet("color: #ffffff; font-size: 14px; background-color: rgba(0, 0, 0, 50%);")
        layout.addWidget(self.label)

        self.file_check_progress_label = QLabel("Checking files...")
        layout.addWidget(self.file_check_progress_label)

        self.file_check_progress_bar = QProgressBar()
        self.file_check_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_check_progress_bar)

        self.download_progress_label = QLabel("Downloading files...")
        layout.addWidget(self.download_progress_label)

        self.download_progress_bar = QProgressBar()
        self.download_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.download_progress_bar)

        self.download_status_label = QLabel("Status: None")
        layout.addWidget(self.download_status_label)

        self.choose_dir_button = QPushButton("Choose Directory")
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        self.start_button = QPushButton("Check for Updates")
        self.start_button.setEnabled(bool(self.local_dir))
        self.start_button.clicked.connect(self.start_check)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f).get("ffxi_dir", None)
        return None

    def save_settings(self):
        settings = {"ffxi_dir": self.local_dir}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)

    def choose_directory(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select FFXI Directory")
        if selected_dir:
            self.local_dir = selected_dir
            self.label.setText(f"Selected Directory: {selected_dir}")
            self.save_settings()

    def start_check(self):
        self.file_check_progress_bar.setValue(0)
        self.download_progress_bar.setValue(0)
        self.download_status_label.setText("Status: Starting update process...")
        self.file_check_progress_label.setText("Checking files...")
        self.download_progress_label.setText("Downloading files...")

        self.thread = FileCheckThread(self.local_dir)
        self.thread.check_progress.connect(self.file_check_progress_bar.setValue)
        self.thread.download_progress.connect(self.download_progress_bar.setValue)
        self.thread.download_status.connect(self.download_status_label.setText)
        self.thread.finished.connect(self.update_complete)
        self.thread.start()

    def update_complete(self, success):
        if success:
            QMessageBox.information(self, "Update Check", "All required updates have been applied!")
        else:
            QMessageBox.warning(self, "Update Check", "Failed to fetch updates or complete the process.")
