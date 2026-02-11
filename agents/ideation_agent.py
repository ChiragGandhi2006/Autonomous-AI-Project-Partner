class IdeationAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, project_goal):
        prompt = f"""
You are an expert AI project architect.

Generate the project idea STRICTLY in this format:

IDEA_TITLE:
LEVEL:
OBJECTIVE:
KEY_FEATURES:
TECH_STACK:
REAL_WORLD_USER:

Project Goal:
{project_goal}
"""
        idea = self.llm.generate(prompt)

        # ✅ CORRECT MEMORY METHOD
        self.memory.add_short_term("idea", idea)

        return idea

    def add_features(self):
        idea = self.memory.get_short_term("idea")
        prompt = f"Suggest extra features for this project:\n{idea}"
        return self.llm.generate(prompt)
