from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
from model.dummy_model import DummyModel


def run():
    model = DummyModel()

    agent_a = ProfitAgent("Agent A", model)
    agent_b = FairAgent("Agent B", model)

    game = NegotiationGame()

    current_agent = agent_a

    while not game.is_over():
        state = game.get_state()
        response = current_agent.act(state)

        game.update_proposal(response)

        # Switch turns
        current_agent = agent_b if current_agent == agent_a else agent_a

    print("Negotiation ended.")


if __name__ == "__main__":
    run()
