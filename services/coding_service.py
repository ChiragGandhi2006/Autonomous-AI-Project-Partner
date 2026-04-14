import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class CodingService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def generate_code(self, prompt: str) -> str:
        response = self.model.generate_content(
            f"""
You are an expert software engineer.

Return ONLY clean, working code.
No explanation.
Proper formatting.

User Request:
{prompt}
"""
        )
        return response.text