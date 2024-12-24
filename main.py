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
        try:
            print("Loading main launcher...")  # Debug message
            splash.close()

            # Create and show Launcher
            launcher = Launcher()
            launcher.show()
            print("Launcher is now visible.")  # Debug message
        except Exception as e:
            print(f"Error in load_main_window: {e}")  # Catch exceptions during launcher initialization

    # Connect the worker's finished signal to load the main window
    splash.worker.finished.connect(load_main_window)

    # Start the application event loop
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in app.exec_(): {e}")  # Catch errors in the event loop


if __name__ == "__main__":
    print("Starting the application...")  # Debug message
    main()
