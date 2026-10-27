import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random


def run_simulation(Psize=101, max_gen=1000, alpha_num=50, periodic_mode=False):
    population = list(range(0, Psize))

    for gen in range(max_gen):
        
        if periodic_mode:
            if (gen // 100) % 2 == 0:
                current_alpha = 70
            else:
                current_alpha = 30
            current_beta = Psize - current_alpha
        else:
            current_alpha = alpha_num
            current_beta = Psize - alpha_num
            
        next_pop = []
        num = 0
        while num < current_alpha:  
            target_index = random.randint(0, len(population) - 1)
            val = population[target_index]
            
            if val < random.randint(0, 100): 
                next_pop.append(val) 
                num += 1
                
        num = 0
        while num < current_beta: 
            target_index = random.randint(0, len(population) - 1) 
            val = population[target_index]
            
            if 100 - val < random.randint(0, 100):
                next_pop.append(val)
                num += 1
                
        population = next_pop
        
        if len(population) > Psize:
            population = random.sample(population, Psize)
            
    return list(set(population))


def calculate_alpha(x1, x2):
    u_a1 = (100 - x1) / 100
    u_b1 = x1 / 100
    u_a2 = (100 - x2) / 100
    u_b2 = x2 / 100
        
    numerator = u_a1 * u_a2 + u_b1 * u_b2
    denom1 = u_a1**2 + u_b1**2
    denom2 = u_a2**2 + u_b2**2
    alpha_12 = numerator / denom1 if denom1 > 0 else 0
    alpha_21 = numerator / denom2 if denom2 > 0 else 0
    
    return alpha_12, alpha_21


def analyze(Psize=101, trials=100, alpha_num=50, periodic_mode=False):
    all_survivors = []
    single_species = []
    two_species_low = []
    two_species_high = []
   
    two_species_count = 0      
    alpha_over_1_count = 0    
    
    for _ in range(trials):
        result = run_simulation(Psize=Psize, alpha_num=alpha_num, periodic_mode=periodic_mode)
        all_survivors.extend(result)
        
        if len(result) == 1:
            single_species.append(result[0])
        elif len(result) == 2:
            two_species_count += 1
            result.sort()
            two_species_low.append(result[0])
            two_species_high.append(result[1])
        
            x1, x2 = result[0], result[1]
            a12, a21 = calculate_alpha(x1, x2)
            # K1_K2 = alpha_num / (Psize - alpha_num) if Psize-alpha_num != 0 else 0
            # K2_K1 = (Psize - alpha_num) / alpha_num if alpha_num != 0 else 1
            # Fallback values in the exploratory unequal-capacity comparison
            # if a12 > K1_K2 or a21 > K2_K1:
            #     alpha_over_1_count += 1
            if a12 > 1 or a21 > 1:
                alpha_over_1_count += 1
    
    print("result")
    print(f"Total trials: {trials}")
    print(f"Trials with two surviving types: {two_species_count}")
    print(f"Trials with a competition coefficient above one: {alpha_over_1_count}")
    if two_species_count > 0:
        pct = (alpha_over_1_count / two_species_count) * 100
        print(f"Percentage: {pct:.1f} %")
    else:
        print("No two-type outcomes")
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    
    ax[0].hist(single_species, bins=20, range=(0, 100), color='blue', alpha=0.7)
    ax[0].set_title('1 Species Remaining')
    ax[0].set_xlabel('Trait Value')
    ax[0].set_ylabel('Frequency')
    ax[0].set_xlim(0, 100)
    
    ax[1].hist(two_species_low, bins=20, range=(0, 100), color='red', alpha=0.6, label='Species A')
    ax[1].hist(two_species_high, bins=20, range=(0, 100), color='green', alpha=0.6, label='Species B')
    ax[1].set_title('2 Species Remaining')
    ax[1].set_xlabel('Trait Value')
    ax[1].set_ylabel('Frequency')
    ax[1].set_xlim(0, 100)
    ax[1].legend()
    
    plt.tight_layout()
    plt.show()
    
    return all_survivors

def machine_learning(all_survivors):
    X = np.array(all_survivors).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X)
    centers = np.sort(kmeans.cluster_centers_.flatten())
    
    print("Results")
    print(f"Cluster 1 (Alpha) : {centers[0]:.1f}")
    print(f"Cluster 2 (Eat both) : {centers[1]:.1f}")
    print(f"Cluster 3 (Beta)  : {centers[2]:.1f}")

if __name__ == "__main__":
    all_survivors = analyze(trials=100, alpha_num=70, periodic_mode=False)
    machine_learning(all_survivors)
    
