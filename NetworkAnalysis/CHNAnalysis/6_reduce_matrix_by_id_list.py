import argparse
import os
import sys
from typing import List, Set

import pandas as pd


def load_ids_from_csv(csv_path: str, id_column: str | None = None) -> List[str]:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    if id_column is None:
        id_column = df.columns[0]
    ids = df[id_column].astype(str).str.strip().tolist()
    # 去重同时保持原始顺序
    seen = set()
    ordered_unique = []
    for x in ids:
        if x not in seen:
            seen.add(x)
            ordered_unique.append(x)
    return ordered_unique


def read_matrix(xlsx_path: str, sheet_name: str | int | None = 0) -> pd.DataFrame:
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    # 推断索引列：默认取第一列作为行名
    index_col = df.columns[0]
    df = df.set_index(index_col)
    return df


def reduce_matrix_by_ids(df: pd.DataFrame, ids: List[str]) -> pd.DataFrame:
    id_set: Set[str] = set(ids)
    # 与行索引和列名的交集
    rows_found = [i for i in ids if i in df.index]
    cols_found = [i for i in ids if i in df.columns]
    # 如果列名不是成套ID（例如首列是索引名），尝试用行索引作为列集合的参考
    # 通常矩阵是方阵，行索引与列名相同集合
    if len(cols_found) == 0:
        # 用行索引集合与ids做交集作为列集合
        shared_set = [i for i in ids if i in df.index]
        cols_found = shared_set

    # 最终选择两边都存在的ID，保证方阵一致性
    final_ids = [i for i in ids if (i in df.index and i in df.columns)]

    reduced = df.loc[final_ids, final_ids]
    return reduced


def main():
    parser = argparse.ArgumentParser(
        description="根据一个ID列表精减共享组件矩阵，仅保留列表中存在的行与列。",
    )
    parser.add_argument(
        "--id_csv",
        default=r"d:\trae开发的项目文件\网络图2\Table_5（非洲）equals_nonhuman.csv",
        help="包含ID列表的CSV路径，默认使用（非洲）equals_nonhuman.csv",
    )
    parser.add_argument(
        "--id_column",
        default=None,
        help="ID列名（缺省时使用CSV首列）",
    )
    parser.add_argument(
        "--matrix_xlsx",
        default=r"d:\trae开发的项目文件\网络图2\strain_shared_components_matrix.xlsx",
        help="共享组件矩阵Excel路径，默认使用当前目录的strain_shared_components_matrix.xlsx",
    )
    parser.add_argument(
        "--sheet_name",
        default=0,
        help="Excel工作表名或索引（默认0，第一张表）",
    )
    parser.add_argument(
        "--output",
        default=r"d:\trae开发的项目文件\网络图2\strain_shared_components_matrix_equals_nonhuman_精减.xlsx",
        help="输出精减后的矩阵Excel路径",
    )

    args = parser.parse_args()

    print("加载ID列表…")
    ids = load_ids_from_csv(args.id_csv, args.id_column)
    print(f"ID总数: {len(ids)}")

    print("读取矩阵…")
    df = read_matrix(args.matrix_xlsx, args.sheet_name)
    print(f"矩阵尺寸: {df.shape[0]} 行 x {df.shape[1]} 列")

    # 统计命中情况
    ids_in_rows = sum(1 for i in ids if i in df.index)
    ids_in_cols = sum(1 for i in ids if i in df.columns)
    print(f"与行索引匹配的ID: {ids_in_rows}")
    print(f"与列名匹配的ID: {ids_in_cols}")

    print("执行精减…")
    reduced = reduce_matrix_by_ids(df, ids)
    print(f"精减后矩阵尺寸: {reduced.shape[0]} 行 x {reduced.shape[1]} 列")

    # 保留原始首列名作为index_label
    index_label = df.index.name if df.index.name else df.columns[0]
    # 写出到Excel
    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"写出结果到: {args.output}")
    reduced.to_excel(args.output, index_label=index_label)
    print("完成。")


if __name__ == "__main__":
    # 避免在极大Excel上默认显示过长的repr
    pd.options.display.max_rows = 20
    pd.options.display.max_columns = 20
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)