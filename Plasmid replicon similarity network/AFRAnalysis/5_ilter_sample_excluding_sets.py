import csv
import argparse
from typing import Set, Dict


def load_exclude_strains(*paths: str) -> Set[str]:
    exclude: Set[str] = set()
    for p in paths:
        with open(p, 'r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            # Prefer column named 'strain'
            fieldnames = reader.fieldnames or []
            strain_col = None
            # Try exact 'strain'
            if 'strain' in fieldnames:
                strain_col = 'strain'
            else:
                # Fallback: case-insensitive match
                for fn in fieldnames:
                    if fn.lower() == 'strain':
                        strain_col = fn
                        break
            if not strain_col:
                raise ValueError(f'无法在文件中找到strain列: {p}')
            for row in reader:
                s = row.get(strain_col, '').strip()
                if s:
                    exclude.add(s)
    return exclude


def classify_label(source: str) -> str:
    return 'human' if source == 'Human' else 'nohuman'

def parse_int(value: str) -> int:
    try:
        return int(float(value))
    except Exception:
        return 0


def load_shared_components_map(pairs_path: str) -> Dict[str, int]:
    """读取pairs文件，为每个strain聚合其出现过的shared_components（取最大值）。"""
    shared_max: Dict[str, int] = {}
    with open(pairs_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s1 = (row.get('strain_1') or '').strip()
            s2 = (row.get('strain_2') or '').strip()
            shared = parse_int(row.get('shared_components', '0'))
            if s1:
                shared_max[s1] = max(shared_max.get(s1, 0), shared)
            if s2:
                shared_max[s2] = max(shared_max.get(s2, 0), shared)
    return shared_max


def filter_sample(sample_path: str, exclude: Set[str], out_path: str, shared_map: Dict[str, int]) -> tuple[int, int, int]:
    total = 0
    excluded = 0
    kept_rows = []
    with open(sample_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        # Expect: strain, Mash_cluster, Source
        for row in reader:
            total += 1
            s = row.get('strain', '').strip()
            if s in exclude:
                excluded += 1
                continue
            kept_rows.append(row)

    with open(out_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['strain', 'Mash_cluster', 'Source', 'label', 'shared_components'])
        writer.writeheader()
        for r in kept_rows:
            source = r.get('Source', '')
            label = classify_label(source)
            writer.writerow({
                'strain': r.get('strain', ''),
                'Mash_cluster': r.get('Mash_cluster', ''),
                'Source': source,
                'label': label,
                'shared_components': shared_map.get((r.get('strain', '') or '').strip(), 0),
            })

    return total, excluded, len(kept_rows)


def main():
    parser = argparse.ArgumentParser(description='从AFR_sampled中排除孤岛菌与交叉菌名，生成新表，并输出shared_components列')
    parser.add_argument('--sample', default=r'd:\trae开发的项目文件\网络图2\AFR_sampled.csv')
    parser.add_argument('--island', default=r'd:\trae开发的项目文件\网络图2\AFR_矩阵表_孤岛菌.csv')
    parser.add_argument('--cross', default=r'd:\trae开发的项目文件\网络图2\AFR_交叉菌_strains.csv')
    parser.add_argument('--pairs', default=r'd:\trae开发的项目文件\网络图2\AFR_shared_components_pairs.csv', help='用于计算shared_components的pairs文件')
    parser.add_argument('--out', default=r'd:\trae开发的项目文件\网络图2\AFR_sampled_内联菌.csv')

    args = parser.parse_args()

    exclude = load_exclude_strains(args.island, args.cross)
    shared_map = load_shared_components_map(args.pairs)
    total, excluded, kept = filter_sample(args.sample, exclude, args.out, shared_map)

    print(f'输入总数: {total}')
    print(f'排除数量: {excluded} (来自 {args.island} 与 {args.cross})')
    print(f'保留数量: {kept}')
    print(f'输出: {args.out}')


if __name__ == '__main__':
    main()