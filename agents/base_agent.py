import json
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    def __init__(self, name, model):
        self.name = name
        self.model = model  # An instance of a language model

    @abstractmethod
    def system_prompt(self):
        """Defines the behavior of the agent"""
        pass

    def build_prompt(self, negotiation_state, agent_names, history=None):
        """Build the prompt for the LLM"""
        history_str = ""
        if history:
            for i, (author_name, proposal, message) in enumerate(history):
                if proposal is not None:
                    history_str += f"Round {i+1} - {author_name}: {proposal} ({message})\n"
                else:
                    history_str += f"Round {i+1} - {author_name}: {message}\n"
        else:
            history_str = "No previous proposals.\n"

        prompt = f"""
{self.system_prompt()}

Your name: {self.name}
All parties: {', '.join(agent_names)}

Negotiation state:
{negotiation_state}

Conversation history:
{history_str}

Please reply ONLY in JSON format, following this pattern:

{{
  "shares": {{
    "<agent_name>": <percentage>,
    "<agent_name>": <percentage>
  }},
  "message": "<short explanation>" 
}}
DO NOT use text outside of the JSON.
If you want to accept the current proposal, repeat the shares from the last proposal.
Always ensure that the shares sum up to 100%.
If you want to make a counteroffer, provide new shares that sum up to 100% and a brief explanation of your reasoning.
"""
        return prompt

    def act(self, negotiation_state, agent_names, history=None):
        """Generate the next move"""
        prompt = self.build_prompt(negotiation_state, agent_names, history)
        response = self.model.generate(prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {
                "action": "invalid",
                "raw": response
            }

        return parsed
