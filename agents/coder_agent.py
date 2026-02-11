class CoderAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self):
        idea = self.memory.get_short_term("idea")
        plan = self.memory.get_short_term("plan")

        prompt=f"""
    You are a professional embedded system engineer.
    

    Generate code using this formate ONLY:

    LANGUAGE:
    FILES:
    CODE:
    COMMENTS:

    Idea:
    {idea}

    Plan:
    {plan}
    """
        code = self.llm.generate(prompt)
        self.memory.add_short_term("generated_code", code)
        return code
        

       
