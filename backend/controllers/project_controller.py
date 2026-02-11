from core.orchestrator import Orchestrator

orchestrator = Orchestrator()

def start_project(project_goal):
    return orchestrator.initialize_project(project_goal)

def continue_project(action):
    return orchestrator.handle_action(action)
