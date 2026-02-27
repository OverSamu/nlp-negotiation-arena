def run_negotiation_step(game):
    agent_name, n_round, proposal, message = game.step()

    return {
        "agent": agent_name,
        "message": message,
        "shares": proposal.shares
    }
