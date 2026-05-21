# core/workflow_engine.py

class WorkflowEngine:
    """
    Executes tasks in sequence
    """

    def __init__(self, task_manager):
        self.task_manager = task_manager

    def run(self):
        for task in self.task_manager.get_all_tasks():
            task["status"] = "IN_PROGRESS"
            # Simulated execution
            task["status"] = "COMPLETED"
