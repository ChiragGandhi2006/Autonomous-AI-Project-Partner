from services.llm_service import LLMService
from services.coding_service import CodingService

class Router:
    def __init__(self):
        self.llm = LLMService()
        self.coder = CodingService()

    def is_coding_query(self, prompt: str) -> bool:
        coding_keywords = [
            "code", "python", "java", "c++", "function",
            "bug", "error", "fix", "algorithm", "program",
            "script", "api", "implement", "class", "method"
        ]

        prompt_lower = prompt.lower()

        return any(word in prompt_lower for word in coding_keywords) or "```" in prompt

    def handle_prompt(self, prompt: str) -> str:
        try:
            if self.is_coding_query(prompt):
                print("⚡ Coding API used")
                return self.coder.generate_code(prompt)
            else:
                print("🤖 Local LLM used")
                return self.llm.generate_response(prompt)

        except Exception as e:
            return f"Error: {str(e)}"