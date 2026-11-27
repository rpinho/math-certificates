"""Recover control polynomials from raw arc sets and compare with the Lean definitions."""
import itertools
import json
import subprocess
from fractions import Fraction
from pathlib import Path


def color_count(n, arcs, palette):
    def proper(colors):
        outgoing = [[] for _ in range(n)]
        indegree = [0] * n
        for u, v in arcs:
            if colors[u] == colors[v]:
                outgoing[u].append(v)
                indegree[v] += 1
        ready = [u for u in range(n) if indegree[u] == 0]
        seen = 0
        while ready:
            u = ready.pop()
            seen += 1
            for v in outgoing[u]:
                indegree[v] -= 1
                if indegree[v] == 0:
                    ready.append(v)
        return seen == n

    return sum(proper(colors) for colors in itertools.product(range(palette), repeat=n))


def interpolate(values):
    """Lagrange interpolation at consecutive integers, in the monomial basis."""
    result = [Fraction(0)] * len(values)
    for i, value in enumerate(values):
        basis = [Fraction(value)]
        for j in range(len(values)):
            if i == j:
                continue
            product = [Fraction(0)] * (len(basis) + 1)
            for k, coeff in enumerate(basis):
                product[k] -= j * coeff / (i - j)
                product[k + 1] += coeff / (i - j)
            basis = product
        result = [a + b for a, b in zip(result, basis)]
    assert all(a.denominator == 1 for a in result)
    return [int(a) for a in result]


def complete(n):
    return [(u, v) for u in range(n) for v in range(n) if u != v]


def main():
    cases = [
        ("empty₃", "empty 3", 3, []),
        ("bidirected K₂", "complete 2", 2, complete(2)),
        ("oriented C₃", "cycle3", 3, [(0, 1), (1, 2), (2, 0)]),
        ("bidirected K₃", "complete 3", 3, complete(3)),
        ("bidirected K₄", "complete 4", 4, complete(4)),
    ]
    probe = """import Dichrom
open Dichrom Dichrom.Controls
def raw (D : Digraph n) : List (List Int) :=
  let vs := vertices n
  [[n], vs.flatMap (fun u => (vs.filter (D.arc u)).map (fun v => (u.val*n+v.val:Int))),
    (polynomial D.acyclic vs).coeffs, (defect D.acyclic vs).coeffs]
"""
    for _, graph, _, _ in cases:
        probe += f"#eval IO.println (toString (raw ({graph})))\n"
    result = subprocess.run(
        ["lake", "env", "lean", "-j1", "-M1200", "--stdin"],
        input=probe, capture_output=True, text=True, cwd=Path(__file__).parent,
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    checked = 0
    for (label, _, n, arcs), (order, edges, lean_p, lean_h) in zip(cases, rows, strict=True):
        assert order == [n] and [divmod(e, n) for e in edges] == sorted(arcs), label
        counts = [color_count(n, arcs, x) for x in range(n + 2)]
        p = interpolate(counts[:n + 1])
        assert sum(a * (n + 1)**j for j, a in enumerate(p)) == counts[-1], label
        h = [(j - n) * a for j, a in enumerate(p)]
        while h and h[-1] == 0:
            h.pop()
        assert (p, h) == (lean_p, lean_h), (label, p, h, lean_p, lean_h)
        if label == "bidirected K₃":
            assert sum(h) == -1
        checked += sum(x**n for x in range(n + 2))
        print(f"{label}: counts {counts}, P {p}, H {h}")
    print(f"Verified {len(rows)} arc sets and {checked} colour maps.")


if __name__ == "__main__":
    main()
