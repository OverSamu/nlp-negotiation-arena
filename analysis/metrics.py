import json
import numpy as np
from collections import defaultdict


def run_multiple_experiments(run_experiment_fn, n_runs, config):
    """
    Run multiple negotiation experiments and collect results.
    """
    results = []

    for i in range(n_runs):
        result = run_experiment_fn(config=config)
        results.append(result)

    return results


def get_run_results(all_results, run_name):
    """
    Filter results for a specific run name.
    """
    return [r for r in all_results if r["run_name"] == run_name]


def compute_aggregate_metrics(results):
    """
    Calculate aggregate metrics from a list of results.
    """

    total_runs = len(results)
    agreements = [r["agreement"] for r in results]
    rounds = [r["rounds"] for r in results]
    final_shares = [r["history"][-1]["proposal"]["shares"] for r in results if r["history"]]

    agreement_rate = sum(agreements) / total_runs
    avg_rounds = np.mean(rounds)

    avg_utilities = compute_average_utilities(final_shares)
    fairness_index = compute_fairness_index(final_shares)

    return {
        "total_runs": total_runs,
        "agreement_rate": agreement_rate,
        "avg_rounds": avg_rounds,
        "avg_utilities": avg_utilities,
        "fairness_index": fairness_index
    }


def compute_average_utilities(final_shares):
    """
    Average utilities for each agent across all final shares.
    """
    if not final_shares:
        return {}

    agent_totals = defaultdict(list)

    for share_dict in final_shares:
        for agent, share in share_dict.items():
            agent_totals[agent].append(share)

    return {
        agent: np.mean(values)
        for agent, values in agent_totals.items()
    }


def compute_fairness_index(final_shares):
    """
    Simple fairness index:
    1 - (|diff| / total_resource)
    Assume division of 100.
    """

    if not final_shares:
        return 0

    fairness_scores = []

    for share_dict in final_shares:
        values = list(share_dict.values())
        if len(values) != 2:
            continue

        diff = abs(values[0] - values[1])
        fairness = 1 - (diff / 100)
        fairness_scores.append(fairness)

    return np.mean(fairness_scores)


def diff_proposal(proposal1, proposal2):
    """
    Calculate the difference between two proposals.
    """
    if proposal1 is None or proposal2 is None:
        return None

    shares1 = proposal1["shares"]
    shares2 = proposal2["shares"]

    diff = {agent: abs(shares1.get(agent, 0) - shares2.get(agent, 0))
            for agent in set(shares1) | set(shares2)}

    return diff


def save_results_jsonl(run_name, results, filepath):
    with open(filepath, "a") as f:
        for r in results:
            f.write(json.dumps({"run_name": run_name, **r}) + "\n")
