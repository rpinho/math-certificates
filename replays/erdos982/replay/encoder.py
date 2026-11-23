"""Primary Erdős 982 distance-order encoder and family provenance."""
import argparse
from itertools import combinations, permutations, product
from pathlib import Path

FAMILIES = ("ASYM", "TRANS", "FIRST", "BOUND", "BISECTOR", "CROSS", "CAP", "SYM", "FAN")


class Encoding:
    def __init__(self, n, k, omit=(), fan=False):
        self.n = n
        self.k = k
        self.omit = set(omit)
        self.fan = fan
        self.edges = list(combinations(range(n), 2))
        self.edge_id = {edge: index for index, edge in enumerate(self.edges)}
        self.m = len(self.edges)
        self.variables = self.m * (self.m - 1) + n * (n - 1)
        self.clauses = {}

    def edge(self, a, b):
        return self.edge_id[min(a, b), max(a, b)]

    def lt(self, e, f):
        return 1 + e * (self.m - 1) + f - (f > e)

    def rep(self, v, w):
        return 1 + self.m * (self.m - 1) + v * (self.n - 1) + w - (w > v)

    def add(self, family, *literals):
        if family not in self.omit:
            self.clauses.setdefault(tuple(sorted(literals)), set()).add(family)

    def order(self):
        for e, f in combinations(range(self.m), 2):
            self.add("ASYM", -self.lt(e, f), -self.lt(f, e))
        for e, f, g in permutations(range(self.m), 3):
            self.add("TRANS", self.lt(f, e), self.lt(g, f), -self.lt(g, e))

    def rows(self):
        for v in range(self.n):
            row = [w for w in range(self.n) if w != v]
            for index, w in enumerate(row):
                first = self.rep(v, w)
                e = self.edge(v, w)
                comparisons = []
                for earlier in row[:index]:
                    f = self.edge(v, earlier)
                    lt = self.lt(e, f)
                    gt = self.lt(f, e)
                    self.add("FIRST", -first, lt, gt)
                    comparisons.append((-lt, -gt))
                for choices in product(*comparisons):
                    self.add("FIRST", first, *choices)
            for excess in combinations(row, self.k + 1):
                self.add("BOUND", *(-self.rep(v, w) for w in excess))

    def quadrilaterals(self):
        for quad in combinations(range(self.n), 4):
            a, b, c, d = quad
            ac, bd = self.edge(a, c), self.edge(b, d)
            for e, f in ((self.edge(a, b), self.edge(c, d)),
                         (self.edge(a, d), self.edge(b, c))):
                self.add("CROSS", self.lt(e, ac), self.lt(f, bd))
                self.add("CROSS", self.lt(f, ac), self.lt(e, bd))
            for i in range(4):
                a, b, c, d = quad[i:] + quad[:i]
                ab, ac, ad = (self.edge(a, w) for w in (b, c, d))
                bc, bd, cd = self.edge(b, c), self.edge(b, d), self.edge(c, d)
                self.add("BISECTOR", self.lt(ab, bd), self.lt(cd, ac))
                premise = (self.lt(ab, ad), self.lt(ad, ab), self.lt(ab, ac))
                self.add("CAP", *premise, self.lt(bc, bd))
                self.add("CAP", *premise, self.lt(cd, bd))

    def symmetry(self):
        for i in range(1, self.n):
            edge = self.edge(i, (i + 1) % self.n)
            self.add("SYM", -self.lt(edge, self.edge(0, 1)))

    def fans(self):
        for group in combinations(range(self.n), 5):
            for index, center in enumerate(group):
                rays = group[index + 1:] + group[:index]
                comparisons = []
                for a, b in zip(rays, rays[1:]):
                    opposite = self.edge(a, b)
                    comparisons.extend(self.lt(opposite, self.edge(center, w)) for w in (a, b))
                self.add("FAN", *comparisons)

    def build(self):
        self.order()
        self.rows()
        self.quadrilaterals()
        self.symmetry()
        if self.fan:
            self.fans()
        return self

    def write(self, target, families=None):
        clauses = sorted(self.clauses)
        with Path(target).open("w") as stream:
            stream.write(f"p cnf {self.variables} {len(clauses)}\n")
            for clause in clauses:
                stream.write(" ".join(map(str, clause)) + " 0\n")
        if families:
            with Path(families).open("w") as stream:
                for index, clause in enumerate(clauses, 1):
                    stream.write(f"{index}\t{','.join(sorted(self.clauses[clause]))}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("k", type=int)
    parser.add_argument("target")
    parser.add_argument("--families")
    parser.add_argument("--omit", action="append", choices=FAMILIES, default=[])
    parser.add_argument("--fan", action="store_true")
    args = parser.parse_args()
    Encoding(args.n, args.k, args.omit, args.fan).build().write(args.target, args.families)
