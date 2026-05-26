import csv
from config import SIMULATION_CONFIG
from simulation import run_simulation


def save_results():
    with open("simulation_step_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scenario",
            "time",
            "visible_mempool_size",
            "pending_transaction_count",
            "confirmed_in_step",
            "avg_confirmation_time_step",
            "resource_cost",
            "chain_length"
        ])

        for scenario_name, scenario_config in SIMULATION_CONFIG.items():
            stats, summary = run_simulation(scenario_config)

            for row in stats:
                writer.writerow([
                    scenario_name,
                    row["time"],
                    row["visible_mempool_size"],
                    row["pending_transaction_count"],
                    row["confirmed_in_step"],
                    row["avg_confirmation_time_step"],
                    row["resource_cost"],
                    row["chain_length"]
                ])

    with open("simulation_summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scenario",
            "duration",
            "tx_rate_mean",
            "block_size",
            "avg_block_time",
            "final_visible_mempool_size",
            "pending_transaction_count",
            "blocks_visible_in_chain",
            "total_confirmed_transactions",
            "throughput_tps",
            "avg_confirmation_time"
        ])

        for scenario_name, scenario_config in SIMULATION_CONFIG.items():
            stats, summary = run_simulation(scenario_config)

            writer.writerow([
                scenario_name,
                summary["duration"],
                summary["tx_rate_mean"],
                summary["block_size"],
                summary["avg_block_time"],
                summary["final_visible_mempool_size"],
                summary["pending_transaction_count"],
                summary["blocks_visible_in_chain"],
                summary["total_confirmed_transactions"],
                summary["throughput_tps"],
                summary["avg_confirmation_time"]
            ])


if __name__ == "__main__":
    save_results()
    print("Simulation completed. Results saved to CSV files.")