import matplotlib.pyplot as plt
import random
import numpy as np

Psize = 100
p = 0.1
MutationEffect = -1 # Deleterious mutation effect
Allele = 10
initialFitness = 2

# Initialization
senniMutationA = []
# Retain population lists to match the original model structure
populationA = ["A"] * Psize
# Initialize NumPy arrays
genotypesA = np.zeros((Psize, Allele), dtype=int)

senniMutationB = []
populationB = ["B"] * Psize
genotypesB1 = np.zeros((Psize, Allele), dtype=int)
genotypesB2 = np.zeros((Psize, Allele), dtype=int)

# Introduce mutations in the initial population
for i in range(Psize):
    genotypesA[i] = np.random.choice([0, 1], size=Allele, p=[1-p, p])
    genotypesB1[i] = np.random.choice([0, 1], size=Allele, p=[1-p, p])
    genotypesB2[i] = np.random.choice([0, 1], size=Allele, p=[1-p, p])

# Iterate through generations
for generation in range(80):
    # Asexual reproduction
    nextpopulationA = []
    nextgenotypesA = []
    
    for i in range(len(populationA)):
        fitness = initialFitness + np.sum(genotypesA[i]) * MutationEffect
        if fitness < 0:
            fitness = 0
            
        # Stochastic rounding: use the fractional part as an extra-offspring probability
        integer_fitness = int(fitness)
        if random.random() < (fitness - integer_fitness):
            integer_fitness += 1
            
        for h in range(integer_fitness):
            nextpopulationA.append("A")
            # Copy the NumPy genotype array
            nextgenotypesA.append(genotypesA[i].copy())
            
    populationA = nextpopulationA
    genotypesA = nextgenotypesA
    
    # Limit population size by random deletion
    while len(populationA) > Psize:
        del_index = random.randint(0, len(populationA) - 1)
        del populationA[del_index]
        del genotypesA[del_index]
        
    # Record the mean mutation load
    tempA = np.sum(genotypesA)
    senniMutationA.append(tempA / Psize)

    # Sexual reproduction
    nextpopulationB = []
    nextgenotypesB1 = []
    nextgenotypesB2 = []
    
    for i in range(len(populationB)):
        # Retain the original partner-selection rule and its possible bias
        pair = random.randint(0, len(populationB) - 2) - (len(populationB) - 1 - i)
        
        fitness = initialFitness + (np.sum(genotypesB1[i]) + np.sum(genotypesB2[i])) / 2 * MutationEffect
        if fitness < 0:
            fitness = 0
            
        # Stochastic rounding
        integer_fitness = int(fitness)
        if random.random() < (fitness - integer_fitness):
            integer_fitness += 1
            
        for h in range(integer_fitness):
            nextpopulationB.append("B")
            
            # Inherit alleles randomly from the two parents
            mask1 = np.random.choice([True, False], size=Allele)
            mask2 = np.random.choice([True, False], size=Allele)
            
            child1 = np.where(mask1, genotypesB1[i], genotypesB2[i])
            child2 = np.where(mask2, genotypesB1[pair], genotypesB2[pair])
            
            nextgenotypesB1.append(child1)
            nextgenotypesB2.append(child2)
            
    populationB = nextpopulationB
    genotypesB1 = nextgenotypesB1
    genotypesB2 = nextgenotypesB2
    
    # Limit population size
    while len(populationB) > Psize:
        del_index = random.randint(0, len(populationB) - 1)
        del populationB[del_index]
        del genotypesB1[del_index]
        del genotypesB2[del_index]
        
    # Record the mean mutation load
    tempB = np.sum(genotypesB1) + np.sum(genotypesB2)
    senniMutationB.append(tempB / (Psize * 2))

# Plot results
plt.plot(senniMutationA, label="asexual")
plt.plot(senniMutationB, label="sexual")
plt.legend(loc="upper left")
plt.xlabel("Generation")
plt.ylabel("Average Mutations per Individual")
plt.show()
