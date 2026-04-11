#!/bin/bash

### Prompt user to input genus or species name
read -p "Enter genus or species name (e.g., 'Salmonella' or 'Escherichia coli'): " targetname_raw

### Check if input is empty
if [ -z "$targetname_raw" ]; then
    echo "Error: Input genus or species name cannot be empty."
    exit 1
fi

### Replace spaces with underscores
targetname=$(echo "$targetname_raw" | tr ' ' '_')

# Check if directory already exists
if [ -d "$targetname" ]; then
    echo "Directory $targetname already exists. Please remove or rename it before running the script."
    exit 1
fi

# Create working directory
mkdir "$targetname"
ln -s $(realpath assembly_summary_genbank.txt) "$targetname/assembly_summary_genbank.txt"
cd "$targetname"

### Initialize metadata file
> "${targetname}_assembly_summary_genbank.txt"

### Extract metadata for target genus/species
# Copy header
sed -n '2p' assembly_summary_genbank.txt > "${targetname}_assembly_summary_genbank.txt"

# Filter rows based on conditions:
# Column 8: organism_name
# Column 23: asm_not_live_date
# Column 25: group
# Column 3: biosample
# Column 20: ftp_path
grep -E "$targetname_raw" assembly_summary_genbank.txt | \
awk -F'\t' -v target="$targetname_raw" \
'$8 ~ target && $25 == "bacteria" && $23 == "na" && $3 != "na" && $20 != "na" {print}' \
>> "${targetname}_assembly_summary_genbank.txt"

echo "${targetname}_assembly_summary_genbank.txt completed at $(date)"

### Count metadata rows (excluding header)
metadata_row_count=$(wc -l < "${targetname}_assembly_summary_genbank.txt")
metadata_row_count=$((metadata_row_count - 1))
echo "${targetname}_assembly_summary_genbank.txt contains ${metadata_row_count} records (excluding header)"

### Check for one-to-many biosample relationships
input_file="${targetname}_assembly_summary_genbank.txt"

duplicates=$(awk -F'\t' '{print $3}' "$input_file" | sort | uniq -d)
duplicates_count=$(echo "$duplicates" | wc -l)

if [ -z "$duplicates" ]; then
    echo "Each biosample corresponds to a unique assembly_accession (no one-to-many relationships found)."
else
    comma_separated_duplicates=$(echo "$duplicates" | tr '\n' ',' | sed 's/,$//')
    echo "One-to-many biosample relationships detected."
    echo "Number of affected biosamples: $duplicates_count"
    echo "Biosamples: $comma_separated_duplicates"

    sed -n '2p' "assembly_summary_genbank.txt" > "repeated_biosample.txt"

    pipe_separated_duplicates=$(echo "$comma_separated_duplicates" | tr ',' '|')
    grep -E "$pipe_separated_duplicates" "$input_file" | sort -k3,3 >> "repeated_biosample.txt"

    echo "Repeated biosample entries saved to repeated_biosample.txt"

    ### Run Python filtering script
    python ../filter_script.py && \
    echo "filter_script.py completed. Filtered results saved in filtered_biosample.txt"

    ### Merge filtered results
    comma_separated_repeat_biosample_gca=$(tail -n +2 filtered_biosample.txt | awk -F'\t' '{print $1}' | tr '\n' ',' | sed 's/,$//')
    pipe_separated_repeat_biosample_gca=$(echo "$comma_separated_repeat_biosample_gca" | tr ',' '|')

    sed -n '1p' "repeated_biosample.txt" > retain_repeat_biosample_gca.txt
    grep -E "$pipe_separated_repeat_biosample_gca" "repeated_biosample.txt" >> retain_repeat_biosample_gca.txt

    pipe_separated_repeat_biosample_gca_v2=$(tail -n +2 "repeated_biosample.txt" | awk -F'\t' '{print $1}' | tr '\n' ',' | sed 's/,$//' | tr ',' '|')

    grep -vE "$pipe_separated_repeat_biosample_gca_v2" "${targetname}_assembly_summary_genbank.txt" > "filter_${targetname}_assembly_summary_genbank.txt"

    tail -n +2 retain_repeat_biosample_gca.txt >> "filter_${targetname}_assembly_summary_genbank.txt"

    ### Rename files
    mv "${targetname}_assembly_summary_genbank.txt" "raw_${targetname}_assembly_summary_genbank.txt"
    mv "filter_${targetname}_assembly_summary_genbank.txt" "${targetname}_assembly_summary_genbank.txt"

    echo "Filtering completed. Raw and filtered metadata files updated."
fi

### Generate genome download URLs
awk -F'\t' '{print $20}' "$input_file" > lie20.txt && \
paste -d '/' lie20.txt <(awk -F'/' '{print $NF"_genomic.fna.gz"}' lie20.txt) > download_http.txt && \
rm lie20.txt && \
sed -i '1d' download_http.txt

### Activate conda environment
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Please install Anaconda/Miniconda."
    exit 1
fi

if ! conda env list | grep -q "^parallel"; then
    echo "Error: conda environment 'parallel' not found."
    exit 1
fi

conda_env_base_path=$(conda info --envs | grep '^base' | awk '{print $NF}')

if [ -f "${conda_env_base_path}/etc/profile.d/conda.sh" ]; then
    . "${conda_env_base_path}/etc/profile.d/conda.sh"
else
    echo "Error loading conda environment."
    exit 1
fi

conda activate parallel

### Parallel download
genomes_gz_file="${targetname}_genomes_gz_file"
genomes_fna_file="${targetname}_genomes_fna_file"

mkdir "$genomes_gz_file" "$genomes_fna_file"
cd "$genomes_gz_file"

file_lines=$(wc -l < ../download_http.txt)

echo "Starting download of $file_lines genomes..."
echo "Estimated time: $((file_lines / 300)) to $((file_lines / 200)) minutes."

nohup cat ../download_http.txt | parallel --gnu 'wget {}' > ../"download_${targetname}_genomes_nohup.out" 2>&1 &
wait

completed_count=$(grep -c '100%' "../download_${targetname}_genomes_nohup.out")

file_lines=$(echo "$file_lines" | tr -d '[:space:]')
completed_count=$(echo "$completed_count" | tr -d '[:space:]')

if [ "$file_lines" -eq "$completed_count" ]; then
    echo "Download completed successfully."
else
    echo "Download incomplete. Some files may have failed."
fi