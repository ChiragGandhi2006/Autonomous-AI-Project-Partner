class FeedbackAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, output):

        prompt = f"""
Give feedback on this output.

FORMAT:
- Strengths
- Weaknesses
- Suggestions

OUTPUT:
{output}
"""

        return self.llm.generate(prompt)