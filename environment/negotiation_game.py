from environment.proposal import Proposal


class NegotiationGame:
    def __init__(self, agents, total_resource=100):
        self.total = total_resource
        self.history = [] # List of (agent name, proposal, message)
        self.agents = agents
        self.agent_turn = 0  # Index to track whose turn it is

    def last_proposal(self):
        """Returns the last valid proposal made by any agent."""
        for author_name, proposal, message in reversed(self.history):
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

    def add_judge_feedback(self, feedback):
        """Allows the judge to provide feedback that can be seen by agents."""
        self.history.append(("Judge", None, feedback)) # None for agent and proposal

    def step(self):
        state = self.get_state()
        history = self.get_history()
        current_agent = self.agents[self.agent_turn]
        agent_names = [agent.name for agent in self.agents]
        response = current_agent.act(state, agent_names, history)
        current_proposal = Proposal(response["shares"])
        current_message = response.get("message", "")

        last_proposal = self.last_proposal()
        self.history.append((current_agent.name, current_proposal, current_message))
        if last_proposal and current_proposal == last_proposal:
            return True, current_agent, current_proposal, current_message  # Agreement reached
        self.agent_turn = (self.agent_turn + 1) % len(self.agents)  # Switch turn
        return False, current_agent, current_proposal, current_message  # No agreement yet
