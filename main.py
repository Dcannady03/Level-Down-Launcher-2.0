from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher
import sys

# Retain global references
splash = None
launcher = None


def main():
    global splash, launcher  # Declare globals

    app = QApplication(sys.argv)
    # Load dark theme
    with open("dark_theme.qss", "r") as file:
        app.setStyleSheet(file.read())
    # Enable or disable updates
    enable_updates = True  # Set to True to enable updates
    print(f"Updates enabled: {enable_updates}")  # Debug message

    # Initialize updater and splash screen
    updater = Updater(enable_updates=enable_updates)
    splash = SplashScreen(updater)
    splash.show()

    # Function to load the main launcher
    def load_main_window():
        global launcher  # Retain reference to launcher
        try:
            print("Loading main launcher...")  # Debug message
            splash.hide()  # Hide splash screen (retain its reference)
            print("Splash screen hidden.")  # Debug message

            launcher = Launcher()  # Initialize the launcher
            launcher.show()  # Show the launcher window
            print("Launcher is now visible.")  # Debug message
        except Exception as e:
            print(f"Error loading launcher: {e}")  # Debug error message

    # Connect splash worker's signal to load the main window
    splash.worker.finished.connect(load_main_window)

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Starting the application...")  # Debug message
    main()
