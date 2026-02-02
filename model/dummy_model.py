from model.base_model import BaseLLM
import random
import json

class DummyModel(BaseLLM):

    def generate(self, prompt: str) -> str:
        responses = [
            {"action": "propose", "share": 50, "message": "Divisione equa"},
            {"action": "propose", "share": 70, "message": "Richiesta iniziale"},
            {"action": "accept", "message": "Accetto"}
        ]
        return json.dumps(random.choice(responses))
