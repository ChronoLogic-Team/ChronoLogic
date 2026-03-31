from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QHBoxLayout, QFrame, QScroller, QScrollerProperties
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QDrag
from PyQt6.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, pyqtSignal
from datetime import datetime, timedelta

class TaskInfoWidget(QWidget):
    def __init__(self, title, meta, assignee_initial, assignee_color):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Avatar
        self.avatar = QLabel(assignee_initial)
        self.avatar.setFixedSize(32, 32)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet(f"background-color: {assignee_color}; color: white; font-weight: bold; border-radius: 16px; font-size: 12px;")
        
        # Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("font-weight: 600; font-size: 13px; color: #333;")
        self.meta_lbl = QLabel(meta)
        self.meta_lbl.setStyleSheet("color: #888; font-size: 11px;")
        
        text_layout.addWidget(self.title_lbl)
        text_layout.addWidget(self.meta_lbl)
        
        layout.addWidget(self.avatar)
        layout.addLayout(text_layout)
        layout.addStretch()

class DraggableTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.main_view = parent

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-chronologic-task"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-chronologic-task"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-chronologic-task"):
            item_data = event.mimeData().data("application/x-chronologic-task")
            data_stream = QDataStream(item_data, QIODevice.OpenModeFlag.ReadOnly)
            
            task_id = data_stream.readQString()
            duration_hours = data_stream.readInt()
            
            # Determine which row/col the mouse dropped onto
            drop_pos = event.position().toPoint()
            row = self.rowAt(drop_pos.y())
            col = self.columnAt(drop_pos.x())
            
            # Column 0 is the task details, cannot drop there
            if col <= 0 or row < 0:
                event.ignore()
                return
                
            event.acceptProposedAction()
            
            if self.main_view:
                self.main_view.handle_task_dropped(task_id, row, col, duration_hours)

class TimelineBarWidget(QWidget):
# ... (keep TimelineBarWidget unchanged) ...
    def __init__(self, task_id, color, duration):
        super().__init__()
        self.task_id = task_id
        self.duration = duration
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 15, 5, 15) 
        
        self.bar = QFrame()
        self.bar.setFixedHeight(24) 
        self.bar.setStyleSheet(self.bar.setStyleSheet(f"""
            QFrame {{
                background-color: {color}; 
                border-radius: 12px;
            }}
            QFrame:hover {{
                background-color: rgba(90, 74, 209, 0.8); /* Use a safe rgba color for hover */
            }}
        """))
        
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.bar.setGraphicsEffect(shadow)
        
        layout.addWidget(self.bar)
        self.drag_start_position = None
        
    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return
            
        drag = QDrag(self)
        mime_data = QMimeData()
        
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.OpenModeFlag.WriteOnly)
        data_stream.writeQString(str(self.task_id))
        data_stream.writeInt(self.duration)
        
        mime_data.setData("application/x-chronologic-task", item_data)
        drag.setMimeData(mime_data)
        
        drag.exec(Qt.DropAction.MoveAction)

class TimelineView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.api_client = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = DraggableTableWidget(self)
        
        # Generate 30-day timeline (Calendar View)
        # Starting from today (or a fixed start for demo consistency)
        self.start_date = datetime.now().date() - timedelta(days=2) # Start a bit back so we can scroll left
        
        self.days = []
        cols = ["TASK"]
        
        # Generate 60 days
        for d in range(60): # 60 Days for "scroll as much as I want" feel
            current_date = self.start_date + timedelta(days=d)
            # Format: "Mon 10"
            day_label = current_date.strftime("%a %d") 
            self.days.append(day_label)
            
            for h in range(24):
                cols.append(f"{day_label}\n{h:02d}:00")
                
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        
        # Style headers
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) 
        self.table.setColumnWidth(0, 280) # Fixed Sidebar width for Task Info
        
        # Time slots - Fixed width
        for i in range(1, len(cols)):
            self.table.setColumnWidth(i, 65) # 65px per hour
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)  # Turn off the default grid completely
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Add custom styling for a fresh, elegant grid background
        self.table.setStyleSheet("""
            QTableWidget { 
                border: none; 
                background-color: transparent;
            }
            QTableWidget::item {
                border-right: 1px solid #EBEBEB; 
                border-bottom: 1px solid #EBEBEB;
                border-left: 0px solid transparent; 
                border-top: 0px solid transparent;
                outline: none;
            }
        """)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) # Remove blue border on click-drag
        
        self.update_tasks([]) # Initialize empty or with default
        
        layout.addWidget(self.table)

        # Notion-like Scrolling Behavior
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # Connect scroll signal once
        try:
            self.table.horizontalScrollBar().valueChanged.connect(self.update_cur_time_line)
        except:
            pass
            
        # Enable QScroller for kinetic dragging
        # Note: In PyQt6, ScrollerGesture is ScrollerGestureType
        QScroller.grabGesture(self.table.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        QScroller.grabGesture(self.table.verticalHeader(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        QScroller.grabGesture(self.table.horizontalHeader(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        
        # Adjust friction for smooth "kinetic" feel
        scroller = QScroller.scroller(self.table.viewport())
        props = scroller.scrollerProperties()
        
        # ScrollMetric is in QScrollerProperties
        props.setScrollMetric(QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor, 0.6)
        props.setScrollMetric(QScrollerProperties.ScrollMetric.MinimumVelocity, 0.0)
        props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumClickThroughVelocity, 0.5)
        props.setScrollMetric(QScrollerProperties.ScrollMetric.AcceleratingFlickMaximumTime, 0.4)
        
        scroller.setScrollerProperties(props)
            
        # Initialize Drag variables (fallback/unused if QScroller works)
        self._is_panning = False
        self._pan_start_x = 0
        self._pan_start_scroll_x = 0

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_cur_time_line()

    def update_cur_time_line(self):
        
        now = datetime.now()
        current_minute = now.minute
        current_hour = now.hour
        
        day_offset_idx = 2 
        
        start_x = 280 # Col 0 width
        col_width = 60
        
        # Pixels for days passed
        days_pixels = day_offset_idx * (24 * col_width)
        
        # Pixels for today's time
        time_pixels = (current_hour * col_width) + ((current_minute / 60) * col_width)
        
        # Scroll offset
        scroll_x = self.table.horizontalScrollBar().value()
        
        target_x = start_x + int(days_pixels + time_pixels) - scroll_x
        
        if not hasattr(self, 'time_line'):
            self.time_line = QFrame(self.table.viewport())
            self.time_line.setStyleSheet("background-color: #E74C3C; border: none;")
            self.time_line.setFixedWidth(2)
            
            # Label
            self.time_label = QLabel("NOW", self.table.viewport())
            self.time_label.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold; font-size: 10px; padding: 2px 4px; border-radius: 4px;")
            self.time_label.adjustSize()
            
        # Update label text to real time
        self.time_label.setText(now.strftime("%a %H:%M"))
        self.time_label.adjustSize()
            
        # Update geometry
        full_height = self.table.viewport().height()
        
        # Visibility Check (if scrolled out of view)
        target_viewport_x = target_x # relative to viewport 0
        
        # Only show if within logical viewport range (approx)
        if target_viewport_x < 280 or target_viewport_x > self.table.viewport().width():
            self.time_line.hide()
            self.time_label.hide()
        else:
            self.time_line.show()
            self.time_label.show()
            self.time_line.setGeometry(target_viewport_x, 0, 2, full_height)
            self.time_label.move(target_viewport_x - (self.time_label.width() // 2), 0)
    
    # Custom signal for when a task is rescheduled via drop
    task_rescheduled = pyqtSignal(str, dict)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
             pass
        super().mousePressEvent(event)

    def handle_task_dropped(self, task_id, target_row, target_col, duration_hours):
        print(f"Task {task_id} dropped at Row {target_row}, Col {target_col}")
        
        # 1. Calculate the new datetime based on the drop column
        col_offset = target_col - 1
        day_offset = col_offset // 24
        hour_remainder = col_offset % 24
        
        # Reconstruct the target datetime
        new_date = self.start_date + timedelta(days=day_offset)
        new_deadline = datetime.combine(new_date, datetime.min.time()) + timedelta(hours=hour_remainder)
        
        print(f"Calculated New Deadline: {new_deadline.isoformat()}")
        
        # 2. Visually move the widget immediately
        for c in range(1, self.table.columnCount()):
            if self.table.cellWidget(target_row, c):
                self.table.removeCellWidget(target_row, c)
                self.table.setSpan(target_row, c, 1, 1)
                
        if target_col + duration_hours <= self.table.columnCount():
            self.table.setSpan(target_row, target_col, 1, duration_hours)
            new_bar = TimelineBarWidget(task_id, "#5A4AD1AA", duration_hours)
            self.table.setCellWidget(target_row, target_col, new_bar)
            
        # 3. Emit signal with payload for the API Client
        payload = {
            "deadline": new_deadline.isoformat() + "Z" 
        }
        self.task_rescheduled.emit(task_id, payload)

    def update_tasks(self, api_tasks):
        if not api_tasks:
            # Clear completely if there are no tasks from API
            api_tasks = []

        self.table.clearContents()
        self.table.clearSpans() # Clear spans before loop
        
        # Ensure a minimum number of rows so the empty grid is always visible 
        # (even when there are 0 tasks)
        min_rows = max(12, len(api_tasks))
        self.table.setRowCount(min_rows)
        
        # Set all rows to the default height
        for i in range(min_rows):
            self.table.setRowHeight(i, 70)
            
        # Example processing API tasks, falling back to defaults if needed
        # Backend Task model: title, category, deadline (str), estimated_duration (float), status
        for i, task in enumerate(api_tasks):
            title = task.get("title", "Unknown Task")
            cat = task.get("category", "General")
            status = task.get("status", "Pending")
            meta = f"{cat} • {status}"
            initial = title[:2].upper() if title else "UK"
            color = "#5A4AD1" # Default purple
            if status == "Completed": color = "#2ECC71"
            elif status == "In Progress": color = "#F1C40F"
            
            self.table.setRowHeight(i, 70)
            
            info_widget = TaskInfoWidget(title, meta, initial, color)
            self.table.setCellWidget(i, 0, info_widget)
            
            # Parse deadline for start position mapping (Mock mapping for now)
            # Parse deadline for start position mapping 
            try:
                # FIX 1: Changed "deadline" to "dead_line" to match database
                deadline_str = task.get("dead_line", "")
                deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                days_diff = (deadline.date() - self.start_date).days
                start_day_offset = max(0, days_diff)
                start_hour = deadline.hour # Use the actual hour instead of hardcoded 9AM
            except:
                start_day_offset = 2
                start_hour = 9
                
            duration = int(task.get("estimated_duration", 2))
            start_col = 1 + (start_day_offset * 24) + start_hour
            
            # FIX 2: Safely grab the ID (MongoDB uses 'id' or '_id' in the JSON)
            task_id = str(task.get("id", task.get("_id", i)))
            
            if start_col + duration <= self.table.columnCount():
                self.table.setSpan(i, start_col, 1, duration)
                
                # FIX 3: Pass all 3 required arguments to the widget!
                bar_widget = TimelineBarWidget(task_id, color + "AA", duration)
                
                self.table.setCellWidget(i, start_col, bar_widget)