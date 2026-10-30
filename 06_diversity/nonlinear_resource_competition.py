import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def run_simulation(Psize=101, max_gen=1000, alpha_num=50, optional_mode=False):
    population = list(range(0, Psize))
    beta_num = Psize - alpha_num
    for _ in range(max_gen):
        next_pop = []
        
        num = 0
        while num < alpha_num:  
            target_index = random.randint(0, len(population) - 1)
            val = population[target_index]
            threshold = (val ** 2) / 100 if optional_mode else val
            
            if threshold < random.randint(0, 100): 
                next_pop.append(val) 
                num += 1
                
        num = 0
        while num < beta_num: 
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


def calculate_alpha(x1, x2, optional_mode=False):
    """
    Compute competition coefficients from trait-dependent resource-use overlap.
    """
    if optional_mode:
        # Resource-acquisition probabilities under nonlinear preferences
        u_a1 = 1 - (x1 ** 2) / 10000
        u_b1 = 1 - ((100 - x1) ** 2) / 10000
        u_a2 = 1 - (x2 ** 2) / 10000
        u_b2 = 1 - ((100 - x2) ** 2) / 10000
    else:
        # Resource-acquisition probabilities under linear preferences
        u_a1 = (100 - x1) / 100
        u_b1 = x1 / 100
        u_a2 = (100 - x2) / 100
        u_b2 = x2 / 100
        
    # Numerator: overlap in resource use
    numerator = u_a1 * u_a2 + u_b1 * u_b2
    
    # Denominators: within-type resource-use overlap
    denom1 = u_a1**2 + u_b1**2
    denom2 = u_a2**2 + u_b2**2
    
    # Compute competition coefficients with zero-denominator guards
    alpha_12 = numerator / denom1 if denom1 > 0 else 0
    alpha_21 = numerator / denom2 if denom2 > 0 else 0
    
    return alpha_12, alpha_21


def analyze(trials=100, alpha_num=50, optional_mode=False):
    all_survivors = []
    single_species = []
    two_species_low = []
    two_species_high = []
    
    # Initialize counters
    two_species_count = 0      # Number of trials with two surviving types
    alpha_over_1_count = 0     # Number of two-type trials with a coefficient above one
    
    for _ in range(trials):
        # Use keyword arguments to avoid positional mismatches
        result = run_simulation(alpha_num=alpha_num, optional_mode=optional_mode)
        all_survivors.extend(result)
        
        if len(result) == 1:
            single_species.append(result[0])
        elif len(result) == 2:
            two_species_count += 1
            result.sort()
            two_species_low.append(result[0])
            two_species_high.append(result[1])
            
            # Compute coefficients for the two surviving types
            x1, x2 = result[0], result[1]
            a12, a21 = calculate_alpha(x1, x2, optional_mode=optional_mode)
            
            # Count a trial if either coefficient exceeds one
            if a12 > 1 or a21 > 1:
                alpha_over_1_count += 1

    # Print the comparison results
    print("\n" + "="*50)
    print(f" Competition-coefficient comparison (optional_mode={optional_mode})")
    print("="*50)
    print(f"Total trials: {trials}")
    print(f"Trials with two surviving types: {two_species_count}")
    print(f"Trials with alpha above one: {alpha_over_1_count}")
    if two_species_count > 0:
        pct = (alpha_over_1_count / two_species_count) * 100
        print(f"Percentage with alpha > 1 among two-type trials: {pct:.1f} %")
    else:
        print("No two-type outcomes; percentage is undefined.")
    print("="*50 + "\n")

    # Plot survivor distributions
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
    if len(all_survivors) < 3:
        print("Skipping clustering: insufficient data.")
        return
    X = np.array(all_survivors).reshape(-1, 1)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X)
    centers = np.sort(kmeans.cluster_centers_.flatten())
    
    print("Results")
    print(f"Cluster 1 (Alpha) : {centers[0]:.1f}")
    print(f"Cluster 2 (Eat both) : {centers[1]:.1f}")
    print(f"Cluster 3 (Beta)  : {centers[2]:.1f}")

if __name__ == "__main__":
    # Run the linear preference model
    all_survivors = analyze(trials=100, alpha_num=50, optional_mode=False)
    machine_learning(all_survivors)
