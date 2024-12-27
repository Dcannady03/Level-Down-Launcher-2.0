from PyQt6.QtWidgets import QApplication
from launcher import Launcher
import sys
import ctypes
import os

def ensure_admin_privileges():
    """Ensure the application runs with admin privileges."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Relaunch the application with admin privileges
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

def apply_dark_theme(app):
    """Load and apply the dark theme stylesheet."""
    theme_path = os.path.join("assets", "styles", "dark_theme.qss")
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r", encoding="utf-8") as file:
                app.setStyleSheet(file.read())
            print(f"Dark theme successfully loaded from {theme_path}")
        except Exception as e:
            print(f"Error loading dark theme: {e}")
    else:
        print(f"Dark theme file not found at {theme_path}. Using default styles.")

def main():
    """Main function to start the launcher."""
    ensure_admin_privileges()
    
    # Create the application instance
    app = QApplication(sys.argv)

    # Apply dark theme
    apply_dark_theme(app)

    # Initialize the main launcher window
    launcher = Launcher()
    launcher.show()

    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    print("Starting the application...")
    main()
