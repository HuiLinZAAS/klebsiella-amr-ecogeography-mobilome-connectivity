import csv
import argparse
from typing import Set, Dict, List


def load_strain_set(csv_path: str) -> Set[str]:
    strains: Set[str] = set()
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        if not fieldnames:
            return strains
        first_col = fieldnames[0]
        for row in reader:
            s = (row.get(first_col) or '').strip()
            if s:
                strains.add(s)
    return strains


def read_pairs_rows(pairs_csv_path: str) -> tuple[List[Dict[str, str]], List[str]]:
    rows: List[Dict[str, str]] = []
    with open(pairs_csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        for row in reader:
            rows.append(row)
    return rows, header


def match_row(row: Dict[str, str], strain_set: Set[str], mode: str = 'either') -> bool:
    s1 = (row.get('strain_1') or '').strip()
    s2 = (row.get('strain_2') or '').strip()
    if mode == 'strain_1':
        return s1 in strain_set
    if mode == 'strain_2':
        return s2 in strain_set
    if mode == 'both':
        return s1 in strain_set and s2 in strain_set
    # default 'either'
    return (s1 in strain_set) or (s2 in strain_set)


def write_subset(out_path: str, header: List[str], rows: List[Dict[str, str]]) -> int:
    with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for r in rows:
            writer.writerow({h: r.get(h, '') for h in header})
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description='根据三份菌名列表分割AFR_shared_components_pairs.csv，列数保持不变')
    parser.add_argument('--pairs', default=r'd:\trae开发的项目文件\网络图2\AFR_shared_components_pairs.csv', help='输入pairs CSV')
    parser.add_argument('--cross', default=r'd:\trae开发的项目文件\网络图2\AFR_交叉菌_strains.csv', help='交叉菌 strains 列表（取首列）')
    parser.add_argument('--island', default=r'd:\trae开发的项目文件\网络图2\AFR_矩阵表_孤岛菌.csv', help='孤岛菌 strains 列表（取首列）')
    parser.add_argument('--inline', default=r'd:\trae开发的项目文件\网络图2\AFR_sampled_内联菌.csv', help='内联菌 strains 列表（取首列）')
    parser.add_argument('--out_cross', default=r'd:\trae开发的项目文件\网络图2\AFR_shared_components_pairs_分割_交叉菌.csv', help='输出交叉菌子集')
    parser.add_argument('--out_island', default=r'd:\trae开发的项目文件\网络图2\AFR_shared_components_pairs_分割_孤岛菌.csv', help='输出孤岛菌子集')
    parser.add_argument('--out_inline', default=r'd:\trae开发的项目文件\网络图2\AFR_shared_components_pairs_分割_内联菌.csv', help='输出内联菌子集')
    parser.add_argument('--match_mode', choices=['either', 'strain_1', 'strain_2', 'both'], default='either', help='匹配规则：默认任一菌名命中即归入该子集')
    parser.add_argument('--exclusive', action='store_true', help='启用互斥分割：每条pair只归入一个子集，避免重复')
    parser.add_argument('--priority', default='cross,island,inline', help='互斥分割时的优先级顺序，逗号分隔，例如 cross,island,inline')

    args = parser.parse_args()

    # 载入三份菌名集合
    cross_set = load_strain_set(args.cross)
    island_set = load_strain_set(args.island)
    inline_set = load_strain_set(args.inline)

    # 读取pairs所有行与表头
    all_rows, header = read_pairs_rows(args.pairs)
    print(f'输入pairs: {args.pairs} 行数={len(all_rows)} 列={len(header)}')
    print(f'匹配模式: {args.match_mode}')
    print(f'交叉菌strain数: {len(cross_set)}, 孤岛菌strain数: {len(island_set)}, 内联菌strain数: {len(inline_set)}')

    # 构建子集（支持互斥分割）
    cross_rows: List[Dict[str, str]] = []
    island_rows: List[Dict[str, str]] = []
    inline_rows: List[Dict[str, str]] = []

    if args.exclusive:
        # 解析优先级
        pr_raw = [p.strip() for p in args.priority.split(',') if p.strip()]
        valid = {'cross', 'island', 'inline'}
        prio = [p for p in pr_raw if p in valid]
        # 若用户提供不完整或无效，回退为默认顺序
        if len(prio) != 3:
            prio = ['cross', 'island', 'inline']
        print(f'互斥分割启用，优先级顺序: {prio}')

        for r in all_rows:
            hits = {
                'cross': match_row(r, cross_set, args.match_mode),
                'island': match_row(r, island_set, args.match_mode),
                'inline': match_row(r, inline_set, args.match_mode),
            }
            assigned = False
            for tag in prio:
                if hits[tag]:
                    if tag == 'cross':
                        cross_rows.append(r)
                    elif tag == 'island':
                        island_rows.append(r)
                    else:
                        inline_rows.append(r)
                    assigned = True
                    break
            # 未命中任何集合的pair不归入三份输出之一（互斥模式下总行数可能小于输入）
    else:
        for r in all_rows:
            if match_row(r, cross_set, args.match_mode):
                cross_rows.append(r)
            if match_row(r, island_set, args.match_mode):
                island_rows.append(r)
            if match_row(r, inline_set, args.match_mode):
                inline_rows.append(r)

    # 写出
    c = write_subset(args.out_cross, header, cross_rows)
    i = write_subset(args.out_island, header, island_rows)
    n = write_subset(args.out_inline, header, inline_rows)

    print(f'输出交叉菌: {args.out_cross} 行数={c}')
    print(f'输出孤岛菌: {args.out_island} 行数={i}')
    print(f'输出内联菌: {args.out_inline} 行数={n}')
    print(f'三份合计行数: {c + i + n} (互斥模式应≤输入总行数 {len(all_rows)})')


if __name__ == '__main__':
    main()