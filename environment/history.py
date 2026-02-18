from environment.proposal import Proposal


class History:
    history: list[tuple[int, str, Proposal | None, str]]  # List of (round, agent name, proposal, message)

    def __init__(self):
        self.history = []

    def add(self, r: int, agent_name: str, proposal: Proposal | None, message: str):
        self.history.append((r, agent_name, proposal, message))

    def __len__(self):
        return len(self.history)

    def __iter__(self):
        return iter(self.history)

    def __reversed__(self):
        return reversed(self.history)
