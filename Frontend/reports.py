from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt

class ReportsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(141, 153, 174))  # #8d99ae
        self.setPalette(palette)

        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Same margins as MenuWidget
        layout.setSpacing(15)  # Same spacing as MenuWidget
        layout.setAlignment(Qt.AlignTop)  # Align items to the top

        # Title
        title_label = QLabel("Claims Reports")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Bold title
        layout.addWidget(title_label)

        # Report sections
        self.fraud_count_label = self.create_report_section("Total Fraudulent Claims:", 0)
        self.suspicious_count_label = self.create_report_section("Total Suspicious Claims:", 0)
        self.verification_count_label = self.create_report_section("Claims Awaiting Verification:", 0)
        self.success_count_label = self.create_report_section("Claims Successfully Processed:", 0)
        self.total_claims_label = self.create_report_section("Total Claims Processed:", 0)

        # Add report sections to layout
        layout.addLayout(self.fraud_count_label)
        layout.addLayout(self.suspicious_count_label)
        layout.addLayout(self.verification_count_label)
        layout.addLayout(self.success_count_label)
        layout.addLayout(self.total_claims_label)

        # Download PDF Button
        download_button = QPushButton("Download PDF")
        download_button.setStyleSheet("background-color: #FF0000; color: white; font-weight: bold; padding: 10px;")  # Pure red button with white text
        download_button.setFixedSize(150, 40)  # Set fixed size for the button
        download_button.setCursor(Qt.PointingHandCursor)  # Change cursor to pointer on hover
        layout.addWidget(download_button, alignment=Qt.AlignCenter)  # Center the button

        self.setLayout(layout)

    def create_report_section(self, title, count):
        """Helper function to create a report section with title and count."""
        section_layout = QHBoxLayout()

        # Title label (regular weight)
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))  # Regular font for titles

        # Count label (bold weight)
        count_label = QLabel(str(count))
        count_label.setFont(QFont("Arial", 12, QFont.Bold))  # Bold font for counts

        section_layout.addWidget(title_label)
        section_layout.addWidget(count_label)

        return section_layout

    def update_report(self, frauds, suspicious, awaiting_verification, successfully_processed, total_claims):
        """Method to update the report counts."""
        self.fraud_count_label.itemAt(1).widget().setText(str(frauds))
        self.suspicious_count_label.itemAt(1).widget().setText(str(suspicious))
        self.verification_count_label.itemAt(1).widget().setText(str(awaiting_verification))
        self.success_count_label.itemAt(1).widget().setText(str(successfully_processed))
        self.total_claims_label.itemAt(1).widget().setText(str(total_claims))
