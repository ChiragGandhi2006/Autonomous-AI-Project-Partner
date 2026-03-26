from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLMService:

    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            device_map="auto"
        )

    # 🔥 CLEAN OUTPUT (MAIN FIX)
    def clean_text(self, text, prompt):

        # Remove prompt echo
        if prompt in text:
            text = text.replace(prompt, "")

        # Remove duplicates
        lines = text.split("\n")
        unique_lines = []

        for line in lines:
            line = line.strip()
            if line and line not in unique_lines:
                unique_lines.append(line)

        return "\n".join(unique_lines)

    def get_max_tokens(self, prompt):
        if "code" in prompt.lower():
            return 700
        return 250

    def generate(self, prompt):

        max_tokens = self.get_max_tokens(prompt)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=0.2,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return self.clean_text(response, prompt)