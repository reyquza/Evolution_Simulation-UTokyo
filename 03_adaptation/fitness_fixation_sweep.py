import matplotlib.pyplot as plt
import random

Psize = 100
max_adp_A = 2
trial = 50

def simulate(Psize, adp_A, adp_a=1):
    population = ["A"] + ["a"] * (Psize - 1)
    
    for generation in range(100):
        # Reproduction
        next_pop = []
        for gene in population:
            if gene == "a":
                next_pop.extend(["a"] * adp_a)
            elif gene == "A":
                next_pop.extend(["A"] * adp_A)
        # Selection
        if len(next_pop) > Psize:
            population = random.sample(next_pop, Psize)
        else:
            population = next_pop
            
        if "a" not in population:
            return True, generation + 1
    
    return False, 100


adp_A_list = list(range(1, max_adp_A + 1))
fix_probabilities = []
fix_speeds = []

for adp_A in adp_A_list:
    fixed_count = 0
    total_generations = 0
    
    for _ in range(trial):
        is_fixed, gen = simulate(Psize, adp_A)
        if is_fixed:
            fixed_count += 1
            total_generations += gen
            
    prob = fixed_count / trial
    fix_probabilities.append(prob)
    
    if fixed_count > 0:
        avg_gen = total_generations / fixed_count
    else:
        avg_gen = 0
    fix_speeds.append(avg_gen)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(adp_A_list, fix_probabilities, marker='o')
ax1.set_title("Probability of Fixation (A)")
ax1.set_xlabel("Fitness of A (adp_A)")
ax1.set_ylabel("Probability")
ax1.grid(True)

ax2.plot(adp_A_list, fix_speeds, marker='o', color='orange')
ax2.set_title("Speed of Fixation (Generations)")
ax2.set_xlabel("Fitness of A (adp_A)")
ax2.set_ylabel("Average Generations (if fixed)")
ax2.grid(True)

plt.tight_layout()
plt.show()
