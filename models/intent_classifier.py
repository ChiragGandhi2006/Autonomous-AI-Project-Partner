class IntentClassifier:
    """
    Classifies user intent based on input text
    """

    def __init__(self):
        self.supported_intents = [
            "build_project",
            "debug_error",
            "review_code",
            "generate_code",
            "general_query"
        ]

    def classify(self, user_input: str) -> str:
        text = user_input.lower()

        if "build" in text or "create" in text:
            return "build_project"
        elif "error" in text or "bug" in text:
            return "debug_error"
        elif "review" in text:
            return "review_code"
        elif "code" in text:
            return "generate_code"
        else:
            return "general_query"
