import numpy as np
import matplotlib.pyplot as plt

POP_SIZE = 1000
GENERATIONS = 100
TRIALS = 10
REPLICATION_CHANCES = 100

EXPERIMENTS = [
    {"fitness": {"a": 1, "A": 1.05}, "color": "darkorange"},
    {"fitness": {"a": 1, "A": 1.2},  "color": "darkblue"},
    {"fitness": {"a": 1, "A": 1.5},  "color": "darkgreen"},
]


def replication_binominal(fitness_array):
    p = fitness_array / REPLICATION_CHANCES
    return np.random.binomial(REPLICATION_CHANCES, p)

def replication_fixed(fitness_array):
    # Deterministic offspring counts
    return 


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

    freq_history = []

    for _ in range(GENERATIONS):
        population = next_generation(population, fitness)

        freq_A = np.sum(population) / POP_SIZE * 100
        freq_history.append(freq_A)

    fixation = np.all(population == 1)
    return freq_history, fixation


def main():
    for exp in EXPERIMENTS:
        fitness = exp["fitness"]
        color = exp["color"]

        fixation_count = 0

        for _ in range(TRIALS):
            history, fixed = run_trial(fitness)

            if fixed:
                fixation_count += 1

            plt.plot(history, color=color, alpha=0.7)

        print(f"fixation count: {fixation_count}")

    plt.xlabel("Generation")
    plt.ylabel("Frequency (%)")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    main()
