from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
import sys

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Splash Screen")
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Splash Screen Content"))
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Launcher")
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Launcher Content"))
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


def main():
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def show_launcher():
        splash.hide()
        launcher = Launcher()
        launcher.show()

    app.aboutToQuit.connect(lambda: print("Application exiting..."))  # Debug when exiting
    QTimer.singleShot(2000, show_launcher)  # Simulate delay for splash

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()