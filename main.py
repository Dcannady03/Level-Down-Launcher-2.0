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

    # Define the launcher as a global variable to prevent garbage collection
    global launcher

    # Function to load the main launcher after updates
    def load_main_window():
        print("Loading main launcher...")
        splash.close()

        # Create and show Launcher
        global launcher
        launcher = Launcher()
        launcher.show()

        # Test if the application is still running
        print("Launcher should now be visible.")
        print(f"Launcher is visible: {launcher.isVisible()}")  # Check if Launcher is actually visible



if __name__ == "__main__":
    print("Starting the application...")  # Debug message
    main()
