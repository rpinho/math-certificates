"""Exact prefix bounds and sharding, using only Python integers."""
from fractions import Fraction
from math import gcd
import argparse

TARGET = 13_856_993
SIEVE_LIMIT = 13_000_000
FULL = (0, 2**64 - 1)


def extend(p, q, n):
    a, b = p*n - q, q*n
    g = gcd(a, b)
    return a // g, b // g


def span(p, q, left, previous, power):
    lo = max(previous + 1, q // p + 1)
    hi = (left*q - 1) // p
    if power and q % power == 0 and p > q // power:
        hi = min(hi, (left - 1)*q // (p - q // power))
    return lo, hi


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

    caps = []
    q_cap = TARGET
    for depth, partial in enumerate([Fraction(0), *printed]):
        gap = 1 - Fraction(1, TARGET) - partial
        cap = (8 - depth)*gap.denominator // gap.numerator
        caps.append(cap)
        q_cap *= cap
    assert max(caps) <= SIEVE_LIMIT < TARGET
    print(f"main DFS denominator caps={caps}; sieve_limit={SIEVE_LIMIT}; m={TARGET}; q_cap_bits={q_cap.bit_length()}")
    return max(caps)


def shards(m, k, depth, ceiling, power):
    """Disjoint fixed prefixes, split by potential two-term calls."""
    leaves = k - 1
    assert depth < leaves - 2

    def walk(prefix, p, q):
        left = leaves - len(prefix)
        previous = prefix[-1] if prefix else 1
        lo, hi = span(p, q, left, previous, power)
        if len(prefix) == depth:
            if not ceiling:
                yield prefix, lo, hi, max(0, hi - lo + 1)
                return
            start, weight = lo, 0
            for n in range(lo, hi + 1):
                if n == m:
                    continue
                a, b = extend(p, q, n)
                child_lo, child_hi = span(a, b, left - 1, n, power)
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
    bound = five_term_bound() if m == TARGET else None
    with open(f"build/manifest-{m}.tsv", "w") as output:
        print("shard\tweight\ttask", file=output)
        total = 0
        count = 0
        for prefix, lo, hi, weight in shards(m, k, depth, ceiling, m if m == TARGET else 0):
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
