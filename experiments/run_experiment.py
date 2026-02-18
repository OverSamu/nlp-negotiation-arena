from openai import OpenAI

from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
from model.dummy_model import DummyModel
from model.llama_cpp_model import LlamaCppModel
from model.openai_model import OpenAIModel

client = OpenAI()


def run():
    model = OpenAIModel(client, temperature=0.8)

    agent_a = ProfitAgent("Agent A", model)
    agent_b = FairAgent("Agent B", model)

    game = NegotiationGame([agent_a, agent_b])

    max_rounds = 10

    while game.round < max_rounds:
        agreement, agent_name, proposal, message = game.step()

        print(f"Round {game.round + 1}: {agent_name} proposed {proposal.shares} with message: '{message}'")

        if agreement:
            return {
                "agreement": True,
                "rounds": game.round + 1,
                "final_share": game.last_proposal()
            }

    return {
        "agreement": False,
        "rounds": max_rounds,
        "final_share": None
    }


if __name__ == "__main__":
    result = run()
    print("Negotiation Result:")
    print(f"Agreement Reached: {result['agreement']}")
    print(f"Rounds Taken: {result['rounds']}")
    if result["agreement"]:
        print(f"Final Share: {result['final_share']}")
