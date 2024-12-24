from PyQt5.QtWidgets import QApplication
from modules.splash_screen import SplashScreen
from modules.updater import Updater
from modules.launcher import Launcher  # Import the Launcher
import sys


def main():
    updater = Updater()

    # Check for updates
    files_to_update = updater.check_for_updates()

    if files_to_update:
        print(f"{len(files_to_update)} file(s) need to be updated.")
        updater.apply_updates(files_to_update)
    else:
        print("All files are up to date.")


    # On update completion, load the main launcher
    def load_main_window():
        splash.close()  # Close the splash screen
        launcher = Launcher()  # Load main launcher
        launcher.show()

    splash.worker.finished.connect(load_main_window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
