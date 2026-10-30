import numpy as np
import matplotlib.pyplot as plt

def simulate_drift(N_sequence, initial_p, max_gen):
    """
    Simulate an allele-frequency trajectory under genetic drift.
    """
    trajectory = [initial_p]
    p = initial_p
    for gen in range(1, max_gen):
        N = N_sequence[gen]
        if p == 0 or p == 1:
            trajectory.append(p)
        else:
            num_A = np.random.binomial(N, p)
            p = num_A / N
            trajectory.append(p)
    return trajectory


max_gen = 200      
initial_p = 0.1
trials = 20 
# Constant population size
N_constant = [500] * max_gen
# Temporary population bottleneck
N_bottleneck = [500] * max_gen
for i in range(80, 100):
    N_bottleneck[i] = 10

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True)

for _ in range(trials):
    traj = simulate_drift(N_constant, initial_p, max_gen)
    ax1.plot(traj, alpha=0.6)
ax1.set_title("Constant Large Population (N=500)")
ax1.set_ylabel("Frequency of Rare Trait")
ax1.set_xlabel("Generation")
ax1.grid(True)

for _ in range(trials):
    traj = simulate_drift(N_bottleneck, initial_p, max_gen)
    ax2.plot(traj, alpha=0.6)
ax2.axvspan(80, 100, color='red', alpha=0.2, label='Bottleneck (N=10)')
ax2.set_title("Population with Bottleneck")
ax2.set_xlabel("Generation")
ax2.legend()
ax2.grid(True)

plt.suptitle(f"Simulation of Rare Trait (Initial Frequency = {initial_p*100}%)")
plt.tight_layout()
plt.show()
