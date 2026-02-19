from model.base_model import BaseLLM


class OpenAIModel(BaseLLM):
    def __init__(self, client, model_name="gpt-4o-mini", temperature=0.7):
        self.client = client
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            instructions=system_prompt,
            input=user_prompt,
            temperature=self.temperature
        )

        return response.output_text.strip()
