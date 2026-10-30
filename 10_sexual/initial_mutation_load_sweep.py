import matplotlib.pyplot as plt
import random
import numpy as np


def run_simulation(Psize=100, p=0.1, MutationEffect=-1, Allele=10, initialFitness=10, generations=80):
    """Run one simulation and return final mean mutation loads."""
    
    # Asexual initialization
    populationA = ["A"] * Psize
    genotypesA = [[1 if random.random() < p else 0 for _ in range(Allele)] for _ in range(Psize)]
    
    # Sexual initialization
    populationB = ["B"] * Psize
    genotypesB1 = [[1 if random.random() < p else 0 for _ in range(Allele)] for _ in range(Psize)]
    genotypesB2 = [[1 if random.random() < p else 0 for _ in range(Allele)] for _ in range(Psize)]
    
    for _ in range(generations):
        # Asexual reproduction
        if len(populationA) > 0:
            nextpopulationA, nextgenotypesA = [], []
            for i in range(len(populationA)):
                fitness = initialFitness + sum(genotypesA[i]) * MutationEffect
                if fitness < 0: fitness = 0
                for _ in range(int(fitness)):
                    nextpopulationA.append("A")
                    nextgenotypesA.append(list(genotypesA[i]))
            
            populationA, genotypesA = nextpopulationA, nextgenotypesA
            while len(populationA) > Psize:
                del_index = random.randint(0, len(populationA)-1)
                del populationA[del_index]
                del genotypesA[del_index]

        # Sexual reproduction
        if len(populationB) >= 2:
            nextpopulationB, nextgenotypesB1, nextgenotypesB2 = [], [], []
            for i in range(len(populationB)):
                available_pairs = [idx for idx in range(len(populationB)) if idx != i]
                if not available_pairs: break
                pair = random.choice(available_pairs)
                
                fitness = initialFitness + (sum(genotypesB1[i]) + sum(genotypesB2[i])) / 2 * MutationEffect
                if fitness < 0: fitness = 0
                for _ in range(int(fitness)):
                    nextpopulationB.append("B")
                    templist1 = [genotypesB1[i][j] if random.random() < 0.5 else genotypesB2[i][j] for j in range(Allele)]
                    templist2 = [genotypesB1[pair][j] if random.random() < 0.5 else genotypesB2[pair][j] for j in range(Allele)]
                    nextgenotypesB1.append(templist1)
                    nextgenotypesB2.append(templist2)
            
            populationB, genotypesB1, genotypesB2 = nextpopulationB, nextgenotypesB1, nextgenotypesB2
            while len(populationB) > Psize:
                del_index = random.randint(0, len(populationB)-1)
                del populationB[del_index]
                del genotypesB1[del_index]
                del genotypesB2[del_index]

    avg_mut_A = sum(sum(g) for g in genotypesA) / Psize if len(populationA) > 0 else Allele
    avg_mut_B = sum((sum(g1) + sum(g2)) for g1, g2 in zip(genotypesB1, genotypesB2)) / (Psize * 2) if len(populationB) >= 2 else Allele
    
    return avg_mut_A, avg_mut_B


"""
Sweep the initial mutation probability p.
"""
p_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
results_p_A = []
results_p_B = []
trials = 5

for p in p_values:
    sum_A, sum_B = 0, 0
    for _ in range(trials):
        a, b = run_simulation(p=p, Allele=10, initialFitness=10, generations=80)
        sum_A += a
        sum_B += b
    results_p_A.append(sum_A / trials)
    results_p_B.append(sum_B / trials)

"""
Sweep the number of loci.
"""
allele_values = [10, 20, 30, 40, 50]
results_al_A = []
results_al_B = []

for al in allele_values:
    sum_A, sum_B = 0, 0
    for _ in range(trials):
        a, b = run_simulation(p=0.5, Allele=al, initialFitness=10, generations=80) # Higher baseline fitness reduces extinction at larger mutation loads
        sum_A += a
        sum_B += b
    results_al_A.append(sum_A / trials)
    results_al_B.append(sum_B / trials)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(p_values, results_p_A, marker='o', label="Asexual (A)", color="blue")
ax1.plot(p_values, results_p_B, marker='s', label="Sexual (B)", color="orange")
ax1.set_xlabel("Initial Mutation Probability (p)")
ax1.set_ylabel("Final Average Mutations")
ax1.set_title("Effect of Mutation Probability")
ax1.legend()
ax1.grid(True)

ax2.plot(allele_values, results_al_A, marker='o', label="Asexual (A)", color="blue")
ax2.plot(allele_values, results_al_B, marker='s', label="Sexual (B)", color="orange")
ax2.set_xlabel("Number of Allele")
ax2.set_ylabel("Final Average Mutations")
ax2.set_title("Effect of Genome Size")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
