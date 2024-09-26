from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from functools import partial

class MenuWidget(QWidget):
    # Signal to notify when a menu item is clicked
    menu_item_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(10, 25, 49))  # #0A1931
        self.setPalette(palette)

        # Set layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins around the layout
        layout.setSpacing(15)  # Reduce spacing between items
        layout.setAlignment(Qt.AlignTop)  # Align items to the top

        # Dashboard Label
        dashboard_label = QLabel("KRE Dashboard")
        dashboard_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")  # Customize as needed
        layout.addWidget(dashboard_label)

        # User Info
        user_info_layout = QHBoxLayout()
        user_icon = QLabel()
        user_icon.setPixmap(QIcon(":/path/to/user-circle.png").pixmap(32, 32))  # Use appropriate path and size
        user_name = QLabel("Username")
        user_name.setStyleSheet("color: white;")
        user_info_layout.addWidget(user_icon)
        user_info_layout.addWidget(user_name)
        layout.addLayout(user_info_layout)

        # Menu Items
        menu_items = [
            ("Home", "fa-home"),
            ("Notifications", "fa-bell"),
            ("Claims", "fa-file-invoice-dollar"),
            ("Bank Reconciliations", "fa-university"),
            ("Sort Documents", "fa-file-upload"),
            ("Settings", "fa-gear"),
            ("Help", "fa-circle-info"),
            ("Logout", "fa-sign-out-alt")
        ]

        for item in menu_items:
            btn = QPushButton(item[0])  # Use item[0] for the button text
            btn.setIcon(QIcon(f":/path/to/{item[1]}.png"))  # Use appropriate path for icons
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: transparent;
                    text-align: left;
                    padding: 8px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                }
            """)
            btn.setIconSize(QSize(24, 24))
            # Connect button click to emit the menu item clicked signal using partial
            btn.clicked.connect(partial(self.menu_item_clicked.emit, item[0]))
            btn_layout = QHBoxLayout()
            btn_layout.addWidget(btn)
            layout.addLayout(btn_layout)

        self.setLayout(layout)
