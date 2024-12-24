from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher
import os
import sys

# Retain global references
splash = None
launcher = None


def load_dark_theme(app):
    """Load the dark theme stylesheet from the assets/styles directory."""
    theme_path = os.path.join(os.getcwd(), "assets/styles/dark_theme.qss")
    if os.path.exists(theme_path):
        try:
            with open(theme_path, "r") as file:
                app.setStyleSheet(file.read())
            print(f"Dark theme loaded from {theme_path}")  # Debug message
        except Exception as e:
            print(f"Error loading dark theme: {e}")  # Debug error message
    else:
        print(f"Dark theme not found at {theme_path}. Using default styles.")  # Debug message


def main():
    global splash, launcher  # Declare globals

    print("Starting the application...")  # Debug message

    # Step 1: Initialize the application
    app = QApplication(sys.argv)

    # Step 2: Load dark theme
    load_dark_theme(app)

    # Step 3: Initialize updater and splash screen
    enable_updates = True  # Enable updates
    updater = Updater(enable_updates=enable_updates)
    splash = SplashScreen(updater)
    splash.show()

    # Function to load the main launcher after updates
    def load_main_window():
        global launcher  # Retain reference to launcher
        try:
            print("Loading main launcher...")  # Debug message
            splash.hide()  # Hide splash screen
            launcher = Launcher()  # Initialize the launcher
            launcher.show()  # Show the launcher window
            print("Launcher is now visible.")  # Debug message
        except Exception as e:
            print(f"Error loading launcher: {e}")  # Debug error message

    # Connect splash worker's signal to load the main window
    splash.worker.finished.connect(load_main_window)

    # Step 4: Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
