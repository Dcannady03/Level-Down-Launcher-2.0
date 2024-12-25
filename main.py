from PyQt5.QtWidgets import QApplication
from launcher import Launcher
import sys
import ctypes
import os


def ensure_admin_privileges():
    """Ensure the application runs with admin privileges."""
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # Relaunch the application with admin privileges
            params = " ".join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            sys.exit()
    except Exception as e:
        print(f"Error ensuring admin privileges: {e}")
        sys.exit(1)  # Exit with an error status


def resource_path(relative_path):
    """Get the absolute path to a resource, works for both dev and PyInstaller."""
    if getattr(sys, "frozen", False):  # If running as a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


def apply_dark_theme(app):
    """Load and apply the dark theme stylesheet."""
    theme_path = resource_path(os.path.join("assets", "styles", "dark_theme.qss"))
    print(f"Resolving theme path: {theme_path}")  # Debug path
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as file:
                app.setStyleSheet(file.read())
            print(f"Dark theme loaded successfully from {theme_path}")
        except Exception as e:
            print(f"Error loading dark theme: {e}")
    else:
        print(f"Dark theme file not found at {theme_path}. Using default styles.")


def main():
    """Main function to start the launcher."""
    print("Initializing QApplication...")  # Debug message
    app = QApplication(sys.argv)

    # Apply dark theme before initializing the launcher
    apply_dark_theme(app)

    # Initialize the main launcher window
    try:
        print("Initializing Launcher...")  # Debug message
        launcher = Launcher()
        launcher.show()
    except Exception as e:
        print(f"Error initializing launcher: {e}")
        sys.exit(1)

    # Start the event loop
    print("Starting event loop...")  # Debug message
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Starting the application...")  # Debug message
    ensure_admin_privileges()
    main()
