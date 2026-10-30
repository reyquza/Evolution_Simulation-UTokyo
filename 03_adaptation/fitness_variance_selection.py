import numpy as np
import matplotlib.pyplot as plt

POP_SIZE = 1000
GENERATIONS = 100
TRIALS = 30
REPLICATION_CHANCES = 100


EXPERIMENTS = [
    {"fitness": {"a": 2, "A": 3}, "color": "darkorange"},
    {"fitness": {"a": 2, "A": 4},  "color": "darkblue"},
    {"fitness": {"a": 2, "A": 5},  "color": "darkgreen"},
]

def replication_binominal(fitness_array):
    p = fitness_array / REPLICATION_CHANCES
    return np.random.binomial(REPLICATION_CHANCES, p)


def replication_fixed(fitness_array):
    # Each individual produces its integer fitness in offspring
    return fitness_array.astype(int)


def next_generation(population, fitness, replication_func=replication_binominal):
    """Population is a NumPy array with 0 for a and 1 for A."""

    # Construct the fitness array
    fitness_array = np.where(population == 1, fitness["A"], fitness["a"])
    offspring_counts = replication_func(fitness_array)
    
    # Replicate individuals
    new_population = np.repeat(population, offspring_counts)

    # Randomly thin the population
    if len(new_population) > POP_SIZE:
        idx = np.random.choice(len(new_population), POP_SIZE, replace=False)
        new_population = new_population[idx]

    return new_population


def run_trial(fitness):
    population = np.zeros(POP_SIZE, dtype=np.int8)
    population[0] = 1  # A

    x_list = []
    y_list = []

    for _ in range(GENERATIONS):
        # Compute current mean fitness and variance
        W = np.where(population == 1, fitness["A"], fitness["a"])
        W_mean = np.mean(W)
        W_var = np.var(W)
        
        # Horizontal axis: fitness variance divided by mean fitness
        x = W_var / W_mean if W_mean > 0 else 0
        
        # Advance using deterministic offspring counts
        population = next_generation(population, fitness, replication_func=replication_fixed)

        # Compute mean fitness in the next generation
        next_W = np.where(population == 1, fitness["A"], fitness["a"])
        next_W_mean = np.mean(next_W)
        
        # Vertical axis: change in mean fitness
        y = next_W_mean - W_mean
        
        x_list.append(x)
        y_list.append(y)

    return x_list, y_list


def main():
    plt.figure(figsize=(8, 6))
    
    for exp in EXPERIMENTS:
        fitness = exp["fitness"]
        color = exp["color"]

        all_x = []
        all_y = []

        for _ in range(TRIALS):
            x_list, y_list = run_trial(fitness)
            all_x.extend(x_list)
            all_y.extend(y_list)

        plt.scatter(all_x, all_y, color=color, alpha=0.5, label=f'a:{fitness["a"]}, A:{fitness["A"]}')

    max_x = max(plt.xlim()[1], 0)
    plt.plot([0, max_x], [0, max_x], 'k--', alpha=0.7, label='y = x')

    plt.xlabel("Variance of Fitness / Mean Fitness (V(W) / W_mean)")
    plt.ylabel("Evolution Rate (ΔW_mean)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
