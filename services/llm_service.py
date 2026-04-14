from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLMService:
    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"🚀 Loading LLM on {self.device}...")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )

        print("✅ LLM Loaded Successfully!")

    # 🔹 MAIN FUNCTION (used by router)
    def generate_response(self, prompt: str) -> str:
        try:
            # Qwen chat format (IMPORTANT)
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]

            # Convert to proper format
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )

            inputs = self.tokenizer(
                text,
                return_tensors="pt"
            ).to(self.device)

            # Generate response
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )

            # Decode output
            response = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            # 🔥 Clean output (remove prompt part)
            if "assistant" in response.lower():
                response = response.split("assistant")[-1]

            return response.strip()

        except Exception as e:
            return f"LLM Error: {str(e)}"

    # 🔹 OPTIONAL (BACKWARD COMPATIBILITY)
    def generate(self, prompt: str) -> str:
        return self.generate_response(prompt)