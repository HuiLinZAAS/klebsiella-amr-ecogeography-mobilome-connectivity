#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将 AFR_矩阵表.csv 的矩阵转换为一行一行的配对形式（仅上三角，排除对角线）：
输出列为：strain_1, strain_2, shared_components, Source_1, Source_2, Pair_Type。

来源映射来自 AFR_sampled.csv 的列：strain, Source。
Pair_Type 分类：Human / NonHuman / Unknown，按 "<cat1>-<cat2>" 输出。

用法：
python AFR_matrix_to_pairs.py [matrix_csv] [sample_csv] [output_csv]
若不提供参数，默认：
- matrix_csv = ./AFR_矩阵表.csv
- sample_csv = ./AFR_sampled.csv
- output_csv = ./AFR_shared_components_pairs.csv
"""

from pathlib import Path
import sys
import pandas as pd


def to_category(src: str) -> str:
    if src is None:
        return "Unknown"
    val = str(src).strip().lower()
    if val == "human":
        return "Human"
    if val in ("", "unknown"):
        return "Unknown"
    return "NonHuman"


def main():
    # 解析参数
    cwd = Path(__file__).resolve().parent
    matrix_path = Path(sys.argv[1]) if len(sys.argv) > 1 else cwd / "AFR_矩阵表.csv"
    sample_path = Path(sys.argv[2]) if len(sys.argv) > 2 else cwd / "AFR_sampled.csv"
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else cwd / "AFR_shared_components_pairs.csv"

    if not matrix_path.exists():
        raise FileNotFoundError(f"找不到矩阵文件：{matrix_path}")
    if not sample_path.exists():
        raise FileNotFoundError(f"找不到来源文件：{sample_path}")

    # 读取矩阵：第一列为行名（strain），首行是列名（strain）
    matrix_df = pd.read_csv(matrix_path, index_col=0, encoding="utf-8-sig")
    # 转为数值型，缺失填0
    matrix_df = matrix_df.apply(pd.to_numeric, errors="coerce").fillna(0)

    # 读取来源映射
    meta_df = pd.read_csv(sample_path, encoding="utf-8-sig")
    cols = set(meta_df.columns.str.lower())
    if not {"strain", "source"}.issubset(cols):
        raise ValueError("来源文件缺少必要列：'strain' 或 'Source'")
    # 保持原大小写列名的兼容性
    strain_col = [c for c in meta_df.columns if c.lower() == "strain"][0]
    source_col = [c for c in meta_df.columns if c.lower() == "source"][0]
    source_map = meta_df.set_index(strain_col)[source_col].to_dict()

    # 确保列顺序与索引一致
    strains = list(matrix_df.index)
    matrix_df = matrix_df.reindex(index=strains, columns=strains)

    records = []
    n = len(strains)
    for i, s1 in enumerate(strains):
        for j in range(i + 1, n):  # 仅上三角，排除对角线
            s2 = strains[j]
            shared = matrix_df.at[s1, s2]
            # 输出 shared 为 int 或 float
            try:
                shared_out = int(shared) if float(shared).is_integer() else float(shared)
            except Exception:
                shared_out = float(shared)

            src1 = source_map.get(s1, "Unknown")
            src2 = source_map.get(s2, "Unknown")
            cat1 = to_category(src1)
            cat2 = to_category(src2)
            pair_type = f"{cat1}-{cat2}"

            records.append(
                {
                    "strain_1": s1,
                    "strain_2": s2,
                    "shared_components": shared_out,
                    "Source_1": src1 if src1 is not None else "Unknown",
                    "Source_2": src2 if src2 is not None else "Unknown",
                    "Pair_Type": pair_type,
                }
            )

    out_df = pd.DataFrame.from_records(records)
    out_df.to_csv(output_path, index=False, encoding="utf-8-sig")

    # 统计信息
    total_pairs = len(out_df)
    hh = (out_df["Pair_Type"] == "Human-Human").sum()
    nh_h = (out_df["Pair_Type"] == "NonHuman-Human").sum()
    h_nh = (out_df["Pair_Type"] == "Human-NonHuman").sum()
    nn = (out_df["Pair_Type"] == "NonHuman-NonHuman").sum()
    unk = out_df["Pair_Type"].str.contains("Unknown").sum()

    print(f"已生成：{output_path}")
    print(
        f"总配对数：{total_pairs}；Human-Human：{hh}；NonHuman-Human：{nh_h}；Human-NonHuman：{h_nh}；NonHuman-NonHuman：{nn}；含Unknown：{unk}"
    )


if __name__ == "__main__":
    main()