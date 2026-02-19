import json
from abc import ABC, abstractmethod

from environment.history import History
from model.base_model import BaseLLM


class BaseAgent(ABC):
    name: str
    model: BaseLLM

    def __init__(self, name: str, model: BaseLLM):
        self.name = name
        self.model = model  # An instance of a language model

    @abstractmethod
    def system_prompt(self):
        """Defines the behavior of the agent"""
        pass

    def build_user_prompt(self, total_resource: int, agent_names: list[str],
                     current_round: int, max_rounds: int = None,
                     history: History | None = None):
        """Build the prompt for the LLM"""
        history_str = ""
        if history:
            for (n_round, author_name, proposal, message) in history:
                if proposal is not None:
                    history_str += f"Round {n_round + 1} - {author_name}: {proposal} ({message})\n"
                else:
                    history_str += f"Round {n_round + 1} - {author_name}: {message}\n"
        else:
            history_str = "No previous proposals.\n"

        round_str = f"{current_round + 1}"
        if max_rounds is not None:
            round_str += f"\nRemaining rounds: {max_rounds - (current_round + 1)}"
            if current_round + 1 >= max_rounds:
                round_str += " (Final round!)"
                if agent_names.index(self.name) == len(agent_names) - 1:
                    round_str += ("\nYOU ARE THE LAST TO ACT IN THIS LAST ROUND, "
                                  "IF NO AGREEMENT IS REACHED AFTER THIS, ALL AGENTS WILL RECEIVE 0!")

        prompt = f"""
Your name: {self.name}
All parties: {', '.join(agent_names)}

Total resource to be divided: {total_resource}

Current round: {round_str}

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

WARNING:
If no agreement is reached within the remaining rounds, both agents will receive 0!
"""
        return prompt

    def act(self, total_resource: int, agent_names: list[str],
            current_round: int, remaining_rounds: int = None,
            history: History | None = None):
        """Generate the next move"""
        user_prompt = self.build_user_prompt(total_resource, agent_names, current_round, remaining_rounds, history)
        response = self.model.generate(self.system_prompt(), user_prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {
                "action": "invalid",
                "raw": response
            }

        return parsed
