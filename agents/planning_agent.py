class PlanningAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, idea):

        prompt = f"""
You are a senior software architect.

Give ONLY technical plan.

STRICT RULES:
- DO NOT repeat idea
- DO NOT repeat sentences
- MAX 5 lines per section

OUTPUT:

1. Architecture:
2. Tech Stack:
3. Steps:
4. Challenges:

IDEA:
{idea}
"""

        result = self.llm.generate(prompt)

        # Trim unwanted part
        if "1." in result:
            result = result[result.index("1."):]

        self.memory.add_short_term("plan", result)
        self.memory.add_short_term("last_output", result)

        return result

    def improve(self):
        plan = self.memory.get_short_term("plan")

        prompt = f"""
Improve this plan.

RULES:
- Do NOT repeat content

PLAN:
{plan}
"""

        return self.llm.generate(prompt)