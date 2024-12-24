from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher  # Assuming Launcher is your main application window
import sys


def main():
    app = QApplication(sys.argv)

    # Initialize Updater
    updater = Updater()

    # Show Splash Screen
    splash = SplashScreen(updater)
    splash.show()

    # Function to load the main launcher after updates
    def load_main_window():
        splash.close()  # Close the splash screen

        # Launch the main application
        launcher = Launcher()
        launcher.show()

    # Connect the worker's finish signal to load the main window
    splash.worker.finished.connect(load_main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
