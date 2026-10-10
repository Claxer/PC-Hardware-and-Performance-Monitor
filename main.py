
import customtkinter as ctk
import psutil
import platform
import os
import csv

from datetime import datetime
from tkinter import ttk, filedialog, messagebox
from performance_charts import PerformanceCharts


# Application appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PCHardwareMonitor:
    def __init__(self, app):
        self.app = app
        self.app.title("PC Hardware and Performance Monitor")
        self.app.geometry("1200x780")
        self.app.minsize(950, 650)
        self.app.configure(fg_color="#101114")

        # Store performance history
        self.cpu_history = []
        self.ram_history = []

        # Store process information
        self.process_data = []
        self.process_refresh_counter = 0

        # Store current page and metric cards
        self.current_page = "Dashboard"
        self.nav_buttons = {}
        self.metric_cards = {}
        self.performance_charts = None

        # Prepare CPU measurements
        psutil.cpu_percent(interval=None)

        self.create_sidebar()

        self.content_frame = ctk.CTkFrame(
            self.app,
            fg_color="#101114",
            corner_radius=0
        )
        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.show_page("Dashboard")
        self.update_metrics()

    # ------------------------------------------
    # SIDEBAR
    # ------------------------------------------

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.app,
            width=225,
            corner_radius=0,
            fg_color="#18191E"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="PC MONITOR",
            font=("Arial", 23, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Hardware Dashboard",
            font=("Arial", 12),
            text_color="#8B8D98"
        ).pack(pady=(0, 30))

        pages = [
            "Dashboard",
            "CPU Monitor",
            "Memory Monitor",
            "Disk Monitor",
            "Performance Charts",
            "Running Processes",
            "System Information"
        ]

        for page in pages:
            button = ctk.CTkButton(
                self.sidebar,
                text=page,
                height=42,
                corner_radius=8,
                anchor="w",
                fg_color="transparent",
                hover_color="#292B33",
                text_color="#D8D9E0",
                font=("Arial", 13),
                command=lambda name=page: self.show_page(name)
            )
            button.pack(fill="x", padx=13, pady=4)
            self.nav_buttons[page] = button

        ctk.CTkButton(
            self.sidebar,
            text="Export Report",
            height=40,
            fg_color="#276749",
            hover_color="#31805A",
            command=self.export_report
        ).pack(side="bottom", fill="x", padx=13, pady=(5, 12))

        ctk.CTkLabel(
            self.sidebar,
            text="LIVE SYSTEM MONITORING",
            font=("Arial", 10, "bold"),
            text_color="#45C486"
        ).pack(side="bottom", pady=12)

    # ------------------------------------------
    # PAGE NAVIGATION
    # ------------------------------------------

    def show_page(self, page_name):
        self.current_page = page_name

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(
                    fg_color="#30333D",
                    text_color="#FFFFFF"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color="#D8D9E0"
                )

        # Remove the previous page's widgets
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.metric_cards = {}
        self.performance_charts = None

        if page_name == "Dashboard":
            self.create_dashboard()

        elif page_name == "CPU Monitor":
            self.create_cpu_page()

        elif page_name == "Memory Monitor":
            self.create_memory_page()

        elif page_name == "Disk Monitor":
            self.create_disk_page()

        elif page_name == "Performance Charts":
            self.create_charts_page()

        elif page_name == "Running Processes":
            self.create_process_page()

        elif page_name == "System Information":
            self.create_system_page()

    def create_heading(self, title, description):
        ctk.CTkLabel(
            self.content_frame,
            text=title,
            font=("Arial", 28, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", pady=(5, 5))

        ctk.CTkLabel(
            self.content_frame,
            text=description,
            font=("Arial", 13),
            text_color="#92949F"
        ).pack(anchor="w", pady=(0, 22))

    # ------------------------------------------
    # INFORMATION CARDS
    # ------------------------------------------

    def create_info_card(self, title, lines):
        card = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1B1D23",
            corner_radius=12
        )
        card.pack(fill="x", pady=7)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            text_color="#8B8D98"
        ).pack(anchor="w", padx=18, pady=(13, 5))

        for line in lines:
            ctk.CTkLabel(
                card,
                text=line,
                font=("Arial", 13),
                text_color="#FFFFFF",
                wraplength=800,
                justify="left"
            ).pack(anchor="w", padx=18, pady=3)

        return card

    def create_metric_card(self, parent, title, color):
        card = ctk.CTkFrame(
            parent,
            fg_color="#1B1D23",
            corner_radius=12
        )
        card.pack(fill="x", pady=7)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            text_color=color
        ).pack(anchor="w", padx=18, pady=(11, 3))

        value_label = ctk.CTkLabel(
            card,
            text="Loading...",
            font=("Arial", 25, "bold"),
            text_color="#FFFFFF"
        )
        value_label.pack(anchor="w", padx=18)

        detail_label = ctk.CTkLabel(
            card,
            text="Collecting information...",
            font=("Arial", 12),
            text_color="#92949F"
        )
        detail_label.pack(anchor="w", padx=18, pady=(2, 0))

        progress_bar = ctk.CTkProgressBar(
            card,
            height=8,
            progress_color=color
        )
        progress_bar.pack(fill="x", padx=18, pady=(10, 14))
        progress_bar.set(0)

        return {
            "value": value_label,
            "detail": detail_label,
            "bar": progress_bar
        }

    # ------------------------------------------
    # DASHBOARD
    # ------------------------------------------

    def create_dashboard(self):
        self.create_heading(
            "System Overview",
            "Monitor your computer's hardware performance in real time."
        )

        self.create_info_card(
            "COMPUTER",
            [
                f"Computer Name: {platform.node()}",
                f"Operating System: {platform.system()}",
                f"Platform: {platform.machine()}"
            ]
        )

        self.metric_cards["cpu"] = self.create_metric_card(
            self.content_frame,
            "CPU USAGE",
            "#579BFF"
        )

        self.metric_cards["memory"] = self.create_metric_card(
            self.content_frame,
            "MEMORY USAGE",
            "#45C486"
        )

        self.metric_cards["disk"] = self.create_metric_card(
            self.content_frame,
            "SYSTEM DRIVE USAGE",
            "#E9B44C"
        )

    # ------------------------------------------
    # CPU MONITOR
    # ------------------------------------------

    def create_cpu_page(self):
        self.create_heading(
            "CPU Monitor",
            "View processor utilization, frequency, and core information."
        )

        self.metric_cards["cpu"] = self.create_metric_card(
            self.content_frame,
            "CPU UTILIZATION",
            "#579BFF"
        )

        frequency = psutil.cpu_freq()

        if frequency:
            frequency_text = f"{frequency.current:.0f} MHz"
        else:
            frequency_text = "Unavailable"

        self.create_info_card(
            "PROCESSOR DETAILS",
            [
                f"Processor: {platform.processor() or 'Unavailable'}",
                f"Logical Cores: {psutil.cpu_count(logical=True)}",
                f"Physical Cores: {psutil.cpu_count(logical=False)}",
                f"Current Frequency: {frequency_text}"
            ]
        )

    # ------------------------------------------
    # MEMORY MONITOR
    # ------------------------------------------

    def create_memory_page(self):
        self.create_heading(
            "Memory Monitor",
            "View RAM utilization and memory availability."
        )

        self.metric_cards["memory"] = self.create_metric_card(
            self.content_frame,
            "RAM UTILIZATION",
            "#45C486"
        )

        memory = psutil.virtual_memory()

        self.create_info_card(
            "MEMORY DETAILS",
            [
                f"Total RAM: {self.format_bytes(memory.total)}",
                f"Used RAM: {self.format_bytes(memory.used)}",
                f"Available RAM: {self.format_bytes(memory.available)}",
                f"Memory Utilization: {memory.percent:.1f}%"
            ]
        )

    # ------------------------------------------
    # DISK MONITOR
    # ------------------------------------------

    def get_system_drive(self):
        drive = os.environ.get("SystemDrive", "C:")
        return drive + "\\"

    def create_disk_page(self):
        self.create_heading(
            "Disk Monitor",
            "View the capacity and available space of your system drive."
        )

        self.metric_cards["disk"] = self.create_metric_card(
            self.content_frame,
            "SYSTEM DRIVE UTILIZATION",
            "#E9B44C"
        )

        try:
            disk = psutil.disk_usage(self.get_system_drive())

            self.create_info_card(
                "STORAGE DETAILS",
                [
                    f"Drive: {self.get_system_drive()}",
                    f"Total Storage: {self.format_bytes(disk.total)}",
                    f"Used Storage: {self.format_bytes(disk.used)}",
                    f"Free Storage: {self.format_bytes(disk.free)}",
                    f"Storage Utilization: {disk.percent:.1f}%"
                ]
            )

        except OSError:
            self.create_info_card(
                "STORAGE DETAILS",
                ["Unable to retrieve system drive information."]
            )

    # ------------------------------------------
    # PERFORMANCE CHARTS
    # ------------------------------------------

    def create_charts_page(self):
        self.create_heading(
            "Performance Charts",
            "Track recent CPU and RAM utilization readings."
        )

        chart_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#101114",
            corner_radius=12
        )
        chart_frame.pack(fill="both", expand=True)

        self.performance_charts = PerformanceCharts(
            chart_frame,
            self.cpu_history,
            self.ram_history
        )

    # ------------------------------------------
    # RUNNING PROCESSES
    # ------------------------------------------

    def create_process_page(self):
        self.create_heading(
            "Running Processes",
            "Search processes and inspect their resource consumption."
        )

        search_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        search_frame.pack(fill="x", pady=(0, 12))

        self.process_search = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by process name or PID...",
            height=38
        )
        self.process_search.pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )
        self.process_search.bind(
            "<KeyRelease>",
            lambda event: self.display_processes()
        )

        ctk.CTkButton(
            search_frame,
            text="Refresh",
            width=100,
            height=38,
            command=self.refresh_processes
        ).pack(side="left")

        table_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#1B1D23",
            corner_radius=10
        )
        table_frame.pack(fill="both", expand=True)

        columns = ("pid", "name", "cpu", "memory")

        self.process_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.process_table.heading("pid", text="PID")
        self.process_table.heading("name", text="Process Name")
        self.process_table.heading("cpu", text="CPU (%)")
        self.process_table.heading("memory", text="Memory (%)")

        self.process_table.column("pid", width=85, anchor="center")
        self.process_table.column("name", width=300)
        self.process_table.column("cpu", width=100, anchor="center")
        self.process_table.column("memory", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.process_table.yview
        )
        self.process_table.configure(yscrollcommand=scrollbar.set)

        self.process_table.pack(
            side="left", fill="both", expand=True, padx=(8, 0), pady=8
        )
        scrollbar.pack(side="right", fill="y", padx=8, pady=8)

        # Style the process table
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#1B1D23",
            foreground="#FFFFFF",
            fieldbackground="#1B1D23",
            rowheight=29,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#292B33",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold"),
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[("selected", "#315B85")],
            foreground=[("selected", "#FFFFFF")]
        )

        self.process_status = ctk.CTkLabel(
            self.content_frame,
            text="",
            font=("Arial", 11),
            text_color="#92949F"
        )
        self.process_status.pack(anchor="w", pady=(8, 0))

        self.refresh_processes()

    def refresh_processes(self):
        processes = []

        total_memory = psutil.virtual_memory().total

        for process in psutil.process_iter(
            ["pid", "name", "memory_info"]
        ):
            try:
                info = process.info
                memory_info = info.get("memory_info")

                memory_percent = 0

                if memory_info and total_memory:
                    memory_percent = (
                        memory_info.rss / total_memory
                    ) * 100

                processes.append({
                    "pid": info["pid"],
                    "name": info.get("name") or "Unknown",
                    "cpu": process.cpu_percent(interval=None),
                    "memory": memory_percent
                })

            except (psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess):
                continue

        self.process_data = processes
        self.display_processes()

    def display_processes(self):
        if not hasattr(self, "process_table"):
            return

        for item in self.process_table.get_children():
            self.process_table.delete(item)

        search_text = self.process_search.get().strip().lower()

        filtered_processes = []

        for process in self.process_data:
            name = process["name"].lower()
            pid = str(process["pid"])

            if (
                search_text in name
                or search_text in pid
            ):
                filtered_processes.append(process)

        # Show the processes with the highest CPU usage first
        filtered_processes.sort(
            key=lambda process: process["cpu"],
            reverse=True
        )

        for process in filtered_processes:
            self.process_table.insert(
                "",
                "end",
                values=(
                    process["pid"],
                    process["name"],
                    f"{process['cpu']:.1f}",
                    f"{process['memory']:.2f}"
                )
            )

        self.process_status.configure(
            text=f"Showing {len(filtered_processes)} of "
                 f"{len(self.process_data)} detected processes"
        )

    # ------------------------------------------
    # SYSTEM INFORMATION
    # ------------------------------------------

    def create_system_page(self):
        self.create_heading(
            "System Information",
            "View operating system, processor, memory, and storage details."
        )

        self.create_info_card(
            "COMPUTER",
            [
                f"Computer Name: {platform.node()}",
                f"Operating System: {platform.system()}",
                f"OS Version: {platform.version()}",
                f"Platform: {platform.platform()}",
                f"Architecture: {platform.machine()}"
            ]
        )

        self.create_info_card(
            "PROCESSOR",
            [
                f"Processor: {platform.processor() or 'Unavailable'}",
                f"Logical Cores: {psutil.cpu_count(logical=True)}",
                f"Physical Cores: {psutil.cpu_count(logical=False)}"
            ]
        )

        memory = psutil.virtual_memory()

        self.create_info_card(
            "MEMORY",
            [
                f"Total RAM: {self.format_bytes(memory.total)}",
                f"Available RAM: {self.format_bytes(memory.available)}"
            ]
        )

        try:
            disk = psutil.disk_usage(self.get_system_drive())

            self.create_info_card(
                "SYSTEM DRIVE",
                [
                    f"Drive: {self.get_system_drive()}",
                    f"Total Capacity: {self.format_bytes(disk.total)}",
                    f"Free Space: {self.format_bytes(disk.free)}"
                ]
            )
        except OSError:
            pass

    # ------------------------------------------
    # LIVE PERFORMANCE UPDATES
    # ------------------------------------------

    def update_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()

        try:
            disk = psutil.disk_usage(self.get_system_drive())
        except OSError:
            disk = None

        # Keep the latest 30 readings for the charts
        self.cpu_history.append(cpu_usage)
        self.ram_history.append(memory.percent)

        if len(self.cpu_history) > 30:
            self.cpu_history.pop(0)
            self.ram_history.pop(0)

        # Update the visible CPU card
        if "cpu" in self.metric_cards:
            card = self.metric_cards["cpu"]

            card["value"].configure(
                text=f"{cpu_usage:.1f}%"
            )
            card["detail"].configure(
                text="Current processor utilization"
            )
            card["bar"].set(cpu_usage / 100)

        # Update the visible RAM card
        if "memory" in self.metric_cards:
            card = self.metric_cards["memory"]

            card["value"].configure(
                text=f"{memory.percent:.1f}%"
            )
            card["detail"].configure(
                text=f"{self.format_bytes(memory.used)} used "
                     f"of {self.format_bytes(memory.total)}"
            )
            card["bar"].set(memory.percent / 100)

        # Update the visible disk card
        if "disk" in self.metric_cards and disk is not None:
            card = self.metric_cards["disk"]

            card["value"].configure(
                text=f"{disk.percent:.1f}%"
            )
            card["detail"].configure(
                text=f"{self.format_bytes(disk.free)} free"
            )
            card["bar"].set(disk.percent / 100)

        # Refresh the performance charts when visible
        if (
            self.current_page == "Performance Charts"
            and self.performance_charts is not None
        ):
            self.performance_charts.update_chart()

        # Refresh process information every three seconds
        self.process_refresh_counter += 1

        if (
            self.current_page == "Running Processes"
            and self.process_refresh_counter >= 3
        ):
            self.process_refresh_counter = 0
            self.refresh_processes()

        # Schedule another update without blocking the window
        self.app.after(1000, self.update_metrics)

    # ------------------------------------------
    # HELPER FUNCTIONS
    # ------------------------------------------

    @staticmethod
    def format_bytes(size):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"

            size /= 1024

        return f"{size:.2f} PB"

    # ------------------------------------------
    # EXPORT CSV REPORT
    # ------------------------------------------

    def export_report(self):
        file_path = filedialog.asksaveasfilename(
            title="Export Performance Report",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=(
                "performance_report_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".csv"
            )
        )

        if not file_path:
            return

        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage(self.get_system_drive())

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as report:
                writer = csv.writer(report)

                writer.writerow(["PC HARDWARE MONITOR REPORT"])
                writer.writerow([
                    "Generated At",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
                writer.writerow([])

                writer.writerow(["SYSTEM INFORMATION"])
                writer.writerow(["Computer Name", platform.node()])
                writer.writerow(["Operating System", platform.platform()])
                writer.writerow([
                    "Processor",
                    platform.processor() or "Unavailable"
                ])
                writer.writerow([
                    "Logical Cores",
                    psutil.cpu_count(logical=True)
                ])
                writer.writerow([
                    "Physical Cores",
                    psutil.cpu_count(logical=False)
                ])
                writer.writerow([])

                writer.writerow(["PERFORMANCE SNAPSHOT"])
                writer.writerow([
                    "CPU Usage (%)",
                    psutil.cpu_percent(interval=None)
                ])
                writer.writerow([
                    "RAM Usage (%)",
                    memory.percent
                ])
                writer.writerow([
                    "Total RAM",
                    self.format_bytes(memory.total)
                ])
                writer.writerow([
                    "Available RAM",
                    self.format_bytes(memory.available)
                ])
                writer.writerow([
                    "System Drive",
                    self.get_system_drive()
                ])
                writer.writerow([
                    "Disk Usage (%)",
                    disk.percent
                ])
                writer.writerow([
                    "Total Disk Space",
                    self.format_bytes(disk.total)
                ])
                writer.writerow([
                    "Free Disk Space",
                    self.format_bytes(disk.free)
                ])
                writer.writerow([])

                writer.writerow([
                    "RECENT CPU AND RAM HISTORY"
                ])
                writer.writerow([
                    "Reading",
                    "CPU Usage (%)",
                    "RAM Usage (%)"
                ])

                for index, (cpu, ram) in enumerate(
                    zip(self.cpu_history, self.ram_history),
                    start=1
                ):
                    writer.writerow([index, cpu, ram])

                writer.writerow([])
                writer.writerow(["RUNNING PROCESSES"])
                writer.writerow([
                    "PID",
                    "Process Name",
                    "CPU Usage (%)",
                    "Memory Usage (%)"
                ])

                for process in self.process_data:
                    writer.writerow([
                        process["pid"],
                        process["name"],
                        process["cpu"],
                        process["memory"]
                    ])

            messagebox.showinfo(
                "Report Exported",
                f"Your performance report was saved to:\n{file_path}"
            )

        except (OSError, PermissionError, csv.Error) as error:
            messagebox.showerror(
                "Export Error",
                f"Unable to export the report:\n{error}"
            )


# ------------------------------------------
# START THE APPLICATION
# ------------------------------------------

if __name__ == "__main__":
    root = ctk.CTk()
    application = PCHardwareMonitor(root)
    root.mainloop()
