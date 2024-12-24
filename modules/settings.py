import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QCheckBox

SETTINGS_FILE = "settings.json"


class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Settings")
        self.settings = self.load_settings()
        self.initUI()

    def initUI(self):
        """Initialize the UI components."""
        layout = QVBoxLayout()
        # Checkbox for closing launcher after launch
        self.close_after_launch_checkbox = QCheckBox("Close Launcher After Launch")
        self.ensure_setting_exists("close_after_launch", False)  # Ensure the setting exists in the JSON file
        self.close_after_launch_checkbox.setChecked(self.settings.get("close_after_launch", False))
        self.close_after_launch_checkbox.stateChanged.connect(self.save_close_after_launch_setting)
        layout.addWidget(self.close_after_launch_checkbox)

        

        # Labels for paths
        self.ashita_label = QLabel(f"Ashita Directory: {self.settings.get('ashita_dir', 'Not Set')}")
        self.windower_label = QLabel(f"Windower Directory: {self.settings.get('windower_dir', 'Not Set')}")
        self.ffxi_label = QLabel(f"Final Fantasy XI Directory: {self.settings.get('ffxi_dir', 'Not Set')}")

        layout.addWidget(self.ashita_label)
        layout.addWidget(self.windower_label)
        layout.addWidget(self.ffxi_label)

        # Buttons for browsing directories
        self.ashita_button = QPushButton("Browse Ashita Directory")
        self.ashita_button.clicked.connect(lambda: self.browse_directory("ashita_dir", self.ashita_label))
        layout.addWidget(self.ashita_button)

        self.windower_button = QPushButton("Browse Windower Directory")
        self.windower_button.clicked.connect(lambda: self.browse_directory("windower_dir", self.windower_label))
        layout.addWidget(self.windower_button)

        self.ffxi_button = QPushButton("Browse Final Fantasy XI Directory")
        self.ffxi_button.clicked.connect(lambda: self.browse_directory("ffxi_dir", self.ffxi_label))
        layout.addWidget(self.ffxi_button)

        

        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        """Save settings to the JSON file."""
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
            print("Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")

    def save_close_after_launch_setting(self):
        """Save the 'Close After Launch' setting to the JSON file."""
        self.settings["close_after_launch"] = self.close_after_launch_checkbox.isChecked()
        self.save_settings()

    def ensure_setting_exists(self, key, default_value):
        """Ensure a specific setting exists in the JSON file."""
        if key not in self.settings:
            self.settings[key] = default_value
            self.save_settings()

    def save_close_after_launch_setting(self):
        """Save the 'Close After Launch' setting to the JSON file."""
        self.settings["close_after_launch"] = self.close_after_launch_checkbox.isChecked()
        self.save_settings()

    def browse_directory(self, key, label):
        """Open a dialog to browse for a directory."""
        selected_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        if selected_dir:
            self.settings[key] = selected_dir
            label.setText(f"{key.replace('_', ' ').title()}: {selected_dir}")
            self.save_settings()
