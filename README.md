# PC Hardware and Performance Monitor

A **PC Hardware and Performance Monitor** built with Python to help users monitor their computer's performance through a desktop application. It provides real-time CPU, memory, and disk usage, performance charts, running process information, and system details in one interface.

The project demonstrates the use of Python, system monitoring libraries, data visualization, and graphical user interface development.

---

## Overview

The PC Hardware and Performance Monitor is designed to help users understand how their computer uses its hardware resources. It collects system performance information and displays it through a clean desktop interface.

The application is intended for learning and basic system monitoring. It does not modify system settings or terminate running processes.

## Features

* **Dashboard** — View a summary of your computer's current performance.
* **CPU Monitor** — Monitor processor usage in real time.
* **Memory Monitor** — Check RAM usage and memory availability.
* **Disk Monitor** — View disk usage information.
* **Performance Charts** — Visualize CPU and memory usage through line charts.
* **Running Processes** — View running processes and their CPU usage, with search and refresh functionality.
* **System Information** — Display operating system and hardware-related details.
* **CSV Report Export** — Export available monitoring information into a CSV file.
* **Automatic Updates** — Refresh performance readings periodically while the application is running.
* **Graphical User Interface** — Navigate between monitoring pages using a sidebar.

## Technologies Used

* **Python** — Main programming language.
* **CustomTkinter** — Desktop graphical user interface.
* **psutil** — Retrieves system and process performance information.
* **Matplotlib** — Creates performance charts.
* **CSV** — Supports exporting monitoring reports.

## Project Structure

```text
PC-Hardware-Monitor/
│
├── main.py
├── performance_charts.py
├── requirements.txt
├── README.md
├── .gitignore
```

## Requirements

Before running the application, make sure you have:

* Python 3.10 or newer recommended
* pip (Python package installer)
* An operating system supported by Python and the required libraries

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PC-Hardware-Monitor.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project Folder

```bash
cd PC-Hardware-Monitor
```

### 3. Install the Required Libraries

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
customtkinter
psutil
matplotlib
```

### 4. Run the Application

```bash
python main.py
```

The desktop application should open and display the performance dashboard.

## How to Use

1. Start the application by running `main.py`.
2. Open the **Dashboard** to view the current system performance summary.
3. Select **CPU Monitor** to check processor usage.
4. Select **Memory Monitor** to view RAM usage.
5. Select **Disk Monitor** to check disk information.
6. Open **Performance Charts** to view CPU and memory usage trends.
7. Use **Running Processes** to search for and inspect active processes.
8. Open **System Information** to view details about your computer.
9. Use the CSV export feature to save available monitoring information to a report.

## Learning Objectives

This project helps demonstrate practical programming concepts, including:

* Using external Python libraries.
* Creating a desktop application with multiple pages.
* Collecting and displaying system performance data.
* Updating interface elements periodically.
* Working with lists and historical performance readings.
* Creating charts to visualize data.
* Retrieving and displaying running process information.
* Exporting information to CSV files.
* Organizing a Python project into multiple modules.

## Limitations

* Available system information depends on the operating system and hardware.
* CPU and memory readings may fluctuate as other applications run.
* Some process details may require additional permissions.
* CPU temperature and fan speed monitoring are not included in the current version because hardware support varies.
* The application is intended for monitoring and does not automatically optimize system performance or terminate processes.

## Future Improvements

Possible improvements for future versions include:

* CPU temperature and fan speed monitoring where supported.
* More detailed disk activity monitoring.
* Additional performance charts and historical data.
* Customizable monitoring intervals.
* Automatic report generation.
* Performance alerts when resource usage becomes unusually high.
* A more detailed hardware information page.

## Disclaimer

This project is intended for educational purposes and basic computer performance monitoring. The displayed information may vary depending on the user's hardware, operating system, permissions, and installed drivers.

## Author

**Jose Navoa**

Aspiring Information Technology Student
