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


def check_and_apply_updates():
    """Check for updates and apply them if necessary."""
    print("Checking for updates...")  # Debug message
    updater = Updater(enable_updates=True)  # Enable updates

    # Run the update process
    updater.run()

    # If the main executable was updated, restart the application
    if any(file["name"] == "main.exe" for file in updater.manifest.get("files", [])):
        print("main.exe updated. Restarting application...")
        python_executable = sys.executable
        script_path = sys.argv[0]
        os.execv(python_executable, [python_executable, script_path])


def main():
    global splash, launcher  # Declare globals

    # Step 1: Check and apply updates before launching the app
    check_and_apply_updates()

    # Step 2: Initialize the application
    app = QApplication(sys.argv)

    # Load dark theme
    load_dark_theme(app)

    # Initialize updater and splash screen
    enable_updates = True  # Set to True to enable updates
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

