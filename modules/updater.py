import os
import requests
import hashlib
import json
from time import sleep

class Updater:
    def __init__(self, enable_updates=True):
        self.enable_updates = enable_updates  # Control updates with this flag

    def check_for_updates(self):
        """Check for missing or outdated files."""
        if not self.enable_updates:
            print("Update check skipped.")  # Debug message
            return []

        # Normal update logic
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()

            manifest = response.json()
            files_to_update = []

            for file in manifest.get("files", []):
                file_path = os.path.join(self.LOCAL_DIR, file["name"])
                if not os.path.exists(file_path) or self.calculate_checksum(file_path) != file["checksum"]:
                    files_to_update.append(file)

            return files_to_update
        except Exception as e:
            print(f"Error during update check: {e}")
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
