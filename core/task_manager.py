# core/task_manager.py

class TaskManager:
    """
    Manages tasks and their states
    """

    def __init__(self):
        self.tasks = []

    def add_task(self, task_name: str):
        task = {
            "task_name": task_name,
            "status": "PENDING"
        }
        self.tasks.append(task)

    def update_task_status(self, task_name: str, status: str):
        for task in self.tasks:
            if task["task_name"] == task_name:
                task["status"] = status

    def get_all_tasks(self):
        return self.tasks
