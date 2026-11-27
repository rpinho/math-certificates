"""Check raw binary witnesses and compute theta directly on the distance graph."""
import argparse
import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check_pairs(n, r, vertices, witnesses):
    require(type(n) is int and type(r) is int and n > r >= 1, 'parameters')
    require(len(vertices) == len(witnesses), 'length mismatch')
    require(all(type(x) is int and 0 <= x < 2**n for x in vertices + witnesses),
            'word outside cube')

    def distance(x, y):
        return sum(a != b for a, b in zip(format(x, f'0{n}b'), format(y, f'0{n}b')))

    for i, (v, w) in enumerate(zip(vertices, witnesses)):
        require(distance(v, w) > r, f'diagonal at {i}')
        for j in range(i):
            require(distance(v, vertices[j]) <= r, f'close at {j},{i}')
            require(distance(w, vertices[j]) <= r, f'ordered cross at {j},{i}')
    return len(vertices)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def distance_graph(n, r):
    return [sum(1 << j for j in range(2**n) if (i ^ j).bit_count() > r)
            for i in range(2**n)]


def theta_control(n, r):
    neighbors = distance_graph(n, r)

    @lru_cache(maxsize=100000)
    def rec(S):
        values = []
        for v in bits(S):
            if neighbors[v] & S:
                deleted = S ^ (1 << v)
                values.append(max(rec(deleted), 1 + rec(deleted & ~neighbors[v])))
        return min(values, default=0)

    return rec((1 << 2**n) - 1)


def five_cube(r):
    n = 5
    adj = distance_graph(n, r)
    S = (1 << 2**n) - 1
    # The coordinate subcube gives a lower certificate from induced edges.
    sub = range(1 << (r + 1))
    edges = [(a, b) for a, b in combinations(sub, 2) if adj[a] & (1 << b)]
    require(sorted(v for edge in edges for v in edge) == list(sub), 'matching')
    lower = len(edges)

    @lru_cache(maxsize=150000)
    def at_most(mask, bound):
        pivots = [v for v in bits(mask) if adj[v] & mask]
        if not pivots:
            return True
        if bound == 0:
            return False
        # Each pivot tries both branches of the defining minimax recurrence.
        for v in sorted(pivots, key=lambda u: -(adj[u] & mask).bit_count()):
            deleted = mask ^ (1 << v)
            if at_most(deleted & ~adj[v], bound - 1) and at_most(deleted, bound):
                return True
        return False

    upper = at_most(S, lower)
    require(upper, 'upper bound failed')
    return lower, at_most.cache_info().misses


def check_kernel(path):
    """Verify the raw matrix without importing the generator or the searchers."""
    f = json.loads(path.read_text())
    n, r = 10, 4
    size = 1 << (r + 1)
    require(len(f) == 2**n, 'kernel length')
    for z, value in enumerate(f):
        require(type(value) is int and 0 <= value < 65536, 'field encoding')
        require(bool(value) == (z.bit_count() > r), f'wrong distance support at {z}')

    # Prove the quotient F_2[X]/(X^16+X^12+X^3+X+1) is a field by
    # verifying that powers of X visit all its nonzero elements.
    powers = []
    logs = {}
    t = 1
    for i in range(65535):
        require(t != 0 and t not in logs, 'short multiplicative cycle')
        powers.append(t)
        logs[t] = i
        t <<= 1
        if t >= 65536:
            t ^= 0x1100B
    require(t == 1, 'cycle fails to close')
    powers *= 2

    def multiply(a, b):
        return powers[logs[a] + logs[b]] if a and b else 0

    # R_j(x)=f(x xor j). On the first 32 columns, the first 32 rows
    # are a scalar times the antipodal permutation matrix. Test that every
    # outside single-coordinate shift of R_0 is in their span. Shifts by
    # a low word permute those rows and commute with every other shift.
    last = size - 1
    scale = f[last]
    checks = 0
    for h in range(r + 1, n):
        shift = 1 << h
        weights = [f[shift ^ j ^ last] for j in range(size)]
        for x in range(2**n):
            combination = 0
            for j, weight in enumerate(weights):
                combination ^= multiply(weight, f[x ^ j])
            require(combination == multiply(scale, f[x ^ shift]), 'row span')
            checks += 1
    print('kernel n=10 r=4 support', len(f), 'shift identities', checks,
          'rank', size, 'maximum close-skew length', size // 2)


def controls():
    for n, r in [(3, 2), (4, 3)]:
        v = list(range(2**r))
        w = [x ^ (2**n - 1) for x in v]
        print('tight', n, r, check_pairs(n, r, v, w))
        # Put the last witness on its own vertex.
        bad = w.copy()
        bad[-1] = v[-1]
        try:
            check_pairs(n, r, v, bad)
        except ValueError as exc:
            require(str(exc) == f'diagonal at {len(v)-1}', 'mutation rejected elsewhere')
            print('mutation rejected', str(exc))
        else:
            raise ValueError('mutation accepted')
    # This valid one-sided system fails the opposite cross inequality.
    v, w = [0, 1], [7, 2]
    require(check_pairs(3, 1, v, w) == 2, 'asymmetric system')
    original = list(zip(v, w))
    swapped = list(zip(w, v))
    def skew_violations(pairs):
        return [(i, j) for i, (a, _) in enumerate(pairs)
                for j, (_, b) in enumerate(pairs)
                if (i == j and (a ^ b).bit_count() <= 1)
                or (i < j and (a ^ b).bit_count() > 1)]
    require(skew_violations(original + swapped[::-1]) == [], 'reversed doubling')
    require(skew_violations(original + swapped) == [(2, 3)], 'unreversed mutation')
    print('asymmetric doubling accepted; unreversed mutation rejected at (2,3)')
    for n in (2, 3, 4):
        for r in range(1, n):
            observed = theta_control(n, r)
            print('theta', n, r, observed)
            require(observed == 2**r, 'theta control')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['controls', 'five', 'witness', 'kernel'])
    parser.add_argument('file', nargs='?', type=Path)
    args = parser.parse_args()
    if args.mode == 'controls':
        controls()
    elif args.mode == 'five':
        for r in (2, 3, 4):
            value, states = five_cube(r)
            print('theta', 5, r, value, 'upper decision states', states)
    elif args.mode == 'kernel':
        check_kernel(args.file or Path(__file__).with_name('rank_kernel.json'))
    else:
        data = json.loads(args.file.read_text())
        k = check_pairs(data['n'], data['r'], data['v'], data['w'])
        print('valid length', k, 'counterexample', k > 2**data['r'])
