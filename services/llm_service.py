import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


class LLMService:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name)
        self.system_prompt = (
            "You are a helpful AI assistant. "
            "Give clear, concise, and relevant answers."
        )

    def generate(self, prompt):
        response = self.model.generate_content(
            f"{self.system_prompt}\n\n{prompt}"
        )
        return response.text

    def generate_response(self, prompt):
        return self.generate(prompt)


llm_service = LLMService()