from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QComboBox, QDateTimeEdit, QDoubleSpinBox, 
                             QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QDateTime

class NewTaskDialog(QDialog):
    # UPGRADE: Added task_data=None to handle editing!
    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        
        # Change titles based on whether we are creating or editing
        dialog_title = "Edit Task" if task_data else "Create New Task"
        button_text = "Save Changes" if task_data else "Create Task"
        
        self.setWindowTitle(dialog_title)
        self.setFixedSize(500, 550)  
        
        self.setStyleSheet("""
            QDialog { background-color: #ffffff; }
            QLabel { font-weight: 600; color: #4A4A4A; font-size: 13px; margin-top: 5px; }
            QLabel#HeaderTitle { font-size: 20px; font-weight: 800; color: #1A1A1A; margin-bottom: 15px; margin-top: 0px; }
            QLineEdit, QComboBox, QDateTimeEdit, QDoubleSpinBox, QTextEdit { padding: 6px 10px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #F9FAFB; color: #111827; font-size: 13px; min-height: 24px; }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateTimeEdit:focus, QDoubleSpinBox:focus { border: 1px solid #4A3AFF; background-color: #FFFFFF; }
            QPushButton { padding: 10px 16px; border-radius: 6px; font-weight: bold; font-size: 13px; }
            QPushButton#SaveBtn { background-color: #4A3AFF; color: white; border: none; }
            QPushButton#SaveBtn:hover { background-color: #3D29E0; }
            QPushButton#CancelBtn { background-color: #F3F4F6; color: #4B5563; border: none; }
            QPushButton#CancelBtn:hover { background-color: #E5E7EB; }
            QComboBox QAbstractItemView { border: 1px solid #e5e7eb; border-radius: 6px; background-color: #ffffff; selection-background-color: #4A3AFF; selection-color: #ffffff; outline: none; padding: 4px; }
            QComboBox QAbstractItemView::item { min-height: 28px; padding: 4px 8px; border-radius: 4px; color: #374151; }
            QComboBox QAbstractItemView::item:hover { background-color: #f3f4f6; color: #111827; }
            QCalendarWidget { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; }
            QCalendarWidget QToolButton { height: 28px; color: #111827; font-weight: bold; border-radius: 4px; background-color: transparent; }
            QCalendarWidget QToolButton:hover { background-color: #f3f4f6; }
            QCalendarWidget QMenu { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; }
            QCalendarWidget QSpinBox { background-color: #f9fafb; border: 1px solid #d1d5db; border-radius: 4px; margin-top: 2px; margin-bottom: 2px; }
            QCalendarWidget QAbstractItemView:enabled { color: #111827; background-color: #ffffff; selection-background-color: #4A3AFF; selection-color: #ffffff; border-radius: 4px; outline: 0; }
            QCalendarWidget QAbstractItemView:disabled { color: #9ca3af; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)
        
        header_label = QLabel(dialog_title)
        header_label.setObjectName("HeaderTitle")
        layout.addWidget(header_label)
        
        layout.addWidget(QLabel("Task Title"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter a clear, concise title...")
        layout.addWidget(self.title_input)
        
        layout.addWidget(QLabel("Description"))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Add details about this task...")
        self.desc_input.setFixedHeight(100)
        layout.addWidget(self.desc_input)
        
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        
        cat_layout = QVBoxLayout()
        cat_layout.addWidget(QLabel("Category"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["study", "work", "personal", "shopping", "other"])
        cat_layout.addWidget(self.category_combo)
        
        dur_layout = QVBoxLayout()
        dur_layout.addWidget(QLabel("Estimated Duration"))
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.5, 100.0)
        self.duration_spin.setSingleStep(0.5)
        self.duration_spin.setValue(2.0)
        self.duration_spin.setSuffix(" hrs")
        dur_layout.addWidget(self.duration_spin)
        
        row1.addLayout(cat_layout)
        row1.addLayout(dur_layout)
        layout.addLayout(row1)
        
        layout.addWidget(QLabel("Deadline"))
        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setDateTime(QDateTime.currentDateTime().addDays(1)) 
        self.deadline_edit.setCalendarPopup(True)
        layout.addWidget(self.deadline_edit)
        
        layout.addStretch()
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #E5E7EB;")
        layout.addWidget(line)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("CancelBtn")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton(button_text)
        save_btn.setObjectName("SaveBtn")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.validate_and_accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)

        # UPGRADE: If we are editing, pre-fill all the fields!
        if self.task_data:
            self.pre_fill_data()

    def pre_fill_data(self):
        self.title_input.setText(self.task_data.get("title", ""))
        self.desc_input.setText(self.task_data.get("description", ""))
        
        cat = self.task_data.get("category", "study")
        index = self.category_combo.findText(cat)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
            
        self.duration_spin.setValue(float(self.task_data.get("estimated_duration", 2.0)))
        
        dl_str = self.task_data.get("dead_line")
        if dl_str:
            try:
                # Convert backend ISO string to PyQt DateTime
                dt = QDateTime.fromString(dl_str.replace("Z", "").split("+")[0], Qt.DateFormat.ISODate)
                if dt.isValid():
                    self.deadline_edit.setDateTime(dt)
            except Exception as e:
                pass

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Task title cannot be empty.")
            return
        self.accept()
        
    def get_task_data(self):
        dt = self.deadline_edit.dateTime().toPyDateTime()
        data = {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "category": self.category_combo.currentText(),
            "dead_line": dt.isoformat(), 
            "estimated_duration": self.duration_spin.value()
        }
        # If we are editing, send the ID back so the API knows which one to update
        if self.task_data:
            task_id = self.task_data.get("id", self.task_data.get("_id"))
            if task_id:
                data["id"] = str(task_id)
        return data