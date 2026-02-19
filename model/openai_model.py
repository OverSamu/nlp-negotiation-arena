from model.base_model import BaseLLM


class OpenAIModel(BaseLLM):
    def __init__(self, client, model_name="gpt-4o-mini", temperature=0.7):
        self.client = client
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        return response.choices[0].message.content.strip()
