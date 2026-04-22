from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtCore import Qt, QSize

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(260)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 25, 20, 25)

        logo_icon = QLabel("C")
        logo_icon.setStyleSheet("background-color: #5A4AD1; color: white; border-radius: 8px; font-weight: bold; font-size: 18px; padding: 5px 10px;")
        logo_text = QLabel("ChronoLogic")
        logo_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-left: 8px;")

        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        layout.addWidget(logo_container)

        self.add_nav_button(layout, "Dashboard", "assets/icons/dashboard.svg", checked=True)

        self.add_nav_button(layout, "Execution Plan", "assets/icons/timeline.svg")

        layout.addSpacing(20)

        projects_label = QLabel("MY WORKSPACES")
        projects_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1px;
            padding: 15px 0px 5px 20px;
        """)
        layout.addWidget(projects_label)

        self.add_project_item(layout, "Primary AI Engine", "#5A4AD1")
        self.add_project_item(layout, "University Thesis", "#2ECC71")

        layout.addStretch()

    def add_nav_button(self, layout, text, icon_path, checked=False):
        btn = QPushButton(text)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn)

    def add_project_item(self, layout, name, color):
        from PyQt6.QtWidgets import QPushButton
        from PyQt6.QtCore import Qt
        
        btn = QPushButton(f"  {name}")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # FIX: Ensure the entire stylesheet is wrapped in f""" ... """
        btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px 10px;
                border: none;
                border-radius: 6px;
                background-color: transparent;
                color: #6B7280;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #F3F4F6;
                color: #111827;
            }}
        """)
        
        layout.addWidget(btn)