from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QFile, QTextStream

from ui.widgets.sidebar import Sidebar
from ui.views.dashboard_page import DashboardPage
from ui.views.execution_views import ExecutionView

class MainWindow(QMainWindow):
    def __init__(self, api_client): 
        super().__init__()
        self.setWindowTitle("ChronoLogic")
        self.setGeometry(100, 100, 1280, 800)
        self.api_client = api_client 
        self.overdue_task_titles = []
        self.load_styles()
        self.setup_ui() 
        self.api_client.stats_fetched.connect(self.dashboard_page.update_stats)
        self.api_client.tasks_fetched.connect(self.on_tasks_fetched)
        self.api_client.error_occurred.connect(self.on_api_error)
        self.api_client.task_created.connect(self.on_task_created)
        self.api_client.task_updated.connect(self.on_task_updated)
        self.api_client.task_deleted.connect(lambda task_id: print(f"Deleted task {task_id}"))
        self.api_client.task_deleted.connect(lambda _: self.api_client.fetch_tasks())

    def load_styles(self):
        file = QFile("assets/styles.qss")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def setup_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("centralwidget")
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        self.create_top_bar(content_layout)
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        if hasattr(self.dashboard_page, 'task_edit_requested'):
            self.dashboard_page.task_edit_requested.connect(self.open_edit_task_dialog)
            self.dashboard_page.task_delete_requested.connect(self.api_client.delete_task)
        self.execution_page = ExecutionView()
        self.execution_page.status_changed.connect(self.api_client.update_task)
        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.execution_page)
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_widget)
        self.connect_sidebar()

    def create_top_bar(self, layout):
        top_bar = QHBoxLayout()
        page_title = QLabel("My AI Workspace")
        page_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search tasks...")
        search_input.setObjectName("SearchInput")
        self.notif_btn = QPushButton("🔔")
        self.notif_btn.setObjectName("IconButton")
        self.notif_btn.setStyleSheet("color: #333; background: transparent; border: none; font-size: 16px;")
        self.notif_btn.clicked.connect(self.show_overdue_tasks)
        new_task_btn = QPushButton("+ New Task")
        new_task_btn.setObjectName("NewTaskButton")
        new_task_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_task_btn.clicked.connect(self.open_new_task_dialog)
        top_bar.addWidget(page_title)
        top_bar.addStretch()
        top_bar.addWidget(search_input)
        top_bar.addWidget(self.notif_btn) 
        top_bar.addWidget(new_task_btn)
        layout.addLayout(top_bar)

    def connect_sidebar(self):    
        buttons = self.sidebar.findChildren(QPushButton, "SidebarButton")
        for btn in buttons:
            if btn.text() == "Dashboard":
                btn.clicked.connect(lambda checked, idx=0: self.switch_page(idx))
            elif btn.text() == "Execution Plan":
                btn.clicked.connect(lambda checked, idx=1: self.switch_page(idx))

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        if index == 0:
            print("📊 Dashboard active: Fetching Neuro-Stats...")
            self.api_client.fetch_stats()
        buttons = self.sidebar.findChildren(QPushButton, "SidebarButton")
        for btn in buttons:
            if index == 0 and btn.text() == "Dashboard":
                btn.setChecked(True)
            elif index == 1 and btn.text() == "Execution Plan":
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def on_tasks_fetched(self, tasks):
        if hasattr(self.dashboard_page, 'update_tasks'):
            self.dashboard_page.update_tasks(tasks)
        if hasattr(self.execution_page, 'update_tasks'):
            self.execution_page.update_tasks(tasks)
        from datetime import datetime, timezone
        overdue_count = 0
        self.overdue_task_titles = [] 
        now_utc = datetime.now(timezone.utc)
        for task in tasks:
            dl_str = task.get('dead_line', '')
            try:
                dl_obj = datetime.fromisoformat(dl_str.replace("Z", "+00:00"))
                if dl_obj < now_utc:
                    overdue_count += 1
                    self.overdue_task_titles.append(task.get('title', 'Unknown Task'))
            except:
                pass
        if overdue_count > 0:
            self.notif_btn.setText(f"🔔 {overdue_count}")
            self.notif_btn.setStyleSheet("background-color: #DC2626; color: white; border-radius: 12px; padding: 4px 10px; font-weight: bold;")
        else:
            self.notif_btn.setText("🔔")
            self.notif_btn.setStyleSheet("color: #333; background: transparent; border: none; font-size: 16px;")

    def show_overdue_tasks(self):
        if not hasattr(self, 'overdue_task_titles') or not self.overdue_task_titles:
            return
        msg = "The following tasks have missed their deadlines:\n\n"
        for title in self.overdue_task_titles:
            msg += f"• {title}\n"
        QMessageBox.warning(self, "Overdue Tasks", msg)

    def on_api_error(self, error):
        print(f"MainWindow API Error: {error}")

    def open_new_task_dialog(self):
        from ui.widgets.new_task_dialog import NewTaskDialog
        dialog = NewTaskDialog(self)
        if dialog.exec():
            task_data = dialog.get_task_data()
            self.api_client.create_task(task_data)
            
    def open_edit_task_dialog(self, task_data):
        from ui.widgets.new_task_dialog import NewTaskDialog
        dialog = NewTaskDialog(self, task_data=task_data)
        if dialog.exec():
            updated_data = dialog.get_task_data()
            task_id = updated_data.pop("id", None)
            if task_id:
                self.api_client.update_task(task_id, updated_data)
            
    def on_task_created(self, task):
        print("Task created successfully:", task.get("title"))
        self.api_client.fetch_tasks()
        
    def on_task_updated(self, task):
        print("Task updated successfully:", task.get("title"))
        self.api_client.fetch_tasks()