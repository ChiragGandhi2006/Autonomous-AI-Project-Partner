class ReviewAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, code):

        prompt = f"""
You are a senior code reviewer.

Analyze the code.

FORMAT:
1. Issues
2. Improvements
3. Optimization Suggestions

CODE:
{code}
"""

        return self.llm.generate(prompt)