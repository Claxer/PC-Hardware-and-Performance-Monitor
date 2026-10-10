
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PerformanceCharts:
    def __init__(self, parent, cpu_history, ram_history):
        self.parent = parent
        self.cpu_history = cpu_history
        self.ram_history = ram_history

        self.figure, (self.cpu_axis, self.ram_axis) = plt.subplots(
            2, 1, figsize=(8, 5), dpi=100
        )

        self.figure.patch.set_facecolor("#101114")

        self.cpu_line, = self.cpu_axis.plot(
            [], [], color="#579BFF", linewidth=2
        )
        self.ram_line, = self.ram_axis.plot(
            [], [], color="#45C486", linewidth=2
        )

        self.configure_axis(
            self.cpu_axis, "CPU Usage", "#579BFF"
        )
        self.configure_axis(
            self.ram_axis, "RAM Usage", "#45C486"
        )

        self.figure.tight_layout(pad=3)

        self.canvas = FigureCanvasTkAgg(
            self.figure, master=self.parent
        )
        self.canvas.get_tk_widget().pack(
            fill="both", expand=True, padx=10, pady=10
        )

        self.update_chart()

    def configure_axis(self, axis, title, color):
        axis.set_facecolor("#1B1D23")
        axis.set_title(title, color="white", fontsize=12)
        axis.set_xlabel("Recent Readings", color="#B5B7C2")
        axis.set_ylabel("Usage (%)", color="#B5B7C2")
        axis.set_ylim(0, 100)
        axis.tick_params(colors="#B5B7C2")
        axis.grid(True, color="#393B45", linestyle="--", alpha=0.6)

        for spine in axis.spines.values():
            spine.set_color("#393B45")

    def update_chart(self):
        count = len(self.cpu_history)
        x_values = list(range(1, count + 1))

        self.cpu_line.set_data(x_values, self.cpu_history)
        self.ram_line.set_data(x_values, self.ram_history)

        if count <= 30:
            left = 1
            right = 30
        else:
            left = count - 29
            right = count

        self.cpu_axis.set_xlim(left, right)
        self.ram_axis.set_xlim(left, right)

        self.canvas.draw_idle()
