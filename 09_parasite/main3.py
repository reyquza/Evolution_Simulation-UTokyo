import copy
import random
import matplotlib.pyplot as plt

def plot_metapopulation_dynamics():
    SIZE = 30
    FOOD = 50
    P = 0.010
    Q = 0.02
    GENERATIONS = 500

    mutation_threshold = int(1 / P)
    move_threshold = int(1 / Q)

    # Record total-population histories
    total_a_history = []
    total_b_history = []
    
    # Record one central patch, such as [15, 15]
    local_a_history = []
    local_b_history = []

    population_a = [[100 for _ in range(SIZE)] for _ in range(SIZE)]
    population_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for generation in range(GENERATIONS):
        next_a = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        next_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        
        total_a = 0
        total_b = 0

        # Reproduction and parasite appearance
        for i in range(SIZE):
            for j in range(SIZE):
                if FOOD >= population_a[i][j]:
                    next_a[i][j] = population_a[i][j] * 2
                else:
                    next_a[i][j] = FOOD * 2

                if next_a[i][j] >= population_b[i][j]:
                    next_b[i][j] = population_b[i][j] * 2
                    next_a[i][j] -= population_b[i][j]
                else:
                    next_b[i][j] = next_a[i][j] * 2
                    next_a[i][j] = 0

                if random.randint(0, mutation_threshold) == 0:
                    next_b[i][j] += 1

        # Movement
        for i in range(-1, SIZE - 1):
            for j in range(-1, SIZE - 1):
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i + 1][j] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i - 1][j] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i][j + 1] += 1; next_a[i][j] -= 1
                if random.randint(0, move_threshold) < next_a[i][j]:
                    next_a[i][j - 1] += 1; next_a[i][j] -= 1

                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i + 1][j] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i - 1][j] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i][j + 1] += 1; next_b[i][j] -= 1
                if random.randint(0, move_threshold) < next_b[i][j]:
                    next_b[i][j - 1] += 1; next_b[i][j] -= 1

        # Record this generation
        for i in range(SIZE):
            for j in range(SIZE):
                total_a += next_a[i][j]
                total_b += next_b[i][j]

        total_a_history.append(total_a)
        total_b_history.append(total_b)
        
        # Record populations in the central patch
        local_a_history.append(next_a[SIZE//2][SIZE//2])
        local_b_history.append(next_b[SIZE//2][SIZE//2])

        population_a = copy.deepcopy(next_a)
        population_b = copy.deepcopy(next_b)

    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top: total populations across the grid
    ax1.plot(total_a_history, color='blue', label='Total Host (A)')
    ax1.plot(total_b_history, color='red', label='Total Parasite (B)')
    ax1.set_title("Macro Dynamics: Total Population in the Whole Space (SIZE=30)")
    ax1.set_ylabel("Total Population")
    ax1.legend()
    ax1.grid(True)

    # Bottom: populations in one patch
    ax2.plot(local_a_history, color='dodgerblue', linestyle='--', label='Local Host (A) at [15,15]')
    ax2.plot(local_b_history, color='orange', linestyle='--', label='Local Parasite (B) at [15,15]')
    ax2.set_title("Micro Dynamics: Population in a Single Local Compartment")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Local Population")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_metapopulation_dynamics()
