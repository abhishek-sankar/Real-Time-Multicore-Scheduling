import math
import random


class Task:
    """
    Represents a single task in the DAG.
    :param tid: unique task ID
    :param base_time: base execution time at nominal frequency
    :param successors: list of tasks that depend on this task
    """

    def __init__(self, tid, base_time, successors=None):
        self.tid = tid
        self.base_time = base_time
        self.successors = successors if successors else []
        self.pred_count = 0  # number of predecessors (filled later)
        self.assigned_core = None
        self.frequency = 1.0  # default frequency

    def __repr__(self):
        return f"T{self.tid}(time={self.base_time}, freq={self.frequency})"


class Core:
    """
    Represents a core in the heterogeneous system.
    :param core_id: unique core ID
    :param is_high_perf: True if HP core, False if LP core
    :param freq_range: (min_freq, max_freq)
    """

    def __init__(self, core_id, is_high_perf, freq_range=(0.5, 2.0)):
        self.core_id = core_id
        self.is_high_perf = is_high_perf
        self.freq_min, self.freq_max = freq_range
        self.schedule = []  # ordered list of tasks
        self.utilization = 0.0

    def __repr__(self):
        ctype = "HP" if self.is_high_perf else "LP"
        return f"Core{self.core_id}({ctype}, util={self.utilization:.2f})"


def generate_random_dag(num_tasks=8):
    """
    Generate random DAG tasks with some random dependencies.
    Returns a list of Task objects with filled successors/pred_count.
    """
    tasks = [Task(i, random.randint(1, 5)) for i in range(num_tasks)]
    for i in range(num_tasks - 1):
        # Randomly link tasks with some probability
        for j in range(i + 1, num_tasks):
            if random.random() < 0.3:  # 30% chance of i->j
                tasks[i].successors.append(tasks[j].tid)
                tasks[j].pred_count += 1
    return tasks


def ltf_partitioning(tasks, cores):
    """
    Largest Task First (LTF) partitioning & ordering:
    - Sort tasks by descending base_time, then assign each to the core with least utilization.
    - After assignment, order them on each core by topological constraints.
    """
    tasks_sorted = sorted(tasks, key=lambda t: t.base_time, reverse=True)
    for t in tasks_sorted:
        target_core = min(cores, key=lambda c: c.utilization)
        t.assigned_core = target_core.core_id
        target_core.schedule.append(t.tid)
        target_core.utilization += t.base_time
    return tasks


def tb_list_scheduling(tasks, cores, threshold=10):
    """
    Threshold-based List Scheduling (TBLS):
    - Assign tasks to the LP core until utilization exceeds threshold, else to HP.
    - Order is a simple topological-like approach (small pred_count first).
    """
    # Sort tasks by (pred_count, base_time) for a naive topological approach
    tasks_sorted = sorted(tasks, key=lambda t: (t.pred_count, -t.base_time))
    for t in tasks_sorted:
        if cores[1].utilization + t.base_time <= threshold:
            t.assigned_core = cores[1].core_id  # LP core
            cores[1].schedule.append(t.tid)
            cores[1].utilization += t.base_time
        else:
            t.assigned_core = cores[0].core_id  # HP core
            cores[0].schedule.append(t.tid)
            cores[0].utilization += t.base_time
    return tasks


def uniform_scaling(tasks, freq=1.0):
    """
    Uniform scaling (US): Assign the same frequency to all tasks (bounded by core constraints).
    """
    for t in tasks:
        t.frequency = freq


def cp_static_speed_assignment(tasks):
    """
    Critical Path-based Static Speed (CPSS) – Simplified:
    - Identify longest path in DAG, increase speed on tasks in that path.
    - Here, we just pick top 2 or 3 tasks with largest base_time as 'critical path'.
    """
    top_critical = sorted(tasks, key=lambda t: t.base_time, reverse=True)[:3]
    for t in tasks:
        if t in top_critical:
            t.frequency = 1.5
        else:
            t.frequency = 1.0


def duplicate_for_fault_tolerance(tasks, cores):
    """
    Duplicate tasks on opposite core for permanent fault tolerance.
    Each 'contingency' task is scheduled but only activated if fault occurs.
    """
    contingency_map = {}
    for t in tasks:
        # Assign duplicate task to the other core
        other_core_id = 1 - t.assigned_core
        # Store the mapping: original task ID -> duplicate task ID
        dup_id = f"dup{t.tid}"
        contingency_map[dup_id] = (t.tid, other_core_id)
    return contingency_map


def energy_consumption(tasks, alpha=0.1, a=1.0):
    """
    Compute approximate dynamic energy = sum over tasks of a*f^3*exec_time + alpha*exec_time
    """
    total_energy = 0.0
    for t in tasks:
        exec_time_scaled = t.base_time / t.frequency
        total_energy += (
            a * (t.frequency**3) * exec_time_scaled + alpha * exec_time_scaled
        )
    return total_energy


def simulate_example(num_tasks=8, method="LTF", scaling="US"):
    # Setup 2 cores: core0 = HP, core1 = LP
    cores = [Core(0, True), Core(1, False)]
    # Generate random DAG
    tasks = generate_random_dag(num_tasks)
    # Partition & order tasks
    if method == "LTF":
        tasks = ltf_partitioning(tasks, cores)
    else:
        tasks = tb_list_scheduling(tasks, cores)
    # Speed assignment
    if scaling == "US":
        uniform_scaling(tasks, freq=1.0)
    else:
        cp_static_speed_assignment(tasks)
    # Fault tolerance duplication
    contingency_map = duplicate_for_fault_tolerance(tasks, cores)
    # Compute overall energy
    en = energy_consumption(tasks)
    # Print results
    print("Cores:")
    for c in cores:
        print(c, " -> ", c.schedule)
    print("Tasks:", tasks)
    print("Contingency Mapping:", contingency_map)
    print(f"Approx. total energy consumption: {en:.3f}")


if __name__ == "__main__":
    simulate_example(num_tasks=8, method="LTF", scaling="US")
    simulate_example(num_tasks=8, method="TBLS", scaling="CPSS")
