import json


def run_multiple_experiments(run_experiment_fn, n_runs, config):
    """
    Run multiple negotiation experiments and collect results.
    """
    results = []

    for i in range(n_runs):
        result = run_experiment_fn(config=config)
        results.append(result)

    return results


def save_results_jsonl(run_name, results, filepath):
    with open(filepath, "w") as f:
        for r in results:
            f.write(json.dumps({"run_name": run_name, **r}) + "\n")
