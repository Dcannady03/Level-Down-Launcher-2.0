from splash_screen import SplashScreen
from launcher import Launcher
from PyQt5.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)

    # Show splash/updater
    splash = SplashScreen()
    splash.show()

    # Launch main application once the updater is complete
    def launch_app():
        launcher = Launcher()
        launcher.show()
        splash.close()

    splash.worker.finished.connect(launch_app)

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

