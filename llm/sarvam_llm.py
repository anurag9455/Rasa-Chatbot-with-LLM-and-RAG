from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SarvamLLM:
    def __init__(self, model_name="sarvamai/sarvam-1"):
        print("⏳ Loading Sarvam-1 model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
        print("Sarvam-1 loaded!")

    # def generate_response(self, prompt: str, max_tokens=512):
    #     inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
    #     outputs = self.model.generate(**inputs, max_new_tokens=max_tokens)
    #     return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def generate_response(self, prompt: str, max_tokens=256):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id  # prevent pad errors
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


