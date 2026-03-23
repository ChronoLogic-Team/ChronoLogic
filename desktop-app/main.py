import sys
from PyQt6.QtWidgets import QApplication
from ui.windows.main_window import MainWindow 
from ui.windows.login_window import LoginWindow
from services.api_client import APIClient

class AppController:
    def __init__(self):
        self.api_client = APIClient()
        self.login_window = LoginWindow(api_client=self.api_client)
        self.login_window.login_successful.connect(self.show_main_window)
        self.main_window = None
        
    def start(self):
        self.login_window.show()
        
    def show_main_window(self):
        self.login_window.close()
        # Initialize MainWindow only after successful login
        self.main_window = MainWindow(api_client=self.api_client)
        self.main_window.show()

def main():
    app = QApplication(sys.argv)
    
    # Use controller to manage window lifecycle
    controller = AppController()
    controller.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()