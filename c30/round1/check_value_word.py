"""Exhaustive finite control of FIRST_MOMENT_PROOF.md, Lemma 2.1.

Enumerate permutations, recognize 213 avoidance directly, and derive arches
from consecutive values. No marginal recurrence or candidate code is imported.
Every upper projection of a domino/prefix is among these 213-avoiding cells.
"""
import argparse
from collections import Counter
from itertools import permutations
import json
from math import comb
from pathlib import Path


def avoids_213(p):
    return not any(p[j] < p[i] < p[k]
                   for i in range(len(p))
                   for j in range(i + 1, len(p))
                   for k in range(j + 1, len(p)))


def value_word(p):
    leaves = set()
    largest = -1
    for x in reversed(p):
        if x > largest:
            leaves.add(x)
            largest = x
    return ''.join('0' if x in leaves else '1' for x in sorted(p))


def check_node(p, counts):
    counts['recursive_nodes'] += 1
    if not p:
        return ''
    positions = {x: i for i, x in enumerate(p)}
    # BBEP's forward arch map, applied to standardized upper-cell ranks.
    values = sorted(p)
    incoming = {positions[b]: positions[a]
                for a, b in zip(values, values[1:])
                if positions[a] < positions[b]}
    chain = [len(p) - 1]
    while chain[-1] in incoming:
        chain.append(incoming[chain[-1]])
    chain.reverse()
    if len(chain) == 1:
        counts['isolated_nodes'] += 1
        assert p[-1] == min(p), ('isolated point not minimal', p)
        predicted = '0' + check_node(p[:-1], counts)
    else:
        counts['chain_nodes'] += 1
        chain_values = [p[i] for i in chain]
        assert all(b == a + 1 for a, b in zip(chain_values, chain_values[1:])), p
        objects = [p[:chain[0]]] + [p[a + 1:b] for a, b in zip(chain, chain[1:])]
        for obj in objects:
            assert all(x > max(chain_values) for x in obj), ('above chain', p, obj)
            counts['above_chain_point_checks'] += len(obj)
        for i, left in enumerate(objects):
            for right in objects[i + 1:]:
                assert all(x > y for x in left for y in right), ('reverse order', p, left, right)
                counts['reverse_order_pair_checks'] += len(left) * len(right)
        words = [check_node(obj, counts) for obj in objects]
        predicted = '1' * (len(chain) - 1) + '0' + ''.join(reversed(words))
    actual = value_word(p)
    assert predicted == actual, ('value word', p, predicted, actual)
    counts['word_checks'] += 1
    return predicted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=9)
    parser.add_argument('--output', default='artifacts/value_word_check.json')
    args = parser.parse_args()
    assert 0 <= args.max_n <= 9, 'small local check only'
    rows = []
    for n in range(args.max_n + 1):
        counts = Counter()
        cells = 0
        for p in permutations(range(1, n + 1)):
            if avoids_213(p):
                check_node(p, counts)
                cells += 1
        assert cells == comb(2 * n, n) // (n + 1), ('Catalan count', n, cells)
        row = {'n': n, 'cells': cells, **dict(counts)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    result = {
        'status': 'PASS', 'max_n': args.max_n,
        'scope': 'Lemma 2.1 on all 213-avoiding upper projections; finite control only',
        'cells_checked': sum(row['cells'] for row in rows), 'rows': rows,
    }
    output = Path(args.output)
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}))


if __name__ == '__main__':
    main()
