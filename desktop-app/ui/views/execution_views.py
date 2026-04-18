from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from datetime import datetime

class TaskCard(QFrame):
    def __init__(self, task):
        super().__init__()
        # Clean, modern, minimalist styling
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 12px;
                padding: 12px 20px;
                margin-bottom: 8px;
            }
            QFrame:hover {
                border: 1px solid #C7D2FE;
                background-color: #F9FAFB;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side: Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title = QLabel(task.get("title", "Untitled Task"))
        title.setStyleSheet("font-size: 15px; font-weight: 700; color: #111827; border: none; background: transparent;")
        
        # Safely parse the deadline
        dl_str = task.get('dead_line', '')
        try:
            dl_obj = datetime.fromisoformat(dl_str.replace("Z", "+00:00"))
            formatted_dl = dl_obj.strftime("%b %d, %H:%M")
        except:
            formatted_dl = "Unknown"
            
        meta_str = f"Due: {formatted_dl}  •  Est: {task.get('estimated_duration', 0)}h"
        meta = QLabel(meta_str)
        meta.setStyleSheet("font-size: 12px; font-weight: 500; color: #6B7280; border: none; background: transparent;")
        
        text_layout.addWidget(title)
        text_layout.addWidget(meta)
        
        # Right side: AI Action Badge
        badge = QLabel("⚡ AI Prioritized")
        badge.setStyleSheet("""
            background-color: #EEF2FF; 
            color: #4F46E5; 
            padding: 4px 10px; 
            border-radius: 6px; 
            font-weight: 700; 
            font-size: 11px; 
            border: none;
        """)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(badge)

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