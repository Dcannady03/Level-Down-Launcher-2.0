import os
import hashlib
import json

# Base directory to scan
BASE_DIR = r"I:\git\Level-Down-Launcher-2.0"

# Base URL for hosted files (update this if hosted remotely, e.g., GitHub raw URL)
BASE_URL = "https://raw.githubusercontent.com/Dcannady03/Level-Down-Launcher-2.0/main"

# Output file for the manifest
OUTPUT_FILE = os.path.join(BASE_DIR, "manifest.json")


def calculate_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_manifest(base_dir, base_url):
    """Generate a manifest of files in the directory."""
    manifest = {"files": []}

    for root, _, files in os.walk(base_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Skip manifest.json itself
            if file_name == "manifest.json":
                continue

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
    # Generate the manifest
    manifest = generate_manifest(BASE_DIR, BASE_URL)

    # Save the manifest to the output file
    save_manifest(manifest, OUTPUT_FILE)
