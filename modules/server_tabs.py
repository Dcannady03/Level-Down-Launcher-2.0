from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ServerTabs(QWidget):
    def __init__(self, server_name: str):
        super().__init__()
        
        # Validate server_name
        if not isinstance(server_name, str) or not server_name.strip():
            server_name = "Unknown Server"

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align content to the top

        # Header label
        server_label = QLabel(f"{server_name} - Login and Auction House")
        server_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #fff;")
        server_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(server_label)

        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(50, 50, 50, 80%);")  # Dark transparent background
