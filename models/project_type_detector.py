class ProjectTypeDetector:
    """
    Detects project type based on project description
    """

    def __init__(self):
        self.project_types = [
            "web_application",
            "machine_learning",
            "data_science",
            "automation",
            "api_service"
        ]

    def detect(self, project_description: str) -> str:
        text = project_description.lower()

        if "flask" in text or "api" in text or "backend" in text:
            return "api_service"
        elif "machine learning" in text or "model" in text:
            return "machine_learning"
        elif "data" in text or "analysis" in text:
            return "data_science"
        elif "automation" in text or "script" in text:
            return "automation"
        else:
            return "web_application"
