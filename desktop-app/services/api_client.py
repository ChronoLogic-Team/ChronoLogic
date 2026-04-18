import requests
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class FetchTasksThread(QThread):
    finished = pyqtSignal(list, str)

    def __init__(self, api_url, headers=None):
        super().__init__()
        self.api_url = api_url
        self.headers = headers or {} 

    def run(self):
        try:
            response = requests.get(self.api_url, headers=self.headers)
            if response.status_code == 200:
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit([], f"Error {response.status_code}")
        except Exception as e:
            self.finished.emit([], str(e))

class CreateTaskThread(QThread):
    finished = pyqtSignal(dict, str)

    def __init__(self, api_url, task_data, headers=None):
        super().__init__()
        self.api_url = api_url
        self.task_data = task_data
        self.headers = headers or {}

    def run(self):
        try:
            response = requests.post(self.api_url, json=self.task_data, headers=self.headers)
            if response.status_code == 201:
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit({}, f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit({}, str(e))

class UpdateTaskThread(QThread):
    finished = pyqtSignal(dict, str)

    def __init__(self, api_url, task_data, headers=None):
        super().__init__()
        self.api_url = api_url
        self.task_data = task_data
        self.headers = headers or {}

    def run(self):
        try:
            response = requests.patch(self.api_url, json=self.task_data, headers=self.headers)
            if response.status_code in (200, 201):
                self.finished.emit(response.json(), "")
            else:
                self.finished.emit({}, f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit({}, str(e))

class DeleteTaskThread(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, api_url, task_id, headers=None):
        super().__init__()
        self.api_url = api_url
        self.task_id = task_id
        self.headers = headers or {}

    def run(self):
        try:
            response = requests.delete(self.api_url, headers=self.headers)
            if response.status_code in (200, 204): 
                self.finished.emit(str(self.task_id), "")
            else:
                self.finished.emit(str(self.task_id), f"Error {response.status_code}: {response.text}")
        except Exception as e:
            self.finished.emit(str(self.task_id), str(e))

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
    task_deleted = pyqtSignal(str)
    
    login_successful = pyqtSignal(dict)
    login_failed = pyqtSignal(str)

    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        super().__init__()
        self.base_url = base_url
        self.access_token = None
        self.active_threads = [] 

    def _track_thread(self, thread):
        # THE FIX: Clean up old threads FIRST
        self.active_threads = [t for t in self.active_threads if t.isRunning()]
        # THEN safely store the new thread!
        self.active_threads.append(thread)

    def get_auth_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
        
    def login(self, email, password):
        thread = LoginThread(f"{self.base_url}/login/", {'email': email, 'password': password})
        thread.finished.connect(self._on_login_finished)
        thread.start() # Start it first
        self._track_thread(thread) # Then protect it

    def _on_login_finished(self, data, error):
        if error:
            self.login_failed.emit(error)
        elif 'error' in data:
            self.login_failed.emit(data['error'])
        elif not data.get('token'):
            self.login_failed.emit("Login failed: No token received.")
        else:
            self.access_token = data.get('token')
            self.login_successful.emit(data)

    def fetch_tasks(self):
        thread = FetchTasksThread(
            f"{self.base_url}/tasks/", 
            headers=self.get_auth_headers()
        )
        thread.finished.connect(self._on_fetch_tasks_finished)
        thread.start()
        self._track_thread(thread)

    def _on_fetch_tasks_finished(self, tasks, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Error: {error}")
        else:
            self.tasks_fetched.emit(tasks)

    def create_task(self, task_data):
        thread = CreateTaskThread(
            f"{self.base_url}/tasks/", 
            task_data,
            headers=self.get_auth_headers()
        )
        thread.finished.connect(self._on_task_created_finished)
        thread.start()
        self._track_thread(thread)
        
    def _on_task_created_finished(self, task, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Create Error: {error}")
        else:
            self.task_created.emit(task)

    def update_task(self, task_id, task_data):
        thread = UpdateTaskThread(
            f"{self.base_url}/tasks/{task_id}/", 
            task_data,
            headers=self.get_auth_headers()
        )
        thread.finished.connect(self._on_task_updated_finished)
        thread.start()
        self._track_thread(thread)

    def _on_task_updated_finished(self, task, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Update Error: {error}")
        else:
            self.task_updated.emit(task)

    def delete_task(self, task_id):
        thread = DeleteTaskThread(
            f"{self.base_url}/tasks/{task_id}/",
            task_id,
            headers=self.get_auth_headers()
        )
        thread.finished.connect(self._on_task_deleted_finished)
        thread.start()
        self._track_thread(thread)

    def _on_task_deleted_finished(self, task_id, error):
        if error:
            self.error_occurred.emit(error)
            print(f"API Delete Error: {error}")
        else:
            self.task_deleted.emit(task_id)