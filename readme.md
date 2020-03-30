# Energy-Efficient Fault Tolerance for Real-Time Tasks with Precedence Constraints on Heterogeneous Multicore Systems

## Overview

This repository provides a simplified Python implementation based on the paper:

> **Energy-Efficient Fault Tolerance for Real-Time Tasks with Precedence Constraints on Heterogeneous Multicore Systems**  
> _Abhishek Roy, Hakan Aydin (George Mason University), and Dakai Zhu (University of Texas at San Antonio)_

It implements DAG-based task modeling, basic partitioning (LTF, TBLS), speed assignment (Uniform Scaling, CPSS), and fault-tolerance via contingency tasks. While not a full production-grade system, it demonstrates core ideas in a concise form.

## Features

1. **DAG Task Model**
   - Each task has a base execution time, references to successor tasks, and a frequency parameter.
2. **Heterogeneous Dual-Core Architecture**
   - Simulates a high-performance (HP) core and a low-power (LP) core.
3. **Partitioning & Ordering Heuristics**
   - **Largest Task First (LTF)**: Sort tasks by descending execution time; assign to the core with the lowest utilization.
   - **Threshold-based List Scheduling (TBLS)**: Assign tasks to the LP core until the utilization exceeds a threshold, then assign to the HP core.
4. **Speed Assignment**
   - **Uniform Scaling (US)**: Same frequency for all tasks.
   - **Critical Path-based Static Speed (CPSS)**: Detects a simplified “critical path” (in this demo, tasks with the largest execution times) and boosts their frequency.
5. **Fault Tolerance**
   - Each task is duplicated on the opposite core, executed only if a primary fault is detected.
6. **Energy Model**
   - Simplistic formula \( P(f) = a \cdot f^3 + \alpha \), integrated over execution time.

## File Structure

<pre lang="markdown">
├── README.md 
└── energy_fault_tolerance.py 
</pre>

- **energy_fault_tolerance.py**: Main code containing classes (`Task`, `Core`), DAG generation, partitioning heuristics, speed assignment, duplication for fault tolerance, and a simple main function that simulates example configurations.

## Installation and Usage

1. **Clone or Download** this repository.
2. **Python Environment**: Any Python 3.7+ environment should work. It is recommended to use a virtual environment.
3. **Install Dependencies**: If a `requirements.txt` is provided, install via:
   ```bash
   pip install -r requirements.txt
   ```

python energy_fault_tolerance.py
