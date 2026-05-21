from core.orchestrator import Orchestrator

orchestrator = Orchestrator()
orchestrator.initialize_project("Build an AI-powered chatbot")

tasks = orchestrator.execute()

for task in tasks:
    print(task)
