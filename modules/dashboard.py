from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt6.QtCore import QTimer
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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
            "background-color: rgba(0, 0, 0, 70%); color: #fff; border: none; padding: 5px;"
        )
        layout.addWidget(self.rss_feed_display)

        # Set the layout
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(50, 50, 50, 80%);")  # Dark transparent background

        # Initialize RSS data
        self.last_fetched_content = ""
        self.rss_url = "https://raw.githubusercontent.com/Dcannady03/discord-update-bot/main/update_notification.txt"

        # Load RSS feed initially
        self.load_rss_feed()

        # Setup timer for auto-refresh every 1 minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_rss_feed)
        self.timer.start(60000)  # 1 minute (60000 ms)

    def load_rss_feed(self):
        """Fetch and display the RSS feed."""
        try:
            logging.info("Fetching RSS feed...")
            response = requests.get(self.rss_url, timeout=10)
            if response.status_code == 200:
                content = response.text.strip()
                if content != self.last_fetched_content:
                    self.last_fetched_content = content
                    self.rss_feed_display.setPlainText(content)
                    logging.info("RSS feed updated successfully.")
                else:
                    logging.info("No new updates in RSS feed.")
            else:
                self.handle_error(f"HTTP Error {response.status_code}: Failed to fetch updates.")
        except requests.RequestException as e:
            self.handle_error(f"Error fetching RSS feed: {e}")

    def handle_error(self, error_message):
        """Handle errors gracefully."""
        logging.error(error_message)
        if not self.last_fetched_content:
            self.rss_feed_display.setPlainText("Failed to fetch updates. Please try again later.")
