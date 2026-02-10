from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame, Proposal
from model.dummy_model import DummyModel
from model.llama_cpp_model import LlamaCppModel


def run():
    model = LlamaCppModel(
        model_path="D:/negotiation-arena/models/qwen2.5-3b-instruct-q5_k_m.gguf",
        temperature=0.5
    )

    agent_a = ProfitAgent("Agent A", model)
    agent_b = FairAgent("Agent B", model)

    game = NegotiationGame()

    current_agent = agent_a
    rounds = 0

    while not game.is_over():
        state = game.get_state()
        response = current_agent.act(state)
        current_proposal = Proposal(
            agent1_share=response["my_share"] if current_agent == agent_a else response["your_share"],
            agent2_share=response["your_share"] if current_agent == agent_a else response["my_share"]
        )
        rounds += 1
        last_proposal = game.last_proposal

        if last_proposal and current_proposal == last_proposal:
            return {
                "agreement": True,
                "rounds": rounds,
                "final_share": {
                    "Agent A": current_proposal.agent1_share,
                    "Agent B": current_proposal.agent2_share
                }
            }

        game.update_proposal(current_proposal)

        # Switch turns
        current_agent = agent_b if current_agent == agent_a else agent_a

    return {
        "agreement": False,
        "rounds": rounds,
        "final_share": None
    }


if __name__ == "__main__":
    run()
