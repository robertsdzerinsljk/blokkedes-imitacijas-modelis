import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config import SIMULATION_CONFIG
from simulation import run_simulation


class SimulationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blokķēdes simulācijas rīks")
        self.root.geometry("1180x780")
        self.root.minsize(1020, 700)

        self.current_stats = []
        self.current_summary = {}

        self.summary_labels = {
            "duration": "Simulācijas ilgums",
            "tx_rate_mean": "Vidējā darījumu intensitāte",
            "block_size": "Bloka izmērs",
            "avg_block_time": "Vidējais bloka izveides laiks",
            "final_visible_mempool_size": "Beigu mempool izmērs",
            "pending_transaction_count": "Neizplatīto darījumu skaits",
            "blocks_visible_in_chain": "Ķēdē redzamo bloku skaits",
            "total_confirmed_transactions": "Kopējais apstiprināto darījumu skaits",
            "throughput_tps": "Caurlaidspēja (TPS)",
            "avg_confirmation_time": "Vidējais apstiprināšanas laiks",
        }

        self.preset_labels = {
            "low_load": "Zema slodze",
            "medium_load": "Vidēja slodze",
            "high_load": "Augsta slodze",
        }

        self._build_layout()

    def _build_layout(self):
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill="x")

        left = ttk.LabelFrame(top, text="Konfigurācija", padding=12)
        left.pack(side="left", fill="y")

        right = ttk.LabelFrame(top, text="Kopsavilkums", padding=12)
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        ttk.Label(left, text="Scenārijs").grid(row=0, column=0, sticky="w", pady=6)
        self.preset_var = tk.StringVar(value="medium_load")
        preset_box = ttk.Combobox(
            left,
            textvariable=self.preset_var,
            values=list(SIMULATION_CONFIG.keys()),
            state="readonly",
            width=18,
        )
        preset_box.grid(row=0, column=1, pady=6)
        preset_box.bind("<<ComboboxSelected>>", self.load_preset)

        ttk.Label(left, text="Vidējā darījumu intensitāte").grid(row=1, column=0, sticky="w", pady=6)
        self.tx_rate_mean = tk.DoubleVar(value=2.0)
        ttk.Entry(left, textvariable=self.tx_rate_mean, width=20).grid(row=1, column=1, pady=6)

        ttk.Label(left, text="Bloka izmērs").grid(row=2, column=0, sticky="w", pady=6)
        self.block_size = tk.IntVar(value=12)
        ttk.Entry(left, textvariable=self.block_size, width=20).grid(row=2, column=1, pady=6)

        ttk.Label(left, text="Vidējais bloka izveides laiks").grid(row=3, column=0, sticky="w", pady=6)
        self.avg_block_time = tk.IntVar(value=6)
        ttk.Entry(left, textvariable=self.avg_block_time, width=20).grid(row=3, column=1, pady=6)

        ttk.Label(left, text="Simulācijas ilgums").grid(row=4, column=0, sticky="w", pady=6)
        self.duration = tk.IntVar(value=180)
        ttk.Entry(left, textvariable=self.duration, width=20).grid(row=4, column=1, pady=6)

        ttk.Label(left, text="Minimālā tīkla aizkave").grid(row=5, column=0, sticky="w", pady=6)
        self.delay_min = tk.IntVar(value=1)
        ttk.Entry(left, textvariable=self.delay_min, width=20).grid(row=5, column=1, pady=6)

        ttk.Label(left, text="Maksimālā tīkla aizkave").grid(row=6, column=0, sticky="w", pady=6)
        self.delay_max = tk.IntVar(value=3)
        ttk.Entry(left, textvariable=self.delay_max, width=20).grid(row=6, column=1, pady=6)

        ttk.Label(left, text="Nejaušības sēkla").grid(row=7, column=0, sticky="w", pady=6)
        self.seed = tk.IntVar(value=43)
        ttk.Entry(left, textvariable=self.seed, width=20).grid(row=7, column=1, pady=6)

        button_row = ttk.Frame(left)
        button_row.grid(row=8, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        ttk.Button(button_row, text="Ielādēt scenāriju", command=self.load_preset).pack(side="left")
        ttk.Button(button_row, text="Palaist simulāciju", command=self.run_simulation).pack(side="left", padx=8)
        ttk.Button(button_row, text="Eksportēt CSV", command=self.export_csv).pack(side="left")

        self.summary_text = tk.Text(right, height=11, wrap="word")
        self.summary_text.pack(fill="both", expand=True)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.tab_mempool = ttk.Frame(notebook)
        self.tab_confirmed = ttk.Frame(notebook)
        self.tab_resource = ttk.Frame(notebook)

        notebook.add(self.tab_mempool, text="Mempool")
        notebook.add(self.tab_confirmed, text="Apstiprinātie darījumi")
        notebook.add(self.tab_resource, text="Resursu izmaksas")

        self.fig_mempool, self.ax_mempool, self.canvas_mempool = self._make_plot(self.tab_mempool)
        self.fig_confirmed, self.ax_confirmed, self.canvas_confirmed = self._make_plot(self.tab_confirmed)
        self.fig_resource, self.ax_resource, self.canvas_resource = self._make_plot(self.tab_resource)

        self.load_preset()

    def _make_plot(self, parent):
        fig = Figure(figsize=(8, 4.8), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return fig, ax, canvas

    def load_preset(self, event=None):
        cfg = SIMULATION_CONFIG[self.preset_var.get()]
        self.tx_rate_mean.set(cfg["tx_rate_mean"])
        self.block_size.set(cfg["block_size"])
        self.avg_block_time.set(cfg["avg_block_time"])
        self.duration.set(cfg["duration"])
        self.delay_min.set(cfg["network_delay_min"])
        self.delay_max.set(cfg["network_delay_max"])
        self.seed.set(cfg["seed"])

    def run_simulation(self):
        try:
            config = {
                "tx_rate_mean": float(self.tx_rate_mean.get()),
                "block_size": int(self.block_size.get()),
                "avg_block_time": int(self.avg_block_time.get()),
                "duration": int(self.duration.get()),
                "network_delay_min": int(self.delay_min.get()),
                "network_delay_max": int(self.delay_max.get()),
                "seed": int(self.seed.get()),
            }

            if config["tx_rate_mean"] <= 0:
                raise ValueError("Vidējai darījumu intensitātei jābūt lielākai par nulli.")
            if min(
                config["block_size"],
                config["avg_block_time"],
                config["duration"],
                config["network_delay_min"],
                config["network_delay_max"]
            ) <= 0:
                raise ValueError("Visiem veselajiem parametriem jābūt lielākiem par nulli.")
            if config["network_delay_min"] > config["network_delay_max"]:
                raise ValueError("Minimālā tīkla aizkave nevar būt lielāka par maksimālo.")

            self.current_stats, self.current_summary = run_simulation(config)
            self._update_summary()
            self._update_plots()
            messagebox.showinfo("Pabeigts", "Simulācija veiksmīgi pabeigta.")

        except Exception as exc:
            messagebox.showerror("Kļūda", str(exc))

    def _update_summary(self):
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, "Simulācijas kopsavilkums\n")
        self.summary_text.insert(tk.END, "========================\n\n")

        for key, value in self.current_summary.items():
            label = self.summary_labels.get(key, key)
            self.summary_text.insert(tk.END, f"{label}: {value}\n")

    def _update_plots(self):
        times = [row["time"] for row in self.current_stats]
        mempool = [row["visible_mempool_size"] for row in self.current_stats]
        confirmed = [row["confirmed_in_step"] for row in self.current_stats]
        resource = [row["resource_cost"] for row in self.current_stats]

        self.ax_mempool.clear()
        self.ax_mempool.plot(times, mempool)
        self.ax_mempool.set_title("Redzamā mempool izmēra izmaiņas laikā")
        self.ax_mempool.set_xlabel("Laiks")
        self.ax_mempool.set_ylabel("Redzamais mempool izmērs")
        self.fig_mempool.tight_layout()
        self.canvas_mempool.draw()

        self.ax_confirmed.clear()
        self.ax_confirmed.plot(times, confirmed)
        self.ax_confirmed.set_title("Apstiprināto darījumu skaits katrā solī")
        self.ax_confirmed.set_xlabel("Laiks")
        self.ax_confirmed.set_ylabel("Apstiprināto darījumu skaits")
        self.fig_confirmed.tight_layout()
        self.canvas_confirmed.draw()

        self.ax_resource.clear()
        self.ax_resource.plot(times, resource)
        self.ax_resource.set_title("Resursu izmaksu izmaiņas laikā")
        self.ax_resource.set_xlabel("Laiks")
        self.ax_resource.set_ylabel("Resursu izmaksas")
        self.fig_resource.tight_layout()
        self.canvas_resource.draw()

    def export_csv(self):
        if not self.current_stats:
            messagebox.showwarning("Nav datu", "Vispirms palaid simulāciju.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV fails", "*.csv")],
            title="Saglabāt simulācijas rezultātus"
        )

        if not file_path:
            return

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "time", "generated_in_step", "visible_mempool_size",
                "pending_transaction_count", "confirmed_in_step",
                "avg_confirmation_time_step", "resource_cost", "chain_length"
            ])
            for row in self.current_stats:
                writer.writerow([
                    row["time"],
                    row["generated_in_step"],
                    row["visible_mempool_size"],
                    row["pending_transaction_count"],
                    row["confirmed_in_step"],
                    row["avg_confirmation_time_step"],
                    row["resource_cost"],
                    row["chain_length"],
                ])

        messagebox.showinfo("Saglabāts", "CSV fails veiksmīgi eksportēts.")


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = SimulationGUI(root)
    root.mainloop()