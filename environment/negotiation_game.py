class Proposal:
    def __init__(self, agent1_share, agent2_share):
        self.agent1_share = agent1_share
        self.agent2_share = agent2_share

    def __str__(self):
        return f"Agent 1: {self.agent1_share}, Agent 2: {self.agent2_share}"

    def __eq__(self, other):
        if not isinstance(other, Proposal):
            return False
        return self.agent1_share == other.agent1_share and self.agent2_share == other.agent2_share


class NegotiationGame:
    def __init__(self, total_resource=100, max_rounds=5):
        self.total = total_resource
        self.max_rounds = max_rounds
        self.round = 0
        self.last_proposal = None

    def get_state(self):
        """Provides the current state of the negotiation."""
        return f"Total resource to be divided: {self.total}. Last proposal: {self.last_proposal}"

    def update_proposal(self, proposal):
        self.last_proposal = proposal
        self.round += 1

    def is_over(self):
        return self.round >= self.max_rounds
