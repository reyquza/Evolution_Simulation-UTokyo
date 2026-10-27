import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.stats import binom

# ==========================================
# Simulation
# ==========================================
Psize = 100
p = 0.1
MutationEffect = 1
Allele = 10
initialFitness = 2

senniMutationA = []
populationA = ["A"] * (Psize)
genotypesA = [[0 for _ in range(Allele)] for _ in range(Psize)]

senniMutationB = []
populationB = ["B"] * (Psize)
genotypesB1 = [[0 for _ in range(Allele)] for _ in range(Psize)]
genotypesB2 = [[0 for _ in range(Allele)] for _ in range(Psize)]

# Initialize genotypes
for i in range(len(populationA)):  
    for j in range(Allele):
        if random.randint(0, int(1/p)-1) == 0: genotypesA[i][j] = 1
        if random.randint(0, int(1/p)-1) == 0: genotypesB1[i][j] = 1
        if random.randint(0, int(1/p)-1) == 0: genotypesB2[i][j] = 1
            
# Iterate through generations
for generation in range(80):
    # Asexual reproduction
    nextpopulationA = []
    nextgenotypesA = []
    for i in range(len(populationA)):  
        fitness = initialFitness + sum(genotypesA[i]) * MutationEffect
        if fitness < 0: fitness = 0
        for h in range(int(fitness)):  
            nextpopulationA.append("A")
            nextgenotypesA.append(list(genotypesA[i]))   
                    
    populationA = nextpopulationA
    genotypesA = nextgenotypesA
    
    while len(populationA) > Psize:
        del_index = random.randint(0, len(populationA)-1)
        del populationA[del_index]
        del genotypesA[del_index]
    
    temp = sum(sum(g) for g in genotypesA)
    senniMutationA.append(float(temp) / float(Psize))
    
    # Sexual reproduction
    nextpopulationB = []
    nextgenotypesB1 = []
    nextgenotypesB2 = []
    for i in range(len(populationB)):  
        pair = random.randint(0, len(populationB)-2) - (len(populationB)-1-i)
        fitness = initialFitness + (sum(genotypesB1[i]) + sum(genotypesB2[i])) / 2 * MutationEffect
        if fitness < 0: fitness = 0
        for h in range(int(fitness)):  
            nextpopulationB.append("B")
            
            templist1 = [genotypesB1[i][j] if random.randint(0, 1) == 0 else genotypesB2[i][j] for j in range(Allele)]
            templist2 = [genotypesB1[pair][j] if random.randint(0, 1) == 0 else genotypesB2[pair][j] for j in range(Allele)]
                    
            nextgenotypesB1.append(templist1)
            nextgenotypesB2.append(templist2)
                    
    populationB = nextpopulationB
    genotypesB1 = nextgenotypesB1
    genotypesB2 = nextgenotypesB2
    
    while len(populationB) > Psize:
        del_index = random.randint(0, len(populationB)-1)
        del populationB[del_index]
        del genotypesB1[del_index]
        del genotypesB2[del_index]
    
    temp = sum((sum(g1) + sum(g2)) for g1, g2 in zip(genotypesB1, genotypesB2))
    senniMutationB.append(float(temp) / float(Psize) / 2)


# ==========================================
# Calculate theoretical approximations
# ==========================================

# Asexual approximation using a replicator equation
theo_asexual = []
k = np.arange(Allele + 1)
# Expected initial counts for each mutation load
expected_counts = binom.pmf(k, Allele, p) * Psize
# Approximate finite-population absence by excluding expected counts below 0.5
x = np.where(expected_counts >= 0.5, binom.pmf(k, Allele, p), 0)
x = x / np.sum(x) # Normalize frequencies
W_k = initialFitness + k * MutationEffect

for _ in range(80):
    mean_W = np.sum(x * W_k)
    x = x * W_k / mean_W
    theo_asexual.append(np.sum(k * x))

# Sexual approximation using an allele-frequency recurrence
theo_sexual = []
q = p # Initial allele frequency
for _ in range(80):
    # Update using marginal fitness and mean fitness
    W_marginal = 2.5 + 9.5 * q
    W_mean = 2.0 + 10.0 * q
    q = q * (W_marginal / W_mean)
    theo_sexual.append(Allele * q)


# ==========================================
# Plot results
# ==========================================
plt.figure(figsize=(9, 6))

# Simulation results as solid lines
plt.plot(senniMutationA, label="Simulation: Asexual", color="tab:blue")
plt.plot(senniMutationB, label="Simulation: Sexual", color="tab:orange")

# Theoretical approximations as dashed lines
plt.plot(theo_asexual, label="Theory: Asexual", color="darkblue", linestyle="--", linewidth=2)
plt.plot(theo_sexual, label="Theory: Sexual", color="darkred", linestyle="--", linewidth=2)

plt.xlabel("Generation")
plt.ylabel("Average Mutations per Individual")
plt.title("Simulation vs Theoretical Expectation")
plt.legend(loc="upper left")
plt.grid(True, alpha=0.3)
plt.show()
