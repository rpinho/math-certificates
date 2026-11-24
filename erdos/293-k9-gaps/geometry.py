"""Exact prefix bounds and sharding, using only Python integers."""
from fractions import Fraction
from functools import cache
from math import gcd
import argparse

TARGET = 13_856_993
SIEVE_LIMIT = 13_000_000
FULL = (0, 2**64 - 1)


def factorization(n):
    factors = []
    p = 2
    while p*p <= n:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        if e:
            factors.append((p, e))
        p = 3 if p == 2 else p + 2
    if n > 1:
        factors.append((n, 1))
    return factors


def root_powers(m):
    return tuple(sorted((p**e for p, e in factorization(m)), reverse=True))


def extend(p, q, n):
    a, b = p*n - q, q*n
    g = gcd(a, b)
    return a // g, b // g


def span(p, q, left, previous, powers):
    lo = max(previous + 1, q // p + 1)
    hi = (left*q - 1) // p
    for power in powers:
        if q % power:
            continue
        if p > q // power:
            hi = min(hi, (left - 1)*q // (p - q // power))
        break
    return lo, hi


@cache
def five_term_bound():
    greedy = (2, 3, 7, 43, 1807)
    printed = []
    for length in range(1, 6):
        goal = sum((Fraction(1, d) for d in greedy[:length]), Fraction())
        nodes = [0]*(length + 1)
        equal = []

        def visit(prefix, partial):
            nodes[len(prefix)] += 1
            if partial >= goal:
                assert len(prefix) == length and partial == goal, (prefix, partial)
                equal.append(prefix)
                return
            left = length - len(prefix)
            if not left:
                return
            gap = goal - partial
            upper = left*gap.denominator // gap.numerator
            lower = prefix[-1] + 1 if prefix else 2
            for n in range(lower, upper + 1):
                new_sum = partial + Fraction(1, n)
                if new_sum < 1:
                    visit(prefix + (n,), new_sum)

        visit((), Fraction(0))
        assert equal == [greedy[:length]]
        printed.append(goal)
        print(f"length={length} bound={goal} nodes={nodes} equality={equal}")

    return tuple(printed)


def campaign_bounds(m):
    assert TARGET <= m <= 20_000_000
    caps = []
    q_cap = m
    printed = five_term_bound()
    for depth, partial in enumerate([Fraction(0), *printed]):
        gap = 1 - Fraction(1, m) - partial
        cap = (8 - depth)*gap.denominator // gap.numerator
        caps.append(cap)
        q_cap *= cap
    assert max(caps) <= SIEVE_LIMIT < TARGET
    return caps, q_cap.bit_length()


def shards(m, k, depth, ceiling, powers):
    """Disjoint fixed prefixes, split by potential two-term calls."""
    leaves = k - 1
    assert depth < leaves - 2

    def walk(prefix, p, q):
        left = leaves - len(prefix)
        previous = prefix[-1] if prefix else 1
        lo, hi = span(p, q, left, previous, powers)
        if len(prefix) == depth:
            if not ceiling:
                yield prefix, lo, hi, max(0, hi - lo + 1)
                return
            start, weight = lo, 0
            for n in range(lo, hi + 1):
                if n == m:
                    continue
                a, b = extend(p, q, n)
                child_lo, child_hi = span(a, b, left - 1, n, powers)
                cost = max(1, child_hi - child_lo + 1)
                if weight and weight + cost > ceiling:
                    yield prefix, start, n - 1, weight
                    start, weight = n, 0
                if cost > ceiling:
                    assert weight == 0
                    assert left == 4
                    for x in range(child_lo, child_hi + 1, ceiling):
                        y = min(x + ceiling - 1, child_hi)
                        yield prefix + (n,), x, y, y - x + 1
                    start = n + 1
                    continue
                weight += cost
            if weight:
                yield prefix, start, hi, weight
            return
        for n in range(lo, hi + 1):
            if n != m:
                yield from walk(prefix + (n,), *extend(p, q, n))

    yield from walk((), m - 1, m)


def write_manifest(m, k, depth, ceiling):
    bound = None
    if k == 9 and TARGET <= m <= 20_000_000:
        caps, bits = campaign_bounds(m)
        bound = max(caps)
        print(f"main DFS denominator caps={caps}; sieve_limit={SIEVE_LIMIT}; m={m}; q_cap_bits={bits}")
    with open(f"build/manifest-{m}.tsv", "w") as output:
        print("shard\tweight\ttask", file=output)
        total = 0
        count = 0
        for prefix, lo, hi, weight in shards(m, k, depth, ceiling, root_powers(m)):
            if lo > hi:
                continue
            if bound:
                assert max(*prefix, hi) <= bound
            task = " ".join(map(str, (m, k, *prefix, lo, hi)))
            print(f"{count:06d}\t{weight}\t{task}", file=output)
            total += weight
            count += 1
    print(f"manifest m={m} shards={count} estimated_two_term_calls={total}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    parser.add_argument("k", type=int)
    parser.add_argument("--depth", type=int, required=True)
    parser.add_argument("--ceiling", type=int, default=0)
    args = parser.parse_args()
    write_manifest(args.m, args.k, args.depth, args.ceiling)
