from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QFile, QTextStream

# Import Widgets
from ui.widgets.sidebar import Sidebar

# Import Pages
from ui.views.dashboard_page import DashboardPage
from ui.views.timeline_page import TimelinePage

class MainWindow(QMainWindow):
    def __init__(self, api_client): 
        super().__init__()
        self.setWindowTitle("ChronoLogic")
        self.setGeometry(100, 100, 1280, 800)
        
        self.load_styles()
        self.setup_ui()
        
        self.api_client = api_client 
        self.api_client.tasks_fetched.connect(self.on_tasks_fetched)
        self.api_client.error_occurred.connect(self.on_api_error)
        self.api_client.task_created.connect(self.on_task_created)
        self.api_client.task_updated.connect(self.on_task_updated)
        self.api_client.fetch_tasks()
        
        if hasattr(self.timeline_page, 'timeline_view'):
            self.timeline_page.timeline_view.task_rescheduled.connect(self.on_task_rescheduled)

    def load_styles(self):
        file = QFile("assets/styles.qss")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def setup_ui(self):
        # Main Container
        main_widget = QWidget()
        main_widget.setObjectName("centralwidget")
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # 2. Main Content Area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        
        # -- Top Bar --
        self.create_top_bar(content_layout)
        
        # -- Stacked Widget for Pages --
        self.stack = QStackedWidget()
        self.dashboard_page = DashboardPage()
        self.timeline_page = TimelinePage()
        
        self.stack.addWidget(self.dashboard_page) # Index 0
        self.stack.addWidget(self.timeline_page)  # Index 1
        
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_widget)

        # Connect Sidebar Signals
        self.connect_sidebar()

    def create_top_bar(self, layout):
        top_bar = QHBoxLayout()
        
        page_title = QLabel("My AI Workspace")
        page_title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search tasks...")
        search_input.setObjectName("SearchInput")
        
        notif_btn = QPushButton("🔔")
        notif_btn.setObjectName("IconButton")
        
        new_task_btn = QPushButton("+ New Task")
        new_task_btn.setObjectName("NewTaskButton")
        new_task_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_task_btn.clicked.connect(self.open_new_task_dialog)

        top_bar.addWidget(page_title)
        top_bar.addStretch()
        top_bar.addWidget(search_input)
        top_bar.addWidget(notif_btn)
        top_bar.addWidget(new_task_btn)
        
        layout.addLayout(top_bar)

    def connect_sidebar(self):    
        buttons = self.sidebar.findChildren(QPushButton, "SidebarButton")
        
        page_map = {
            "Dashboard": 0,
            "Timeline": 1
        }
        
        for btn in buttons:
            if btn.text() in page_map:
                index = page_map[btn.text()]
                btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        
        buttons = self.sidebar.findChildren(QPushButton, "SidebarButton")
        page_map = ["Dashboard", "Timeline"]
        
        if 0 <= index < len(page_map):
            target_text = page_map[index]
            for btn in buttons:
                if btn.text() == target_text:
                    btn.setChecked(True)
                elif btn.text() in page_map: 
                    btn.setChecked(False)

    def on_tasks_fetched(self, tasks):
        if hasattr(self.dashboard_page, 'update_tasks'):
            self.dashboard_page.update_tasks(tasks)
        if hasattr(self.timeline_page, 'update_tasks'):
            self.timeline_page.update_tasks(tasks)

    def on_api_error(self, error):
        print(f"MainWindow API Error: {error}")

    def open_new_task_dialog(self):
        from ui.widgets.new_task_dialog import NewTaskDialog
        dialog = NewTaskDialog(self)
        if dialog.exec():
            task_data = dialog.get_task_data()
            self.api_client.create_task(task_data)
            
    def on_task_created(self, task):
        print("Task created successfully:", task.get("title"))
        self.api_client.fetch_tasks()
        
    def on_task_rescheduled(self, task_id, payload):
        print(f"Syncing drag & drop for task {task_id} with payload: {payload}")
        self.api_client.update_task(task_id, payload)
        
    def on_task_updated(self, task):
        print("Task updated successfully:", task.get("title"))
        self.api_client.fetch_tasks()