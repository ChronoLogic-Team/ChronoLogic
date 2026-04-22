from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QPushButton, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal

class DashboardPage(QWidget):
    task_edit_requested = pyqtSignal(dict)
    task_delete_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        content_widget = QWidget()
        content_widget.setObjectName("ScrollContent")
        content_widget.setStyleSheet("#ScrollContent { background-color: transparent; }")

        layout = QGridLayout(content_widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.health_card = QFrame()
        self.health_card.setObjectName("ContentCard")
        health_layout = QVBoxLayout(self.health_card)
        health_layout.setContentsMargins(20, 20, 20, 20)

        health_title = QLabel("Neuro-Activity Distribution")
        health_title.setObjectName("CardTitle")
        health_layout.addWidget(health_title)

        self.chart_area = QHBoxLayout()
        self.chart_area.setSpacing(15)
        health_layout.addLayout(self.chart_area)

        self.draw_bars({"Dev": 1, "ADM": 1, "LOG": 1})

        layout.addWidget(self.health_card, 0, 0)

        track_card = QFrame()
        track_card.setObjectName("OnTrackCard")
        track_layout = QVBoxLayout(track_card)
        track_layout.setContentsMargins(25, 30, 25, 30)

        icon = QLabel("⚡")
        icon.setStyleSheet("font-size: 32px; color: white; margin-bottom: 20px;")

        self.track_title = QLabel("System Idle")
        self.track_title.setStyleSheet("font-size: 26px; font-weight: 800; color: white; margin-bottom: 10px;")

        self.track_desc = QLabel('Analyze tasks in Execution Plan to see cognitive deployment.')
        self.track_desc.setWordWrap(True)
        self.track_desc.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.85);")

        self.energy_val_label = QLabel("0.0 Units")
        self.energy_val_label.setStyleSheet("font-size: 40px; font-weight: 900; color: white; margin-top: 10px;")

        track_layout.addWidget(icon)
        track_layout.addWidget(self.track_title)
        track_layout.addWidget(self.track_desc)
        track_layout.addStretch()
        track_layout.addWidget(self.energy_val_label)

        layout.addWidget(track_card, 0, 1)

        deps_card = QFrame()
        deps_card.setObjectName("ContentCard")
        deps_layout = QVBoxLayout(deps_card)
        deps_layout.setContentsMargins(20, 20, 20, 20)

        deps_title = QLabel("AI Focus Recommendation")
        deps_title.setObjectName("CardTitle")
        deps_layout.addWidget(deps_title)

        self.dep_item = QFrame()
        self.dep_item.setStyleSheet("background-color: #F5F3FF; border-radius: 10px; padding: 10px;")
        dep_row = QHBoxLayout(self.dep_item)

        alert_icon = QLabel("🧠")
        alert_icon.setFixedSize(32, 32)
        alert_icon.setStyleSheet("background-color: #EDE9FE; border-radius: 8px;")
        alert_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dep_info = QVBoxLayout()
        self.rec_title = QLabel("Ready for Deep Work")
        self.rec_title.setStyleSheet("font-weight: 700; color: #333; font-size: 14px;")
        self.rec_meta = QLabel("No high-risk bottlenecks.")
        self.rec_meta.setStyleSheet("color: #6366F1; font-size: 12px;")
        dep_info.addWidget(self.rec_title)
        dep_info.addWidget(self.rec_meta)

        dep_row.addWidget(alert_icon)
        dep_row.addLayout(dep_info)
        dep_row.addStretch()
        deps_layout.addWidget(self.dep_item)
        layout.addWidget(deps_card, 1, 0)

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
        layout.addWidget(deadlines_card, 1, 1)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def draw_bars(self, distribution):
        while self.chart_area.count():
            child = self.chart_area.takeAt(0)
            if child.widget(): child.widget().deleteLater()
            elif child.layout():
                while child.layout().count():
                    c = child.layout().takeAt(0)
                    if c.widget(): c.widget().deleteLater()

        self.chart_area.addStretch()
        for cat, val in distribution.items():
            container = QVBoxLayout()
            bar = QFrame()
            bar.setObjectName("BarChartBar")
            bar.setFixedWidth(35)
            bar.setFixedHeight(min(150, int(val) * 30))
            lbl = QLabel(cat[:3].upper())
            lbl.setObjectName("ChartLabel")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container.addStretch()
            container.addWidget(bar)
            container.addWidget(lbl)
            self.chart_area.addLayout(container)
        self.chart_area.addStretch()

    def update_stats(self, stats_data):
        print(f"📊 Dashboard Received: {stats_data}")
        energy = stats_data.get('total_brainpower', 0)
        completed = stats_data.get('tasks_completed', 0)
        dist = stats_data.get('category_distribution', {})

        self.energy_val_label.setText(f"{energy} Units")
        if energy > 0:
            self.track_title.setText("Neuro-Flow Active")
            self.track_desc.setText(f"AI verified {completed} technical objectives completed.")

        if dist:
            self.draw_bars(dist)

    def confirm_delete(self, task):
        task_id = str(task.get("id", task.get("_id", "")))
        if not task_id: return
        reply = QMessageBox.question(self, 'Confirm Deletion', f"Delete task?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.task_delete_requested.emit(task_id)

    def update_tasks(self, tasks):
        while self.deadlines_layout.count():
            item = self.deadlines_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        from datetime import datetime
        sorted_tasks = sorted(tasks, key=lambda x: x.get('dead_line', ''))[:4]

        for task in sorted_tasks:
            row_widget = QWidget()
            row = QHBoxLayout(row_widget)
            row.setContentsMargins(0,0,0,0)

            dot = QLabel("●")
            color = "#2ECC71" if task.get("status") == "Done" else "#5A4AD1"
            dot.setStyleSheet(f"color: {color};")

            lbl = QLabel(task.get("title", "Task")[:20])
            lbl.setStyleSheet("font-weight: 600; color: #555;")

            edit_btn = QPushButton("✏️")
            edit_btn.setStyleSheet("background: transparent; border: none; font-size: 14px;")
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.clicked.connect(lambda ch, t=task: self.task_edit_requested.emit(t))

            del_btn = QPushButton("🗑️")
            del_btn.setStyleSheet("background: transparent; border: none; font-size: 14px;")
            del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            del_btn.clicked.connect(lambda ch, t=task: self.confirm_delete(t))

            row.addWidget(dot); row.addWidget(lbl); row.addStretch()
            row.addWidget(edit_btn); row.addWidget(del_btn)
            self.deadlines_layout.addWidget(row_widget)