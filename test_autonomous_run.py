from core.orchestrator import Orchestrator

orchestrator = Orchestrator()
orchestrator.initialize_project("Build a Flask REST API")
result = orchestrator.execute()

print(result)
