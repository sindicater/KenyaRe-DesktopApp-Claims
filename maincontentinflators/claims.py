import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QListWidget, QHBoxLayout
)
from PyQt5.QtCore import Qt


class ClaimsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Claims Processing Automation")
        self.setGeometry(100, 100, 800, 600)

        self.upload_history = []
        self.analytics = {
            'total_claims': 100,
            'pending_claims': 20,
            'approved_claims': 70,
            'declined_claims': 10
        }

        # Layouts
        main_layout = QVBoxLayout()
        upload_layout = QVBoxLayout()
        history_layout = QVBoxLayout()
        analytics_layout = QVBoxLayout()

        # Header
        title = QLabel("Claims Processing Automation")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; color: #007bff;")

        main_layout.addWidget(title)

        # Upload Sections
        self.create_upload_section(upload_layout, "Treaty Slips", ".pdf")
        self.create_upload_section(upload_layout, "Claims Bordereaux", ".xlsx")
        self.create_upload_section(upload_layout, "Cedant Statement", ".pdf")

        main_layout.addLayout(upload_layout)

        # Upload History Section
        history_label = QLabel("Upload History")
        history_label.setStyleSheet("font-size: 18px;")
        history_layout.addWidget(history_label)

        self.history_list = QListWidget()
        history_layout.addWidget(self.history_list)
        main_layout.addLayout(history_layout)

        # Analytics Section
        analytics_label = QLabel("Claims Analytics")
        analytics_label.setStyleSheet("font-size: 28px;")
        analytics_layout.addWidget(analytics_label)

        self.create_analytics_section(analytics_layout)

        main_layout.addLayout(analytics_layout)
        self.setLayout(main_layout)

    def create_upload_section(self, layout, title, file_type):
        section_layout = QHBoxLayout()
        label = QLabel(f"Upload {title}")
        input_field = QLineEdit()
        input_field.setReadOnly(True)
        upload_button = QPushButton(f"Upload {title}")

        upload_button.clicked.connect(lambda: self.upload_file(input_field, file_type))

        section_layout.addWidget(label)
        section_layout.addWidget(input_field)
        section_layout.addWidget(upload_button)

        layout.addLayout(section_layout)

    def create_analytics_section(self, layout):
        for key, value in self.analytics.items():
            layout.addWidget(QLabel(f"{key.replace('_', ' ').title()}: {value}"))

    def upload_file(self, input_field, file_type):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, f"Select a {file_type} file", "",
                                                   f"Files (*{file_type});;All Files (*)", options=options)
        if file_name:
            input_field.setText(file_name)
            self.upload_history.append(file_name)
            self.update_history_list()

    def update_history_list(self):
        self.history_list.clear()
        for file_name in self.upload_history:
            self.history_list.addItem(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClaimsWidget()  # Changed this from ClaimsProcessingApp to ClaimsWidget
    window.show()
    sys.exit(app.exec_())
