import numpy as np
import matplotlib.pyplot as plt


days = 300
strains = 4 # Original, alpha, delta, and hypothetical target strains

# Growth rates
r = [0.20, 0.28, 0.40, 0.65] 

# Removal rate
m = 0.10 

# Shared carrying capacity
K = 1000 

# Introduction day of each strain
emergence_times = [0, 60, 120, 180] 

# Daily population counts for each strain
population = np.zeros((strains, days))
population[0, 0] = 10 # Initial population


for t in range(1, days):
    # Total population across strains on the previous day
    total_population = np.sum(population[:, t-1])
    
    for i in range(strains):
        if t == emergence_times[i]:
            population[i, t-1] = 5 

        if population[i, t-1] > 0:
            current_numbers = population[i, t-1]
            # Lotka-Volterra-style competition with shared density dependence
            growth = r[i] * current_numbers * (1 - total_population / K) - m * current_numbers
            population[i, t] = max(0, current_numbers + growth)
        else:
            population[i, t] = 0

percentages = np.zeros((strains, days))
for t in range(days):
    total = np.sum(population[:, t])
    if total > 0:
        percentages[:, t] = (population[:, t] / total) * 100


fig, ax = plt.subplots(figsize=(10, 6))
labels = ['Original Strain', 'Variant Alpha', 'Variant Delta', 'Goal']
colors = ['#cccccc', '#ff9999', '#ff3333', '#66b3ff']

# Show replacement as a stacked area chart
ax.stackplot(range(days), percentages, labels=labels, colors=colors, alpha=0.8)

ax.set_title('Viral Variant Replacement', fontsize=14)
ax.set_xlabel('Time (Days)', fontsize=12)
ax.set_ylabel('Variant Frequency (%)', fontsize=12)
ax.set_xlim(0, days)
ax.set_ylim(0, 100)
ax.legend(loc='upper left')

plt.show()
