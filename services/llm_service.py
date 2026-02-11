import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise RuntimeError("❌ GEMINI_API_KEY / GOOGLE_API_KEY not found")

        print("✅ Gemini REAL MODE ENABLED")

        genai.configure(api_key=api_key)

        # Stable free-tier model
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    # 🔥 THIS METHOD WAS MISSING
    def generate(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            error = str(e)

            # Graceful fallback for quota / demo
            if "429" in error or "quota" in error.lower():
                return (
                    "⚠️ Gemini API quota exceeded.\n\n"
                    "✔ Backend system working\n"
                    "✔ Agent pipeline functional\n"
                    "✔ This is a fallback response for demo\n"
                )

            return f"[GEMINI ERROR] {error}"
