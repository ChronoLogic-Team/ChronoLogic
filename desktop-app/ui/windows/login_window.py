from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QStackedWidget, QFrame, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

class LoginWindow(QWidget):
    login_successful = pyqtSignal()
    
    def __init__(self, api_client=None):
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("ChronoLogic - Welcome")
        self.setFixedSize(450, 550)
        
        # Connect APIClient signals if provided
        if self.api_client:
            self.api_client.login_successful.connect(self._on_login_success)
            self.api_client.login_failed.connect(self._on_login_failed)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7FE;
            }
            QFrame#MainCard {
                background-color: white;
                border-radius: 12px;
            }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #333;
            }
            QLabel#Title {
                font-size: 24px;
                font-weight: 800;
                color: #4A3AFF;
            }
            QLabel#Subtitle {
                font-size: 14px;
                color: #888;
                margin-bottom: 20px;
            }
            QLabel#InputLabel {
                font-size: 12px;
                font-weight: 600;
                color: #555;
                margin-top: 10px;
            }
            QLineEdit {
                padding: 0px 12px;
                min-height: 40px;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: #F9F9F9;
                font-size: 14px;
                color: #333333;
            }
            QLineEdit:focus {
                border: 2px solid #4A3AFF;
                background-color: #FFFFFF;
                color: #111111;
            }
            QPushButton {
                padding: 0px 12px;
                min-height: 44px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton#PrimaryBtn {
                background-color: #4A3AFF;
                color: white;
                border: none;
                margin-top: 15px;
            }
            QPushButton#PrimaryBtn:hover {
                background-color: #3D29E0;
            }
            QPushButton#SwitchBtn {
                background-color: transparent;
                color: #4A3AFF;
                border: none;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#SwitchBtn:hover {
                text-decoration: underline;
            }
        """)
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card = QFrame()
        card.setObjectName("MainCard")
        # simple shadow could be added here
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 40, 30, 40)
        card_layout.setSpacing(10)
        
        # Header
        title = QLabel("ChronoLogic")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.subtitle = QLabel("Login to your account")
        self.subtitle.setObjectName("Subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        card_layout.addWidget(title)
        card_layout.addWidget(self.subtitle)
        
        # Stacked Widget for Forms
        self.stack = QStackedWidget()
        
        # Login Form
        self.login_widget = QWidget()
        login_layout = QVBoxLayout(self.login_widget)
        login_layout.setContentsMargins(0, 0, 0, 0)
        
        self.log_email = QLineEdit()
        self.log_email.setPlaceholderText("Email address")
        self.log_pass = QLineEdit()
        self.log_pass.setPlaceholderText("Password")
        self.log_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_btn = QPushButton("Log In")
        login_btn.setObjectName("PrimaryBtn")
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.clicked.connect(self.handle_login)
        
        login_layout.addWidget(QLabel("Email", objectName="InputLabel"))
        login_layout.addWidget(self.log_email)
        login_layout.addWidget(QLabel("Password", objectName="InputLabel"))
        login_layout.addWidget(self.log_pass)
        login_layout.addWidget(login_btn)
        login_layout.addStretch()
        
        # Register Form
        self.reg_widget = QWidget()
        reg_layout = QVBoxLayout(self.reg_widget)
        reg_layout.setContentsMargins(0, 0, 0, 0)
        
        self.reg_name = QLineEdit()
        self.reg_name.setPlaceholderText("Full Name")
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email address")
        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        reg_btn = QPushButton("Create Account")
        reg_btn.setObjectName("PrimaryBtn")
        reg_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reg_btn.clicked.connect(self.handle_register)
        
        reg_layout.addWidget(QLabel("Name", objectName="InputLabel"))
        reg_layout.addWidget(self.reg_name)
        reg_layout.addWidget(QLabel("Email", objectName="InputLabel"))
        reg_layout.addWidget(self.reg_email)
        reg_layout.addWidget(QLabel("Password", objectName="InputLabel"))
        reg_layout.addWidget(self.reg_pass)
        reg_layout.addWidget(reg_btn)
        reg_layout.addStretch()
        
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.reg_widget)
        card_layout.addWidget(self.stack)
        
        # Switcher
        switch_layout = QHBoxLayout()
        self.switch_label = QLabel("Don't have an account?")
        self.switch_label.setStyleSheet("color: #888; font-size: 13px;")
        
        self.switch_btn = QPushButton("Register")
        self.switch_btn.setObjectName("SwitchBtn")
        self.switch_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_btn.clicked.connect(self.toggle_mode)
        
        switch_layout.addStretch()
        switch_layout.addWidget(self.switch_label)
        switch_layout.addWidget(self.switch_btn)
        switch_layout.addStretch()
        
        card_layout.addLayout(switch_layout)
        
        main_layout.addWidget(card)
        
    def toggle_mode(self):
        if self.stack.currentIndex() == 0:
            self.stack.setCurrentIndex(1)
            self.subtitle.setText("Create a new account")
            self.switch_label.setText("Already have an account?")
            self.switch_btn.setText("Log In")
        else:
            self.stack.setCurrentIndex(0)
            self.subtitle.setText("Login to your account")
            self.switch_label.setText("Don't have an account?")
            self.switch_btn.setText("Register")

    def handle_login(self):
        email = self.log_email.text().strip()
        pwd = self.log_pass.text().strip()
        
        if not email or not pwd:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
        
        if self.api_client:
            print(f"Logging in user: {email}")
            self.api_client.login(email, pwd)
        else:
            # Fallback if no API client (should not happen in production)
            print("WARNING: No API client connected!")
            QMessageBox.warning(self, "Error", "Cannot connect to server.")

    def handle_register(self):
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        pwd = self.reg_pass.text().strip()
        
        if not name or not email or not pwd:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return
            
        print(f"Registering user: {name} ({email})")
        # TODO: Connect to register API endpoint
        QMessageBox.information(self, "Info", "Registration coming soon! Please use an existing account.")

    def _on_login_success(self, data):
        """Called when the APIClient confirms login was successful."""
        print("Login successful! Token received.")
        self.login_successful.emit()

    def _on_login_failed(self, error_message):
        """Called when the APIClient reports login failure."""
        print(f"Login failed: {error_message}")
        QMessageBox.warning(self, "Login Failed", error_message)