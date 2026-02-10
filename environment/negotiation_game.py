class NegotiationGame:
    def __init__(self, agent_names, total_resource=100, max_rounds=5):
        self.total = total_resource
        self.max_rounds = max_rounds
        self.round = 0
        self.proposals = []
        self.agent_names = agent_names

    def last_proposal(self):
        return self.proposals[-1][1] if self.proposals else None

    def get_state(self):
        """Provides the current state of the negotiation."""
        last_proposal = self.last_proposal()
        return f"Total resource to be divided: {self.total}. Last proposal: {last_proposal}"

    def get_proposal_history(self):
        """Returns a history of all proposals made."""
        return self.proposals

    def update_proposal(self, author, proposal):
        self.proposals.append((author, proposal))
        self.round += 1

    def is_over(self):
        return self.round >= self.max_rounds
