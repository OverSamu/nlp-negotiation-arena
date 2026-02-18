from agents.base_agent import BaseAgent
from environment.proposal import Proposal


class NegotiationGame:
    history: list[tuple[int, str, Proposal | None, str]]  # List of (round, agent name, proposal, message)
    agents: list[BaseAgent]

    def __init__(self, agents: list[BaseAgent], total_resource=100):
        self.total = total_resource
        self.history = []
        self.agents = agents
        self.agent_turn = 0  # Index to track whose turn it is
        self.round = 0 # Track the number of rounds (a round is completed when all agents have had a turn)

    def get_agent_proposals_in_rounds(self) -> list[list[int | None]]:
        """Returns an array (length = number of rounds) of arrays (length = number of agents) of proposals made by each agent in each round."""
        result = []
        for n_round in range(self.round + 1):
            round_proposals = []
            for agent in self.agents:
                proposal = next((proposal for r, author_name, proposal, message in self.history if r == n_round and author_name == agent.name), None)
                round_proposals.append(proposal.shares[agent.name] if proposal else None)
            result.append(round_proposals)
        return result

    def last_proposal(self):
        """Returns the last valid proposal made by any agent."""
        for n_round, author_name, proposal, message in reversed(self.history):
            if proposal is not None:
                return proposal
        return None

    def get_state(self):
        """Provides the current state of the negotiation."""
        last_proposal = self.last_proposal()
        shares = last_proposal.shares if last_proposal else None
        return f"Total resource to be divided: {self.total}. Last proposal: {shares}"

    def get_history(self):
        """Returns a history of all proposals and feedback."""
        return self.history

    def add_judge_feedback(self, feedback: str):
        """Allows the judge to provide feedback that can be seen by agents."""
        self.history.append((self.round, "Judge", None, feedback)) # None for agent and proposal

    def step(self):
        state = self.get_state()
        history = self.get_history()
        current_agent = self.agents[self.agent_turn]
        agent_names = [agent.name for agent in self.agents]
        response = current_agent.act(state, agent_names, history)
        current_proposal = Proposal(response["shares"])
        current_message = response.get("message", "")

        last_proposal = self.last_proposal()
        self.history.append((self.round, current_agent.name, current_proposal, current_message))
        if last_proposal and current_proposal == last_proposal:
            return True, current_agent.name, current_proposal, current_message  # Agreement reached
        self.agent_turn = (self.agent_turn + 1) % len(self.agents)  # Switch turn
        if self.agent_turn == 0:
            self.round += 1
        return False, current_agent.name, current_proposal, current_message  # No agreement yet
