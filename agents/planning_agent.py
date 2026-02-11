class PlanningAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, idea):
        prompt = f"""
You are a senior project planner.

Create a STEP-BY-STEP PLAN in this exact format:

PHASE_1:
PHASE_2:
PHASE_3:
PHASE_4:
FINAL_OUTPUT:

Project Idea:
{idea}
"""
        plan = self.llm.generate(prompt)

        # ✅ CORRECT MEMORY METHOD
        self.memory.add_short_term("plan", plan)

        return plan

    def improve(self):
        plan = self.memory.get_short_term("plan")
        prompt = f"Improve this plan:\n{plan}"
        improved = self.llm.generate(prompt)

        self.memory.add_short_term("plan", improved)
        return improved
