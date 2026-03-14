from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QScrollArea
from PyQt6.QtCore import Qt

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # Main Wrapper Layout
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
        
        layout = QGridLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 1. Project Health Velocity (Bar Chart)
        health_card = QFrame()
        health_card.setObjectName("ContentCard")
        health_layout = QVBoxLayout(health_card)
        health_layout.setContentsMargins(20, 20, 20, 20)
        
        health_title = QLabel("Project Health Velocity")
        health_title.setObjectName("CardTitle")
        health_layout.addWidget(health_title)
        
        # Chart Container
        chart_area = QHBoxLayout()
        chart_area.addStretch()
        chart_area.setSpacing(15)
        
        # Data: Height factor, Color override (optional)
        bars_data = [40, 60, 30, 80, 50, 90, 75]
        
        for val in bars_data:
            bar_container = QVBoxLayout()
            bar_container.setSpacing(10)
            
            bar = QFrame()
            bar.setObjectName("BarChartBar")
            bar.setFixedWidth(30)
            bar.setFixedHeight(val * 2) 
            # Make the last bar slightly lighter or different if needed
            
            bar_container.addStretch() # Push bar down
            bar_container.addWidget(bar)
            
            chart_area.addLayout(bar_container)
            
        chart_area.addStretch()
        health_layout.addLayout(chart_area)
        
        # X-Axis Labels
        labels_layout = QHBoxLayout()
        labels_layout.addStretch()
        labels_layout.setSpacing(15)
        for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]:
            lbl = QLabel(day)
            lbl.setObjectName("ChartLabel")
            lbl.setFixedWidth(30)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            labels_layout.addWidget(lbl)
        labels_layout.addStretch()
        
        health_layout.addLayout(labels_layout)
        health_layout.addStretch() # Push everything to top

        layout.addWidget(health_card, 0, 0)

        # 2. On Track Card
        track_card = QFrame()
        track_card.setObjectName("OnTrackCard")
        track_layout = QVBoxLayout(track_card)
        track_layout.setContentsMargins(25, 30, 25, 30)
        
        icon = QLabel("⚡")
        icon.setStyleSheet("font-size: 32px; color: rgba(255,255,255,0.9); margin-bottom: 20px;")
        
        track_title = QLabel("On Track")
        track_title.setStyleSheet("font-size: 26px; font-weight: 800; color: white; margin-bottom: 10px;")
        
        track_desc = QLabel('Your current "Infrastructure" branch is 12% faster than baseline estimates.')
        track_desc.setWordWrap(True)
        track_desc.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.85); line-height: 1.4;")
        
        track_layout.addWidget(icon)
        track_layout.addStretch()
        track_layout.addWidget(track_title)
        track_layout.addWidget(track_desc)
        track_layout.addStretch()
        
        btn = QPushButton("View Insights")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.2); 
                color: white; 
                border-radius: 10px; 
                padding: 12px; 
                font-weight: bold; 
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """)
        track_layout.addWidget(btn)
        
        layout.addWidget(track_card, 0, 1)

        # 3. Critical Dependencies
        deps_card = QFrame()
        deps_card.setObjectName("ContentCard")
        deps_layout = QVBoxLayout(deps_card)
        deps_layout.setContentsMargins(20, 20, 20, 20)
        
        deps_title = QLabel("Critical Dependencies")
        deps_title.setObjectName("CardTitle")
        deps_layout.addWidget(deps_title)
        
        dep_item = QFrame()
        dep_item.setStyleSheet("background-color: #FFF5F5; border-radius: 10px; padding: 10px;")
        dep_row = QHBoxLayout(dep_item)
        
        alert_icon = QLabel("!")
        alert_icon.setFixedSize(32, 32)
        alert_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alert_icon.setStyleSheet("background-color: #FFDEDE; color: #E74C3C; font-weight: bold; border-radius: 8px; font-size: 16px;")
        
        dep_info = QVBoxLayout()
        dep_name = QLabel("API Integration Layer")
        dep_name.setStyleSheet("font-weight: 700; color: #333; font-size: 14px;")
        dep_meta = QLabel("Blocked by T-101")
        dep_meta.setStyleSheet("color: #E74C3C; font-size: 12px; font-weight: 600;")
        dep_info.addWidget(dep_name)
        dep_info.addWidget(dep_meta)
        
        dep_row.addWidget(alert_icon)
        dep_row.addSpacing(10)
        dep_row.addLayout(dep_info)
        dep_row.addStretch()
        dep_row.addWidget(QLabel("→"))
        
        deps_layout.addWidget(dep_item)
        deps_layout.addStretch()
        
        layout.addWidget(deps_card, 1, 0)

        # 4. Upcoming Deadlines
        deadlines_card = QFrame()
        deadlines_card.setObjectName("ContentCard")
        dead_layout = QVBoxLayout(deadlines_card)
        dead_layout.setContentsMargins(20, 20, 20, 20)
        
        dead_title = QLabel("Upcoming Deadlines")
        dead_title.setObjectName("CardTitle")
        dead_layout.addWidget(dead_title)
        
        self.deadlines_container = QWidget()
        self.deadlines_layout = QVBoxLayout(self.deadlines_container)
        self.deadlines_layout.setContentsMargins(0,0,0,0)
        
        dead_layout.addWidget(self.deadlines_container)
        dead_layout.addStretch()

        layout.addWidget(deadlines_card, 1, 1)

        # Column stretching
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def update_tasks(self, tasks):
        # Clear existing deadlines
        while self.deadlines_layout.count():
            item = self.deadlines_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Simple cleanup for nested layouts we create below
                while item.layout().count():
                     child = item.layout().takeAt(0)
                     if child.widget(): child.widget().deleteLater()
                item.layout().deleteLater()
                
        # Sort tasks by deadline if possible, for now just show top 4
        from datetime import datetime
        sorted_tasks = reversed(tasks[-4:]) # Last added
        
        for task in sorted_tasks:
            title = task.get("title", "Unknown")
            try:
                deadline_dt = datetime.fromisoformat(task.get("deadline", "").replace("Z", "+00:00"))
                time_str = deadline_dt.strftime("%H:%M")
            except:
                time_str = "--:--"
                
            color = "#5A4AD1"
            if task.get("status") == "Completed": color = "#2ECC71"
            
            row_widget = QWidget()
            row = QHBoxLayout(row_widget)
            row.setContentsMargins(0,0,0,0)
            
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 12px;")
            lbl = QLabel(title[:20] + ("..." if len(title) > 20 else ""))
            lbl.setStyleSheet("font-weight: 600; color: #555; font-size: 13px;")
            time_lbl = QLabel(time_str)
            time_lbl.setStyleSheet("color: #333; font-size: 13px; font-weight: 600;")
            
            row.addWidget(dot)
            row.addSpacing(10)
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(time_lbl)
            
            self.deadlines_layout.addWidget(row_widget)

