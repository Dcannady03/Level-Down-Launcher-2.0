from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QProgressBar, QWidget, QApplication
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
import os
import sys
import requests
import hashlib


class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
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
            # Step 1: Check for updates
            files_to_update = self.updater.check_for_updates()  # No additional arguments
            total_files = len(files_to_update)

            # Determine if a restart is required
            restart_required = any(file["name"] == "main.exe" for file in files_to_update)

            if total_files == 0:
                print("No updates found. All files are up to date.")  # Debug message
                self.update_progress.emit(100, "No updates found.")
                self.finished.emit(False)  # No restart required
                return

            print(f"Files to update: {total_files}")  # Debug message

            # Step 2: Apply updates
            for i, file in enumerate(files_to_update, start=1):
                try:
                    self.update_progress.emit(
                        int((i / total_files) * 100), f"Updating {file['name']}..."
                    )
                    self.updater.download_file(file)
                except Exception as e:
                    print(f"Error updating {file['name']}: {e}")  # Debug message
                    self.update_progress.emit(0, f"Error updating {file['name']}.")

            # Step 3: Finalize
            self.update_progress.emit(100, "Updates complete!")
            print("UpdateWorker finished successfully.")  # Debug message
            self.finished.emit(restart_required)
        except Exception as e:
            print(f"Critical error in UpdateWorker: {e}")  # Debug message
            self.update_progress.emit(0, f"Critical error: {e}")
            self.finished.emit(False)


    def fetch_manifest(self):
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            print("Manifest fetched successfully.")
            return response.json()
        except Exception as e:
            print(f"Error fetching manifest: {e}")
            return None

    def calculate_checksum(self, file_path):
        """Calculate the checksum of a local file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def check_for_updates(self):
        """Check for files that need updates."""
        if not self.enable_updates:
            print("Updates are disabled.")
            return []

        if not self.manifest:
            print("No manifest available. Skipping update check.")
            return []

        updates = []
        for file in self.manifest.get("files", []):
            local_path = os.path.join(os.getcwd(), file["name"])
            if not os.path.exists(local_path):
                print(f"File missing: {file['name']}")  # Debug message
                updates.append(file)
            else:
                # Compare checksums
                local_checksum = self.calculate_checksum(local_path)
                print(f"File: {file['name']} | Local checksum: {local_checksum} | Manifest checksum: {file['checksum']}")  # Debug message
                if local_checksum != file["checksum"]:
                    print(f"Checksum mismatch for: {file['name']}")  # Debug message
                    updates.append(file)

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
    splash = SplashScreen()  # Create the splash screen
    splash.show()  # Show the splash screen
    sys.exit(app.exec_())  # Run the application event loop
