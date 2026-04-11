import csv
import os
import random


def sample_afr(input_path: str, output_path: str, human_n: int = 100, nonhuman_n: int = 100, seed: int = 42) -> None:
    random.seed(seed)

    # Read rows
    with open(input_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or ["strain", "Mash_cluster", "Source"]
        rows = list(reader)

    # Split into human and non-human
    human_rows = [r for r in rows if (r.get("Source") or "").strip() == "Human"]
    nonhuman_rows = [r for r in rows if (r.get("Source") or "").strip() != "Human"]

    # Determine sample sizes
    take_human = min(human_n, len(human_rows))
    take_nonhuman = min(nonhuman_n, len(nonhuman_rows))

    if take_human == 0:
        raise ValueError("No 'Human' rows found in Source column.")
    if take_nonhuman == 0:
        raise ValueError("No non-human rows found in Source column.")

    # Sample without replacement
    human_sample = random.sample(human_rows, take_human)
    nonhuman_sample = random.sample(nonhuman_rows, take_nonhuman)
    sampled_rows = human_sample + nonhuman_sample

    # Write output
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sampled_rows)

    print(
        f"Wrote {len(sampled_rows)} rows to {output_path} (Human={take_human}, NonHuman={take_nonhuman})."
    )


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__) or "."
    input_csv = os.path.join(base_dir, "AFR.csv")
    output_csv = os.path.join(base_dir, "AFR_sampled.csv")
    sample_afr(input_csv, output_csv)