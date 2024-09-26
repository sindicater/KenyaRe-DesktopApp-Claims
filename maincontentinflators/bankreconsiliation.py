from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class BankReconciliationsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Create a label for the content
        label = QLabel("Bank Reconciliations Content")
        label.setAlignment(Qt.AlignCenter)  # Center align the label
        layout.addWidget(label)  # Add the label to the layout

        # Set the layout for this widget
        self.setLayout(layout)
