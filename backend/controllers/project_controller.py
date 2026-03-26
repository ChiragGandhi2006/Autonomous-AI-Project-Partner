from core.orchestrator import Orchestrator

orchestrator = Orchestrator()


def start_project(goal):
    return orchestrator.initialize_project(goal)


def continue_project(action):
    return orchestrator.handle_action(action)