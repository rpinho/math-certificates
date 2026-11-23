"""Exact G1 and G3 generators. G2 uses binary necklaces in validate.cpp."""
from collections import Counter
import argparse
from fractions import Fraction as Q
from itertools import combinations
import random
import struct

rng = random.Random(9821123)
ORDERS = tuple(range(3, 14))
KINDS = ("circle-fan", "equilateral", "concentric", "thin", "symmetric")


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull(points):
    points = sorted(set(points))
    chains = []
    for sequence in (points, reversed(points)):
        chain = []
        for point in sequence:
            while len(chain) >= 2 and cross(*chain[-2:], point) <= 0:
                chain.pop()
            chain.append(point)
        chains.extend(chain[:-1])
    if len(chains) >= 3:
        assert all(cross(chains[i], chains[(i + 1) % len(chains)], other) > 0
                   for i in range(len(chains))
                   for other in chains if other not in (chains[i], chains[(i + 1) % len(chains)]))
    return chains


def metric(points, scale=1):
    return [(a - c) ** 2 + scale * (b - d) ** 2
            for (a, b), (c, d) in combinations(points, 2)]


def unit(t, scale=1):
    return ((1 - scale*t*t)/(1 + scale*t*t), 2*t/(1 + scale*t*t))


def generic(n):
    while True:
        xs = sorted(rng.sample(range(-10000, 10001), n))
        points = hull([(1000*x, 1000*x*x + rng.randrange(-100, 101)) for x in xs])
        if len(points) == n:
            distances = metric(points)
            if len(distances) == len(set(distances)):
                return distances


def fan(n, targeted=False):
    if targeted and n >= 5:
        fixed = [-800, -125, 125, 800]
        ts = fixed + rng.sample([t for t in range(-799,800) if t not in fixed], n-5)
        a,b,c,d = [unit(Q(t,1000)) for t in fixed]
        assert metric([a,b])[0] > 1 and metric([c,d])[0] > 1
    else:
        ts = rng.sample(range(-650, 651), n - 1)
    points = hull([(0, 0)] + [unit(Q(t, 1000)) for t in ts])
    assert len(points) == n
    return metric(points)


def equilateral(n):
    points = [(Q(1), Q(0)), (Q(-1, 2), Q(1, 2)), (Q(-1, 2), Q(-1, 2))]
    ts = rng.sample(range(-2500, 2501), n - 3)
    while 0 in ts or 1000 in ts or -1000 in ts:
        ts = rng.sample(range(-2500, 2501), n - 3)
    points = hull(points + [unit(Q(t,1000), scale=3) for t in ts])
    assert len(points) == n
    return metric(points, scale=3)


def concentric(n, require_tie=False):
    # Full even carrier: p_j=(1+epsilon*(j mod 2))*zeta_m**j,
    # epsilon = 1/10000, with m even and m<=28.
    # PROOFS.md proves the lexicographic chord-order key exactly.
    while True:
        m = 2 * rng.randrange((n + 1) // 2, n + 2)
        vertices = sorted(rng.sample(range(m), n))
        keys = [(min(b-a, m-b+a), (a % 2) + (b % 2))
                for a, b in combinations(vertices, 2)]
        if not require_tie or len(set(keys)) < len(keys):
            return keys


def thin(n, require_tie=False):
    if require_tie:
        positive = rng.sample(range(1,10001), n//2)
        xs = positive + [-x for x in positive] + ([0] if n%2 else [])
    else:
        xs = rng.sample(range(-10000, 10001), n)
    points = hull([(x, Q(x*x, 10**10)) for x in xs])
    assert len(points) == n
    assert max(y for x,y in points) - min(y for x,y in points) < Q(1, 100)
    return metric(points)


def symmetric(n):
    r = rng.sample(range(1, 1001), n // 2)
    xs = [-x for x in r] + r
    if n % 2:
        xs.append(0)
    delta = rng.randrange(1, 2000)
    points = hull([(x, x*x + delta) for x in xs])
    assert len(points) == n
    return metric(points)


def write_sample(stream, n, kind, distances):
    distinct = sorted(set(distances))
    rank = {d: i for i, d in enumerate(distinct)}
    stream.write(struct.pack("BB", n, kind))
    stream.write(bytes(rank[d] for d in distances))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targeted", action="store_true")
    args = parser.parse_args()
    suffix = "_targeted" if args.targeted else ""
    counts = Counter()
    with open(f"runs/witnesses{suffix}.bin", "wb") as stream:
        for index in range(10000):
            n = ORDERS[index % len(ORDERS)]
            write_sample(stream, n, 0, generic(n))
            counts["generic", n] += 1
        constructors = (lambda n: fan(n,args.targeted), equilateral,
                        lambda n: concentric(n,args.targeted),
                        lambda n: thin(n,args.targeted), symmetric)
        for kind, constructor in enumerate(constructors, 1):
            for index in range(1000):
                n = ORDERS[index % len(ORDERS)]
                distances = constructor(n)
                if args.targeted:
                    assert len(set(distances)) < len(distances)
                write_sample(stream, n, kind, distances)
                counts[KINDS[kind-1], n] += 1
    with open(f"runs/generators{suffix}.tsv", "w") as stream:
        print("construction\tn\tsamples", file=stream)
        for (kind, n), count in sorted(counts.items()):
            print(kind, n, count, sep="\t", file=stream)
