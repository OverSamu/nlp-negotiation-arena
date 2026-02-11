def run_negotiation_step(game):
    agreement, agent, proposal, message = game.step()

    return {
        "agent": agent.name,
        "message": message,
        "shares": proposal.shares
    }, agreement
