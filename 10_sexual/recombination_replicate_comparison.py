import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.special import comb

# Simulation settings
Psize = 100
p = 0.1
MutationEffect = 1
Allele = 10
initialFitness = 2
generations = 80
trials = 5  # Average multiple trials for smoother curves

history_A_all = np.zeros(generations)
history_B_all = np.zeros(generations)

print("Running simulations...")
for t in range(trials):
    # Initialize the asexual population
    populationA = ["A"] * Psize
    genotypesA = [[0 for _ in range(Allele)] for _ in range(Psize)]
    
    # Initialize the sexual population
    populationB = ["B"] * Psize
    genotypesB1 = [[0 for _ in range(Allele)] for _ in range(Psize)]
    genotypesB2 = [[0 for _ in range(Allele)] for _ in range(Psize)]
    
    # Introduce initial mutations
    for i in range(Psize):  
        for j in range(Allele):
            if random.random() < p: genotypesA[i][j] = 1
            if random.random() < p: genotypesB1[i][j] = 1
            if random.random() < p: genotypesB2[i][j] = 1
                
    for generation in range(generations):
        # One asexual generation
        nextpopulationA = []
        nextgenotypesA = []
        for i in range(len(populationA)):  
            fitness = initialFitness + sum(genotypesA[i]) * MutationEffect
            for h in range(int(max(0, fitness))):  
                nextpopulationA.append("A")
                nextgenotypesA.append(genotypesA[i].copy())
        populationA = nextpopulationA
        genotypesA = nextgenotypesA
        while len(populationA) > Psize:
            del_index = random.randint(0, len(populationA) - 1)
            del populationA[del_index]; del genotypesA[del_index]
        history_A_all[generation] += sum(sum(g) for g in genotypesA) / Psize
        
        # One sexual generation
        nextpopulationB = []
        nextgenotypesB1 = []
        nextgenotypesB2 = []
        for i in range(len(populationB)):
            fitness = initialFitness + (sum(genotypesB1[i]) + sum(genotypesB2[i])) / 2 * MutationEffect
            for h in range(int(max(0, fitness))):  
                nextpopulationB.append("B")
                pair = random.randint(0, len(populationB) - 1)
                templist1 = [genotypesB1[i][j] if random.randint(0, 1) == 0 else genotypesB2[i][j] for j in range(Allele)]
                templist2 = [genotypesB1[pair][j] if random.randint(0, 1) == 0 else genotypesB2[pair][j] for j in range(Allele)]
                nextgenotypesB1.append(templist1)
                nextgenotypesB2.append(templist2)
        populationB = nextpopulationB
        genotypesB1 = nextgenotypesB1; genotypesB2 = nextgenotypesB2
        while len(populationB) > Psize:
            del_index = random.randint(0, len(populationB) - 1)
            del populationB[del_index]; del genotypesB1[del_index]; del genotypesB2[del_index]
        history_B_all[generation] += sum((sum(g1) + sum(g2)) / 2 for g1, g2 in zip(genotypesB1, genotypesB2)) / Psize

history_A_sim = history_A_all / trials
history_B_sim = history_B_all / trials

# Calculate mathematical approximations
theory_A = []
theory_B = []

# Asexual approximation: discrete selection on clone frequencies
# Initialize frequencies from a binomial distribution
p_k = [comb(Allele, k) * (p**k) * ((1-p)**(Allele-k)) for k in range(Allele + 1)]
for g in range(generations):
    avg_mut = sum(k * p_k[k] for k in range(Allele + 1))
    theory_A.append(avg_mut)
    # Update with the selection equation
    W = [initialFitness + k * MutationEffect for k in range(Allele + 1)]
    mean_W = sum(p_k[k] * W[k] for k in range(Allele + 1))
    p_k = [p_k[k] * W[k] / mean_W for k in range(Allele + 1)]

# Sexual approximation: selection on allele frequencies
q = p
alpha = 0.55  # Heuristic correction for finite-population effects and integer offspring counts
for g in range(generations):
    theory_B.append(q * Allele)
    # Allele-frequency increment used in the exploratory comparison
    delta_q = (0.5 * q * (1 - q)) / (2 + 10 * q)
    q += delta_q * alpha

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(history_A_sim, label="Asexual (Simulation)", color="blue", alpha=0.4, linestyle="--")
plt.plot(theory_A, label="Asexual (Mathematical Theory)", color="blue", linewidth=2)
plt.plot(history_B_sim, label="Sexual (Simulation)", color="orange", alpha=0.4, linestyle="--")
plt.plot(theory_B, label="Sexual (Mathematical Theory)", color="orange", linewidth=2)

plt.xlabel("Generations")
plt.ylabel("Average Mutations per Individual")
plt.title("Comparison of Simulation and Mathematical Theory")
plt.grid(True, linestyle=":")
plt.legend()
plt.show()
