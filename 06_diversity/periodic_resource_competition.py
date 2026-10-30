import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Optional periodic resource availability
def run_simulation(Psize=101, max_gen=1000, alpha_num=50, optional_mode=False, periodic_mode=False):
    population = list(range(0, Psize))
    
    # Track generations to switch resource allocation
    for gen in range(max_gen):
        
        # Alternate 80:21 and 20:81 resource slots every 100 generations
        if periodic_mode:
            if (gen // 100) % 2 == 0:
                current_alpha = 80
            else:
                current_alpha = 20
            current_beta = Psize - current_alpha
        else:
            # Constant resource allocation
            current_alpha = alpha_num
            current_beta = Psize - alpha_num
            
        next_pop = []
        
        # Use the current allocation for resource a
        num = 0
        while num < current_alpha:  
            target_index = random.randint(0, len(population) - 1)
            val = population[target_index]
            threshold = (val ** 2) / 100 if optional_mode else val
            
            if threshold < random.randint(0, 100): 
                next_pop.append(val) 
                num += 1
                
        # Use the current allocation for resource b
        num = 0
        while num < current_beta: 
            target_index = random.randint(0, len(population) - 1) 
            val = population[target_index]
            threshold = ((100 - val) ** 2) / 100 if optional_mode else 100 - val
            
            if threshold < random.randint(0, 100):
                next_pop.append(val)
                num += 1
                
        population = next_pop
        
        if len(population) > Psize:
            population = random.sample(population, Psize)
            
    return list(set(population))


# Optional periodic resource availability
def analyze(trials=100, alpha_num=50, optional_mode=False, periodic_mode=False):
    all_survivors = []
    single_species = []
    two_species_low = []
    two_species_high = []
    
    for _ in range(trials):
        # Pass the selected resource regime into each trial
        result = run_simulation(alpha_num=alpha_num, optional_mode=optional_mode, periodic_mode=periodic_mode)
        all_survivors.extend(result)
        
        if len(result) == 1:
            single_species.append(result[0])
        elif len(result) == 2:
            result.sort()
            two_species_low.append(result[0])
            two_species_high.append(result[1])

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
    # Run the linear model with periodic resource availability
    all_survivors = analyze(trials=100, alpha_num=50, optional_mode=False, periodic_mode=True)
    machine_learning(all_survivors)
