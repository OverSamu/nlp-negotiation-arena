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
