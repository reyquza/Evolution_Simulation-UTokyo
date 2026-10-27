import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from main import run_simulation  # Import the reusable simulation

# Examine the region around grid widths 10 to 15
size_list = list(range(8, 19))
TRIALS = 10  # Trials per grid width

def worker(args):
    """Worker for one grid-size experiment."""
    size, trial_idx = args
    # Run without animation
    a_surv, b_surv = run_simulation(SIZE=size, GENERATIONS=500, graph_mode=False)
    # Whether both hosts and parasites survive
    is_coexist = (a_surv and b_surv)
    return size, is_coexist

if __name__ == '__main__':
    print(f"Starting {TRIALS} trials per grid width ({len(size_list)*TRIALS} tasks)...")
    
    # Create a flat task list
    tasks = [(s, t) for s in size_list for t in range(TRIALS)]
    
    # Count coexistence outcomes by grid width
    coexist_counts = {s: 0 for s in size_list}
    
    # Run tasks in separate processes
    with ProcessPoolExecutor() as executor:
        results = executor.map(worker, tasks)
        for size, is_coexist in results:
            if is_coexist:
                coexist_counts[size] += 1

    # Convert counts to percentages
    probabilities = [(coexist_counts[s] / TRIALS) * 100 for s in size_list]

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(size_list, probabilities, marker='o', linestyle='-', color='blue', linewidth=2)
    plt.xlabel('Grid SIZE')
    plt.ylabel('Coexistence Probability (%)')
    plt.title(f'Effect of Spatial Size on Coexistence Probability ({TRIALS} trials per size)')
    plt.xticks(size_list)
    plt.ylim(-5, 105)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
