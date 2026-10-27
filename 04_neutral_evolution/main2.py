import numpy as np
import matplotlib.pyplot as plt
from neutral import neutral_evolution

population_sizes = [10, 20, 50, 100, 200, 500, 1000]
trial_count = 10000

mean_fixation_times = []
two_N_curve = []
n_ln_n_curve = []

for population_size in population_sizes:
    result, _, mean_fixation_time, _ = neutral_evolution(population_size, trial_count=trial_count)
    mean_fixation_times.append(mean_fixation_time)
    two_N_curve.append(2 * population_size)
    n_ln_n_curve.append(population_size * np.log(population_size))
    plt.scatter([population_size]*len(result), result, label=f"N={population_size}")

plt.plot(population_sizes, mean_fixation_times, label="mean_experiment")
plt.plot(population_sizes, two_N_curve, label="2N")
plt.plot(population_sizes, n_ln_n_curve, label="Nln(N)")
plt.title("neutral_evolution: fixation time vs N")
plt.xlabel("population size (N)")
plt.ylabel("fixation time")
plt.legend()
plt.grid(True)
plt.savefig("2.png")
plt.show()
