import matplotlib.pyplot as plt
import random
import numpy as np


Psize = 200                 # Host population size
VirusPsize = 80            # Virus population size
Allele = 8                 # Binary loci in both hosts and viruses
generations = 250          # Generations per simulation
trials = 20                # Replicates per condition

InitialSexualRate = 0.5    # Initial sexual fraction
HostMutationRate = 0.001   # Host mutation probability per locus
VirusMutationRate = 0.02   # Virus mutation probability per locus
InfectionMatch = 7         # Infection requires at least seven of eight matching loci
InfectionCost = 0.95       # Strength of the infection-associated reduction in host fitness
MateSearchTrials = 10      # Number of possible mate-search encounters


def mutation(genotypes, mutationRate):
    """Flip each binary locus with probability mutationRate."""
    for i in range(len(genotypes)):
        for j in range(Allele):
            if random.random() < mutationRate:
                genotypes[i][j] = 1 - genotypes[i][j]
    return genotypes


def infection_check(hostGenotypes, virusGenotypes):
    """Check whether host and virus genotypes meet the matching threshold."""
    # Rows are hosts, columns are viruses; count matching loci by broadcasting
    sameAllele = np.sum(
        hostGenotypes[:, np.newaxis, :] == virusGenotypes[np.newaxis, :, :],
        axis=2
    )
    """
    AI helped vectorize the following conceptual triple loop using NumPy broadcasting.
    for i in range(Psize):
        for j in range(VirusPsize):
            sameAllele = 0
            for k in range(Allele):
                if hostGenotypes[i][k] == virusGenotypes[j][k]:
                    sameAllele += 1
    """
    """ 
    infectionMatrix[i][j] indicates whether virus j can infect host i (200 by 80 by default).
    """
    infectionMatrix = (sameAllele >= InfectionMatch).astype(int)
    return infectionMatrix


def genotype_diversity(hostGenotypes):
    """Return the number of distinct genotypes normalized by the attainable maximum."""
    genotypeNumber = len(np.unique(hostGenotypes, axis=0))
    maximumNumber = min(Psize, 2**Allele)
    return genotypeNumber / maximumNumber


def run_simulation(condition="evolving", seed=None):
    """Run one host-virus simulation.

    Conditions: none (no viruses), static (fixed viral genotypes),
    or evolving (selection and mutation in viruses).
    """

    if condition not in {"none", "static", "evolving"}:
        raise ValueError("condition must be none, static, or evolving")
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Zero denotes asexual hosts; one denotes sexual hosts
    populationType = [0 for _ in range(Psize)]
    for i in range(int(Psize * InitialSexualRate)):
        populationType[i] = 1
    random.shuffle(populationType)

    # Initialize both reproductive types from the same allele distribution
    hostGenotypes = np.random.choice([0, 1], size=(Psize, Allele))

    # All viruses start with the same genotype
    virusGenotypes = np.zeros((VirusPsize, Allele), dtype=int)

    senniSexualRate = []
    senniInfection = []
    senniDiversity = []

    for _ in range(generations):
        infectionMatrix = infection_check(hostGenotypes, virusGenotypes)
        infectionRate = np.mean(infectionMatrix, axis=1)

        if condition == "none":
            fitness = [1.0 for _ in range(Psize)]
            averageInfection = 0
        else:
            fitness = [max(0.01, 1 - InfectionCost * x) for x in infectionRate]
            averageInfection = np.mean(infectionRate)

        sexualNumber = sum(populationType)
        sexualRate = sexualNumber / Psize

        # The chance of encountering a sexual host is the sexual fraction
        # Subtract the probability that all mate-search encounters fail
        if sexualNumber >= 2:
            mateFindProbability = 1 - (1 - sexualRate) ** MateSearchTrials
        else:
            mateFindProbability = 0

        # Sexual hosts reproduce only when a mate can be found
        reproductiveWeight = list(fitness)
        for i in range(Psize):
            if populationType[i] == 1:
                reproductiveWeight[i] *= mateFindProbability

        # Choose parents in proportion to fitness and mate availability
        parentList = random.choices(
            range(Psize), weights=reproductiveWeight, k=Psize
        )
        nextPopulationType = []
        nextHostGenotypes = []

        sexualIndex = [i for i in range(Psize) if populationType[i] == 1]
        for parent1 in parentList:
            if populationType[parent1] == 0 or len(sexualIndex) < 2:
                # Asexual offspring copy their parent
                nextPopulationType.append(0)
                nextHostGenotypes.append(list(hostGenotypes[parent1]))
            else:
                # Sexual offspring use another sexual host as their second parent
                availableMate = [i for i in sexualIndex if i != parent1]
                parent2 = random.choice(availableMate)
                childGenotype = []
                for j in range(Allele):
                    if random.randint(0, 1) == 0:
                        childGenotype.append(hostGenotypes[parent1][j])
                    else:
                        childGenotype.append(hostGenotypes[parent2][j])
                nextPopulationType.append(1)
                nextHostGenotypes.append(childGenotype)

        populationType = nextPopulationType
        hostGenotypes = np.array(nextHostGenotypes)
        hostGenotypes = mutation(hostGenotypes, HostMutationRate)

        if condition == "evolving":
            virusFitness = list(np.mean(infectionMatrix, axis=0) + 0.01)
            """
            Average over hosts to obtain each viral genotype's infection success.
            The baseline 0.01 allows viruses with no matches to reproduce.
            """
            virusParent = random.choices(
                range(VirusPsize), weights=virusFitness, k=VirusPsize
            )
            nextVirusGenotypes = []
            for parent in virusParent:
                nextVirusGenotypes.append(list(virusGenotypes[parent]))
            virusGenotypes = np.array(nextVirusGenotypes)
            virusGenotypes = mutation(virusGenotypes, VirusMutationRate)

        senniSexualRate.append(sexualRate)
        senniInfection.append(averageInfection)
        senniDiversity.append(genotype_diversity(hostGenotypes))

    return senniSexualRate, senniInfection, senniDiversity


def run_trials(condition, seed=None):
    """Repeat the condition and return mean trajectories and final frequencies."""
    sexualAll = []
    infectionAll = []
    diversityAll = []

    for trial in range(trials):
        sexual, infection, diversity = run_simulation(
            condition, seed=None if seed is None else seed + trial
        )
        sexualAll.append(sexual)
        infectionAll.append(infection)
        diversityAll.append(diversity)

    return (
        np.mean(sexualAll, axis=0),
        np.mean(infectionAll, axis=0),
        np.mean(diversityAll, axis=0),
        np.array(sexualAll)[:, -1],
    )


def main():
    """Run the comparison without overwriting the archived report figure."""
    import argparse
    import json
    from pathlib import Path

    global trials, generations
    parser = argparse.ArgumentParser(description="Compare host reproduction under viral coevolution.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--generations", type=int, default=250)
    parser.add_argument("--output", default="generated/red_queen_result.png")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    if args.trials < 1 or args.generations < 1:
        parser.error("trials and generations must be positive")
    if args.seed < 0 or args.seed + 3 * args.trials - 1 > 2**32 - 1:
        parser.error("seed and trial count must fit the NumPy seed range")
    trials, generations = args.trials, args.generations

    conditions = [
        ("none", "No virus", "gray"),
        ("static", "Static virus", "blue"),
        ("evolving", "Evolving virus", "red"),
    ]

    results = {}
    print("Running simulations...")
    for index, (condition, label, color) in enumerate(conditions):
        results[condition] = run_trials(condition, seed=args.seed + index * trials)
        finalSexualRate = np.mean(results[condition][3])
        print(label, "final sexual frequency =", round(finalSexualRate, 3))


    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.6))
    for condition, label, color in conditions:
        sexual, infection, diversity, finalSexual = results[condition]
        ax1.plot(sexual, label=label, color=color)
        ax2.plot(infection, label=label, color=color)
        ax3.plot(diversity, label=label, color=color)

    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Frequency of sexual hosts")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Mean infection rate")
    ax3.set_xlabel("Generation")
    ax3.set_ylabel("Proportion of different host genotypes")

    for ax in (ax1, ax2, ax3):
        ax.grid(alpha=0.3)
        ax.legend()

    plt.suptitle("Sexual reproduction under host-virus coevolution")
    plt.tight_layout()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=200)
    metadata = {
        "seed": args.seed, "trials": trials, "generations": generations,
        "host_population": Psize, "virus_population": VirusPsize, "loci": Allele,
        "host_mutation_rate": HostMutationRate, "virus_mutation_rate": VirusMutationRate,
        "infection_match": InfectionMatch, "infection_cost": InfectionCost,
        "initial_sexual_rate": InitialSexualRate, "mate_search_trials": MateSearchTrials,
        "final_sexual_frequencies": {key: value[3].tolist() for key, value in results.items()},
    }
    output.with_suffix(".json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Saved plot to {output}")
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
