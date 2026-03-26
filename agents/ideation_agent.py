class IdeationAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, project_goal):

        prompt = f"""
You are an AI product expert.

Give ONLY project idea.

FORMAT:
1. Title
2. Problem
3. Solution
4. Features

RULES:
- Do NOT generate code
- Do NOT repeat text

INPUT:
{project_goal}
"""

        result = self.llm.generate(prompt)

        self.memory.add_short_term("idea", result)
        self.memory.add_short_term("last_output", result)

        return result