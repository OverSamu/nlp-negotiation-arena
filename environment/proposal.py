class Proposal:
    def __init__(self, shares):
        self.shares = shares # {agent_name: share}

    def __str__(self):
        return f"Proposal({self.shares})"

    def __eq__(self, other):
        if not isinstance(other, Proposal):
            return False
        return self.shares == other.shares
