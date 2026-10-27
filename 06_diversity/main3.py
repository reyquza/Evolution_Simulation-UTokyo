import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Periodically varying carrying capacities
def get_dynamic_K(t):
    # Switch between (70, 30) and (30, 70) every 100 time units
    if (int(t) // 100) % 2 == 0:
        return 70, 30
    else:
        return 30, 70

def lotka_volterra_periodic(N, t, r1, r2, alpha, beta):
    N1, N2 = N
    # Get both carrying capacities at the current time
    K1, K2 = get_dynamic_K(t)
    
    dN1_dt = r1 * N1 * (1 - (N1 + alpha * N2) / K1)
    dN2_dt = r2 * N2 * (1 - (N2 + beta * N1) / K2)
    return [dN1_dt, dN2_dt]

# Run the simulation
t = np.linspace(0, 400, 2000) # Two full cycles over 400 time units
N0 = [10, 10]                 # Initial populations
r1, r2 = 0.1, 0.1             # Growth rates

# Two distinct niches with low competition coefficients
result = odeint(lotka_volterra_periodic, N0, t, args=(r1, r2, 0.2, 0.2))

# Plot the trajectories
plt.figure(figsize=(10, 5))
plt.plot(t, result[:, 0], label='Species A (Alpha Specialist)', color='red')
plt.plot(t, result[:, 1], label='Species B (Beta Specialist)', color='green')
plt.title('Lotka-Volterra with Periodic Environmental Change')
plt.xlabel('Time (Generations)')
plt.ylabel('Population Size')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
