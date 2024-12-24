from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer
import requests


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Dashboard")  # For QSS styling

        # Main layout
        layout = QVBoxLayout()

        # Header label
        header_label = QLabel("Server Updates")
        header_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #fff;")
        layout.addWidget(header_label)

        # RSS Feed Display
        self.rss_feed_display = QPlainTextEdit()
        self.rss_feed_display.setReadOnly(True)  # Make it read-only
        self.rss_feed_display.setStyleSheet(
            "background-color: rgba(255, 255, 255, 50%); color: #000; border: none;"
        )
        layout.addWidget(self.rss_feed_display)

        # Set the layout
        self.setLayout(layout)
        self.setStyleSheet(
            "background-color: rgba(200, 200, 200, 50%);"  # Light gray transparent background
        )

        # Load RSS feed initially
        self.load_rss_feed()

        # Setup timer for auto-refresh every 1 minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_rss_feed)
        self.timer.start(60000)  # 1 minute (60000 ms)

    def load_rss_feed(self):
        """Fetch and display the RSS feed."""
        rss_url = "https://raw.githubusercontent.com/Dcannady03/discord-update-bot/main/update_notification.txt"

        try:
            response = requests.get(rss_url)
            if response.status_code == 200:
                content = response.text.strip()
                self.rss_feed_display.setPlainText(content)
            else:
                self.rss_feed_display.setPlainText("Failed to fetch updates. Please try again later.")
        except Exception as e:
            self.rss_feed_display.setPlainText(f"Error fetching RSS feed: {e}")

