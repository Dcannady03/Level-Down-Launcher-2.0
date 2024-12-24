from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher  # Import the Launcher
import sys


def main():
    app = QApplication(sys.argv)

    # Initialize Updater
    updater = Updater()

    # Show Splash Screen
    splash = SplashScreen(updater)
    splash.show()

    # On update completion, load the main launcher
    def load_main_window():
        splash.close()  # Close the splash screen
        launcher = Launcher()  # Load main launcher
        launcher.show()

    splash.worker.finished.connect(load_main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
