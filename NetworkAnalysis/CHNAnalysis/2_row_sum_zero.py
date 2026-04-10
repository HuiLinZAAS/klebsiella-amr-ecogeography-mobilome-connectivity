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
        # 非数字或异常情况按0处理
        return 0.0


def extract_zero_sum_filenames(csv_path: str) -> list[str]:
    # 读取CSV，第一行是列头，第一列是行名（文件名）
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)

        try:
            header = next(reader)
        except StopIteration:
            return []

        # 跳过第一列列头（通常为空或描述），保留用于定位对角线的列名
        col_names = header[1:]
        # 列名到列索引（行中索引）的映射；行内索引从1开始对应第二列
        name_to_index = {}
        for idx, name in enumerate(col_names, start=1):
            # 若有重复列名，保留第一次出现的位置即可
            if name not in name_to_index:
                name_to_index[name] = idx

        zero_sum_files = []

        # 需要迭代的列数（不含第一列行名）
        expected_cols = len(col_names)

        for row in reader:
            if not row:
                continue
            row_name = row[0].strip() if len(row) > 0 else ""
            # 对齐行长度，防止索引越界
            if len(row) < expected_cols + 1:
                row = row + [""] * (expected_cols + 1 - len(row))

            # 对角线位置（行名在列头中的对应列）
            diag_idx = name_to_index.get(row_name, None)

            total = 0.0
            # 遍历除了第一列（行名）的所有列，排除对角线
            for i in range(1, expected_cols + 1):
                if diag_idx is not None and i == diag_idx:
                    continue
                total += parse_number(row[i])

            if total == 0.0:
                zero_sum_files.append(row_name)

        return zero_sum_files


def load_source_map(sample_csv_path: str) -> dict[str, str]:
    """读取sample文件，返回 {strain: source} 映射"""
    source_map: dict[str, str] = {}
    if not os.path.isfile(sample_csv_path):
        return source_map

    with open(sample_csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return source_map

        # 期望列：strain, Mash_cluster, Source
        # 找到列索引以提高健壮性
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
    # 参数1：矩阵CSV路径；参数2（可选）：sample文件路径（用于标注source）
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = os.path.join(os.path.dirname(__file__), "AFR_矩阵表.csv")

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
    out_name = f"{base_name}_孤岛菌.csv"
    out_path = os.path.join(os.path.dirname(csv_path), out_name)

    # 输出CSV：列为 strain, source, label（human/no-human）
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

    print(f"文件处理完成: {csv_path}")
    print(f"总和为零的行数: {len(zero_names)}")
    print(f"标注来源文件: {sample_csv_path}")
    print(f"human: {human_count}, no-human: {nohuman_count}, 未匹配source: {missing_source}")
    print(f"已输出CSV到: {out_path}")


if __name__ == "__main__":
    main()