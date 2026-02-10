from llama_cpp import Llama
from model.base_model import BaseLLM

class LlamaCppModel(BaseLLM):
    def __init__(self, model_path, temperature=0.7):
        self.llm = Llama(
            model_path=model_path,
            temperature=temperature,
            n_ctx=2048
        )

    def generate(self, prompt: str) -> str:
        output = self.llm(
            prompt,
            max_tokens=256
        )
        return output["choices"][0]["text"].strip()
