from model.base_model import BaseLLM
import random
import json

class DummyModel(BaseLLM):

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        responses = [
            {"my_share": 50, "your_share": 50, "message": "Fair division"},
            {"my_share": 80, "your_share": 20, "message": "I want the majority"},
            {"my_share": 30, "your_share": 70, "message": "I am willing to concede"},
            {"my_share": 60, "your_share": 40, "message": "I offer a compromise"},
            {"my_share": 90, "your_share": 10, "message": "I want almost everything"},
        ]
        return json.dumps(random.choice(responses))
