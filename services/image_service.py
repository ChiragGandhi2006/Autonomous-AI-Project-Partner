import base64
import os
import urllib.parse
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ImageService:
    """Cloud-safe image generation.

    Uses OpenAI (gpt-image-1) when an OPENAI_API_KEY is set, otherwise
    falls back to pollinations.ai which needs no API key. No local models.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = (
            OpenAI(api_key=self.api_key)
            if OpenAI is not None and self.api_key
            else None
        )

    def generate_image(self, prompt, filename="generated.png") -> str:
        """Returns the saved image path, or raises on failure."""
        prompt = (prompt or "").strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        if self.client is not None:
            try:
                return self._generate_openai(prompt, filename)
            except Exception as exc:
                print("OpenAI image generation failed, falling back:", str(exc))

        return self._generate_pollinations(prompt, filename)

    def _generate_openai(self, prompt: str, filename: str) -> str:
        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        output_path = Path(filename)
        output_path.write_bytes(image_bytes)

        return str(output_path)

    def _generate_pollinations(self, prompt: str, filename: str) -> str:
        enhanced_prompt = (
            f"{prompt}, high quality, modern, professional, realistic, detailed"
        )

        image_url = (
            "https://image.pollinations.ai/prompt/"
            f"{urllib.parse.quote(enhanced_prompt)}"
            "?width=1024&height=1024&nologo=true"
        )

        try:
            response = requests.get(image_url, timeout=90)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise RuntimeError("Image generation timed out")
        except Exception as exc:
            raise RuntimeError(f"Image service failed: {exc}")

        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            raise RuntimeError("Invalid image response from service")

        output_path = Path(filename)
        output_path.write_bytes(response.content)

        return str(output_path)

    def edit_image(self, image_path: str, prompt: str, filename="edited.png") -> str:
        if self.client is None:
            raise RuntimeError("Image editing requires an OPENAI_API_KEY")

        result = self.client.images.edit(
            model="gpt-image-1",
            image=open(image_path, "rb"),
            prompt=prompt,
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        output_path = Path(filename)
        output_path.write_bytes(image_bytes)

        return str(output_path)