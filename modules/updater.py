import os
import requests
import hashlib
import subprocess
import sys

class Updater:
    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def __init__(self, enable_updates=True):
        self.enable_updates = enable_updates
        self.manifest = None
        self.local_version = "1.0.0"  # Replace with your current version

    def fetch_manifest(self):
        """Fetch the remote manifest."""
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            self.manifest = response.json()
            print("Manifest fetched successfully.")
        except Exception as e:
            print(f"Error fetching manifest: {e}")
            self.manifest = None

    def calculate_checksum(self, file_path):
        """Calculate the checksum of a local file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def is_new_version(self):
        """Check if the manifest version is newer than the current version."""
        if not self.manifest or "version" not in self.manifest:
            return False
        return self.manifest["version"] != self.local_version

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
            if not os.path.exists(local_path) or self.calculate_checksum(local_path) != file["checksum"]:
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

    def apply_updates(self, updates):
        """Download and replace outdated files."""
        for file in updates:
            self.download_file(file)

    def restart_application(self):
        """Restart the application after updating the executable."""
        python_executable = sys.executable
        script_path = sys.argv[0]
        subprocess.Popen([python_executable, script_path])
        sys.exit(0)

    def run(self):
        """Perform the update check and apply updates if necessary."""
        if not self.enable_updates:
            print("Updates are disabled.")
            return

        self.fetch_manifest()

        if not self.manifest:
            print("Manifest fetch failed. Aborting updates.")
            return

        if not self.manifest.get("files"):
            print("Manifest is valid but contains no files. Skipping updates.")
            return

        if self.is_new_version():
            print(f"New version available: {self.manifest['version']}")

        updates = self.check_for_updates()
        if updates:
            print(f"Found {len(updates)} file(s) to update.")
            self.apply_updates(updates)
            if any(file["name"] == "main.exe" for file in updates):
                print("main.exe updated. Restarting...")
                self.restart_application()
        else:
            print("All files are up to date.")
