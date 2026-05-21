from core.orchestrator import Orchestrator

orchestrator = Orchestrator()


def run_agents(data: dict):
    result = orchestrator.execute()
    return {
        "message": "Agents executed",
        "memory_state": result
    }
