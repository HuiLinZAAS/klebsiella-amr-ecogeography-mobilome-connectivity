#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
根据 AFR_矩阵表_孤岛菌.csv 的第一列（strain），删除 AFR_shared_components_pairs.csv 中
第一列（strain_1）为这些 strain 的所有行，生成新的过滤后的配对文件。

用法：
python filter_pairs_by_zero.py [zero_csv] [pairs_csv] [output_csv]
默认：
- zero_csv = ./AFR_矩阵表_孤岛菌.csv
- pairs_csv = ./AFR_shared_components_pairs.csv
- output_csv = ./AFR_shared_components_pairs_过滤后.csv
"""

from pathlib import Path
import sys
import pandas as pd


def main():
    cwd = Path(__file__).resolve().parent
    zero_path = Path(sys.argv[1]) if len(sys.argv) > 1 else cwd / "AFR_矩阵表_孤岛菌.csv"
    pairs_path = Path(sys.argv[2]) if len(sys.argv) > 2 else cwd / "AFR_shared_components_pairs.csv"
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else cwd / "AFR_过滤孤岛菌后.csv"

    if not zero_path.exists():
        raise FileNotFoundError(f"找不到零行列表文件：{zero_path}")
    if not pairs_path.exists():
        raise FileNotFoundError(f"找不到配对文件：{pairs_path}")

    # 读取零行列表，获取要排除的 strain 集合
    zero_df = pd.read_csv(zero_path, encoding="utf-8-sig")
    cols = {c.lower() for c in zero_df.columns}
    if "strain" not in cols:
        raise ValueError("零行列表缺少必要列：'strain'")
    strain_col = [c for c in zero_df.columns if c.lower() == "strain"][0]
    exclude_set = set(zero_df[strain_col].dropna().astype(str).str.strip())

    # 读取配对文件并过滤
    pairs_df = pd.read_csv(pairs_path, encoding="utf-8-sig")
    if "strain_1" not in pairs_df.columns:
        raise ValueError("配对文件缺少必要列：'strain_1'")

    before_count = len(pairs_df)
    filtered_df = pairs_df[~pairs_df["strain_1"].astype(str).str.strip().isin(exclude_set)].copy()
    after_count = len(filtered_df)
    removed_count = before_count - after_count

    filtered_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"已生成过滤后的文件：{output_path}")
    print(f"原始行数：{before_count}；移除行数：{removed_count}；保留行数：{after_count}")


if __name__ == "__main__":
    main()