import pandas as pd
import matplotlib.pyplot as plt


SCENARIO_LABELS = {
    "low_load": "Zema slodze",
    "medium_load": "Vidēja slodze",
    "high_load": "Augsta slodze",
}


def generate_plots():
    steps = pd.read_csv("simulation_step_results.csv")
    summary = pd.read_csv("simulation_summary.csv")

    summary["scenario_label"] = summary["scenario"].map(SCENARIO_LABELS)
    steps["scenario_label"] = steps["scenario"].map(SCENARIO_LABELS)

    # 3.1. Darījumu caurlaidspēja
    plt.figure(figsize=(8, 4.8))
    plt.bar(summary["scenario_label"], summary["throughput_tps"])
    plt.xlabel("Slodzes scenārijs")
    plt.ylabel("Darījumi sekundē (TPS)")
    plt.title("Darījumu caurlaidspēja dažādos slodzes scenārijos")
    plt.tight_layout()
    plt.savefig("3_1_darijumu_caurlaidspēja_tps.png", dpi=200)
    plt.close()

    # 3.2. Vidējais apstiprināšanas laiks
    plt.figure(figsize=(8, 4.8))
    plt.bar(summary["scenario_label"], summary["avg_confirmation_time"])
    plt.xlabel("Slodzes scenārijs")
    plt.ylabel("Vidējais apstiprināšanas laiks")
    plt.title("Vidējais darījumu apstiprināšanas laiks dažādos slodzes scenārijos")
    plt.tight_layout()
    plt.savefig("3_2_videjais_apstiprinasanas_laiks.png", dpi=200)
    plt.close()

    # 3.3. Mempool dinamika
    plt.figure(figsize=(9, 5))
    for scenario in steps["scenario"].unique():
        subset = steps[steps["scenario"] == scenario]
        plt.plot(
            subset["time"],
            subset["visible_mempool_size"],
            label=SCENARIO_LABELS.get(scenario, scenario)
        )

    plt.xlabel("Laiks")
    plt.ylabel("Mempool apjoms")
    plt.title("Mempool apjoma dinamika dažādos slodzes scenārijos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("3_3_mempool_dinamika.png", dpi=200)
    plt.close()

    # 3.4. Resursu izmaksu rādītājs
    plt.figure(figsize=(9, 5))
    for scenario in steps["scenario"].unique():
        subset = steps[steps["scenario"] == scenario]
        plt.plot(
            subset["time"],
            subset["resource_cost"],
            label=SCENARIO_LABELS.get(scenario, scenario)
        )

    plt.xlabel("Laiks")
    plt.ylabel("Relatīvās resursu izmaksas")
    plt.title("Relatīvā resursu izmaksu rādītāja dinamika dažādos slodzes scenārijos")
    plt.legend()
    plt.tight_layout()
    plt.savefig("3_4_resursu_izmaksu_raditajs.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    generate_plots()
    print("Plots generated successfully.")