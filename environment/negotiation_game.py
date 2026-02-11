from environment.proposal import Proposal


class NegotiationGame:
    def __init__(self, agents, total_resource=100):
        self.total = total_resource
        self.proposals = []
        self.agents = agents
        self.agent_turn = 0  # Index to track whose turn it is

    def last_proposal(self):
        return self.proposals[-1][1] if self.proposals else None

    def get_state(self):
        """Provides the current state of the negotiation."""
        last_proposal = self.last_proposal()
        return f"Total resource to be divided: {self.total}. Last proposal: {last_proposal}"

    def get_proposal_history(self):
        """Returns a history of all proposals made."""
        return self.proposals

    def step(self):
        state = self.get_state()
        history = self.get_proposal_history()
        current_agent = self.agents[self.agent_turn]
        agent_names = [agent.name for agent in self.agents]
        response = current_agent.act(state, agent_names, history)
        current_proposal = Proposal(response["shares"], response.get("message", ""))

        last_proposal = self.last_proposal()
        self.proposals.append((current_agent, current_proposal))
        if last_proposal and current_proposal == last_proposal:
            return True, current_agent, current_proposal  # Agreement reached
        self.agent_turn = (self.agent_turn + 1) % len(self.agents)  # Switch turn
        return False, current_agent, current_proposal  # No agreement yet
