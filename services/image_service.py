<<<<<<< HEAD
=======
<<<<<<< HEAD
import requests
import urllib.parse
import uuid
from pathlib import Path


class ImageService:

    @staticmethod
    def generate_image(prompt):
        try:
            prompt = prompt.strip()

            if not prompt:
                return {
                    "status": "error",
                    "message": "Prompt cannot be empty"
                }

            enhanced_prompt = f"""
            {prompt},
            high quality,
            modern,
            professional,
            realistic,
            detailed
            """

            encoded_prompt = urllib.parse.quote(
                enhanced_prompt
            )

            image_url = (
                f"https://image.pollinations.ai/prompt/"
                f"{encoded_prompt}"
            )

            response = requests.get(
                image_url,
                timeout=60
            )

            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"API failed with status {response.status_code}"
                }

            content_type = response.headers.get(
                "Content-Type",
                ""
            )

            if "image" not in content_type:
                return {
                    "status": "error",
                    "message": "Invalid image response"
                }

            output_dir = Path(
                "generated_images"
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            filename = (
                f"image_{uuid.uuid4().hex}.png"
            )

            output_path = (
                output_dir / filename
            )

            with open(
                output_path,
                "wb"
            ) as f:
                f.write(response.content)

            return {
                "status": "success",
                "path": str(output_path)
            }

        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "Image generation timeout"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
=======
>>>>>>> 4ca64e112040db182ea1d170d487ab2cfe6d46da
import base64
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class ImageService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.pipe = None
        self.device = None

    def generate_image_openai(self, prompt, filename="generated.png"):
        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        with open(filename, "wb") as f:
            f.write(image_bytes)

        return filename

    def _load_local_pipeline(self):
        if self.pipe is not None:
            return

        try:
            import torch
            from diffusers import StableDiffusionPipeline

            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5"
            ).to(self.device)
        except Exception as e:
            print("Local image model unavailable:", str(e))
            self.pipe = None

    def generate_image_local(self, prompt, filename="generated.png"):
        self._load_local_pipeline()

        if self.pipe is None:
            return "Free image model not available"

        image = self.pipe(prompt).images[0]
        image.save(filename)

        return filename

    def generate_image(self, prompt, filename="generated.png"):
        try:
            return self.generate_image_openai(prompt, filename)
        except Exception as e:
            print("OpenAI image generation failed. Trying local model:", str(e))
            return self.generate_image_local(prompt, filename)

    def edit_image(self, image_path, prompt, filename="edited.png"):
        try:
            result = self.client.images.edit(
                model="gpt-image-1",
                image=open(image_path, "rb"),
                prompt=prompt,
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            with open(filename, "wb") as f:
                f.write(image_bytes)

            return filename

        except Exception as e:
            return f"Edit failed: {str(e)}"
<<<<<<< HEAD
=======
>>>>>>> 8e40865095191439b0aa74490add438f1c48bbb0
>>>>>>> 4ca64e112040db182ea1d170d487ab2cfe6d46da
