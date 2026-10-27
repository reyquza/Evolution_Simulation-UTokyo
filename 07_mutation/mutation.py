import random
import matplotlib.pyplot as plt
import numpy as np


def simulation(
    Psize=101,
    LUCA=50,
    max_generation=1000,
    trial_count=10,
    mutation_rate=0.001,
    alpha_food=50,
    beta_food=50,
    mutation=1,
    new_threshold=5,
    graph_mode=False,
    print_mode=False,
):
    
    if print_mode:
        print(f"LUCA = {LUCA}")
        
    result = []
    stds = []
    ranges = []
    emergence = 0
    
    for _ in range(trial_count):

        population = [LUCA] * Psize

        for _ in range(max_generation):
            next_population = []
            
            while len(next_population) < alpha_food:
                p = random.choice(population)
                if p < random.randint(0, Psize-1):
                    if random.random() < mutation_rate:
                        p += random.choice((-mutation, mutation))
                        p = max(0, min(Psize-1, p))

                    next_population.append(p)

            while len(next_population) < alpha_food + beta_food:
                p = random.choice(population)
                if (100 - p) < random.randint(0, Psize-1):
                    if random.random() < mutation_rate:
                        p += random.choice((-mutation, mutation))
                        p = max(0, min(Psize-1, p))

                    next_population.append(p)

            population = next_population

            if len(population) > Psize:
                population = random.sample(population, Psize)

        if print_mode:
            print(set(population))
        
        new_species = [p for p in population if p >= LUCA + new_threshold or p <= LUCA - new_threshold or p==LUCA]   
        if new_species != []:
            emergence += 1
            print(set(sorted(new_species)))
        result.extend(set(population))
        
        std = np.std(result)
        result_range = max(result) - min(result)
        stds.append(std)
        ranges.append(result_range)

    if graph_mode:
        plt.hist(result)
        plt.title(f"LUCA={LUCA} std={std:.2f} range={result_range}")
        plt.show()
    
    return result, emergence, stds, ranges


if __name__ == "__main__":
    simulation(LUCA=50, graph_mode=True, mutation=10)
