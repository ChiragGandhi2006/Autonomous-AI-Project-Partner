from services.llm_service import LLMService


class EvaluationService:
    """
    Service to evaluate code or project output
    """

    def __init__(self):
        self.llm_service = LLMService()

    def evaluate(self, content: str) -> str:
        prompt = f"Evaluate the following output and provide improvement suggestions:\n{content}"
        return self.llm_service.generate_response(prompt)
