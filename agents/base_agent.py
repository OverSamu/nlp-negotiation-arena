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

Answer with a clear proposal or accept/reject the last proposal.
"""
        return prompt

    def act(self, negotiation_state):
        """Generate the next move"""
        prompt = self.build_prompt(negotiation_state)
        response = self.model.generate(prompt)

        self.observe(f"{self.name}: {response}")
        return response
