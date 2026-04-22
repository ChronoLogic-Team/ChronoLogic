from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class LogicFlowPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)

        container = QFrame()
        container.setObjectName("DashedContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("☊")
        icon.setStyleSheet("font-size: 60px; color: #5A4AD1; margin-bottom: 20px;")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Visual Logic Flow")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel("Toggle to visual node mode to see your project's critical path as a connected network of logic gates.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #777; font-size: 14px; margin: 10px 0 30px 0; max-width: 400px;")

        btn = QPushButton("Initialize Visualizer")
        btn.setObjectName("PrimaryButton")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedWidth(200)

        container_layout.addWidget(icon)
        container_layout.addWidget(title)
        container_layout.addWidget(desc)
        container_layout.addWidget(btn)

        layout.addWidget(container)
