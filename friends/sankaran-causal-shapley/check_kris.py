#!/usr/bin/env python3
"""Exact finite checks for the note; Python 3.9+, standard library only.

No files, downloads, external data, imported local modules, or random inputs.
Matrices B use B[v][u] for the edge u -> v. Fraction arithmetic is exact.
The theorem in the note is proved analytically; these checks are finite.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum((x * y for x, y in zip(row, col)), Q(0))
             for col in zip(*b)] for row in a]


def rank(a):
    a = [[Q(x) for x in row] for row in a]
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][col]
        a[r] = [x / q for x in a[r]]
        for i in range(r + 1, len(a)):
            q = a[i][col]
            a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def order(b):
    n = len(b)
    todo, out = set(range(n)), []
    while todo:
        v = next((v for v in sorted(todo)
                  if all(not b[v][u] for u in todo)), None)
        assert v is not None, 'Directed cycle'
        todo.remove(v)
        out.append(v)
    return out


def games(b):
    """Solve intervened mean equations directly, independently of powers."""
    n, topo = len(b), order(b)
    out = []
    for mask in range(1 << n):
        m = zero(n)
        for v in topo:
            if mask & (1 << v):
                m[v][v] = Q(1)
            else:
                for u in range(n):
                    if b[v][u]:
                        for a in range(n):
                            m[v][a] += b[v][u] * m[u][a]
        out.append(m)
    return out


def attribution(g, j):
    """Return A with phi_j(x) = x^T A c using factorial coalition weights."""
    n, a = len(g[0]), zero(len(g[0]))
    for mask in range(1 << n):
        if mask & (1 << j):
            continue
        s = bin(mask).count('1')
        w = Q(factorial(s) * factorial(n - s - 1), factorial(n))
        for v in range(n):
            for u in range(n):
                a[u][v] += w * (g[mask | (1 << j)][v][u] - g[mask][v][u])
    return a


def powers(b):
    out = [identity(len(b))]
    for _ in range(1, len(b)):
        out.append(matmul(out[-1], b))
    assert not any(map(any, matmul(out[-1], b)))
    return out


def path_attribution(p, j):
    n, a = len(p), zero(len(p))
    for v in range(n):
        a[j][v] = sum((p[r][v][j] / (r + 1) for r in range(n)), Q(0))
        for u in range(n):
            if u != j:
                a[u][v] = -sum((p[s][j][u] * p[r][v][j]
                                   / ((s + r) * (s + r + 1))
                                   for s in range(1, n) for r in range(n)), Q(0))
    return a


def descendants(b, j):
    reached = {j}
    while True:
        new = reached | {v for v in range(len(b))
                         if any(b[v][u] for u in reached)}
        if new == reached:
            return reached
        reached = new


def heights(p, j):
    hm = max(r for r, m in enumerate(p) if any(m[j]))
    hp = max(r for r, m in enumerate(p) if any(row[j] for row in m))
    return hm, hp


def lengths(b, j):
    n = len(b)
    incoming, outgoing = [0] * n, [0] * n
    topo = order(b)
    for v in topo:
        incoming[v] = max([0] + [incoming[u] + 1 for u in range(n) if b[v][u]])
    for u in reversed(topo):
        outgoing[u] = max([0] + [outgoing[v] + 1 for v in range(n) if b[v][u]])
    return incoming[j], outgoing[j]


def verify(b):
    n, g, p = len(b), games(b), powers(b)
    for j in range(n):
        a = attribution(g, j)
        assert a == path_attribution(p, j)
        hm, hp = heights(p, j)
        r = rank(a)
        assert r == min(hm + 1, hp + 1)
        tau = [g[1 << j][v][j] for v in range(n)]
        assert (rank(a + [tau]) == r) == (hm >= hp)
        # Row-space inclusion of every coalition marginal is the stronger null.
        contextual = True
        for mask in range(1 << n):
            if mask & (1 << j):
                continue
            delta = [[g[mask | (1 << j)][v][u] - g[mask][v][u]
                      for v in range(n)] for u in range(n)]
            contextual &= rank(a + delta) == r
        d = len(descendants(b, j))
        assert contextual == (r == d)
        assert contextual == (hp == d - 1 and hm >= d - 1)
        din, dout = lengths(b, j)
        assert (hp == d - 1) == (dout == d - 1)
        if all(x >= 0 for row in b for x in row):
            assert (hm, hp) == (din, dout)


def coefficients(a, c):
    return [sum((x * y for x, y in zip(row, c)), Q(0)) for row in a]


def law(b, c, clamps):
    """Complete outcome law for independent uniform {-1,1} disturbances."""
    n, topo, counts = len(b), order(b), Counter()
    for noise in product((-1, 1), repeat=n + 1):
        x = [Q(0)] * n
        for v in topo:
            x[v] = (Q(clamps[v]) if v in clamps else Q(noise[v])
                    + sum((b[v][u] * x[u] for u in range(n)), Q(0)))
        counts[sum((c[v] * x[v] for v in range(n)), Q(noise[-1]))] += 1
    return {y: Q(count, 2 ** (n + 1)) for y, count in counts.items()}


def examples():
    b = [[Q(0), Q(0)], [Q(1), Q(0)]]
    g = games(b)
    a = attribution(g, 0)
    assert a == [[Q(1), Q(1, 2)], [Q(0), Q(0)]]
    assert coefficients(a, [-1, 2]) == [0, 0]
    assert sum(c * g[1][v][0] for v, c in enumerate([-1, 2])) == 1
    assert sum(c * g[1][v][0] for v, c in enumerate([-1, 1])) == 0
    assert law(b, [-1, 2], {0: -1}) != law(b, [-1, 2], {0: 1})
    assert coefficients(a, [-1, 1]) == [Q(-1, 2), Q(0)]
    assert law(b, [-1, 1], {0: -1}) == law(b, [-1, 1], {0: 1})
    fork = [[Q(0)] * 3, [Q(1), Q(0), Q(0)], [Q(1), Q(0), Q(0)]]
    c = [0, 1, -1]
    g = games(fork)
    assert coefficients(attribution(g, 0), c) == [0, 0, 0]
    assert sum(c[v] * g[1][v][0] for v in range(3)) == 0
    assert law(fork, c, {0: -1}) == law(fork, c, {0: 1})
    delta = [[g[3][v][u] - g[2][v][u] for v in range(3)] for u in range(3)]
    assert coefficients(delta, c) == [-1, 0, 0]
    # 1->2->4 and 1->3->4 cancel; 4->5->6 remains.
    b = zero(6)
    for u, v, w in [(0, 1, 1), (0, 2, 1), (1, 3, 1),
                    (2, 3, -1), (3, 4, 1), (4, 5, 1)]:
        b[v][u] = Q(w)
    assert lengths(b, 3) == (2, 2)
    assert heights(powers(b), 3) == (1, 2)
    c = [0, 0, 0, 1, -6, 6]
    g = games(b)
    assert coefficients(attribution(g, 3), c) == [0] * 6
    assert sum(c[v] * g[1 << 3][v][3] for v in range(6)) == 1
    assert [sum(c[v] * p[v][3] for v in range(6))
            for p in powers(b)] == [1, -6, 6, 0, 0, 0]
    assert law(b, c, {3: -1}) != law(b, c, {3: 1})
    verify(b)
    verify(fork)
    # Non-topological relabeling of the signed example.
    perm = [5, 2, 0, 4, 1, 3]
    verify([[b[perm[v]][perm[u]] for u in range(6)] for v in range(6)])
    print('Examples: PASS (two-node, fork, signed diamond, relabeling)')


def legendre_checks():
    for m in range(1, 9):
        coeff = [Q((-1) ** (m - k) * comb(m, k) * comb(m + k, k))
                 for k in range(m + 1)]
        assert sum(coeff) == 1
        for s in range(m):
            assert sum((coeff[k] / (k + s + 1) for k in range(m + 1)), Q(0)) == 0
    print('Endpoint and orthogonality identities: PASS (degrees 1 through 8)')


def nonunit_checks():
    """Fixed chain, complete, and reconverging DAGs with relabeled vertices."""
    models = features = 0
    for n in (5, 6, 7):
        supports = [
            [(u, u + 1) for u in range(n - 1)],
            [(u, v) for u in range(n) for v in range(u + 1, n)],
            [(0, 1), (0, 2), (1, 3), (2, 3)]
            + [(u, u + 1) for u in range(3, n - 1)],
        ]
        # New label v represents old label perm[v]; this is not a
        # topological ordering for any of the three supports.
        perm = list(range(1, n, 2)) + list(range(0, n, 2))
        for edges in supports:
            for signed in (False, True):
                b = zero(n)
                for edge_index, (u, v) in enumerate(edges):
                    w = 1 + (u + 2 * v) % 2
                    if signed and edge_index % 2 == 1:
                        w = -w
                    b[v][u] = Q(w)
                assert any(abs(w) == 2 for row in b for w in row)
                if signed:
                    assert any(w < 0 for row in b for w in row)
                relabeled = [[b[perm[v]][perm[u]] for u in range(n)]
                             for v in range(n)]
                assert order(relabeled) != list(range(n))
                verify(relabeled)
                models += 1
                features += n
    assert (models, features) == (18, 108)
    print('Non-unit fixed graphs on 5--7 vertices with relabeling: PASS')
    print('Additional models: {}; feature checks: {}'.format(models, features))


def main():
    examples()
    legendre_checks()
    models = features = 0
    for n in range(1, 5):
        slots = [(u, v) for u in range(n) for v in range(u + 1, n)]
        for weights in product((-1, 0, 1), repeat=len(slots)):
            b = zero(n)
            for (u, v), w in zip(slots, weights):
                b[v][u] = Q(w)
            verify(b)
            models += 1
            features += n
    assert (models, features) == (760, 3004)
    print('Signed-unit ordered graphs through 4 vertices: PASS')
    print('Models: {}; feature checks: {}'.format(models, features))
    nonunit_checks()
    print('PASS: exact finite checks; no claim of a general proof by enumeration.')


if __name__ == '__main__':
    main()
