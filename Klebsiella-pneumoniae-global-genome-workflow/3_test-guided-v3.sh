#!/bin/bash

# Define input directory (modify if needed)
# read -p "Enter the directory containing .fasta files (e.g., 'Helicobacter_pylori_genomes_fna_file'): " genomes_fna_file
genomes_fna_file="Klebsiella_pneumoniae_genomes_fna_file"

# Count number of fasta files
genomes_fna_file_count=$(find "$genomes_fna_file" -maxdepth 1 -type f -name '*.fasta' | wc -l)
echo "Directory $genomes_fna_file contains $genomes_fna_file_count FASTA files"

# Search for files containing 'guided' in contig names
echo "Checking for contigs containing the keyword 'guided' in $genomes_fna_file..."
files_with_guided=$(find "$genomes_fna_file" -type f -exec grep -l 'guided' {} +)

# If no such files found
if [ -z "$files_with_guided" ]; then
    echo "No contigs containing 'guided' were found in $genomes_fna_file"
else
    echo "Files containing contigs with 'guided':"
    echo "$files_with_guided"

    files_with_guided_count=$(echo "$files_with_guided" | wc -l)
    echo "Total files with 'guided' contigs: $files_with_guided_count"

    # Define processing function
    process_file() {
        local file="$1"
        local genomes_fna_file="$2"

        filename=$(basename "$file")

        # Create required directories
        mkdir -p "${genomes_fna_file}_guided_temp"
        mkdir -p "${genomes_fna_file}_only_guided"
        mkdir -p "${genomes_fna_file}_deleted_guided"
        mkdir -p "${genomes_fna_file}_contain_guided"

        # Extract contig names
        seqkit seq -n "$file" | grep 'guided' > "${genomes_fna_file}_guided_temp/${filename}_guided_contigs.txt"
        seqkit seq -n "$file" | grep -v 'guided' > "${genomes_fna_file}_guided_temp/${filename}_non_guided_contigs.txt"

        # Extract sequences
        seqkit grep -w 80 -n -f "${genomes_fna_file}_guided_temp/${filename}_guided_contigs.txt" "$file" > "${genomes_fna_file}_only_guided/$filename"
        seqkit grep -w 80 -n -f "${genomes_fna_file}_guided_temp/${filename}_non_guided_contigs.txt" "$file" > "${genomes_fna_file}_deleted_guided/$filename"

        # Move original file and replace with filtered version
        mv "$file" "${genomes_fna_file}_contain_guided"
        cp "${genomes_fna_file}_deleted_guided/$filename" "$genomes_fna_file"

        echo "Processed: $file"
    }

    # Export function for GNU parallel
    export -f process_file

    # Run in parallel
    echo "$files_with_guided" | parallel -j+0 process_file {} "$genomes_fna_file"
fi