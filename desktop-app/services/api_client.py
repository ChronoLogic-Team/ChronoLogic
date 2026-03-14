import requests
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class FetchTasksThread(QThread):
    finished = pyqtSignal(list, str) # tasks, error_message

    # NEW: Accepts headers as a parameter
    def __init__(self, api_url, headers=None):
        super().__init__()
        self.api_url = api_url
        self.headers = headers or {} 

    def run(self):
        try:
            # NEW: Attaches headers to the GET request
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code == 200:
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit([], f"Error {response.status_code}")
        except Exception as e:
            self.finished.emit([], str(e))

class CreateTaskThread(QThread):
    finished = pyqtSignal(dict, str)

    # NEW: Accepts headers as a parameter
    def __init__(self, api_url, task_data, headers=None):
        super().__init__()
        self.api_url = api_url
        self.task_data = task_data
        self.headers = headers or {}

    def run(self):
        try:
            # NEW: Attaches headers to the POST request
            response = requests.post(self.api_url, json=self.task_data, headers=self.headers)
            if response.status_code == 201:
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit({}, f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit({}, str(e))

class UpdateTaskThread(QThread):
    finished = pyqtSignal(dict, str)

    # NEW: Accepts headers as a parameter
    def __init__(self, api_url, task_data, headers=None):
        super().__init__()
        self.api_url = api_url
        self.task_data = task_data
        self.headers = headers or {}

    def run(self):
        try:
            # NEW: Attaches headers to the PATCH request
            response = requests.patch(self.api_url, json=self.task_data, headers=self.headers)
            if response.status_code in (200, 201):
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit({}, f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit({}, str(e))

# NEW THREAD: Specifically for sending login credentials
class LoginThread(QThread):
    finished = pyqtSignal(dict, str)
    def __init__(self, api_url, credentials):
        super().__init__()
        self.api_url = api_url
        self.credentials = credentials
    def run(self):
        try:
            response = requests.post(self.api_url, json=self.credentials)
            if response.status_code == 200:
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit({}, response.json().get('error', 'Login Failed'))
        except Exception as e:
            self.finished.emit({}, str(e))


class APIClient(QObject):
    tasks_fetched = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    task_created = pyqtSignal(dict)
    task_updated = pyqtSignal(dict)
    
    # NEW: Signals for Login success/failure
    login_successful = pyqtSignal(dict)
    login_failed = pyqtSignal(str)

    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        super().__init__()
        self.base_url = base_url
        self._fetch_thread = None
        self._create_thread = None
        self._update_thread = None
        
        # NEW: The variable where the app remembers the user's Token
        self.access_token = None

    # NEW: Formats the pocketed token into a recognized ID Badge
    def get_auth_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
        
    # NEW: Method called by LoginWindow to start the Login process
    def login(self, email, password):
        self._login_thread = LoginThread(f"{self.base_url}/login/", {'email': email, 'password': password})
        self._login_thread.finished.connect(self._on_login_finished)
        self._login_thread.start()

    # NEW: Method called when Login finishes. Saves the token!
    def _on_login_finished(self, data, error):
        if error:
            self.login_failed.emit(error)
        else:
            self.access_token = data.get('token')
            self.login_successful.emit(data)

    def fetch_tasks(self):
        # NEW: Injects the Auth Headers into the Thread
        self._fetch_thread = FetchTasksThread(
            f"{self.base_url}/tasks/", 
            headers=self.get_auth_headers()
        )
        self._fetch_thread.finished.connect(self._on_fetch_tasks_finished)
        self._fetch_thread.start()

    def _on_fetch_tasks_finished(self, tasks, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Error: {error}")
        else:
            self.tasks_fetched.emit(tasks)

    def create_task(self, task_data):
        # NEW: Injects the Auth Headers into the Thread
        self._create_thread = CreateTaskThread(
            f"{self.base_url}/tasks/", 
            task_data,
            headers=self.get_auth_headers()
        )
        self._create_thread.finished.connect(self._on_task_created_finished)
        self._create_thread.start()
        
    def _on_task_created_finished(self, task, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Create Error: {error}")
        else:
            self.task_created.emit(task)

    def update_task(self, task_id, task_data):
        # NEW: Injects the Auth Headers into the Thread
        self._update_thread = UpdateTaskThread(
            f"{self.base_url}/tasks/{task_id}/", 
            task_data,
            headers=self.get_auth_headers()
        )
        self._update_thread.finished.connect(self._on_task_updated_finished)
        self._update_thread.start()

    def _on_task_updated_finished(self, task, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Update Error: {error}")
        else:
            self.task_updated.emit(task)
