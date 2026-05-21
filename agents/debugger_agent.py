class DebuggerAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self):
        code = self.memory.get_short_term("generated_code")
        prompt = f"Debug the following code and explain fixes:\n{code}"
        return self.llm.generate(prompt)
