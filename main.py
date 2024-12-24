from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher
import sys


def main():
    app = QApplication(sys.argv)

    # Initialize Updater
    updater = Updater()

    # Show Splash Screen
    splash = SplashScreen(updater)  # Define splash screen
    splash.show()

    # Check for updates during the splash screen
    def load_main_window():
        # Close the splash screen after updates are applied
        splash.close()

        # Launch the main application
        launcher = Launcher()
        launcher.show()

    splash.worker.finished.connect(load_main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()