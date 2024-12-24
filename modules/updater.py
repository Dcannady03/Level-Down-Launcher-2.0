import os
import requests
import hashlib

class Updater:
    # Updated manifest URL
    MANIFEST_URL = "https://raw.github.com/Dcannady03/Level-Down-Launcher-2.0/main/manifest.json"

    def __init__(self, enable_updates=True):
        self.enable_updates = enable_updates
        self.manifest = None

    def fetch_manifest(self):
        """Fetch the remote manifest."""
        try:
            print(f"Fetching manifest from {self.MANIFEST_URL}...")  # Debug message
            response = requests.get(self.MANIFEST_URL)
            response.raise_for_status()
            print(f"Manifest raw response: {response.text[:200]}...")  # Debug: Log first 200 chars

            self.manifest = response.json()
            print("Manifest fetched successfully.")  # Debug message
        except requests.RequestException as e:
            print(f"Error fetching manifest: {e}")
            self.manifest = None
        except ValueError as e:
            print(f"Error parsing manifest JSON: {e}")
            print(f"Manifest content received: {response.text}")
            self.manifest = None


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
            print("Updates are disabled.")  # Debug message
            return []

        if not self.manifest:
            print("No manifest available. Skipping update check.")  # Debug message
            return []

        updates = []
        for file in self.manifest.get("files", []):
            local_path = os.path.join(os.getcwd(), file["name"])
            
            # Check if the file exists locally
            if not os.path.exists(local_path):
                print(f"File missing: {file['name']}")  # Debug message
                updates.append(file)
                continue

            # Check if the checksum matches
            local_checksum = self.calculate_checksum(local_path)
            if local_checksum != file["checksum"]:
                print(f"Checksum mismatch for: {file['name']}")  # Debug message
                updates.append(file)

        return updates

    def apply_updates(self, updates):
        """Download and replace outdated files."""
        for file in updates:
            file_path = os.path.join(os.getcwd(), file["name"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            try:
                print(f"Downloading {file['name']}...")
                response = requests.get(file["url"], stream=True)
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Updated: {file['name']}")
            except Exception as e:
                print(f"Error downloading {file['name']}: {e}")

    def run(self):
        """Perform the update check and apply updates if necessary."""
        if not self.enable_updates:
            print("Updates are disabled.")  # Debug message
            return

        self.fetch_manifest()

        if not self.manifest:
            print("Manifest fetch failed. Aborting updates.")
            return

        updates = self.check_for_updates()
        if updates:
            print(f"Found {len(updates)} file(s) to update.")
            self.apply_updates(updates)
        else:
            print("All files are up to date.")
