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

Please reply ONLY in JSON format, following this pattern:

{{
  "my_share": int (0-100, representing the percentage of the total resource you want to claim),
  "your_share": int (0-100, representing the percentage of the total resource you are willing to offer to the other agent),
  "message": "<short explanation>" 
}}
DO NOT use text outside of the JSON.
If you want to accept the last proposal, set "my_share" to the value proposed by the other agent and "your_share" to 100 - that value.
Always ensure that "my_share" + "your_share" equals 100, and that both values are between 0 and 100.
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
