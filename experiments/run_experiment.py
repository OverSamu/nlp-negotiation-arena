from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
from model.dummy_model import DummyModel
from model.llama_cpp_model import LlamaCppModel


def run():
    model = LlamaCppModel(
        model_path="D:/negotiation-arena/models/qwen2.5-3b-instruct-q5_k_m.gguf",
        temperature=0.5
    )

    agent_a = ProfitAgent("Agent A", model)
    agent_b = FairAgent("Agent B", model)

    game = NegotiationGame([agent_a, agent_b])

    max_rounds = 5
    rounds = 0

    while rounds < max_rounds:
        agreement = game.step()
        rounds += 1
        if agreement:
            return {
                "agreement": True,
                "rounds": rounds,
                "final_share": game.last_proposal()
            }

    return {
        "agreement": False,
        "rounds": rounds,
        "final_share": None
    }


if __name__ == "__main__":
    result = run()
    print("Negotiation Result:")
    print(f"Agreement Reached: {result['agreement']}")
    print(f"Rounds Taken: {result['rounds']}")
    if result["agreement"]:
        print(f"Final Share: {result['final_share']}")
