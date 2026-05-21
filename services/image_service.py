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