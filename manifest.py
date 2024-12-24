import os
import hashlib
import json

# Base directory to scan
BASE_DIR = r"I:\git\Level-Down-Launcher-2.0"

# Base URL for hosted files (update this if hosted remotely, e.g., GitHub raw URL)
BASE_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main"

# Output file for the manifest
OUTPUT_FILE = os.path.join(BASE_DIR, "manifest.json")

# Files and folders to skip
SKIP_FOLDERS = [".git"]
SKIP_FILES = ["manifest.py", "manifest.json", ".gitattributes"]

# Manifest version
MANIFEST_VERSION = "2.1.0"


def calculate_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_manifest(base_dir, base_url, version):
    """Generate a manifest of files in the directory."""
    manifest = {"version": version, "files": []}  # Include version at the top

    for root, dirs, files in os.walk(base_dir):
        # Skip specified folders
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDERS]

        for file_name in files:
            # Skip specified files
            if file_name in SKIP_FILES:
                continue

            file_path = os.path.join(root, file_name)

            # Calculate relative path
            relative_path = os.path.relpath(file_path, base_dir).replace("\\", "/")

            # Calculate checksum
            checksum = calculate_checksum(file_path)

            # Append file details to the manifest
            manifest["files"].append({
                "name": relative_path,
                "url": f"{base_url}/{relative_path}",
                "checksum": checksum
            })

    return manifest


def save_manifest(manifest, output_file):
    """Save the manifest to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(manifest, f, indent=4)
    print(f"Manifest saved to {output_file}")


if __name__ == "__main__":
    # Generate the manifest with the specified version
    manifest = generate_manifest(BASE_DIR, BASE_URL, MANIFEST_VERSION)

    # Save the manifest to the output file
    save_manifest(manifest, OUTPUT_FILE)

