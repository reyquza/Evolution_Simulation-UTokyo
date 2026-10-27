import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def assortative_mating_simulation(
    Psize=100, LUCA=50, max_generation=1000, trial_count=100,
    mutation_rate=0.001, alpha_food=50, beta_food=50,
    mutation_step=5, mating_threshold=100, max_attempts_per_slot=2000
):
    all_results = []

    for _ in range(trial_count):
        population = [LUCA] * Psize

        for _ in range(max_generation):
            next_population = []

            def make_child():
                p1 = random.choice(population)
                p2 = p1
                for _ in range(10):
                    candidate = random.choice(population)
                    if abs(p1 - candidate) <= mating_threshold:
                        p2 = candidate
                        break
                child = (p1 + p2) / 2.0
                if random.random() < mutation_rate:
                    child += random.choice((-mutation_step, mutation_step))
                return max(0, min(100, child))

            attempts = 0
            while len(next_population) < alpha_food and attempts < max_attempts_per_slot:
                attempts += 1
                child = make_child()
                if child < random.randint(0, 100):
                    next_population.append(child)

            attempts = 0
            while len(next_population) < Psize and attempts < max_attempts_per_slot:
                attempts += 1
                child = make_child()
                if (100 - child) < random.randint(0, 100):
                    next_population.append(child)

            population = next_population

        all_results.extend(population)

    return all_results

def run_mating_experiment():
    print("Random mating")
    random_mating = assortative_mating_simulation(mating_threshold=100)
    print("Assortative mating")
    assortative_mating = assortative_mating_simulation(mating_threshold=3)
    
    df = pd.DataFrame({
        "mating_type": ["1. Random Mating"] * len(random_mating) + ["2. Assortative Mating"] * len(assortative_mating),
        "species (p)": random_mating + assortative_mating
    })
    
    plt.figure(figsize=(8, 6))
    sns.violinplot(data=df, x="mating_type", y="species (p)", inner="box", hue="mating_type", legend=False)
    plt.axhline(50, color='red', linestyle='--', alpha=0.5, label='LUCA (p=50)')
    
    plt.title("Assortative Mating")
    plt.ylabel("species")
    plt.show()

if __name__ == "__main__":
    run_mating_experiment()
