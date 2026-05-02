import mimetypes
import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


class MediaAnalysisService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def analyze(self, prompt: str, files: list[dict]) -> str:
        user_prompt = prompt.strip() or "Solve or explain the attached file clearly."
        parts = [
            f"""
You are a helpful AI tutor and debugging assistant.

The user attached one or more files/images.
If it is an error screenshot, identify the error and give the fix.
If it is a concept/question image, solve it step by step.
If it is a code or text file, analyze the content and answer the user's request.
Be clear, practical, and concise.

User request:
{user_prompt}
"""
        ]

        unsupported_files = []

        for file_info in files:
            file_path = Path(file_info["path"])
            mime_type = file_info.get("mime_type") or mimetypes.guess_type(file_path.name)[0]

            if not mime_type:
                mime_type = "application/octet-stream"

            if mime_type.startswith("text/") or file_path.suffix.lower() in self._text_extensions():
                parts.append(self._text_part(file_path))
            elif mime_type.startswith("image/") or mime_type == "application/pdf":
                parts.append({
                    "mime_type": mime_type,
                    "data": file_path.read_bytes()
                })
            else:
                unsupported_files.append(file_path.name)

        if unsupported_files:
            parts.append(
                "Unsupported attachments skipped: " + ", ".join(unsupported_files)
            )

        response = self.model.generate_content(parts)
        return response.text

    def _text_part(self, file_path: Path) -> str:
        content = file_path.read_text(encoding="utf-8", errors="replace")
        max_chars = 30000

        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[File truncated because it is too large.]"

        return f"\nAttached file: {file_path.name}\n```text\n{content}\n```"

    def _text_extensions(self) -> set[str]:
        return {
            ".txt", ".md", ".csv", ".json", ".xml", ".yaml", ".yml",
            ".py", ".js", ".ts", ".html", ".css", ".java", ".cpp",
            ".c", ".h", ".hpp", ".cs", ".php", ".rb", ".go", ".rs",
            ".sql", ".log"
        }
