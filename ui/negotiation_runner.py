def run_negotiation_step(game):
    agreement, agent, proposal = game.step()

    return {
        "agent": agent.name,
        "message": proposal.reasoning,
        "shares": proposal.shares
    }, agreement
