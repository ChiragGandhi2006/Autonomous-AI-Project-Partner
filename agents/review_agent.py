class ReviewAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self):
        code = self.memory.get_short_term("generated_code")
        prompt = f"Review and improve this code:\n{code}"
        return self.llm.generate(prompt)
