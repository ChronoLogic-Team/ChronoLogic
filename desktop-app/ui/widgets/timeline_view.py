from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QHBoxLayout, QFrame, QScroller, QScrollerProperties
from PyQt6.QtCore import Qt, QMimeData, QByteArray, QDataStream, QIODevice, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QDrag, QCursor
from datetime import datetime, timedelta

class TaskInfoWidget(QWidget):
    def __init__(self, title, meta, assignee_color):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 10, 0)
        layout.setSpacing(12)
        
        # Notion-style minimal dot indicator
        self.dot = QFrame()
        self.dot.setFixedSize(8, 8)
        self.dot.setStyleSheet(f"background-color: {assignee_color}; border-radius: 4px;")
        
        # Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        self.title_lbl = QLabel(title)
        # Notion's specific dark gray text
        self.title_lbl.setStyleSheet("font-weight: 500; font-size: 13px; color: #37352F;") 
        
        self.meta_lbl = QLabel(meta)
        self.meta_lbl.setStyleSheet("color: #9CA3AF; font-size: 11px;")
        
        text_layout.addWidget(self.title_lbl)
        text_layout.addWidget(self.meta_lbl)
        
        layout.addWidget(self.dot)
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
            
            # Determine drop location
            drop_pos = event.position().toPoint()
            row = self.rowAt(drop_pos.y())
            col = self.columnAt(drop_pos.x())
            
            # Prevent dropping on the sidebar (Column 0)
            if col <= 0 or row < 0:
                event.ignore()
                return
                
            event.acceptProposedAction()
            
            if self.main_view:
                self.main_view.handle_task_dropped(task_id, row, col, duration_hours)

class TimelineBarWidget(QWidget):
    def __init__(self, task_id, title, color, duration):
        super().__init__()
        self.task_id = task_id
        self.duration = duration
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 8, 2, 8) 
        
        self.bar = QFrame()
        self.bar.setFixedHeight(28) 
        
        # Notion-style Task Block: Slightly rounded, solid color, text inside
        self.bar.setStyleSheet(f"""
            QFrame {{
                background-color: {color}; 
                border-radius: 4px;
            }}
            QFrame:hover {{
                background-color: {color}DD; 
                border: 1px solid rgba(0,0,0,0.1);
            }}
        """)
        
        # Add the title text inside the block
        bar_layout = QHBoxLayout(self.bar)
        bar_layout.setContentsMargins(8, 0, 8, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-weight: 600; font-size: 11px;")
        
        bar_layout.addWidget(title_label)
        bar_layout.addStretch()
        
        layout.addWidget(self.bar)
        self.drag_start_position = None
        
    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().enterEvent(event)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if not self.drag_start_position:
            return
            
        # Add a slight delay before drag starts so it feels smooth
        if (event.pos() - self.drag_start_position).manhattanLength() < 5:
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
    # Custom signal for when a task is rescheduled via drop
    task_rescheduled = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.api_client = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = DraggableTableWidget(self)
        
        self.start_date = datetime.now().date() - timedelta(days=2) 
        self.days = []
        cols = ["Tasks"]
        
        for d in range(60): 
            current_date = self.start_date + timedelta(days=d)
            # Notion formats headers very cleanly
            day_label = current_date.strftime("%a %d") 
            self.days.append(day_label)
            for h in range(24):
                # Clean header formatting
                time_str = f"{h:02d}:00" if h % 2 == 0 else "" # Only show every 2 hours to reduce clutter
                cols.append(f"{day_label}\n{time_str}")
                
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) 
        self.table.setColumnWidth(0, 260) # Sidebar width
        
        for i in range(1, len(cols)):
            self.table.setColumnWidth(i, 40) # Slightly thinner columns for a cleaner look
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)  
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # NOTION STYLING: Faint lines, white background, clean headers
        self.table.setStyleSheet("""
            QTableWidget { 
                border: none; 
                background-color: #FFFFFF;
            }
            QTableWidget::item {
                border-right: 1px solid #EDEDED; 
                border-bottom: 1px solid #EDEDED;
                outline: none;
            }
            QHeaderView::section {
                background-color: #FFFFFF;
                border: none;
                border-bottom: 1px solid #EDEDED;
                border-right: 1px solid #EDEDED;
                color: #787774; /* Notion subtle text */
                font-size: 11px;
                font-weight: 500;
                padding-top: 5px;
            }
        """)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus) 
        
        self.update_tasks([]) 
        layout.addWidget(self.table)

        # Smooth scrolling logic
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        try:
            self.table.horizontalScrollBar().valueChanged.connect(self.update_cur_time_line)
        except:
            pass
            
        QScroller.grabGesture(self.table.viewport(), QScroller.ScrollerGestureType.LeftMouseButtonGesture)
        scroller = QScroller.scroller(self.table.viewport())
        props = scroller.scrollerProperties()
        props.setScrollMetric(QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor, 0.6)
        props.setScrollMetric(QScrollerProperties.ScrollMetric.MinimumVelocity, 0.0)
        scroller.setScrollerProperties(props)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_cur_time_line()

    def update_cur_time_line(self):
        now = datetime.now()
        current_minute = now.minute
        current_hour = now.hour
        
        day_offset_idx = 2 
        start_x = 260 
        col_width = 40
        
        days_pixels = day_offset_idx * (24 * col_width)
        time_pixels = (current_hour * col_width) + ((current_minute / 60) * col_width)
        
        scroll_x = self.table.horizontalScrollBar().value()
        target_x = start_x + int(days_pixels + time_pixels) - scroll_x
        
        if not hasattr(self, 'time_line'):
            self.time_line = QFrame(self.table.viewport())
            self.time_line.setStyleSheet("background-color: #E03E3E; border: none;") # Notion Red
            self.time_line.setFixedWidth(2)
            
            self.time_label = QLabel("Today", self.table.viewport())
            self.time_label.setStyleSheet("background-color: #E03E3E; color: white; font-weight: bold; font-size: 10px; padding: 2px 6px; border-radius: 4px;")
            self.time_label.adjustSize()
            
        self.time_label.setText(now.strftime("%H:%M"))
        self.time_label.adjustSize()
            
        full_height = self.table.viewport().height()
        target_viewport_x = target_x 
        
        if target_viewport_x < 260 or target_viewport_x > self.table.viewport().width():
            self.time_line.hide()
            self.time_label.hide()
        else:
            self.time_line.show()
            self.time_label.show()
            self.time_line.setGeometry(target_viewport_x, 0, 2, full_height)
            self.time_label.move(target_viewport_x - (self.time_label.width() // 2), 0)

    def handle_task_dropped(self, task_id, target_row, target_col, duration_hours):
        col_offset = target_col - 1
        day_offset = col_offset // 24
        hour_remainder = col_offset % 24
        
        new_date = self.start_date + timedelta(days=day_offset)
        new_deadline = datetime.combine(new_date, datetime.min.time()) + timedelta(hours=hour_remainder)
        
        # Visually clear the old location immediately
        for c in range(1, self.table.columnCount()):
            if self.table.cellWidget(target_row, c):
                self.table.removeCellWidget(target_row, c)
                self.table.setSpan(target_row, c, 1, 1)
                
        # API Update
        payload = {
            "dead_line": new_deadline.isoformat() + "Z" 
        }
        self.task_rescheduled.emit(task_id, payload)

    def jump_to_today(self):
        now = datetime.now()
        days_diff = (now.date() - self.start_date).days
        target_col = 1 + (days_diff * 24) + now.hour
        scroll_position = int((target_col - 4) * 40) # 40 is new col width
        self.table.horizontalScrollBar().setValue(max(0, scroll_position))

    def update_tasks(self, api_tasks):
        if not api_tasks:
            api_tasks = []

        self.table.clearContents()
        self.table.clearSpans() 
        
        min_rows = max(15, len(api_tasks)) # Give plenty of vertical space
        self.table.setRowCount(min_rows)
        
        for i in range(min_rows):
            self.table.setRowHeight(i, 44) # Notion standard row height
            
        for i, task in enumerate(api_tasks):
            title = task.get("title", "Untitled")
            cat = task.get("category", "Task")
            status = task.get("status", "To Do")
            meta = f"{cat.capitalize()} • {status}"
            
            # Notion-style muted colors
            color = "#5A4AD1" 
            if status == "Completed": color = "#0F7B6C" # Notion Green
            elif status == "In Progress": color = "#D9730D" # Notion Orange
            
            info_widget = TaskInfoWidget(title, meta, color)
            self.table.setCellWidget(i, 0, info_widget)
            
            try:
                deadline_str = task.get("dead_line", "")
                deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                days_diff = (deadline.date() - self.start_date).days
                start_day_offset = max(0, days_diff)
                start_hour = deadline.hour 
            except:
                start_day_offset = 2
                start_hour = 9
                
            duration = int(task.get("estimated_duration", 2))
            start_col = 1 + (start_day_offset * 24) + start_hour
            
            task_id = str(task.get("id", task.get("_id", i)))
            
            if start_col + duration <= self.table.columnCount():
                self.table.setSpan(i, start_col, 1, duration)
                
                # Pass the TITLE to the widget so it renders inside the block!
                bar_widget = TimelineBarWidget(task_id, title, color, duration)
                self.table.setCellWidget(i, start_col, bar_widget)

        self.jump_to_today()