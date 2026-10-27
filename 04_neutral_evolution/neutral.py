import numpy as np
import matplotlib.pyplot as plt


def neutral_simulate(population_size=100, max_generation=10000):
    population = np.zeros(population_size)
    population[0] = 1
    gen = 0

    while gen < max_generation:
        p_A = np.mean(population)
        num_A = np.random.binomial(population_size, p_A)
        population = np.zeros(population_size)
        population[:num_A] = 1
        gen += 1

        if num_A == population_size:
            return gen

        if num_A == 0:
            return 0

    return None  # The observation window ended before fixation or loss.

def neutral_evolution(
    population_size=100,
    trial_count=10000,
    max_generation=10000,
    graph_mode=False,
    print_mode=False
):
    """
    Encode A as 1 and a as 0 to simplify the course-model calculations.
    """
    result = []
    for _ in range(trial_count):
        result.append(neutral_simulate(
            population_size,
            max_generation
        ))
    result = [gen for gen in result if gen is not None and gen != 0]
    
    fixed_trials = len(result)
    fixation_time = np.mean(result) if result else float('nan')
    
    if print_mode:
        print(f"fixed trials = {len(result)}")
        if len(result) > 0:
            print(f"mean fixation time = {np.mean(result)}", )
            print(f"2N = {2 * population_size}")
            print(f"N ln(N) = {population_size * np.log(population_size)}")
    
    if graph_mode:
        plt.plot(result)
        plt.xlabel("fixed trial")
        plt.ylabel("fixation generation")
        plt.show()
    
    
    return result, fixed_trials, fixation_time, population_size 

if __name__ == "__main__":
    neutral_evolution()
