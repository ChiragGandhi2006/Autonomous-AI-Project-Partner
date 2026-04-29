from openai import OpenAI
import os
import base64
from dotenv import load_dotenv

# 🔥 FREE MODEL (Stable Diffusion)
from diffusers import StableDiffusionPipeline
import torch

load_dotenv()


class ImageService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # 🔥 Load free model (only once)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5"
            ).to(self.device)
        except:
            self.pipe = None

    # 🔹 PRIMARY: OpenAI
    def generate_image_openai(self, prompt, filename="generated.png"):
        result = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        with open(filename, "wb") as f:
            f.write(image_bytes)

        return filename

    # 🔹 FALLBACK: Stable Diffusion (FREE)
    def generate_image_local(self, prompt, filename="generated.png"):
        if self.pipe is None:
            return "❌ Free model not available"

        image = self.pipe(prompt).images[0]
        image.save(filename)

        return filename

    # 🔹 MAIN FUNCTION (AUTO SWITCH)
    def generate_image(self, prompt, filename="generated.png"):
        try:
            return self.generate_image_openai(prompt, filename)

        except Exception as e:
            print("OpenAI failed → switching to FREE model:", str(e))

            # fallback
            return self.generate_image_local(prompt, filename)

    # 🔹 IMAGE EDIT (OpenAI only)
    def edit_image(self, image_path, prompt, filename="edited.png"):
        try:
            result = self.client.images.edit(
                model="gpt-image-1",
                image=open(image_path, "rb"),
                prompt=prompt
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            with open(filename, "wb") as f:
                f.write(image_bytes)

            return filename

        except Exception as e:
            return f"❌ Edit failed: {str(e)}"