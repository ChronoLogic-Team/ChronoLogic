from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy
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

        # 1. Logo Area
        logo_container = QWidget()
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(20, 25, 20, 25)
        
        logo_icon = QLabel("C") # Placeholder or use actual icon
        logo_icon.setStyleSheet("background-color: #5A4AD1; color: white; border-radius: 8px; font-weight: bold; font-size: 18px; padding: 5px 10px;")
        logo_text = QLabel("ChronoLogic")
        logo_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-left: 8px;")
        
        logo_layout.addWidget(logo_icon)
        logo_layout.addWidget(logo_text)
        logo_layout.addStretch()
        layout.addWidget(logo_container)

        # 2. Main Navigation
        self.add_nav_button(layout, "Dashboard", "assets/icons/dashboard.svg", checked=True)
        self.add_nav_button(layout, "Timeline", "assets/icons/timeline.svg")
        self.add_nav_button(layout, "Logic Flow", "assets/icons/logic.svg")
        self.add_nav_button(layout, "Team", "assets/icons/team.svg")

        layout.addSpacing(20)

        # 3. "MY PROJECTS" Section
        projects_label = QLabel("MY PROJECTS")
        projects_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1px;
            padding: 15px 0px 5px 20px;
        """)
        layout.addWidget(projects_label)

        self.add_project_item(layout, "Q1 Product Launch", "#5A4AD1")
        self.add_project_item(layout, "Market Research", "#2ECC71")
        self.add_project_item(layout, "Brand Refresh", "#F1C40F")

        layout.addStretch()

    def add_nav_button(self, layout, text, icon_path, checked=False):
        btn = QPushButton(text)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # TODO: Add icon support when assets are available
        # btn.setIcon(QIcon(icon_path))
        # btn.setIconSize(QSize(20, 20))
        layout.addWidget(btn)

    def add_project_item(self, layout, text, color_hex):
        # Create a perfectly smooth colored circle for the icon
        size = 8
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color_hex))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, size, size)
        painter.end()
        
        btn = QPushButton(f" {text}")
        btn.setIcon(QIcon(pixmap))
        btn.setIconSize(QSize(size, size))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Elegant styling aligned with modern UI trends
        btn.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 10px 15px 10px 20px;
                margin: 2px 10px;
                border-radius: 8px;
                color: #6B7280;
                font-size: 13px;
                font-weight: 500;
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color_hex}1A; /* 10% opacity tint */
                color: #111827;
            }}
        """)
        layout.addWidget(btn)
