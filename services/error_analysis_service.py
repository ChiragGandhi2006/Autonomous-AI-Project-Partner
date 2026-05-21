from services.llm_service import LLMService


class ErrorAnalysisService:
    """
    Service to analyze errors and suggest fixes
    """

    def __init__(self):
        self.llm_service = LLMService()

    def analyze_error(self, error_message: str) -> str:
        prompt = f"Analyze the following error and suggest a fix:\n{error_message}"
        return self.llm_service.generate_response(prompt)
