import csv
import os
import sys


def parse_number(cell: str) -> float:
    if cell is None:
        return 0.0
    s = cell.strip()
    if s == "":
        return 0.0
    try:
        return float(s)
    except ValueError:
               return 0.0


def extract_zero_sum_filenames(csv_path: str) -> list[str]:
 
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        try:
            header = next(reader)
        except StopIteration:
            return []

        
        col_names = header[1:]
        
        name_to_index = {}
        for idx, name in enumerate(col_names, start=1):
            
            if name not in name_to_index:
                name_to_index[name] = idx

        zero_sum_files = []

        
        expected_cols = len(col_names)

        for row in reader:
            if not row:
                continue
            row_name = row[0].strip() if len(row) > 0 else ""
            
            if len(row) < expected_cols + 1:
                row = row + [""] * (expected_cols + 1 - len(row))

           
            diag_idx = name_to_index.get(row_name, None)

            total = 0.0
            
            for i in range(1, expected_cols + 1):
                if diag_idx is not None and i == diag_idx:
                    continue
                total += parse_number(row[i])

            if total == 0.0:
                zero_sum_files.append(row_name)

        return zero_sum_files


def load_source_map(sample_csv_path: str) -> dict[str, str]:
    """"""
    source_map: dict[str, str] = {}
    if not os.path.isfile(sample_csv_path):
        return source_map

    with open(sample_csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return source_map

               header_lower = [h.strip().lower() for h in header]
        try:
            strain_idx = header_lower.index("strain")
        except ValueError:
            strain_idx = 0
        try:
            source_idx = header_lower.index("source")
        except ValueError:
            source_idx = 2

        for row in reader:
            if not row:
                continue
            if len(row) <= max(strain_idx, source_idx):
                continue
            strain = row[strain_idx].strip()
            source = row[source_idx].strip()
            if strain:
                source_map[strain] = source
    return source_map


def main():

    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = os.path.join(os.path.dirname(__file__), "AFR_Matrix.csv")

    if len(sys.argv) > 2:
        sample_csv_path = sys.argv[2]
    else:
        sample_csv_path = os.path.join(os.path.dirname(csv_path), "AFR_sampled.csv")

    if not os.path.isfile(csv_path):
        print(f"找不到CSV文件: {csv_path}")
        sys.exit(1)

    zero_names = extract_zero_sum_filenames(csv_path)
    source_map = load_source_map(sample_csv_path)

    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    out_name = f"{base_name}_IsolatedBacteria.csv"
    out_path = os.path.join(os.path.dirname(csv_path), out_name)

    
    human_count = 0
    nohuman_count = 0
    missing_source = 0
    with open(out_path, "w", encoding="utf-8", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["strain", "source", "label"])
        for name in zero_names:
            src = source_map.get(name, "Unknown")
            label = "human" if src.strip().lower() == "human" else "no-human"
            if src == "Unknown":
                missing_source += 1
            if label == "human":
                human_count += 1
            else:
                nohuman_count += 1
            writer.writerow([name, src, label])

    print(f": {csv_path}")
    print(f": {len(zero_names)}")
    print(f": {sample_csv_path}")
    print(f"human: {human_count}, no-human: {nohuman_count}, Nosource: {missing_source}")
    print(f": {out_path}")


if __name__ == "__main__":
    main()