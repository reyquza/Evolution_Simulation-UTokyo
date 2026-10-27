import random
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

def run_fast_sim(SIZE, P, Q, FOOD, GENERATIONS=500):
    """
    Simulate final survival without plotting or storing population histories.
    """
    mutation_threshold = int(1 / P)
    move_threshold = int(1 / Q) if Q > 0 else float('inf')

    population_a = [[100 for _ in range(SIZE)] for _ in range(SIZE)]
    population_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for _ in range(GENERATIONS):
        next_a = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        next_b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
        total_a = 0
        total_b = 0

        # Reproduction and mutation
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
                # Host movement
                for _ in range(next_a[i][j]):
                    if random.randint(0, move_threshold) == 0:
                        d = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                        next_a[i + d[0]][j + d[1]] += 1
                        next_a[i][j] -= 1
                # Parasite movement
                for _ in range(next_b[i][j]):
                    if random.randint(0, move_threshold) == 0:
                        d = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                        next_b[i + d[0]][j + d[1]] += 1
                        next_b[i][j] -= 1

        # Check survival
        for i in range(SIZE):
            for j in range(SIZE):
                total_a += next_a[i][j]
                total_b += next_b[i][j]
        
        # Stop early if both populations are extinct
        if total_a == 0 and total_b == 0:
            return False

        population_a = next_a
        population_b = next_b

    # Return whether both populations survive the observation window
    return (total_a > 0 and total_b > 0)

def worker_q(args):
    size, p, q, food, gen = args
    return q, run_fast_sim(size, p, q, food, gen)

def worker_food(args):
    size, p, q, food, gen = args
    return food, run_fast_sim(size, p, q, food, gen)

if __name__ == '__main__':
    # Experiment settings
    TARGET_SIZE = 15      # Grid width near the observed coexistence transition
    TRIALS = 20           # Trials per parameter setting
    BASE_P = 0.010
    BASE_Q = 0.02
    BASE_FOOD = 50
    GENS = 500
    
    # Parameter values to sweep
    q_list = [0.02, 0.04, 0.10, 0.20, 0,50, 1.00]
    food_list = [50 + 100* i for i in range(6)]

    print(f"Starting experiments at SIZE={TARGET_SIZE} ({TRIALS} trials per condition)...")

    # Experiment A: vary migration parameter Q
    tasks_q = [(TARGET_SIZE, BASE_P, q, BASE_FOOD, GENS) for q in q_list for _ in range(TRIALS)]
    q_results = {q: 0 for q in q_list}
    
    with ProcessPoolExecutor() as executor:
        for q, is_coexist in executor.map(worker_q, tasks_q):
            if is_coexist:
                q_results[q] += 1
                
    q_probs = [q_results[q] / TRIALS * 100 for q in q_list]
    print("Experiment A (migration Q) complete")

    # Experiment B: vary FOOD
    tasks_food = [(TARGET_SIZE, BASE_P, BASE_Q, f, GENS) for f in food_list for _ in range(TRIALS)]
    food_results = {f: 0 for f in food_list}
    
    with ProcessPoolExecutor() as executor:
        for f, is_coexist in executor.map(worker_food, tasks_food):
            if is_coexist:
                food_results[f] += 1
                
    food_probs = [food_results[f] / TRIALS * 100 for f in food_list]
    print("Experiment B (FOOD) complete")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot the effect of Q
    ax1.plot(q_list, q_probs, marker='o', color='red', linewidth=2)
    ax1.set_title(f"Exp A: Effect of Migration Rate Q (SIZE={TARGET_SIZE})")
    ax1.set_xlabel("Migration Rate (Q)")
    ax1.set_ylabel("Coexistence Probability (%)")
    ax1.set_ylim(-5, 105)
    ax1.grid(True)

    # Plot the effect of FOOD
    ax2.plot(food_list, food_probs, marker='o', color='green', linewidth=2)
    ax2.set_title(f"Exp B: Effect of Enrichment FOOD (SIZE={TARGET_SIZE})")
    ax2.set_xlabel("Amount of Food (FOOD)")
    ax2.set_ylabel("Coexistence Probability (%)")
    ax2.set_ylim(-5, 105)
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
