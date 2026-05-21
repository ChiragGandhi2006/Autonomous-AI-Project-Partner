from services.llm_service import LLMService
from services.coding_service import CodingService
from typing import Optional


class Router:
    def __init__(self):
        self.llm = LLMService()
        self.coder = CodingService()

    def is_code_explanation_query(self, prompt: str) -> bool:
        prompt_lower = prompt.lower()

        explanation_keywords = [
            "explain", "explanation", "line by line", "line-by-line",
            "dry run", "walkthrough", "understand", "what does this code do",
            "describe this code"
        ]

        code_reference_keywords = [
            "code", "program", "script", "function", "class", "method",
            "algorithm", "this", "above", "previous"
        ]

        has_explanation_intent = any(word in prompt_lower for word in explanation_keywords)
        has_code_reference = any(word in prompt_lower for word in code_reference_keywords) or "```" in prompt

        return has_explanation_intent and has_code_reference

    def is_coding_query(self, prompt: str) -> bool:
        if self.is_code_explanation_query(prompt):
            return True

        coding_keywords = [
            "code", "python", "java", "c++", "function",
            "bug", "error", "fix", "algorithm", "program",
            "script", "api", "implement", "class", "method"
        ]

        prompt_lower = prompt.lower()

        return any(word in prompt_lower for word in coding_keywords) or "```" in prompt

    def handle_prompt(self, prompt: str, code_context: Optional[str] = None) -> str:
        try:
            if self.is_code_explanation_query(prompt):
                print("Coding API used for explanation")
                return self.coder.explain_code(prompt, code_context)
            if self.is_coding_query(prompt):
                print("Coding API used")
                return self.coder.generate_code(prompt)

            print("Local LLM used")
            return self.llm.generate_response(prompt)

        except Exception as e:
            return f"Error: {str(e)}"
