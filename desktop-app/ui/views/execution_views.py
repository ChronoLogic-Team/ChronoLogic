from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import datetime

class TaskCard(QFrame):
    # This signal allows the card to tell the API to update the status
    status_changed = pyqtSignal(str, dict)

    def __init__(self, task):
        super().__init__()
        self.task_id = str(task.get("id", task.get("_id", "")))
        
        # Get AI Scores and Status
        cog_score = task.get("cognitive_score", 1.0)
        proc_risk = task.get("procrastination_risk", 1.0)
        ai_category = task.get("category", "Task")
        current_status = task.get("status", "Pending")

        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 12px 20px;
                margin-bottom: 8px;
            }
            QFrame:hover {
                border: 1px solid #4F46E5;
                background-color: #F9FAFB;
            }
        """)
        layout = QHBoxLayout(self)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title = QLabel(task.get("title", "Untitled Task"))
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #111827; border: none; background: transparent;")
        
        dl_str = task.get('dead_line', '')
        try:
            dl_obj = datetime.fromisoformat(dl_str.replace("Z", "+00:00"))
            formatted_dl = dl_obj.strftime("%b %d, %H:%M")
        except:
            formatted_dl = "Unknown"
            
        meta = QLabel(f"Due: {formatted_dl}  •  Est: {task.get('estimated_duration', 0)}h")
        meta.setStyleSheet("font-size: 12px; font-weight: 500; color: #6B7280; border: none; background: transparent;")
        
        # RESTORED: Neuro-Engine labels
        self.neuro_meta = QLabel(f"🧠 Cog Load: {cog_score} | ⚠️ Risk: {proc_risk}")
        self.neuro_meta.setStyleSheet("font-size: 11px; font-weight: 600; color: #4F46E5; border: none; background: transparent;")
        
        # RESTORED: Status Toggle Button
        self.status_btn = QPushButton(current_status)
        self.status_btn.setFixedWidth(90)
        self.status_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_status_style(current_status)
        self.status_btn.clicked.connect(self.cycle_status)
        
        text_layout.addWidget(title)
        text_layout.addWidget(meta)
        text_layout.addWidget(self.neuro_meta)
        text_layout.addWidget(self.status_btn)
        
        # Right side: Dynamic AI Action Badge
        badge = QLabel(f"⚡ {ai_category}")
        badge.setStyleSheet("background-color: #EEF2FF; color: #4F46E5; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 11px;")
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(badge)

    def update_status_style(self, status):
        styles = {"Pending": ("#F3F4F6", "#374151"), "In Progress": ("#DBEAFE", "#1E40AF"), "Done": ("#DCFCE7", "#16A34A")}
        bg, txt = styles.get(status, styles["Pending"])
        self.status_btn.setStyleSheet(f"background: {bg}; color: {txt}; border-radius: 6px; font-weight: 800; font-size: 10px; padding: 5px; border: none;")

    def cycle_status(self):
        steps = ["Pending", "In Progress", "Done"]
        current = self.status_btn.text()
        next_s = steps[(steps.index(current) + 1) % 3]
        self.status_btn.setText(next_s)
        self.update_status_style(next_s)
        self.status_changed.emit(self.task_id, {"status": next_s, "is_completed": next_s == "Done"})

class ExecutionView(QWidget):
    def __init__(self):
        super().__init__()
        # THE FIX: Force the main background to be transparent to remove the black void
        self.setStyleSheet("background-color: transparent;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        header = QLabel("Optimal Execution Plan")
        header.setStyleSheet("font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 15px; background: transparent;")
        layout.addWidget(header)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # THE FIX: Remove borders and backgrounds from the scroll area
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent;")
        
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 15, 0)
        
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)
        
    def update_tasks(self, api_tasks):
        # 1. Clear the old widgets
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                
        if not api_tasks:
            empty = QLabel("Your schedule is clear. Create a task to test the engine.")
            empty.setStyleSheet("color: #9CA3AF; font-size: 14px; font-weight: 500; background: transparent;")
            self.scroll_layout.addWidget(empty)
            return
            
        # --- 2. THE NEURO-SYMBOLIC ALGORITHM (BULLETPROOFED) ---
        from datetime import datetime, timezone
        now_utc = datetime.now(timezone.utc)
        
        for task in api_tasks:
            try:
                dl_str = task.get('dead_line', '')
                dl_obj = datetime.fromisoformat(dl_str.replace("Z", "+00:00"))
                hours_left = (dl_obj - now_utc).total_seconds() / 3600.0
            except:
                hours_left = 999.0 
                
            # THE FIX: Force everything to be a float just in case the DB sends null
            try:
                est_dur = float(task.get('estimated_duration') or 1.0)
                if est_dur <= 0: est_dur = 1.0
                
                symbolic_urgency = hours_left / est_dur
                
                cog_score = float(task.get('cognitive_score') or 1.0)      
                proc_risk = float(task.get('procrastination_risk') or 1.0) 
                reschedule_count = int(task.get('reschedule_count') or 0)
                
                neuro_multiplier = cog_score * proc_risk
                reschedule_penalty = 0.85 ** reschedule_count 
                
                final_ns_score = (symbolic_urgency / neuro_multiplier) * reschedule_penalty
                task['ns_score'] = final_ns_score
            except Exception as e:
                print(f"Math Error on task: {e}")
                task['ns_score'] = 999.0

        # 3. Sort the list! Lowest score goes to the very top.
        sorted_tasks = sorted(api_tasks, key=lambda x: x.get('ns_score', 999.0))
        
        # 4. Draw the sorted cards
        for task in sorted_tasks:
            card = TaskCard(task)
            self.scroll_layout.addWidget(card)