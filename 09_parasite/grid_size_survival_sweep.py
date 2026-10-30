import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from spatial_host_parasite_model import run_simulation 

# Grid widths to test
size_list = [10, 15, 20, 25, 30, 35, 40]

def run_experiment(s):
    """Run one experiment in a worker process."""
    print(f"Starting simulation for SIZE={s}...")
    
    # Skip animation for faster experiments
    # Longer runs can examine persistence over a larger observation window
    a_surv, b_surv = run_simulation(SIZE=s, GENERATIONS=500, graph_mode=False)
    
    if a_surv and b_surv:
        result = 2  # Coexistence
    elif a_surv and not b_surv:
        result = 1  # Only hosts survive
    else:
        result = 0  # Extinction
        
    print(f"Completed SIZE={s}: state={result}")
    return result

if __name__ == '__main__':
    # Run experiments in separate processes
    print("Starting experiments; this may take some time...")
    with ProcessPoolExecutor() as executor:
        # Assign one experiment to each grid width
        results = list(executor.map(run_experiment, size_list))

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.scatter(size_list, results, marker='o', color='black', alpha=0.4)
    
    # Use descriptive state labels
    plt.yticks([0, 1, 2], ['Extinction\n(Both Dead)', 'Host Only\n(Parasite Dead)', 'Coexistence'])
    plt.xlabel('Grid SIZE')
    plt.ylabel('State after 500 generations')
    plt.title('Effect of Spatial Size on Host-Parasite Coexistence')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
