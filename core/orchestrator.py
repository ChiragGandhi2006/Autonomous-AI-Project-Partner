from agents.ideation_agent import IdeationAgent
from agents.planning_agent import PlanningAgent
from agents.coder_agent import CoderAgent
from services.llm_service import LLMService
from memory.memory_manager import MemoryManager


class Orchestrator:
    def __init__(self):
        self.memory = MemoryManager()
        self.llm = LLMService()

        self.ideation_agent = IdeationAgent(self.memory, self.llm)
        self.planning_agent = PlanningAgent(self.memory, self.llm)
        self.coder_agent = CoderAgent(self.memory, self.llm)

    def initialize_project(self, goal):

        self.memory.clear_all()

        idea = self.ideation_agent.run(goal)
        plan = self.planning_agent.run(idea)

        return {
            "idea": idea,
            "plan": plan
        }

    def handle_action(self, action):

        action_lower = action.lower()

        # CODE
        if any(k in action_lower for k in [
            "code", "program", "function", "binary", "algorithm"
        ]):
            return self._generate_code(action)

        # PLAN IMPROVE
        elif "improve" in action_lower:
            return self.planning_agent.improve()

        # CONTINUE
        else:
            last = self.memory.get_short_term("last_output")

            prompt = f"""
Continue based on:

{last}

User:
{action}
"""

            return self.llm.generate(prompt)

    def _generate_code(self, action):

        idea = self.memory.get_short_term("idea")
        plan = self.memory.get_short_term("plan")

        return self.coder_agent.run(idea, plan, action)