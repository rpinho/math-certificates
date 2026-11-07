"""Referee implementation from PPM descendant sums; no claimant imports.

Run only on the authorized compute pod. Trees are generated as undirected
edge subsets, then oriented by breadth-first traversal from the fixed root.
The candidate score is computed by subtracting children's observed signals,
without inverting an ancestry matrix or using a Prufer/parent-map generator.
"""
import itertools
import json
import math
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp


def edge_trees(q):
    edges = list(itertools.combinations(range(q), 2))
    for selected in itertools.combinations(edges, q - 1):
        adj = [[] for _ in range(q)]
        for a, b in selected:
            adj[a].append(b)
            adj[b].append(a)
        parent = [-2] * q
        parent[0] = -1
        order = [0]
        for v in order:
            for w in adj[v]:
                if parent[w] == -2:
                    parent[w] = v
                    order.append(w)
        if len(order) != q:
            continue
        children = [[] for _ in range(q)]
        descendants = [{v} for v in range(q)]
        for v in reversed(order[1:]):
            children[parent[v]].append(v)
            descendants[parent[v]].update(descendants[v])
        yield parent, children, descendants


def ancestry(descendants):
    q = len(descendants)
    return np.array([[int(j in descendants[i]) for j in range(q)]
                     for i in range(q)], dtype=np.int64)


def residual_operator(children):
    q = len(children)
    # The source's F_i equals M_i plus the signals F_j of direct children.
    out = np.eye(q, dtype=np.int64)
    for i, row in enumerate(children):
        for j in row:
            out[i, j] -= 1
    return out


def exhaustive(q):
    start = time.monotonic()
    panel = list(edge_trees(q))
    size = q ** (q - 2)
    assert len(panel) == size
    us = np.array([ancestry(d) for _, _, d in panel])
    ls = np.array([residual_operator(c) for _, c, _ in panel])
    assert np.array_equal(ls @ us, np.broadcast_to(np.eye(q), us.shape))
    ks = us @ us.transpose(0, 2, 1)
    # A direct control using only observed continuous covariation.
    recovered = (ks == np.diagonal(ks, axis1=1, axis2=2)[:, None, :])
    assert np.array_equal(recovered, us)
    coeffs = (ls.transpose(0, 2, 1) @ ls).reshape(size, q * q)
    histogram = Counter()
    wrong_min = q * q * q
    witness = None
    for lo in range(0, size, 192):
        hi = min(size, lo + 192)
        scores = coeffs[lo:hi] @ ks.reshape(size, q * q).T
        # Every computed score is an integer, without floating point inversion.
        gaps = scores - q
        assert np.all(gaps >= 0)
        assert np.all(gaps % 2 == 0)
        zeros = np.argwhere(gaps == 0)
        assert len(zeros) == hi - lo
        assert all(i + lo == j for i, j in zeros)
        v, ct = np.unique(gaps, return_counts=True)
        histogram.update({int(a): int(b) for a, b in zip(v, ct)})
        positive = np.where(gaps > 0, gaps, q * q * q)
        m = int(positive.min())
        if m < wrong_min:
            wrong_min = m
            i, j = np.argwhere(gaps == m)[0]
            witness = {'candidate_parent': panel[lo + i][0],
                       'true_parent': panel[j][0],
                       'residual': (ls[lo + i] @ us[j]).tolist()}
    assert wrong_min == 2
    # Distinct leaf moves count distinctly, also at the smallest q.
    leaf_total = sum(sum(not c[v] for v in range(1, q)) * (q - 2)
                     for _, c, _ in panel)
    factor = Fraction(leaf_total, size)
    claimed_factor = (q - 1) * (q - 2) * Fraction(q - 1, q) ** (q - 2)
    assert factor == claimed_factor
    return {'q': q, 'trees': size, 'ordered_pairs': size * size,
            'gap_histogram': dict(sorted(histogram.items())),
            'minimum_wrong_gap': wrong_min,
            'singleton_minima': size, 'covariance_control_pass': True,
            'mean_leaf_alternatives': str(factor), 'sharp_witness': witness,
            'seconds': round(time.monotonic() - start, 3)}


def symbolic_baseline():
    # Expand the killed half-line kernel determinant independently. With scaled
    # endpoints u,v, the order-four start coefficient uses these two integrals.
    r, theta, x, y = sp.symbols('r theta x y', positive=True)
    radial = sp.integrate(r ** 5 * sp.exp(-r ** 2 / 2), (r, 0, sp.oo))
    angular = sp.integrate(sp.sin(theta) * sp.cos(theta) * sp.cos(2 * theta),
                           (theta, 0, sp.pi / 4))
    determinant_coefficient = sp.simplify(sp.Rational(2, 3) * radial * angular / (2 * sp.pi))
    survival_coefficient = 2 / sp.pi
    conditional = sp.simplify(determinant_coefficient / survival_coefficient)
    fixed_start_constant = sp.integrate(conditional * (y*y - x*x), (x, 0, y), (y, 0, 1))
    # Also test the literal annealed conditioning interpretation of Assumption 5.
    numerator_integral = sp.integrate(x*y*(y*y-x*x), (x, 0, y), (y, 0, 1))
    denominator_integral = sp.integrate(x*y, (x, 0, 1), (y, 0, 1))
    annealed_constant = sp.simplify(conditional * numerator_integral / denominator_integral)
    assert fixed_start_constant == annealed_constant == sp.Rational(1, 36)
    return {k: str(v) for k, v in locals().items() if k in
            ['radial', 'angular', 'determinant_coefficient', 'conditional',
             'fixed_start_constant', 'annealed_constant']}


def sharp_examples():
    rows = []
    for q in range(3, 41):
        true_children = [list(range(1, q))] + [[] for _ in range(q - 1)]
        candidate_children = [list(range(1, q - 1)), [q - 1]] + [[] for _ in range(q - 2)]
        d = [{i} for i in range(q)]
        d[0] = set(range(q))
        u = ancestry(d)
        b = residual_operator(candidate_children) @ u
        assert int(np.sum(b * b)) == q + 2
        # Positive ordered constant paths: a deterministic strict feasibility
        # witness whose open tube has positive conditioned Brownian probability.
        x = np.full(q, Fraction(1, 4), dtype=object)
        x[1] = Fraction(3, 4)
        x[q - 1] = Fraction(1, 8)
        inferred = b.astype(object) @ x
        assert all(v > 0 for v in inferred)
        ratio = Fraction(q + 2, q)
        rows.append({'q': q, 'critical_gamma': str(ratio),
                     'minimum_inferred_witness': str(min(inferred))})
    return rows


def main():
    result = {'method': __doc__, 'baseline': symbolic_baseline(),
              'sharp_examples': sharp_examples(), 'panels': []}
    for q in range(3, 8):
        row = exhaustive(q)
        result['panels'].append(row)
        Path('audit_results.json').write_text(json.dumps(result, indent=2))
        print(json.dumps(row), flush=True)
    result['status'] = 'PASS'
    Path('audit_results.json').write_text(json.dumps(result, indent=2))
    print('PASS', flush=True)


if __name__ == '__main__':
    main()
