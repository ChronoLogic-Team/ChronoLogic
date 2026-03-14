from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

class StatsCard(QFrame):
    def __init__(self, title, value, status_color="#5A4AD1", icon_path=None):
        super().__init__()
        self.setObjectName("StatsCard")
        self.setFixedSize(220, 120)
        self.setup_ui(title, value, status_color)

    def setup_ui(self, title, value, status_color):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Icon placeholder (Circle with icon inside)
        icon_circle = QLabel()
        icon_circle.setFixedSize(40, 40)
        icon_circle.setStyleSheet(f"background-color: {status_color}15; border-radius: 20px; color: {status_color}; font-weight: bold; qproperty-alignment: AlignCenter;")
        icon_circle.setText("•") # Replace with actual icon

        layout.addWidget(icon_circle)
        layout.addStretch()

        value_label = QLabel(value)
        value_label.setObjectName("StatsValue")
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setObjectName("StatsTitle")
        layout.addWidget(title_label)
        
        # Add slight shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 10))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
