from openai import OpenAI

from agents.fair_agent import FairAgent
from agents.hardliner_agent import HardlinerAgent
from agents.profit_agent import ProfitAgent
from agents.tit_for_tat_agent import TitForTatAgent
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
        elif agent_cfg["type"] == "tit_for_tat":
            agents.append(TitForTatAgent(agent_cfg["name"], model))
        elif agent_cfg["type"] == "hardliner":
            agents.append(HardlinerAgent(agent_cfg["name"], model))
    return agents


def run(config):
    model = OpenAIModel(client,
                        temperature=config.get("temperature", 0.7),
                        model_name=config.get("model_name", "gpt-4o-mini"))

    game = NegotiationGame(agents=_agents_from_config(config, model),
                           max_rounds=config.get("max_rounds", 10))

    while not game.is_finished():
        agent_name, n_round, proposal, message = game.step()

        print(f"Round {n_round + 1}: {agent_name} proposed {proposal.shares} with message: '{message}'")

    return {
        "agreement": game.is_agreement(),
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
