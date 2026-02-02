from model.base_model import BaseLLM
import random


class DummyModel(BaseLLM):

    def generate(self, prompt: str) -> str:
        responses = [
            "I propose a 50/50 split.",
            "I accept the proposal.",
            "I propose 70 for me and 30 for you.",
            "I do not accept, counter-proposing 60/40."
        ]
        return random.choice(responses)
