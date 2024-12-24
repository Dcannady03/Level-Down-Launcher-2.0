import os
import requests
import hashlib
import json


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

    def check_for_updates(self):
        """Check for missing or outdated files."""
        try:
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()

            try:
                manifest = response.json()
            except json.JSONDecodeError:
                print("Error: Manifest is not valid JSON or is empty.")
                return []

            # List of files that need to be updated
            files_to_update = []

            for file in manifest.get("files", []):
                file_path = os.path.join(self.LOCAL_DIR, file["name"])

                if not os.path.exists(file_path):
                    # File is missing
                    print(f"File missing: {file['name']}")
                    files_to_update.append(file)
                else:
                    # Verify checksum
                    local_checksum = self.calculate_checksum(file_path)
                    if local_checksum != file["checksum"]:
                        print(f"Checksum mismatch for: {file['name']}")
                        files_to_update.append(file)

            return files_to_update

        except requests.RequestException as e:
            print(f"Error fetching manifest: {e}")
            return []

    def apply_updates(self, files_to_update):
        """Download and update the required files."""
        for file in files_to_update:
            file_path = os.path.join(self.LOCAL_DIR, file["name"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            try:
                print(f"Downloading {file['name']}...")
                response = requests.get(file["url"])
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Updated: {file['name']}")
            except requests.RequestException as e:
                print(f"Error downloading {file['name']}: {e}")
