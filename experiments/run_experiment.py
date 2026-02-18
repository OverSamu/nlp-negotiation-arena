from openai import OpenAI

from agents.fair_agent import FairAgent
from agents.profit_agent import ProfitAgent
from environment.negotiation_game import NegotiationGame
from model.dummy_model import DummyModel
from model.llama_cpp_model import LlamaCppModel
from model.openai_model import OpenAIModel

client = OpenAI()


def _agents_from_config(config, model):
    agents = []
    for agent_cfg in config.get("agents", []):
        if agent_cfg["type"] == "profit":
            agents.append(ProfitAgent(agent_cfg["name"], model))
        elif agent_cfg["type"] == "fair":
            agents.append(FairAgent(agent_cfg["name"], model))
    return agents


def run(config):
    model = OpenAIModel(client,
                        temperature=config.get("temperature", 0.7),
                        model_name=config.get("model_name", "gpt-4o-mini"))

    game = NegotiationGame(agents=_agents_from_config(config, model))

    max_rounds = config.get("max_rounds", 10)

    while game.round < max_rounds:
        agreement, agent_name, proposal, message = game.step()

        print(f"Round {game.round + 1}: {agent_name} proposed {proposal.shares} with message: '{message}'")

        if agreement:
            return {
                "agreement": True,
                "history": game.get_history().toJSON()
            }

    return {
        "agreement": False,
        "history": game.get_history().toJSON()
    }


if __name__ == "__main__":
    result = run({
        "agents": [
            {"type": "profit", "name": "Agent A"},
            {"type": "fair", "name": "Agent B"}
        ],
        "model_name": "gpt-4o-mini",
        "temperature": 0.8,
        "max_rounds": 10,
    })
    print("Negotiation Result:")
    print(f"Agreement Reached: {result['agreement']}")
    print(f"Rounds Taken: {result['rounds']}")
    if result["agreement"]:
        print(f"Final Share: {result['final_share']}")
