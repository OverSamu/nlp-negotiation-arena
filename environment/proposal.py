class Proposal:
    def __init__(self, shares, reasoning=None):
        self.shares = shares # {agent_name: share}
        self.reasoning = reasoning

    def __str__(self):
        return f"Proposal({self.shares}, reasoning={self.reasoning})"

    def __eq__(self, other):
        if not isinstance(other, Proposal):
            return False
        return self.shares == other.shares
