\# Klebsiella pneumoniae Global Genome Workflow



A reproducible bioinformatics workflow for downloading, filtering, quality-controlling, and typing \*Klebsiella pneumoniae\* genomes from NCBI Assembly database.



This pipeline supports large-scale comparative genomics and population structure analysis under a One Health framework.



\---



\##  Overview



This workflow includes the following steps:



1\. Genome metadata retrieval from NCBI Assembly database

2\. Filtering of high-quality bacterial genomes

3\. Removal of problematic biosample redundancies

4\. Genome download using parallelized wget

5\. Contig filtering (removal of short and guided contigs)

6\. Genome size filtering

7\. Genome quality control (QC) using seqkit

8\. MLST-based population typing



\---





