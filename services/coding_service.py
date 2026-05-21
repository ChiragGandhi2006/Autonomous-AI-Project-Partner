import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional

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

    def explain_code(self, prompt: str, code: Optional[str] = None) -> str:
        code_context = f"\nCode to explain:\n```python\n{code}\n```" if code else ""

        response = self.model.generate_content(
            f"""
You are an expert programming teacher.

Explain the code in clear, simple language.
Do NOT rewrite the code with comments.
Do NOT return only code.
If the user asks for line-by-line explanation, explain each important line or block.
Use headings and bullets where helpful.

User Request:
{prompt}
{code_context}
"""
        )
        return response.text
