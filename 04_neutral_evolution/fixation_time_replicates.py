import numpy as np
import matplotlib.pyplot as plt
from neutral_drift_model import neutral_evolution

trial = 20
population_size = 100
mean_experiment = []
N2_data = []
NlnN_data = []
x = [i for i in range(1, trial+1)]

for i in range(trial):
    _, fixed_trials, fixation_time, population_size = neutral_evolution(population_size)
    N2 = 2 * population_size
    NlnN = population_size * np.log(population_size)
    mean_experiment.append(fixation_time)
    N2_data.append(N2)
    NlnN_data.append(NlnN)
    
plt.scatter(x, mean_experiment, label="mean_experiment")
plt.plot(x, N2_data, label="2N")
plt.plot(x, NlnN_data, label="Nln(N)")
plt.title(f"neutral_evolution: N = {population_size}")
plt.xlabel("trial")
plt.ylabel("average_fixation_time")
plt.legend()
plt.show()

