from analysis.metrics import run_multiple_experiments, save_results_jsonl
from experiments.run_experiment import run


def _get_run_name(current_config):
    agent_types = "_vs_".join([agent_cfg["type"]
                               for agent_cfg in current_config.get("agents", [])])
    model_name = current_config.get("model_name", "model")
    temperature = current_config.get("temperature", 0.7)
    return f"{agent_types}_{temperature}_{model_name}"


if __name__ == "__main__":
    config = {
        "agents": [
            {"type": "hardliner", "name": "Alice"},
            {"type": "hardliner", "name": "Bob"}
        ],
        "model_name": "gpt-5.2",
        "temperature": 0.0,
        "max_rounds": 10,
    }

    N_RUNS = 1

    results = run_multiple_experiments(
        run_experiment_fn=run,
        n_runs=N_RUNS,
        config=config
    )

    save_results_jsonl(_get_run_name(config), results, "results.jsonl")

    print("Experiments completed, results saved to results.jsonl")
