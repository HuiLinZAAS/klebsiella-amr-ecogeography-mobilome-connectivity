Plasmid Replicon Network Analysis
Overview

This module profiles plasmid replicons across representative genomes and constructs similarity networks to evaluate source-specific sharing patterns while accounting for sampling bias.

Replicon Identification

Plasmid replicon sequences were identified using Abricate with the PlasmidFinder database (v4.7.2). For each genome, detected replicon types were extracted and used as features for downstream network analysis.

Network Construction

For each region, a plasmid replicon similarity network was constructed:

Nodes represent individual genomes
Edges indicate shared plasmid replicon types between genome pairs

This network captures potential plasmid-mediated connectivity across genomes from different sources.

Down-sampling Strategy

To mitigate source imbalance (e.g., over-representation of human isolates), we implemented a repeated random down-sampling approach:

Human genomes were randomly down-sampled to match the number of nonhuman genomes
The process was repeated 100 iterations to ensure robustness
Network Metrics

Across iterations, we summarized the following metrics:

Proportion of isolated nodes
Fraction of genomes with no shared replicons
Within- vs between-source connectivity
Fraction of edges linking genomes from the same vs different sources
Assortativity by source
Degree to which genomes preferentially connect to others from the same source
Visualization

For visualization purposes, equal-sized subsets were used:

Human: n = 100
Nonhuman: n = 100

These subsets provide a balanced view of plasmid sharing structure without bias from uneven sampling.

Reproducibility

All analyses are reproducible via scripts provided in this repository, including:

Replicon detection (Abricate wrapper)
Network construction
Down-sampling and iteration framework
Metric calculation and visualization
