from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
import json
import hashlib
import requests
import ctypes
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox

REMOTE_MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-updates/main/manifest.json"
BASE_FILE_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-updates/main/update/FINAL%20FANTASY%20XI/"
SETTINGS_FILE = "settings.json"


class FileCheckThread(QThread):
    total_progress = pyqtSignal(int)
    download_status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, local_dir):
        super().__init__()
        self.local_dir = local_dir
        self.total_to_download = 0
        self.downloaded_count = 0

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

            self.downloaded_count += 1
            progress = int((self.downloaded_count / self.total_to_download) * 100)
            self.total_progress.emit(progress)
            self.download_status.emit(f"Downloaded {self.downloaded_count} of {self.total_to_download} files")
            return True
        except Exception as e:
            print(f"Failed to download {file_entry['filename']} from {url}: {e}")
            return False

    def run(self):
        manifest = self.fetch_remote_manifest()
        if not manifest:
            self.finished.emit(False)
            return

        missing_files = []
        mismatched_files = []

        for entry in manifest["manifest"]:
            local_path = os.path.join(self.local_dir, entry["filename"])
            if not os.path.exists(local_path):
                missing_files.append(entry)
            else:
                local_hash = self.calculate_sha256(local_path)
                if local_hash != entry["sha256"]:
                    mismatched_files.append(entry)

        files_to_update = missing_files + mismatched_files
        self.total_to_download = len(files_to_update)
        self.downloaded_count = 0

        for file_entry in files_to_update:
            self.download_file(file_entry)

        self.finished.emit(True)


class XIUpdaterTab(QWidget):  # Changed to QWidget for tab usage
    def __init__(self):
        super().__init__()
        self.setObjectName("XIUpdaterTab")
        self.wallpaper_path = "assets/images/wallpaper3.png"
        self.local_dir = self.load_settings()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add components with improved styling for readability
        self.label = QLabel(f"Selected Directory: {self.local_dir or 'None'}")
        self.label.setStyleSheet("color: #ffffff; font-size: 14px; background-color: rgba(0, 0, 0, 50%);")
        layout.addWidget(self.label)

        self.progress_label = QLabel("Checking for updates...")
        self.progress_label.setStyleSheet("color: #ffffff; background-color: rgba(0, 0, 0, 50%);")
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                text-align: center;
                color: white;
                background: rgba(0, 0, 0, 50%);
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                width: 10px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.download_status_label = QLabel("Status: None")
        self.download_status_label.setStyleSheet("color: #ffffff; background-color: rgba(0, 0, 0, 50%);")
        layout.addWidget(self.download_status_label)

        self.choose_dir_button = QPushButton("Choose Directory")
        self.choose_dir_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.choose_dir_button.clicked.connect(self.choose_directory)
        layout.addWidget(self.choose_dir_button)

        self.start_button = QPushButton("Check for Updates")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.start_button.setEnabled(bool(self.local_dir))
        self.start_button.clicked.connect(self.start_check)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(211, 211, 211, 60%);")  # Light gray transparency

    def paintEvent(self, event):
        """Override paintEvent to draw the wallpaper."""
        painter = QPainter(self)
        background = QPixmap(self.wallpaper_path)

        if background.isNull():
            print(f"Error: Background image '{self.wallpaper_path}' not loaded.")
        else:
            scaled_background = background.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled_background)

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f).get("ffxi_dir", None)
        return None

    def choose_directory(self):
        selected_dir = QFileDialog.getExistingDirectory(self, "Select FFXI Directory")
        if selected_dir:
            self.local_dir = selected_dir
            self.label.setText(f"Selected Directory: {selected_dir}")
            self.save_settings()

    def save_settings(self):
        """Save settings to the JSON file."""
        settings = {"ffxi_dir": self.local_dir}
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                existing = json.load(f)
            settings.update(existing)
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    def start_check(self):
        """Start the update process."""
        self.progress_bar.setValue(0)
        self.download_status_label.setText("Status: Checking files...")
        self.progress_label.setText("Updating files...")

        # Thread for file checking
        self.thread = FileCheckThread(self.local_dir)
        self.thread.total_progress.connect(self.progress_bar.setValue)
        self.thread.download_status.connect(self.download_status_label.setText)
        self.thread.finished.connect(self.update_complete)
        self.thread.start()

    def update_complete(self, success):
        if success:
            QMessageBox.information(self, "Update Check", "All required updates have been applied!")
        else:
            QMessageBox.warning(self, "Update Check", "Failed to fetch updates or complete the process.")

