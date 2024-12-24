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
    splash = SplashScreen(updater)
    splash.show()

    # Function to load the main launcher after updates
    def load_main_window():
        print("Loading main launcher...")  # Debug message
        splash.close()  # Close the splash screen

        # Create and show the Launcher window
        launcher = Launcher()
        launcher.show()
        print("Launcher is now visible.")  # Debug message

    # Connect the worker's finished signal to load the main window
    splash.worker.finished.connect(load_main_window)

    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Starting the application...")  # Debug message
    main()
