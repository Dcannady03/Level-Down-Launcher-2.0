import os
import requests
import hashlib
import json
from time import sleep

class Updater:
    MANIFEST_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"
    LOCAL_DIR = os.getcwd()

    def calculate_checksum(self, file_path):
        """Calculate the MD5 checksum of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def check_for_updates(self, dry_run=False):
        """Check for missing or outdated files."""
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()

            manifest = response.json()
            files_to_update = []

            for file in manifest.get("files", []):
                file_path = os.path.join(self.LOCAL_DIR, file["name"])

                if not os.path.exists(file_path):
                    print(f"File missing: {file['name']}")
                    files_to_update.append(file)
                else:
                    local_checksum = self.calculate_checksum(file_path)
                    if local_checksum != file["checksum"]:
                        print(f"Checksum mismatch for: {file['name']}")
                        files_to_update.append(file)

                if dry_run:
                    print(f"Would update: {file['name']}")

            return files_to_update if not dry_run else []

        except requests.RequestException as e:
            print(f"Error fetching manifest: {e}")
            return []

    def apply_updates(self, files_to_update):
        """Download and update the required files with retries."""
        total_files = len(files_to_update)
        for i, file in enumerate(files_to_update, start=1):
            file_path = os.path.join(self.LOCAL_DIR, file["name"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            success = False
            for attempt in range(3):
                try:
                    print(f"Downloading {file['name']}... (Attempt {attempt + 1}/3)")
                    response = requests.get(file["url"], stream=True)
                    response.raise_for_status()

                    with open(file_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    print(f"Updated: {file['name']}")
                    success = True
                    break
                except requests.RequestException as e:
                    print(f"Error downloading {file['name']} (Attempt {attempt + 1}): {e}")

            if not success:
                print(f"Failed to download {file['name']} after 3 attempts.")
