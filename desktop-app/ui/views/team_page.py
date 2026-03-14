from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QHBoxLayout, QProgressBar, QScrollArea
from PyQt6.QtCore import Qt

class TeamPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Main Layout (contains scroll area)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        
        # Content Widget
        content_widget = QWidget()
        content_widget.setObjectName("ScrollContent")
        content_widget.setStyleSheet("#ScrollContent { background-color: transparent; }")
        
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("Team Workload Velocity")
        header.setObjectName("PageHeader")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-bottom: 20px;")
        layout.addWidget(header)
        
        # Grid for team cards
        grid = QGridLayout()
        grid.setSpacing(20)
        
        team_members = [
            ("Sarah K.", "Lead Architect", "3 Tasks", 70, "#5A4AD1"),
            ("Alex R.", "Product Engineer", "4 Tasks", 80, "#2C3E50"),
            ("Jordan M.", "Lead Architect", "5 Tasks", 90, "#2C3E50"),
            ("Emma L.", "Product Engineer", "6 Tasks", 100, "#2C3E50"),
            ("Chris P.", "UX Designer", "2 Tasks", 40, "#E67E22"),
            ("Mia Wong", "Frontend Dev", "5 Tasks", 85, "#27AE60")
        ]
        
        for i, (name, role, tasks, load, color) in enumerate(team_members):
            card = self.create_team_card(name, role, tasks, load, color)
            row = i // 2
            col = i % 2
            grid.addWidget(card, row, col)
            
        layout.addLayout(grid)
        layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_team_card(self, name, role, tasks, load, avatar_color):
        card = QFrame()
        card.setObjectName("TeamCard")
        # Removing border from Stylesheet for this specific card to use shadow cleanly if wanted, or keep it subtle
        card.setStyleSheet(f"""
            QFrame#TeamCard {{
                background-color: white; 
                border-radius: 16px; 
                border: 1px solid #F0F0F0;
            }}
        """)
        card.setFixedSize(400, 130)
        
        # Add Shadow
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 8))
        shadow.setOffset(0, 4)
        card.setGraphicsEffect(shadow)
        
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        
        # Avatar
        avatar = QLabel(name[0])
        avatar.setFixedSize(56, 56)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet(f"background-color: {avatar_color}; color: white; font-weight: bold; font-size: 20px; border-radius: 12px;")
        
        # Info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet("font-weight: 800; font-size: 15px; color: #2C3E50;")
        role_lbl = QLabel(role)
        role_lbl.setStyleSheet("color: #95A5A6; font-size: 12px; font-weight: 500;")
        
        # Load Bar
        bar_container = QHBoxLayout()
        bar = QProgressBar()
        # Make the bar mock visual with simple stylesheets
        bar.setFixedHeight(6)
        bar.setFixedWidth(100)
        bar.setTextVisible(False)
        bar.setValue(load)
        bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: #5A4AD1; border-radius: 3px; }} QProgressBar {{ background-color: #F0F0F0; border-radius: 3px; border: none; }}")
        bar_container.addWidget(bar)
        bar_container.addStretch()
        
        info_layout.addWidget(name_lbl)
        info_layout.addWidget(role_lbl)
        info_layout.addLayout(bar_container)
        
        # Tasks Stats
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(5)
        stats_lbl = QLabel(tasks)
        stats_lbl.setStyleSheet("font-weight: 800; font-size: 16px; color: #2C3E50;")
        stats_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        load_lbl = QLabel(f"LOAD: {load}%")
        load_lbl.setStyleSheet("color: #95A5A6; font-size: 10px; font-weight: 700;")
        load_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        stats_layout.addWidget(stats_lbl)
        stats_layout.addWidget(load_lbl)
        stats_layout.addStretch()
        
        card_layout.addWidget(avatar)
        card_layout.addSpacing(20)
        card_layout.addLayout(info_layout)
        card_layout.addStretch()
        card_layout.addLayout(stats_layout)
        
        return card
