class LLMService:
    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        self.device = None
        self.tokenizer = None
        self.model = None
        self.system_prompt = (
            "You are a helpful AI assistant. "
            "Give clear, concise, and relevant answers."
        )

    def _load_model(self):
        if self.model is not None and self.tokenizer is not None:
            return

        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading local LLM on: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto",
        )

    def generate(self, prompt):
        self._load_model()

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=800,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )

        decoded = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )

        return decoded[len(text):].strip()

    def generate_response(self, prompt):
        return self.generate(prompt)


llm_service = LLMService()
