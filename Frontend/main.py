from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
import sys
from menu import MenuWidget
from maincontentinflators.home import HomeWidget
from maincontentinflators.notifications import NotificationsWidget
from maincontentinflators.claims import ClaimsWidget
from maincontentinflators.sortdocs import SortDocsWidget
from maincontentinflators.settings import SettingsWidget
from maincontentinflators.help import HelpWidget
from maincontentinflators.logout import LogoutWidget
from maincontentinflators.bankreconsiliation import BankReconciliationsWidget
from reports import ReportsWidget
from backend.claimsprocessing import ClaimsProcessor

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt Application")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Menu widget (20% width)
        self.menu_widget = MenuWidget()
        self.menu_widget.menu_item_clicked.connect(self.handle_menu_click)
        main_layout.addWidget(self.menu_widget, 1)  # 1 part of 5 total

        # Main content widget placeholder (60% width)
        self.main_content_widget = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        main_layout.addWidget(self.main_content_widget, 3)  # 3 parts of 5 total

        # Reports section (20% width)
        self.reports_widget = ReportsWidget()  # Create an instance of the ReportsWidget
        main_layout.addWidget(self.reports_widget, 1)  # 1 part of 5 total

        # Load initial content - default to 'Home'
        self.show_content('Home')  # This ensures 'Home' is displayed by default

        # Initialize the claims processor
        global processor
        processor = ClaimsProcessor()  # Declare it globally for accessibility in ClaimsWidget
    def handle_menu_click(self, text):
        self.show_content(text)

    def show_content(self, section):
        # Clear the existing content
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add new content based on the menu item clicked
        if section == 'Home':
            widget = HomeWidget()
        elif section == 'Notifications':
            widget = NotificationsWidget()
        elif section == 'Claims':
            widget = ClaimsWidget()
        elif section == 'Bank Reconciliations':
            widget = BankReconciliationsWidget()
        elif section == 'Sort Documents':
            widget = SortDocsWidget()
        elif section == 'Settings':
            widget = SettingsWidget()
        elif section == 'Help':
            widget = HelpWidget()
        elif section == 'Logout':
            widget = LogoutWidget()
        else:
            widget = QLabel(f"Unknown section: {section}")

        self.main_content_layout.addWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
