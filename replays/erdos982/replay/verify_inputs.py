"""Independent exhaustive checks for the regular sampling and symmetry projection."""
import csv
from itertools import product
from math import comb, gcd
from pathlib import Path


def totient(d):
    return sum(gcd(i, d) == 1 for i in range(1, d+1))


def verify_necklaces():
    counts = {}
    with open("runs/necklaces.tsv") as stream:
        for line in csv.DictReader(stream, delimiter="\t"):
            n, m, observed = (int(line[column]) for column in ("n", "m", "samples"))
            expected, remainder = divmod(sum(totient(d)*comb(m//d, n//d)
                                             for d in range(1, gcd(n,m)+1)
                                             if m % d == n % d == 0), m)
            assert remainder == 0 and observed == expected and (n,m) not in counts
            counts[n,m] = observed
    assert set(counts) == {(n,m) for n in range(3,14) for m in range(n,2*n+5)}
    print("G2 Burnside:", len(counts), "carrier/order pairs,", sum(counts.values()), "necklaces")


def verify_symmetry():
    from encoder import Encoding
    for n in range(3, 9):
        formula = Encoding(n, n//2)
        formula.symmetry()
        boundary = [formula.edge(i, (i+1)%n) for i in range(n)]
        # Find by variable ID which comparisons are actually used by the encoder.
        comparisons = {formula.lt(u,v):(a,b) for a,u in enumerate(boundary)
                       for b,v in enumerate(boundary) if u != v}
        forbidden = []
        for (literal,) in formula.clauses:
            assert literal < 0 and -literal in comparisons
            forbidden.append(comparisons[-literal])
        assert len(forbidden) == n-1
        # Enumerate every total preorder as a rank vector with no gaps.
        # Lexicographic products over each alphabet size give each exactly once.
        cases = 0
        for levels in range(1,n+1):
            for ranks in product(range(levels), repeat=n):
                if len(set(ranks)) != levels:
                    continue
                for image in range(2*n):
                    offset, reverse = image % n, image >= n
                    direction = -1 if reverse else 1
                    if all(ranks[(offset + direction*a)%n] >= ranks[(offset + direction*b)%n]
                           for a,b in forbidden):
                        break
                else:
                    raise AssertionError((n,ranks))
                cases += 1
        print("SYM exhaustive projected preorders:", n, cases)


def merge_mutants():
    def read(path):
        with open(path) as stream:
            return list(csv.reader(stream, delimiter="\t"))
    other = read("runs/mutants_other.tsv")
    regular = read("runs/mutants_regular.tsv")
    assert other[0] == regular[0] == ["mutant","G1","G2","G3"]
    with open("runs/mutants.tsv", "w") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(other[0])
        for a,b in zip(other[1:], regular[1:], strict=True):
            assert a[0] == b[0] and a[2] == b[1] == b[3] == "0"
            assert sum(int(count) for count in (a[1], b[2], a[3])) > 0, a[0]
            writer.writerow([a[0], a[1], b[2], a[3]])
    print("Mutation checks:", len(other)-1, "killed")


if __name__ == "__main__":
    verify_necklaces()
    merge_mutants()
    verify_symmetry()
