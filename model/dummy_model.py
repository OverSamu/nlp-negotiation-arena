from model.base_model import BaseLLM
import random
import json

class DummyModel(BaseLLM):

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        responses = [
            {
                "shares": {"Alice": 50, "Bob": 50},
                "message": "I think this is a fair split."
            },
            {
                "shares": {"Alice": 70, "Bob": 30},
                "message": "I believe I deserve a larger share based on my contributions."
            },
            {
                "shares": {"Alice": 30, "Bob": 70},
                "message": "I think Bob has contributed more and should receive a larger share."
            },
            {
                "shares": {"Alice": 60, "Bob": 40},
                "message": "I am willing to compromise and take a slightly smaller share to maintain cooperation."
            }
        ]
        return json.dumps(random.choice(responses))
