from PyQt5.QtWidgets import QApplication
from launcher import Launcher
import sys

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
