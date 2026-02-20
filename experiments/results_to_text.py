def results_to_text():
    """
    Convert the results of multiple runs into a human-readable text format.
    """
    lines = ["# Negotiation Experiment Results\n"]
    num = 0
    for run_name in export_run_names:
        lines.append(f"## Run: `{run_name}`\n")
        run_results = [result for result in results if result["run_name"] == run_name]
        for n_res, res in enumerate(run_results):
            lines.append(f"### Experiment {n_res + 1}\n")
            for entry in res["history"]:
                round_num = entry["round"] + 1  # Convert to 1-based indexing
                agent_name = entry["agent_name"]
                proposal = entry["proposal"]
                message = entry["message"]

                if proposal is not None:
                    shares_text = ", ".join(f"{agent}: {share}%" for agent, share in proposal["shares"].items())
                    line = f"Round {round_num}: {agent_name} proposed shares ({shares_text}) with message: '{message}'  "
                else:
                    line = f"Round {round_num}: {agent_name} provided feedback: '{message}'  "

                lines.append(line)
                num += 1
            lines.append("\n---\n")

    return "\n".join(lines)


if __name__ == "__main__":
    import json

    with open("results.jsonl", "r") as f:
        results = [json.loads(line) for line in f]

    export_run_names = [
        "new_profit_vs_fair_0.0_gpt-5.2_no_remaining",
        "new_fair_vs_fair_0.0_gpt-5.2",
        "new_profit_vs_tit_for_tat_0.0_gpt-5.2",
        "new_fair_vs_tit_for_tat_0.0_gpt-5.2",
        "new_fair_vs_hardliner_0.0_gpt-5.2",
        "new_hardliner_vs_fair_0.0_gpt-5.2",
        "new_hardliner_vs_profit_0.0_gpt-5.2",
        "new_hardliner_vs_hardliner_0.0_gpt-5.2"
    ]
    text_output = results_to_text()
    with open("results_summary.md", "w", encoding="utf-8") as f:
        f.write(text_output)
