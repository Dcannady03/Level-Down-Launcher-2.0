import os
import requests
import json


class Updater:
    MANIFEST_URL = "https://yourserver.com/manifest.json"
    LOCAL_DIR = os.getcwd()

    def check_for_updates(self):
        # Download and parse manifest
        response = requests.get(self.MANIFEST_URL)
        manifest = response.json()

        for file in manifest["files"]:
            file_path = os.path.join(self.LOCAL_DIR, file["name"])
            if not os.path.exists(file_path):  # File missing
                return True
        return False

    def apply_updates(self):
        response = requests.get(self.MANIFEST_URL)
        manifest = response.json()

        for file in manifest["files"]:
            file_path = os.path.join(self.LOCAL_DIR, file["name"])
            url = file["url"]

            print(f"Downloading {file['name']}...")
            with open(file_path, "wb") as f:
                f.write(requests.get(url).content)

    def get_update_steps(self):
        # Define update steps with their messages and logic
        return [
            ("Checking for updates...", self.check_for_updates),
            ("Applying updates...", self.apply_updates),
        ]
