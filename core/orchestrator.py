from agents.ideation_agent import IdeationAgent
from agents.planning_agent import PlanningAgent
from services.llm_service import LLMService
from memory.memory_manager import MemoryManager

class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.llm = LLMService()

        self.ideation_agent = IdeationAgent(self.memory, self.llm)
        self.planning_agent = PlanningAgent(self.memory, self.llm)

    # ---------------------------------
    # STEP 1: START PROJECT
    # ---------------------------------
    def initialize_project(self, project_goal):
        self.memory.clear_all()

        idea = self.ideation_agent.run(project_goal)
        plan = self.planning_agent.run(idea)

        return {
            "idea": idea,
            "plan": plan,
            "options": [
                "Generate detailed code",
                "Improve the plan",
                "Add extra features",
                "Debug existing code"
            ]
        }

    # ---------------------------------
    # STEP 2: CONTINUE PROJECT
    # ---------------------------------
    def handle_action(self, action):
        try:
            if action == "Generate detailed code":
                result = self._generate_code()

            elif action == "Improve the plan":
                result = self.planning_agent.improve()

            elif action == "Add extra features":
                result = self.ideation_agent.add_features()

            elif action == "Debug existing code":
                result = "Debugging logic will be added soon."

            else:
                result = "Unknown action."

            return {
                "success": True,
                "action": action,
                "result": result
            }

        except Exception as e:
            return {
                "success": False,
                "action": action,
                "result": f"Error occurred: {str(e)}"
            }

    # ---------------------------------
    # INTERNAL HELPER
    # ---------------------------------
    def _generate_code(self):
        idea = self.memory.get_short_term("idea")
        plan = self.memory.get_short_term("plan")

        prompt = f"""
        Generate full implementation code for this project.

        IDEA:
        {idea}

        PLAN:
        {plan}
        """

        return self.llm.generate(prompt)
