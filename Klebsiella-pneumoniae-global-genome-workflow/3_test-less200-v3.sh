#!/bin/bash

# Prompt for input directory containing FASTA files
read -p "Enter FASTA directory name (e.g., 'Helicobacter_pylori_genomes_fna_file'): " genomes_fna_file

# Create output directories
mkdir -p "${genomes_fna_file}_less200"
mkdir -p "${genomes_fna_file}_more200"

# Define processing function
process_file() {
    local file="$1"
    local genomes_fna_file="$2"

    base_name=$(basename "$file" .fasta)

    # Extract contigs shorter than 200 bp
    seqkit seq -w 80 -m 1 -M 199 "$file" \
        -o "${genomes_fna_file}_less200/less200_${base_name}.fasta"

    # Extract contigs ≥ 200 bp
    seqkit seq -w 80 -m 200 "$file" \
        -o "${genomes_fna_file}_more200/${base_name}.fasta"
}

# Export function for GNU parallel
export -f process_file

# Run processing in parallel
find "$genomes_fna_file" -maxdepth 1 -type f -name '*.fasta' \
| parallel -j+0 process_file {} "$genomes_fna_file"

# Remove empty files (if any)
find "${genomes_fna_file}_less200" -type f -size 0 -delete