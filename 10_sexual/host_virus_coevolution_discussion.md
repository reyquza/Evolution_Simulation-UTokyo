# Sexual reproduction under evolving viral pressure

[Source](host_virus_coevolution.py) · [Week 10 report](sexual_reproduction_report.md)

## Model and assistance

I used generative AI to help develop the model, revise the code, and vectorize host–virus comparisons. The infection rule expresses a simple genotype-matching idea; it was not measured for a real virus.

There are 200 hosts, initially half sexual, with eight binary loci. Asexual offspring copy one parent. Sexual offspring inherit each locus from either of two sexual parents.

Mating success is weighted by $1-(1-s)^{10}$ when at least two sexual hosts exist, where $s$ is the sexual fraction. Rare sexual types have difficulty finding partners.

Viruses also have eight loci. Infection requires seven or more matches. Exact matching made infection too rare during exploratory modeling; a lower threshold made it too widespread. Seven is an assumed value.

Infection reduces host reproduction. Evolving viruses reproduce according to mean infection success plus baseline weight 0.01. Their mutation probability is 0.02 per locus; hosts mutate at 0.001.

## Experiment

The original report compared three conditions for 250 generations and 20 trials each:

1. No viruses.
2. Fixed viral genotypes.
3. Viruses evolving through differential reproduction and mutation.

![Archived host–virus experiment](host_virus_coevolution_results.png)

## Historical results

Final reported sexual frequencies were 0.194, 0.233, and 0.550. Asexual hosts increased in the first two conditions; sexual hosts increased with evolving viruses.

Resistance to static viruses could spread and persist. Evolving viruses instead tracked common genotypes, maintaining infection pressure. New recombinant host genotypes could temporarily escape, while diversity remained higher.

This is consistent with a Red Queen mechanism, not evidence that sex is always advantageous.

## Reproducibility and limitations

The archived image and values come from the original report; no seed was recorded. The publication version fixes an invalid argument in the trial runner and adds seed, trial-count, generation-count, and output controls. New results are distinct from the archived figure.

The model assumes binary matching, free recombination, and equal viral and host generation durations. It contains no explicit immunity or real viral infection mechanism.