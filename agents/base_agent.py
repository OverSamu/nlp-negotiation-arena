import json
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name, model):
        self.name = name
        self.model = model  # An instance of a language model
        self.memory = []

    def observe(self, message):
        """Save a message to memory"""
        self.memory.append(message)

    def reset(self):
        self.memory = []

    @abstractmethod
    def system_prompt(self):
        """Defines the behavior of the agent"""
        pass

    def build_prompt(self, negotiation_state):
        """Build the prompt for the LLM"""
        history = "\n".join(self.memory)

        prompt = f"""
{self.system_prompt()}

Negotiation state:
{negotiation_state}

Conversation history:
{history}

Please reply ONLY in JSON format, following one of these patterns:

PROPOSAL:
{{
  "action": "propose",
  "share": <integer between 0 and 100>,
  "message": "<short explanation>"
}}

ACCEPTANCE:
{{
  "action": "accept",
  "message": "<short explanation>"
}}

DO NOT use text outside of the JSON.
"""
        return prompt

    def act(self, negotiation_state):
        """Generate the next move"""
        prompt = self.build_prompt(negotiation_state)
        response = self.model.generate(prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {
                "action": "invalid",
                "raw": response
            }

        self.observe(f"{self.name}: {parsed}")
        return parsed
