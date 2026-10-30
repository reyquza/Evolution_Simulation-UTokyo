import numpy as np
import matplotlib.pyplot as plt
from mutation_divergence_model import simulation


mut_collection = [1, 2, 3, 4, 5]
mean_std, mean_range, emergences = [], [], []

for mut in mut_collection:
    result, emergence, stds, ranges = simulation(mutation=mut, trial_count=50) 
    emergences.append(emergence)
    mean_std.append(np.mean(stds))
    mean_range.append(np.mean(ranges))

fig, ax1 = plt.subplots(figsize=(8, 5))

ax1.bar(mut_collection, emergences, width=0.0008, color='skyblue', alpha=0.7, label='Emergence (count)')
ax1.set_xlabel('Mutation Rate')
ax1.set_ylabel('Emergence Count', color='dodgerblue')
ax1.tick_params(axis='y', labelcolor='dodgerblue')

ax2 = ax1.twinx()
ax2.plot(mut_collection, mean_std, label='Mean STD', marker='o', color='crimson')
ax2.plot(mut_collection, mean_range, label='Mean Range', marker='^', color='darkorange')
ax2.set_ylabel('Standard Deviation / Range')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('Effect of mut')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
