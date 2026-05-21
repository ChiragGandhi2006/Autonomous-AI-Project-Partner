from services.llm_service import LLMService


class CodeGenerationService:
    """
    Service to generate code using LLM
    """

    def __init__(self):
        self.llm_service = LLMService()

    def generate_code(self, task_description: str) -> str:
        prompt = f"Write clean Python code for the following task:\n{task_description}"
        return self.llm_service.generate_response(prompt)
