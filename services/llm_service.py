from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LLMService:

    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"🚀 Loading model on: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )

        # ✅ KEEP SYSTEM PROMPT GENERIC (VERY IMPORTANT)
        self.system_prompt = (
            "You are a helpful AI assistant. "
            "Give clear, concise, and relevant answers."
        )

    # 🔥 MAIN FUNCTION
    def generate(self, prompt):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        # ✅ APPLY CHAT TEMPLATE
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt"
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=800,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

        decoded = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # ✅ REMOVE PROMPT PART (VERY IMPORTANT)
        response = decoded[len(text):].strip()

        return response


# ✅ SINGLETON INSTANCE
llm_service = LLMService()