class CoderAgent:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self, idea, plan, user_input=None):

        user_input = user_input or ""

        # 🔥 ALWAYS treat direct user query as code request
        return self._generate_clean_code(user_input)

    # ─────────────────────────────
    # MAIN CODE GENERATION
    # ─────────────────────────────
    def _generate_clean_code(self, user_input):

        prompt = f"""
You are a professional programmer.

Generate ONLY code.

STRICT RULES:
- Output ONLY code
- No explanation
- No folder structure
- No headings
- No markdown
- Start directly with code

USER REQUEST:
{user_input}
"""

        result = self.llm.generate(prompt)

        # 🔥 HARD CLEANING
        result = self._extract_code(result)

        self.memory.add_short_term("last_output", result)

        return result

    # ─────────────────────────────
    # CODE EXTRACTOR (VERY POWERFUL)
    # ─────────────────────────────
    def _extract_code(self, text):

        lines = text.split("\n")
        clean_lines = []

        skip_words = [
            "folder", "structure", "project",
            "file:", "directory", "how to run",
            "here is", "below is", "example"
        ]

        for line in lines:
            line_strip = line.strip()
            line_lower = line_strip.lower()

            # ❌ Remove unwanted lines
            if any(word in line_lower for word in skip_words):
                continue

            # ❌ Remove headings
            if line_strip.startswith("#") and len(line_strip) < 10:
                continue

            clean_lines.append(line)

        return "\n".join(clean_lines).strip()