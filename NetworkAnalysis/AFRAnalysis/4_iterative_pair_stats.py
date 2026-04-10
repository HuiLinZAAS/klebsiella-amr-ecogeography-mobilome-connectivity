import csv
import argparse
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set


def parse_int(value: str) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def load_source_map(sample_csv_path: str) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    with open(sample_csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        # Expect columns: strain, Mash_cluster, Source
        for row in reader:
            strain = row.get('strain')
            source = row.get('Source')
            if strain:
                mapping[strain] = source or ''
    return mapping


def classify_label(source: str) -> str:
    return 'human' if source == 'Human' else 'nohuman'


def read_pairs_build_indices(
    pairs_csv_path: str,
    threshold: int,
) -> Tuple[List[Tuple[str, str, int, str, str, str]], Dict[str, List[Tuple[str, str, int, str, str, str]]], Dict[str, List[Tuple[str, str, int, str, str, str]]]]:
    seeds_rows: List[Tuple[str, str, int, str, str, str]] = []
    # Indices for quick expansion (only HH and NNNH with shared_components > threshold)
    hh_index: Dict[str, List[Tuple[str, str, int, str, str, str]]] = defaultdict(list)
    nnh_index: Dict[str, List[Tuple[str, str, int, str, str, str]]] = defaultdict(list)

    with open(pairs_csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        # Expect columns: strain_1,strain_2,shared_components,Source_1,Source_2,Pair_Type
        for row in reader:
            s1 = row.get('strain_1', '')
            s2 = row.get('strain_2', '')
            shared = parse_int(row.get('shared_components', '0'))
            src1 = row.get('Source_1', '')
            src2 = row.get('Source_2', '')
            ptype = row.get('Pair_Type', '')

            if ptype in ('Human-NonHuman', 'NonHuman-Human') and shared > threshold:
                seeds_rows.append((s1, s2, shared, src1, src2, ptype))

            if shared > threshold:
                if ptype == 'Human-Human':
                    hh_index[s1].append((s1, s2, shared, src1, src2, ptype))
                    hh_index[s2].append((s1, s2, shared, src1, src2, ptype))
                elif ptype == 'NonHuman-NonHuman':
                    nnh_index[s1].append((s1, s2, shared, src1, src2, ptype))
                    nnh_index[s2].append((s1, s2, shared, src1, src2, ptype))

    return seeds_rows, hh_index, nnh_index


def expand_pairs(
    seeds_rows: List[Tuple[str, str, int, str, str, str]],
    hh_index: Dict[str, List[Tuple[str, str, int, str, str, str]]],
    nnh_index: Dict[str, List[Tuple[str, str, int, str, str, str]]],
) -> Tuple[List[Tuple[str, str, int, str, str, str]], Set[str]]:
    # Stats rows will include initial cross-type seeds and any expanded HH/NNNH rows
    stats_rows: List[Tuple[str, str, int, str, str, str]] = []
    stats_keys: Set[Tuple[str, str, int, str]] = set()  # (s1,s2,shared,ptype) key

    # Initialize strain set and queue with both strains from seeds
    strain_set: Set[str] = set()
    q: deque[str] = deque()

    for s1, s2, shared, src1, src2, ptype in seeds_rows:
        key = (s1, s2, shared, ptype)
        if key not in stats_keys:
            stats_keys.add(key)
            stats_rows.append((s1, s2, shared, src1, src2, ptype))
        if s1 not in strain_set:
            strain_set.add(s1)
            q.append(s1)
        if s2 not in strain_set:
            strain_set.add(s2)
            q.append(s2)

    while q:
        s = q.popleft()
        # Expand via HH
        for row in hh_index.get(s, []):
            s1, s2, shared, src1, src2, ptype = row
            key = (s1, s2, shared, ptype)
            if key not in stats_keys:
                stats_keys.add(key)
                stats_rows.append(row)
                other = s2 if s == s1 else s1
                if other not in strain_set:
                    strain_set.add(other)
                    q.append(other)
        # Expand via NonHuman-NonHuman
        for row in nnh_index.get(s, []):
            s1, s2, shared, src1, src2, ptype = row
            key = (s1, s2, shared, ptype)
            if key not in stats_keys:
                stats_keys.add(key)
                stats_rows.append(row)
                other = s2 if s == s1 else s1
                if other not in strain_set:
                    strain_set.add(other)
                    q.append(other)

    return stats_rows, strain_set


def write_pairs_csv(out_path: str, rows: List[Tuple[str, str, int, str, str, str]]) -> None:
    with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['strain_1', 'strain_2', 'shared_components', 'Source_1', 'Source_2', 'Pair_Type'])
        for s1, s2, shared, src1, src2, ptype in rows:
            writer.writerow([s1, s2, shared, src1, src2, ptype])


def write_strains_csv(out_path: str, strains: Set[str], source_map: Dict[str, str],
                      rows: List[Tuple[str, str, int, str, str, str]]) -> Tuple[int, int, int]:
    # 为每个strain聚合其出现过的shared_components值（取最大值）
    shared_max: Dict[str, int] = defaultdict(int)
    for s1, s2, shared, _src1, _src2, _ptype in rows:
        if shared > shared_max[s1]:
            shared_max[s1] = shared
        if shared > shared_max[s2]:
            shared_max[s2] = shared

    human_count = 0
    nohuman_count = 0
    unknown_count = 0
    with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 增加shared_components列（为该strain关联pairs中的最大shared_components）
        writer.writerow(['strain', 'Source', 'label', 'shared_components'])
        for strain in sorted(strains):
            source = source_map.get(strain, 'Unknown')
            label = classify_label(source)
            if source == 'Unknown':
                unknown_count += 1
            if label == 'human':
                human_count += 1
            else:
                nohuman_count += 1
            writer.writerow([strain, source, label, shared_max.get(strain, 0)])
    return human_count, nohuman_count, unknown_count


def main():
    parser = argparse.ArgumentParser(description='迭代统计：从Human-NonHuman/NonHuman-Human的shared>阈值开始，扩展到Human-Human与NonHuman-NonHuman的shared>阈值，输出pairs与strains统计并按AFR_sampled分类。')
    parser.add_argument('--pairs', default=r'd:\trae开发的项目文件\网络图2\AFR_过滤孤岛菌后.csv', help='输入的pairs CSV路径')
    parser.add_argument('--sample', default=r'd:\trae开发的项目文件\网络图2\AFR_sampled.csv', help='样本文件，提供Source映射')
    parser.add_argument('--out_pairs', default=r'd:\trae开发的项目文件\网络图2\AFR_交叉菌_pairs.csv', help='输出的统计pairs CSV路径')
    parser.add_argument('--out_strains', default=r'd:\trae开发的项目文件\网络图2\AFR_交叉菌_strains.csv', help='输出的统计strains CSV路径')
    parser.add_argument('--threshold', type=int, default=2, help='shared_components阈值，严格大于该值')

    args = parser.parse_args()

    seeds_rows, hh_index, nnh_index = read_pairs_build_indices(args.pairs, args.threshold)
    stats_rows, strain_set = expand_pairs(seeds_rows, hh_index, nnh_index)

    write_pairs_csv(args.out_pairs, stats_rows)

    source_map = load_source_map(args.sample)
    human_count, nohuman_count, unknown_count = write_strains_csv(args.out_strains, strain_set, source_map, stats_rows)

    print(f'种子跨类型对数(> {args.threshold}): {len(seeds_rows)}')
    print(f'累计统计对数(包括扩展): {len(stats_rows)}')
    print(f'唯一文件名数: {len(strain_set)}')
    print(f'分类计数: human={human_count}, nohuman={nohuman_count}, unknown_in_sample={unknown_count}')
    print(f'输出pairs: {args.out_pairs}')
    print(f'输出strains: {args.out_strains}')


if __name__ == '__main__':
    main()