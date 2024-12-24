from PyQt5.QtWidgets import QApplication
from launcher import Launcher
import sys
import ctypes

def ensure_admin_privileges():
    """Ensure the application runs with admin privileges."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Relaunch the application with admin privileges
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

ensure_admin_privileges()

def main():
    """Main function to start the launcher."""
    app = QApplication(sys.argv)

    # Initialize the main launcher window
    launcher = Launcher()
    launcher.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Starting the application...")
    main()
