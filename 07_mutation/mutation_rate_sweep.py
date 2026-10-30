import numpy as np
import matplotlib.pyplot as plt
from mutation_divergence_model import simulation


rate_collection = np.arange(0.000, 0.010, 0.001)
mean_std, mean_range, emergences = [], [], []

for rate in rate_collection:
    result, emergence, stds, ranges = simulation(mutation_rate=rate, trial_count=50) 
    emergences.append(emergence)
    mean_std.append(np.mean(stds))
    mean_range.append(np.mean(ranges))

fig, ax1 = plt.subplots(figsize=(8, 5))

ax1.bar(rate_collection, emergences, width=0.0008, color='skyblue', alpha=0.7, label='Emergence (count)')
ax1.set_xlabel('Mutation Rate')
ax1.set_ylabel('Emergence Count', color='dodgerblue')
ax1.tick_params(axis='y', labelcolor='dodgerblue')

ax2 = ax1.twinx()
ax2.plot(rate_collection, mean_std, label='Mean STD', marker='o', color='crimson')
ax2.plot(rate_collection, mean_range, label='Mean Range', marker='^', color='darkorange')
ax2.set_ylabel('Standard Deviation / Range')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('Effect of Mutation Rate')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
